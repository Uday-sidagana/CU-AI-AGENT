import os
from dotenv import load_dotenv
from crewai import Crew, Agent, Task, LLM
from crewai_tools import tools
import litellm

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

service = Service('./chromedriver')
driver = webdriver.Chrome()

# Tools
# from crewai_tools import SeleniumScrapingTool
# selenium_tool = SeleniumScrapingTool()

# Load API key from .env
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API")

# Set environment variable for LiteLLM
os.environ["GEMINI_API_KEY"] = GEMINI_API_KEY

# Define the LLM with the correct provider
llm = LLM(model="gemini/gemini-1.5-flash")  # provider="gemini" is optional

# Student details
details = {
    'name': 'Uday', 'number': '9550578004', '10th_Marks': 95, '12th_Marks': 93,
    'Graduation Percentage': 73, 'place': 'Visakhapatnam', 'Backlogs': 0,
    'email': 'uday.sidgana@gmail.com', 'umail': '21bcs7418@cuchd.in'
}
form_url = 'https://forms.gle/L9wcUADe5cCgSUFY6'


def extract_field_name(form_url):
    driver.get(form_url)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "form")))

    # XPath to extract span elements where the label is stored inside div
    labels = driver.find_elements(By.XPATH, "//div[contains(@jsmodel, 'CP1oW')]//span[text()]")

    # Extract text from the labels
    field_names = [label.text for label in labels if label.text.strip() != ""]

    print(f"Number of labels found: {len(field_names)}")
    return field_names


field_names = extract_field_name(form_url)

# Print the extracted field names
print("Extracted Field Names:", field_names)


# Field match    
field_matcher = Agent(
    role="Field Chooser",
    goal=f"Go through {field_names} and for each field name choose one most relevant choice from the {details}, if the field name doesn't match any value from {details} answer it based on your own knowledge",
    backstory=f"""
       You are an expert in matching {field_names} with {details}, You can understand what each item in {field_names} is and match it with {details}.
        """,
    llm=llm
)

field_matcher_task = Task(
    description=f"Go through {field_names} and for each field name choose one most relevant value from the keys of this dictionary {details}",
    agent=field_matcher,
    expected_output="A List of chosen values for each field"
)

# Define the Task

# Create and run the Crew
crew = Crew(agents=[field_matcher], tasks=[field_matcher_task])

try:
    result = crew.kickoff()
    print("\n🔹 AI Response:\n", result)
except Exception as e:
    print(f"\n❌ Error: {e}")

# Fill form with data
def fill_form_with_data(field_names, data):
    for idx, field_name in enumerate(field_names):
        if idx >= len(data):  # In case the data list is shorter than field names
            break

        value = data[idx]

        # Find the input field using the label name (it may vary depending on the form structure)
        # This assumes the input field is adjacent to the label or within the same div
        try:
            input_field = driver.find_element(By.XPATH, f"//span[text()='{field_name}']/ancestor::div[contains(@class,'geS5n')]//input")

            if input_field:
                input_field.send_keys(str(value))
                print(f"Filled field '{field_name}' with value '{value}'")
        except Exception as e:
            print(f"Error filling field '{field_name}': {e}")

# Assuming the AI response is returned in the same order as the form fields
# Here we're mapping field names to the details dictionary (simulated result list for now)
result_list = [
    details['name'], details['number'], details['10th_Marks'],
    details['12th_Marks'], details['Graduation Percentage'],
    details['place'], details['Backlogs'], details['email'], details['umail']
]

# Call the function to fill the form
fill_form_with_data(field_names, result_list)

# Submit the form
try:
    submit_button = driver.find_element(By.XPATH, "//div[@role='button' and @aria-label='Submit']")
    submit_button.click()
    print("Form submitted successfully.")
except Exception as e:
    print(f"Error submitting the form: {e}")
