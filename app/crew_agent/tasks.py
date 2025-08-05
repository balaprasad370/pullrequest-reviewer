from crewai import Task

class TaskGenerator:
    def __init__(self, description, agent, expected_output):
        self.description = description
        self.agent = agent
        self.expected_output = expected_output

    def build(self):
        return Task(
            description=self.description,
            agent=self.agent,
            expected_output=self.expected_output
        )
