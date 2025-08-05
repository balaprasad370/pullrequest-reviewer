from crewai import Agent

# Create an agent to review Python code
code_reviewer = Agent(
    role='Code Reviewer',
    goal='Review code and give suggestions',
    backstory='Experienced developer who checks for quality, syntax, and performance issues.',
    verbose=False
)

# Create another agent to explain Python code
code_explainer = Agent(
    role='Code Explainer',
    goal='Explain code in simple terms',
    backstory='Teaches to beginners and explains code in a simple way.',
    verbose=False
)
