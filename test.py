import os
from dotenv import load_dotenv
from crewai import Crew, Agent, Task, LLM
import litellm

# Load API key from .env
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API")

if not GEMINI_API_KEY:
    raise ValueError("❌ Missing GEMINI_API in .env file")

# Set environment variable for LiteLLM
os.environ["GEMINI_API_KEY"] = GEMINI_API_KEY

# Define the LLM with the correct provider
llm = LLM(model="gemini/gemini-1.5-flash")  # provider="gemini" is optional

# Define an AI agent
researcher = Agent(
    role="AI Researcher",
    goal="Summarize AI advancements",
    backstory="Expert in AI and ML research",
    llm=llm
)

# Define the Task
research_task = Task(
    description="Summarize the latest AI advancements in a short paragraph.",
    agent=researcher,
    expected_output="A concise paragraph summarizing AI advancements."
)

# Create and run the Crew
crew = Crew(agents=[researcher], tasks=[research_task])

try:
    result = crew.kickoff()
    print("\n🔹 AI Response:\n", result)
except Exception as e:
    print(f"\n❌ Error: {e}")
