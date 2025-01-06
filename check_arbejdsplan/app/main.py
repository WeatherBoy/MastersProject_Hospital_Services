import toml
from app.utils.data_process import arbejdsplan_dict_with_date_keys, lejeplan_dict_with_date_keys, load_arbejdsplan_lejeplan

if __name__ == "__main__":
    # Get configs from config file
    config = toml.load("config.toml")

    lejeplan, arbejdsplan = load_arbejdsplan_lejeplan("march")

    lejeplan_dict = lejeplan_dict_with_date_keys(lejeplan)
    arbejdsplan_dict = arbejdsplan_dict_with_date_keys(arbejdsplan, config)

    print(f"LEJEPLAN:\n{lejeplan_dict}")
    print(f"\nARBEJDSPLAN:\n{arbejdsplan_dict}")
