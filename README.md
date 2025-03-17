# AI-Powered Sales Outreach Generator

This project is an AI-powered tool designed to generate customized sales outreach emails based on company information extracted from the web. The tool uses OpenAI's GPT-3.5-turbo model and SERPER API to gather and analyze company data, and then generate tailored emails to enhance sales efforts.

## Features

- Extracts company name from an email address.
- Searches for company details using the SERPER API.
- Extracts full text content from web pages.
- Analyzes company information using AI agents.
- Generates customized sales outreach emails.
- Provides a download option for the generated email.

## Requirements

- Python 3.7+
- Streamlit
- Requests
- BeautifulSoup4
- python-dotenv
- autogen

## Installation

1. Clone the repository:

   ```sh
   git clone https://github.com/madeline0304/autogenaai.git
   cd autogenaai
   ```
2. Install the required packages:

   ```sh
   pip install -r requirements.txt
   ```
3. Create a `.env` file in the project directory and add your OpenAI API key:

   ```env
   OPENAI_API_KEY=your_openai_api_key
   ```

## Usage

1. Run the Streamlit app:

   ```sh
   streamlit run webui_sales_agent.py
   ```
2. Enter an email address in the input field.
3. The tool will extract the company name from the email address and search for relevant information using the SERPER API.
4. The extracted content will be analyzed by AI agents to generate insights about the company.
5. A customized sales outreach email will be generated and displayed on the Streamlit interface.
6. You can download the generated email using the provided download button.

## Configuration

- **SERPER_API_URL**: The URL for the SERPER API.
- **SERPER_API_KEY**: Your SERPER API key.
- **OPENAI_API_KEY**: Your OpenAI API key.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgements

- [OpenAI](https://openai.com) for the GPT-3.5-turbo model.
- [SERPER](https://serper.dev) for the search API.
- [Streamlit](https://streamlit.io) for the web UI framework.
