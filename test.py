import os
from crewai import Agent, Task, Crew
from langchain.llms import OpenAI
from dotenv import load_dotenv

load_dotenv()
gemini_api_key = os.getenv("GEMINI_API")

# Initialize the AI model
class GeminiLLM(LLM):
    """Custom LLM wrapper for Google Gemini API."""

    @property
    def _llm_type(self) -> str:
        return "gemini"

    def _call(self, prompt: str, stop: Optional[List[str]] = None) -> str:
        """Make a request to Gemini API and return the response."""
        url = f"https://generativelanguage.googleapis.com/v1/models/gemini-pro:generateContent?key={gemini_api_key}"
        headers = {"Content-Type": "application/json"}
        data = {"contents": [{"parts": [{"text": prompt}]}]}

        response = requests.post(url, headers=headers, json=data)

        if response.status_code == 200:
            return response.json()["candidates"][0]["content"]["parts"][0]["text"]
        else:
            return f"Error: {response.status_code}, {response.text}"
        
# Initialize Gemini LLM
gemini_llm = GeminiLLM()


# Define the Agent
researcher = Agent(
    name="AI Researcher",
    role="Researcher",
    goal="Find and summarize AI advancements",
    backstory="An expert AI researcher keeping up with recent developments.",
    llm=llm
)

# Define the Task
research_task = Task(
    description="Summarize the latest AI advancements in a short paragraph.",
    agent=researcher
)

# Create the Crew
crew = Crew(agents=[researcher], tasks=[research_task])

# Run the Agent
if __name__ == "__main__":
    result = crew.kickoff()
    print("AI Research Summary:\n", result)
