**# AIMonitor**

AIMonitor is a strategic report generation tool that utilizes **SerpAPI** for fetching Google search results and **Azure OpenAI (GPT-4o)** for generating executive summary reports. This tool allows users to monitor competitors, trends, and specific topics by collecting relevant web information and summarizing insights using AI.

**## Features**
- **Search Query Input**: Users can enter a keyword for monitoring.
- **Country Filter**: Allows filtering search results based on a selected country.
- **Time Filter**: Provides options to filter search results by timeframe (**Past Hour, Day, Week, Month, Year**).
- **AI-Powered Report Generation**: Uses **Azure OpenAI** to generate an **executive summary** based on retrieved search results.
- **Filtered Results**: Social media links are excluded for better report relevance.

**## Technologies Used**
- **Python**
- **Streamlit** (Frontend for user interaction)
- **SerpAPI** (For Google search result retrieval)
- **Azure OpenAI GPT-4o** (For AI-generated reports)
- **Requests** (For API calls)

**## Installation & Setup**
### **Prerequisites**
Ensure you have **Python** installed along with the required dependencies.

### **Steps**
1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-repo/AIMonitor.git
   cd AIMonitor
   ```
2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
3. **Set up your environment variables:**
   ```bash
   export AZURE_OPENAI_ENDPOINT="your_azure_openai_endpoint"
   export AZURE_OPENAI_API_KEY="your_azure_openai_api_key"
   export SERPAPI_KEY="your_serpapi_key"
   ```
4. **Run the application:**
   ```bash
   streamlit run app.py
   ```

**## Usage**
1. **Enter a keyword** related to the topic you want to monitor.
2. **Select a country** to refine results based on location.
3. **Choose a time filter** to fetch results within a specific period.
4. Click **"Generate Report"** to fetch results and generate an **AI-powered executive summary**.
5. View **relevant sources** and read the generated report.

**## API Keys Required**
- **Azure OpenAI API Key** for AI-generated reports.
- **SerpAPI Key** for fetching Google search results.

**## License**
This project is licensed under the **MIT License**.
