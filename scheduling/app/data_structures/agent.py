class Agent:
    def __init__(self, name: str) -> None:
        self.name = name
        self.qualifications = {}
        self.days_off = []
        self.task_preferences = []

    def add_qualifications(self, qualifications: dict[str, bool]) -> None:
        self.qualifications = qualifications

    def add_task_preferences(self, preferences: list[int]) -> None:
        self.task_preferences = preferences

    def add_days_off(self, days_off: list[int]) -> None:
        self.days_off = days_off

    def qualified(self, task: str) -> bool:
        return self.qualifications[task]

    def __str__(self) -> str:
        return f"{self.name}: \n{self.qualifications}\n{self.task_preferences}\n{self.days_off}"
