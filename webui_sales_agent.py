import os
import re
import time
import requests
import streamlit as st
from dotenv import load_dotenv
from bs4 import BeautifulSoup
from autogen import AssistantAgent, UserProxyAgent
import autogen

# Load environment variables
load_dotenv(".env")

OPENAI_API_KEY = "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"
SERPER_API_URL = "https://google.serper.dev/search"
SERPER_API_KEY = "12c9456f7134b76c22d89015fde14eef33cfd208"

if not os.getenv("OPENAI_API_KEY"):
    os.environ["OPENAI_API_KEY"] = "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"

# Streamlit UI
st.title("🔹 AI-Powered Email Outreach Generator")

# Input email address
email_address = st.text_input(" Enter an Email Address:")
position = st.text_input(" Enter a position:")
department = st.text_input(" Enter a department:")

def extract_company_from_email(email):
    match = re.search(r"@([a-zA-Z0-9-]+)\.", email)
    return match.group(1).upper() if match else "Unknown"


def serper_search(query):
    """Search for company details using SERPER API."""
    headers = {"X-API-KEY": SERPER_API_KEY, "Content-Type": "application/json"}
    params = {"q": query, "num": 5}  # Get top 5 results
    response = requests.post(SERPER_API_URL, json=params, headers=headers)

    if response.status_code == 200:
        data = response.json()
        results = data.get("organic", [])
        return [{"title": res["title"], "url": res["link"], "snippet": res["snippet"]} for res in results]
    else:
        st.error("❌ Error fetching search results. Please check API key or try again.")
        return []

def extract_full_page_content(url):
    """Extract text content from the given URL."""
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")
        paragraphs = soup.find_all("p")
        text_content = "\n".join([p.get_text() for p in paragraphs])

        return text_content
    except requests.exceptions.RequestException as e:
        st.error(f"⚠️ Error fetching {url}: {e}")
        return ""

# Ensure email_address is provided
if email_address:
    # Initialize company_name with a default value
    company_name = extract_company_from_email(email_address) or "Unknown"
    st.write(f" **Extracted Company**: `{company_name}`")

    # Search query
    search_query = f"{company_name} company overview, industry, and challenges"
    search_results = serper_search(search_query)

    full_text = ""
    for result in search_results:
        title, url, snippet = result["title"], result["url"], result["snippet"]
        st.write(f" **Extracting content from:** {title} ({url})")

        page_content = extract_full_page_content(url)
        full_text += f"\n\n=== {title} ===\nURL: {url}\nSnippet: {snippet}\n\n{page_content}\n\n"
        time.sleep(2)  # Avoid rapid requests

    # Save extracted content to a .txt file
    file_path = f"{company_name.lower()}_full_content.txt"
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(full_text)

    st.success(f" **Extracted content saved:** `{file_path}`")

    # AI Agents
    user_proxy = autogen.UserProxyAgent(
        name="user_proxy",
        human_input_mode="NEVER",
        max_consecutive_auto_reply=10,
        code_execution_config={"work_dir": "work_dir", "use_docker": False},
    )

    company_research_agent = autogen.AssistantAgent(
        name="Company_Research_Agent",
        llm_config={"model": "gpt-3.5-turbo", "temperature": 0.7},
        system_message="Analyze the company's industry, technological challenges, domain and latest developments using the full extracted content."
    )

    email_generation_agent = autogen.AssistantAgent(
        name="Email_Generation_Agent",
        llm_config={"model": "gpt-3.5-turbo", "temperature": 0.7},
        system_message=(
            "Generate a casual yet professional outreach email tailored to the company’s industry, position, and department. "
            "(e.g., education, manufacturing, finance) and its key challenges, as extracted from the provided content. "
            "The email should feel approachable and engaging while maintaining a professional tone. "
            "Start the email with a short, engaging subject line (e.g., 'Excited to Connect with [Company Name]!') followed by 'Dear [name],' where [name] is the recipient's name. "
            "Clearly articulate how Kavi Global solutions can address these challenges, drive efficiencies, and create value. "
            "Highlight measurable benefits, such as improved decision-making, cost savings, operational efficiency, or enhanced customer engagement. "
            "Keep the email concise, easy to read, and structured in 3 paragraphs. "
            "Ensure the email does not exceed 150 words."
        )
    )

    with open(file_path, "r", encoding="utf-8") as file:
        file_content = file.read()

    company_info_task = f"""
    Extract key insights about {company_name} from the following content:

    {file_content}

    Insights needed:
    1. The **industry sector** of {company_name}
    2. Key **industry trends and challenge in the industrys**
    3. How **analytics solutions** can help address these challenges.
    """
    company_info_result = user_proxy.initiate_chat(
        recipient=company_research_agent,
        message=company_info_task,
        max_turns=2,
        summary_method="last_msg",
    )

    kavi_global_info = """
    Kavi Global provides a range of data analytics and AI solutions to help companies overcome their challenges. Their services include:
    - Business Intelligence
    - Data Engineering
    - Data Management
    - Data Science & AI
    - Internet of Things (IoT)
    - Intelligent Apps
    - Managed Services

    Kavi Global helps companies optimize processes, identify opportunities, and address potential challenges with confidence. They offer solutions such as KPI development, interactive dashboards, self-service BI, visual exploration, mobile BI, embedded BI, and advanced custom visualization.
    """

    email_task = f"""
    Generate a customized sales outreach email for {company_name} based on the extracted content.
    Use these company insights:
    {company_info_result.summary}
    Tailor the email to the recipient's position: {position} and department: {department}.

    Emphasize how Kavi Global's analytics solutions provide value:
    {kavi_global_info}

    Targeting: {position} in {department}
    """
    email_result = user_proxy.initiate_chat(
        recipient=email_generation_agent,
        message=email_task,
        max_turns=2,
        summary_method="last_msg",
    )

    # Display generated email
    st.subheader(f"📧 AI-Generated Sales Outreach Email for {company_name}:")
    if isinstance(email_result.summary, str):
        st.markdown(email_result.summary)
    elif isinstance(email_result.summary, dict) and "output" in email_result.summary:
        st.markdown(email_result.summary["output"])
    else:
        st.error("❌ Could not retrieve the email content. Please try again.")

    # Save generated email
    email_file_path = f"sales_outreach_{company_name.lower()}.txt"
    with open(email_file_path, "w", encoding="utf-8") as file:
        file.write(email_result.summary)

    # Download button for email
    st.download_button(
        label="⬇️ Download Sales Outreach Email",
        data=email_result.summary,
        file_name=email_file_path,
        mime="text/plain"
    )
else:
    st.warning("⚠️ Please provide an email address to proceed.")