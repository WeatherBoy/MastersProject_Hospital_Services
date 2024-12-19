from app.utils.data_process import lejeplan_daily_tasks_lists, load_arbejdsplan_lejeplan

if __name__ == "__main__":
    lejeplan, arbejdsplan = load_arbejdsplan_lejeplan("march")
    tasks_matrix = lejeplan_daily_tasks_lists(lejeplan)
    print(tasks_matrix)
