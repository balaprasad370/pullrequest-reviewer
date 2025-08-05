from crewai import Crew
from app.crew_agent.agents import code_reviewer, code_explainer
import json
from app.crew_agent.tasks import TaskGenerator
import os   

os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_TOKEN")


# Build the complete codes string for the prompt
class CodeReview:
    def __init__(self, code_file):
        self.name = code_file["filename"]
        self.code = code_file["patch"]

    def get_code_content(self):
        return f"\n--- File {self.name} ---\n{self.code}"

    def task_review(self):
        task_review = TaskGenerator(
            description=f"""You are a senior code reviewer. Review the following Python code for bugs, security issues, 
            performance problems, style issues, and other improvements.

            Code to review:
            {self.code}


             **Output Requirements:**
            - Ensure that your final response MUST be a valid JSON object which follows the structure outlined 
            - Do not wrap the response in ```json, ```python, ```code, or ``` symbols.
            - Do not include any explanation or additional text outside of this JSON object.
            - Ensure all of the expected output and code are included within the "response" string.

            Analyze each line and provide detailed feedback. Return the output in this EXACT JSON format:
            {json.dumps(self.review(), indent=2)}
            """,
            agent=code_reviewer,
            expected_output="A JSON object with name and list of issues.",
        )
        return task_review.build()

    def task_explain(self):
        task_explain = TaskGenerator(
            description=f"""You are a programming instructor. Explain the following Python code in detail for beginners.

            Code to explain:
            {self.code}
            
            
            
            **Output Requirements:**
            - Ensure that your final response MUST be a valid JSON object which follows the structure outlined 
            - Do not wrap the response in ```json, ```python, ```code, or ``` symbols.
            - Do not include any explanation or additional text outside of this JSON object.
            - Ensure all of the expected output and code are included within the "response" string.

            Break down the code line by line and provide comprehensive explanation. Return the output in this EXACT JSON format:
            {json.dumps(self.explain(), indent=2)}
            """,
            agent=code_explainer,
            expected_output="A JSON object with 'explanation' containing overview details and 'code_breakdown' with line-by-line analysis.",
        )
        return task_explain.build()

    def run_crew(self):
        crew = Crew(
            agents=[code_reviewer, code_explainer],
            tasks=[self.task_review()],
            verbose=False,
        )
        return crew.kickoff()

    def review(self):
        # Example review logic - this would be replaced with actual code review
        return {
            "name": self.name,
            "issues": [
                {
                    "type": "bug",
                    "line": 2,
                    "description": "Function does not handle negative inputs",
                    "suggestion": "Add input validation for negative numbers",
                },
                {
                    "type": "performance",
                    "line": 4,
                    "description": "Inefficient implementation",
                    "suggestion": "Consider using iterative approach",
                },
            ],
        }

    def explain(self):
        # Example explanation logic
        return {
            "name": self.name,
            "explanation": {
                "overview": "Code explanation overview",
                "purpose": "Purpose of the code",
                "approach": "Implementation approach",
                "complexity": "Time and space complexity",
            },
            "code_breakdown": [
                {
                    "line": 1,
                    "code": "First line of code",
                    "explanation": "Explanation of first line",
                }
            ],
            "commented_code": "# Commented version of code\n" + self.code,
        }
