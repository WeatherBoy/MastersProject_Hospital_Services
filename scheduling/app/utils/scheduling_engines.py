from ortools.sat.python import cp_model

from app.data_structures.agent import Agent
from app.utils.engine_utils import rygvagt_mandatory_leave_info


def back_scheduling(
    tasks: list[str], task_schedules: dict[str, list[int]], agents: list[Agent]
) -> tuple[list[dict[str, int | str]], dict[str, int]] | None:
    """ """
    num_tasks = len(tasks)

    num_days = 0
    for task in tasks:
        # Finding the task with the most days - equals `num_days` or "scheduling horizon"
        num_days = max(num_days, max(task_schedules[task]))

    all_days = range(num_days + 1)  # <-- +1, because task_schedule is 0-indexed
    print(num_days)

    day_of_week, weekend_info = rygvagt_mandatory_leave_info(num_days, all_days)

    # Tasks that require multiple agents
    # NOTE: This design is manual (NOT GOOD!)
    tasks_requiring_multiple_agents = {"O-OP": 2, "O-OP (tirsdag)": 2}

    model = cp_model.CpModel()

    # Decision variables
    x = {}
    for agent in agents:
        for task in tasks:
            for day in all_days:
                x[(agent.name, task, day)] = model.NewBoolVar(f"x_{agent.name}_{task}_{day}")

    # Agents can only be assigned to qualified tasks
    for agent in agents:
        for task in tasks:
            if not agent.qualified(task):
                for day in all_days:
                    model.Add(x[(agent.name, task, day)] == 0)

    # Agents cannot be assigned on unavailable days
    for agent in agents:
        for day in agent.days_off:
            for task in tasks:
                model.Add(x[(agent.name, task, day)] == 0)

    # Each task must be performed on its scheduled days
    for task in tasks:
        for day in task_schedules[task]:
            if task in tasks_requiring_multiple_agents:
                num_agents_required = tasks_requiring_multiple_agents[task]
                model.Add(sum(x[(agent.name, task, day)] for agent in agents if agent.qualified(task)) == num_agents_required)
            else:
                model.AddExactlyOne(x[(agent.name, task, day)] for agent in agents if agent.qualified(task))

    # Agents can perform at most one task per day
    for agent in agents:
        for day in all_days:
            model.AddAtMostOne(x[(agent.name, task, day)] for task in tasks)

    # Weekend constraints
    for info in weekend_info:
        saturday = info["saturday"]
        sunday = info["sunday"]
        monday_before = info["monday_before"]
        monday_after = info["monday_after"]

        # Enforce the same agent works Rygvagt on both days
        for agent in agents:
            model.Add(x[(agent.name, "Rygvagt", saturday)] == x[(agent.name, "Rygvagt", sunday)])

        # Ensure exactly one agent is assigned to Rygvagt on Saturday
        model.AddExactlyOne(x[(agent.name, "Rygvagt", saturday)] for agent in agents if agent.qualified("Rygvagt"))

        # Agents working the weekend must have corresponding Mondays off
        for agent in agents:
            works_weekend = x[(agent.name, "Rygvagt", saturday)]
            if monday_before is not None:
                model.Add(sum(x[(agent.name, task, monday_before)] for task in tasks) == 0).OnlyEnforceIf(works_weekend)
            if monday_after is not None:
                model.Add(sum(x[(agent.name, task, monday_after)] for task in tasks) == 0).OnlyEnforceIf(works_weekend)

    # Compute total assignments per agent
    total_assignments = {}
    for agent in agents:
        total_assignments[agent.name] = model.NewIntVar(0, num_days * num_tasks, f"total_assignments_{agent.name}")
        model.Add(total_assignments[agent.name] == sum(x[(agent.name, task, day)] for task in tasks for day in all_days))

    # Minimize the maximum assignments
    max_assignments = model.NewIntVar(0, num_days * num_tasks, "max_assignments")
    model.AddMaxEquality(max_assignments, [total_assignments[agent.name] for agent in agents])

    model.Minimize(max_assignments)

    # Solve the model
    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = 300.0  # Optional time limit
    status = solver.Solve(model)

    # Initialize a list to store the assignments
    assignments = []

    if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
        for day in all_days:
            for task in tasks:
                if day in task_schedules[task]:
                    assigned_agents = [agent.name for agent in agents if solver.Value(x[(agent.name, task, day)]) == 1]
                    for agent_name in assigned_agents:
                        assignments.append({"Day": day, "Task": task, "Agent": agent_name})
        # Optionally, collect total assignments per agent
        agent_assignments = {agent.name: solver.Value(total_assignments[agent.name]) for agent in agents}

        return assignments, agent_assignments
    else:
        print("No feasible solution found.")
        return  # Exit the function if no solution is found
