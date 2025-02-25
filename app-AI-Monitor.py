import streamlit as st
import requests
import os
from openai import AzureOpenAI
# Load secrets securely
azure_openai_endpoint = st.secrets["azure_openai"]["endpoint"]
azure_openai_api_key = st.secrets["azure_openai"]["api_key"]
serpapi_key = st.secrets["serpapi"]["api_key"]

# Initialize OpenAI client
client = AzureOpenAI(
    azure_endpoint=azure_openai-endpoint,
    api_key=azure_openai_api_key,
    api_version="2024-08-01-preview"
)

# Full Country list
COUNTRIES = {
    "Andorra": "AD", "United Arab Emirates": "AE", "Afghanistan": "AF", "Antigua and Barbuda": "AG",
    "Anguilla": "AI", "Albania": "AL", "Armenia": "AM", "Netherlands Antilles": "AN", "Angola": "AO",
    "Antarctica": "AQ", "Argentina": "AR", "American Samoa": "AS", "Austria": "AT", "Australia": "AU",
    "Aruba": "AW", "Azerbaijan": "AZ", "Bosnia and Herzegovina": "BA", "Barbados": "BB", "Bangladesh": "BD",
    "Belgium": "BE", "Burkina Faso": "BF", "Bulgaria": "BG", "Bahrain": "BH", "Burundi": "BI", "Benin": "BJ",
    "Bermuda": "BM", "Brunei Darussalam": "BN", "Bolivia": "BO", "Brazil": "BR", "Bahamas": "BS", "Bhutan": "BT",
    "Botswana": "BW", "Belarus": "BY", "Belize": "BZ", "Canada": "CA", "Switzerland": "CH", "China": "CN",
    "Colombia": "CO", "Costa Rica": "CR", "Cuba": "CU", "Denmark": "DK", "Dominican Republic": "DO",
    "Ecuador": "EC", "Egypt": "EG", "Spain": "ES", "Finland": "FI", "France": "FR", "United Kingdom": "GB",
    "Germany": "DE", "Greece": "GR", "Hong Kong": "HK", "Hungary": "HU", "India": "IN", "Indonesia": "ID",
    "Ireland": "IE", "Italy": "IT", "Japan": "JP", "Kenya": "KE", "Malaysia": "MY",
    "Mexico": "MX","Morocco": "MA", "Netherlands": "NL", "New Zealand": "NZ", "Nigeria": "NG", "Norway": "NO",
    "Pakistan": "PK", "Philippines": "PH", "Poland": "PL", "Portugal": "PT", "Russia": "RU", "Saudi Arabia": "SA",
    "Singapore": "SG", "South Africa": "ZA", "South Korea": "KR", "Sweden": "SE", "Thailand": "TH",
    "Turkey": "TR", "Ukraine": "UA", "United States": "US", "Venezuela": "VE", "Vietnam": "VN"
}

# Function to fetch Google search results using SerpAPI
def get_google_search_results(query, time_filter, country, max_results=50, api_key=serpapi_key):
    base_url = "https://serpapi.com/search"
    query = f'"{query}"'  # Adding quotes for exact search
    params = {
        "q": query,
        "num": max_results,
        "api_key": api_key,
        "engine": "google",
        "gl": country  # Country filter
    }

    if time_filter:
        params["tbs"] = f"qdr:{time_filter}"
    
    response = requests.get(base_url, params=params)
    if response.status_code != 200:
        return []
    
    data = response.json()
    search_results = [result["link"] for result in data.get("organic_results", [])]
    
    # Filter out social media links
    social_media_domains = ["instagram.com", "twitter.com", "linkedin.com", "facebook.com", "tiktok.com"]
    filtered_results = [url for url in search_results if not any(domain in url for domain in social_media_domains)]
    
    return filtered_results[:max_results]

# Function to generate report using Azure OpenAI
def generate_report(query, urls, time_filter):
    url_list = "\n".join(urls)
    time_filter_text = {
        "h": "hourly", "d": "daily", "w": "weekly", "m": "monthly", "y": "yearly"
    }.get(time_filter, "periodically")
    
    prompt = f"""Our company monitors other companies and gathers {time_filter_text} information about them. 
    Today, we have information about {query}. Your role is to create a report based solely on the data I provide. 
    It is strictly forbidden to use any external knowledge (covering all aspects such as strategy, finance, politics, etc.). 
    The report should not be an introduction but a high-level executive summary for this {time_filter_text}. 
    Below are the sources of information:
    {url_list} """
    
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a Senior strategy consultant."},
            {"role": "user", "content": prompt},
        ]
    )
    return response.choices[0].message.content, url_list

# Streamlit UI
st.title("Strategic Report Generator")

query = st.text_input("Enter a keyword:")
country = st.selectbox("Select a country:", list(COUNTRIES.keys()))
time_filter = st.selectbox(
    "Select Time Filter:",
    ["None", "h", "d", "w", "m", "y"],
    format_func=lambda x: "None" if x == "None" else {
        "h": "Past Hour", "d": "Past Day", "w": "Past Week",
        "m": "Past Month", "y": "Past Year"
    }[x]
)

# Initialize session state for history
if "report_history" not in st.session_state:
    st.session_state.report_history = []

if st.button("Generate Report"):
    if not query:
        st.warning("Please enter a keyword.")
    else:
        time_filter = None if time_filter == "None" else time_filter
        country_code = COUNTRIES.get(country, "US")  # Default to US if not provided
        urls = get_google_search_results(query, time_filter, country_code)

        if urls:
            st.write(f"### Found {len(urls)} Relevant Sources")
            with st.spinner("Generating report..."):
                report, url_list = generate_report(query, urls, time_filter)
                st.subheader("Executive Summary")
                st.write(report)
                
                st.subheader("Sources")
                for url in urls:
                    st.write(f"- [{url}]({url})")

                # Save report in session state
                st.session_state.report_history.append({"query": query, "report": report})
        else:
            st.write("No results found.")

# Sidebar for history
st.sidebar.title("Report History")
if st.session_state.report_history:
    for i, entry in enumerate(st.session_state.report_history):
        if st.sidebar.button(f"View Report {i+1}: {entry['query']}"):
            st.subheader(f"Previous Report: {entry['query']}")
            st.write(entry["report"])
else:
    st.sidebar.write("No reports generated yet.")
