import pandas as pd


class TaskBoard:
    def __init__(self):
        self.nurses = {}  # Key: nurse name, Value: Nurse object
        self.function_to_nurse = {}  # For bidirectional mapping

    def add_nurse(self, nurse: "Nurse") -> None:
        self.nurses[nurse.name] = nurse

    def add_function_to_nurse(self, nurse_name: str, function_assignment: "FunctionAssignment") -> None:
        if nurse_name not in self.nurses:
            self.add_nurse(Nurse(nurse_name))
        self.nurses[nurse_name].add_function(function_assignment)
        # Update bidirectional mapping
        func_name = function_assignment.function_name
        if func_name not in self.function_to_nurse:
            self.function_to_nurse[func_name] = set()
        self.function_to_nurse[func_name].add(nurse_name)

    def get_nurses_by_function(self, function_name: str) -> None:
        return self.function_to_nurse.get(function_name, set())

    def get_functions_by_nurse(self, nurse_name: str) -> list[str] | list[None]:
        if nurse_name in self.nurses:
            return [f.function_name for f in self.nurses[nurse_name].functions]
        return []

    def to_dataframe(self) -> pd.DataFrame:
        data = []
        for nurse in self.nurses.values():
            for func in nurse.functions:
                func_dict = func.to_dict()  # <-- Dictionary of FunctionAssignment objects
                func_dict["Nurse"] = nurse.name
                data.append(func_dict)

        df = pd.DataFrame(data, columns=["Nurse", "Function", "Time", "Extras"])
        return df


class Nurse:
    def __init__(self, name: str):
        self.name = name
        self.functions = []  # List of FunctionAssignment objects

    def add_function(self, function_assignment: "FunctionAssignment") -> None:
        self.functions.append(function_assignment)


class FunctionAssignment:
    def __init__(self, function_name: str, time: str = None, extras: str = None):
        self.function_name = function_name
        self.time = time
        self.extras = extras

    def to_dict(self) -> dict[str, str]:
        return {"Function": self.function_name, "Time": self.time, "Extras": self.extras}
