from app.utils.os_structure import write_schedule_to_excel
from app.utils.schedule_preprocess import parse_constraints
from app.utils.scheduling_engines import back_scheduling

DATA_PATH = "data/2025_january/ryg_data.xlsx"
RESULT_PATH = "data/results/2025_january/ryg_results.xlsx"

if __name__ == "__main__":
    tasks, task_schedules, agents = parse_constraints(DATA_PATH)
    print("*** Agents ***")
    for agent in agents:
        print(agent)

    print("\n*** Tasks ***")
    print(tasks)
    print(task_schedules)

    results = back_scheduling(tasks, task_schedules, agents)
    if results is not None:
        assignments, agent_assignments = results
        write_schedule_to_excel(RESULT_PATH, DATA_PATH, assignments, agent_assignments)
