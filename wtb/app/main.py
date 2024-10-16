import toml
from utils.internal_dev import print_taskboards
from utils.os_structure import save_weekly_taskboards
from utils.string_process import soup_to_weekly_taskboards
from utils.webscrape import get_soup_from_altiplan

if __name__ == "__main__":
    # Get configs from config file
    config = toml.load("config.toml")
    NUM_WEEKDAYS = config["settings"]["NUM_WEEKDAYS"]

    soup = get_soup_from_altiplan(config)

    weekly_taskboards = soup_to_weekly_taskboards(soup, config)
    print_taskboards(weekly_taskboards, config)
    save_weekly_taskboards(weekly_taskboards, NUM_WEEKDAYS)
