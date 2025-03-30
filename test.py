import os
from dotenv import load_dotenv
from crewai import Crew, Agent, Task, LLM
import litellm

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

form_filler = Agent(
    role="Google Form Filler",
    goal="To fill the google form with student data",
    backstory="Expert in using Selenium and can fill Google forms",
    llm= llm

)

# Define the Task
research_task = Task(
    description=f"Use selenium to fill the google form{form_url} using the {details} and submit the form",
    agent=form_filler,
    
)

# Create and run the Crew
crew = Crew(agents=[form_filler], tasks=[research_task])

try:
    result = crew.kickoff()
    print("\n🔹 AI Response:\n", result)
except Exception as e:
    print(f"\n❌ Error: {e}")
