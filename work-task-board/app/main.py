import toml
from utils.string_process import soup_to_weekly_taskboards
from utils.os_structure import save_weekly_taskboards
from utils.internal_dev import print_TaskBoards
from utils.webscrape import get_soup_from_altiplan


if __name__ == "__main__":
    # Get configs from config file
    config = toml.load("config.toml")
    NUM_WEEKDAYS = config["settings"]["NUM_WEEKDAYS"]
    ERGO_AKTIVITETER = config["settings"]["ERGO_AKTIVITETER"]
    BARN_SYG_AND_FERIE = config["settings"]["BARN_SYG_AND_FERIE"]

    soup = get_soup_from_altiplan(config)

    skipable_funcs = [ERGO_AKTIVITETER, *BARN_SYG_AND_FERIE]
    weekly_taskboards = soup_to_weekly_taskboards(soup, skipable_funcs, config, NUM_WEEKDAYS)
    print_TaskBoards(weekly_taskboards, config)
    save_weekly_taskboards(weekly_taskboards, NUM_WEEKDAYS)
