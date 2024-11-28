import time

import toml

from app.utils.data_process import soup_to_weekly_taskboards, update_taskboards_with_stuefordeling
from app.utils.internal_dev import save_functions_mismatch
from app.utils.os_structure import save_weekly_taskboards
from app.utils.visualise import save_taskboards_as_png
from app.utils.webscrape import get_soup_from_altiplan

if __name__ == "__main__":
    start = time.time()
    print("Starting the program...")

    # Get configs from config file
    config = toml.load("config.toml")
    NUM_WEEKDAYS = config["settings"]["NUM_WEEKDAYS"]

    soup = get_soup_from_altiplan(config)

    weekly_taskboards = soup_to_weekly_taskboards(soup, config)
    updated_weekly_taskboards, non_matching_functions = update_taskboards_with_stuefordeling(weekly_taskboards)
    # print_taskboards(updated_weekly_taskboards, config)
    save_functions_mismatch(weekly_taskboards, non_matching_functions)
    save_weekly_taskboards(updated_weekly_taskboards, NUM_WEEKDAYS)
    save_taskboards_as_png(updated_weekly_taskboards, config)

    print(f"\nProgram finished in {time.time() - start:.2f} seconds.")
