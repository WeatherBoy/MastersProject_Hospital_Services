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

    def add_flex(self, flex_dict: dict[str, str]) -> None:
        """
        Updates the flex value of the functions that have a location that matches a key in the flex_dict.

        :param flex_dict: A dictionary with the location as key and the flex value as value.
        """
        for nurse in self.nurses.values():
            for func in nurse.get_functions():
                # Checking if the function has a location that matches a key in flex_dict
                if func.location is not None and func.location in flex_dict:
                    flex_value = flex_dict[func.location]
                    func.update(flex=flex_value)

                elif func.name.lower() == "koordinator" and "koordinator" in flex_dict:  # <-- Handles ONLY "koordinator" edge-case
                    flex_value = flex_dict[func.name.lower()]
                    func.update(flex=flex_value)

    def to_dataframe(self) -> pd.DataFrame:
        """
        Returns a dataframe representation of the TaskBoard.
        """
        data = []
        for nurse in self.nurses.values():
            for func in nurse.get_functions():
                func_dict = func.to_dict()  # <-- Dictionary of FunctionAssignment objects
                func_dict["Nurse"] = nurse.name
                data.append(func_dict)

        df = pd.DataFrame(data, columns=["Nurse", "Function", "Location", "Time", "Doctor", "Extras", "Flex"])
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
    def __init__(self, name: str, location: str = None, time: str = None, doctor: str = None, extras: str = None, flex: int = None):
        self.name = name
        self.location = location
        self.time = time
        self.doctor = doctor
        self.extras = extras
        self.flex = flex

    def update(self, location: str = None, time: str = None, doctor: str = None, extras: str = None, flex: int = None) -> None:
        if location is not None:
            self.location = location
        if time is not None:
            self.time = time
        if doctor is not None:
            self.doctor = doctor
        if extras is not None:
            self.extras = extras
        if flex is not None:
            self.flex = flex

    def to_dict(self) -> dict[str, str]:
        return {
            "Function": self.name,
            "Location": self.location,
            "Time": self.time,
            "Doctor": self.doctor,
            "Extras": self.extras,
            "Flex": self.flex,
        }

    def to_list(self) -> list[str]:
        return [self.name, self.location, self.time, self.doctor, self.extras, self.flex]
