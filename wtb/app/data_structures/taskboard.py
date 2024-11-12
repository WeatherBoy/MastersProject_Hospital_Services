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
        func_name = function_assignment.name
        if func_name not in self.function_to_nurse:
            self.function_to_nurse[func_name] = set()
        self.function_to_nurse[func_name].add(nurse_name)

    def get_nurses_by_function(self, function_name: str) -> None:
        return self.function_to_nurse.get(function_name, set())

    def get_functions_by_nurse(self, nurse_name: str) -> list[str] | list[None]:
        if nurse_name in self.nurses:
            return [function.name for function in self.nurses[nurse_name].get_functions()]
        return []

    def get_function_names(self) -> list[str]:
        return list(self.function_to_nurse.keys())

    def update_function_assignments(
        self, function_name: str, location: str = None, time: str = None, doctor: str = None, extras: str = None
    ) -> None:
        """
        Finds the nurses that have a function with the given name and updates the function with the new information.
        """
        nurses = self.get_nurses_by_function(function_name)
        for nurse_name in nurses:
            self.nurses[nurse_name].update_function(function_name, location, time, doctor, extras)

    def to_dataframe(self) -> pd.DataFrame:
        data = []
        for nurse in self.nurses.values():
            for func in nurse.get_functions():
                func_dict = func.to_dict()  # <-- Dictionary of FunctionAssignment objects
                func_dict["Nurse"] = nurse.name
                data.append(func_dict)

        df = pd.DataFrame(data, columns=["Nurse", "Function", "Location", "Time", "Doctor", "Extras"])
        return df


class Nurse:
    def __init__(self, name: str):
        self.name = name
        self.functions = {}  # Dictionary of FunctionAssignment objects

    def add_function(self, function_assignment: "FunctionAssignment") -> None:
        self.functions[function_assignment.name] = function_assignment

    def get_functions(self) -> list["FunctionAssignment"]:
        """
        This technically doesn't return a `list` but a `dict_values` object. It is still iterable, though.
        """
        return self.functions.values()

    def update_function(self, function_name: str, location: str = None, time: str = None, doctor: str = None, extras: str = None) -> None:
        """
        Updates a function with new information, given the function name.

        NOTE: This function cannot at the moment update the name of the function.
        This is because it doesn't seem necessary for the current use case.
        """
        if function_name in self.functions:
            self.functions[function_name].update(location=location, time=time, doctor=doctor, extras=extras)
        else:
            raise ValueError(f"Function {function_name} not found in nurse {self.name}.")


class FunctionAssignment:
    def __init__(self, name: str, location: str = None, time: str = None, doctor: str = None, extras: str = None):
        self.name = name
        self.location = location
        self.time = time
        self.doctor = doctor
        self.extras = extras

    def update(self, location: str = None, time: str = None, doctor: str = None, extras: str = None):
        if location is not None:
            self.location = location
        if time is not None:
            self.time = time
        if doctor is not None:
            self.doctor = doctor
        if extras is not None:
            self.extras = extras

    def to_dict(self) -> dict[str, str]:
        return {"Function": self.name, "Location": self.location, "Time": self.time, "Doctor": self.doctor, "Extras": self.extras}
