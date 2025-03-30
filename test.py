import os
from dotenv import load_dotenv
from crewai import Crew, Agent, Task, LLM
from crewai_tools import tools
import litellm

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome()



#Tools
# from crewai_tools import SeleniumScrapingTool
# selenium_tool = SeleniumScrapingTool()


# Load API key from .env
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API")


# Set environment variable for LiteLLM
os.environ["GEMINI_API_KEY"] = GEMINI_API_KEY

# Define the LLM with the correct provider
llm = LLM(model="gemini/gemini-1.5-flash")  # provider="gemini" is optional

#student details
details ={'name':'Uday', 'number': '9550578004', 'Xth_Marks': 95}
form_url = 'https://forms.gle/767P3TpZkXktSDM7A'




# Define an AI agent
# researcher = Agent(
#     role="AI Researcher",
#     goal="Summarize AI advancements",
#     backstory="Expert in AI and ML research",
#     llm=llm
# )

# student_data= Agent(
#     role="Google Form Filler",
#     goal="To fill the google form with student data",
#     backstory="Expert in using Selenium and can fill Google forms",
#     llm= llm
# )

def extract_field_name(form_url):
    driver.get(form_url)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "form")))
    
    labels = driver.find_elements(By.TAG_NAME, 'label')
    return labels
field_names= extract_field_name()

# #Form field extraction
# form_field_extractor = Agent(
#     role="Google Form Filler",
#     goal="Extract each field name using the tools and pass the labels list to the field_matcher agent",
#     backstory="Expert in using Selenium and extracting the field names",
#     tools=[extract_field_name],
#     llm= llm

# )

# form_field_extract_task = Task(
#     description="Extract each field name using the tools and pass the labels list to the field_matcher agent",
#     agent=form_field_extractor,
#     expected_output="The list of labels extracted from the form"
#)


#Field match    
field_matcher = Agent(
    role="Google Form Filler",
    goal=f"Run through the list of labels from the list{extract_field_name()}",
    backstory="Expert in using Selenium and can fill Google forms",
    tools=[selenium_tool],
    llm= llm

)

form_field_extract_task = Task(
    description="Extract each field name using the tools and pass the labels list to the field_matcher agent",
    agent=form_field_extractor,
    expected_output="The list of labels extracted from the form"

# Define the Task


# Create and run the Crew
crew = Crew(agents=[form_filler], tasks=[research_task])

try:
    result = crew.kickoff()
    print("\n🔹 AI Response:\n", result)
except Exception as e:
    print(f"\n❌ Error: {e}")
