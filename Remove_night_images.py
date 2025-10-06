import os
import argparse
from datetime import time
import pytz
from myutils.Process_EXIF import *


def get_parser():
    parser = argparse.ArgumentParser(description='The date to be process')
    parser.add_argument('--date-str', type=str, required=True,
                        help='Date string YYYY-MM-DD')

    return parser.parse_args()


def main(args):
    # Folder containing images
    folder_path = f"/home/shirui_hao/V-FloodNet-SH/nhd_data/lavenders_bridge/{args.date_str}"

    # Time window
    start_time = time(18, 0)  # 19
    end_time = time(7, 0)     # 6


    def is_in_night_window(dt):
        # If time is >= 19:00 or < 06:00, we consider it "night"
        return dt.time() >= start_time or dt.time() < end_time


    for filename in os.listdir(folder_path):
        if filename.lower().endswith(('.jpg', '.jpeg', '.png')):
            filepath = os.path.join(folder_path, filename)
            date_taken = get_date_taken(filepath, 'datetime')
            if date_taken:
                if is_in_night_window(date_taken):
                    print(f"Deleting {filename} (taken at {date_taken})")
                    os.remove(filepath)


if __name__ == '__main__':

    _args = get_parser()
    print(_args)

    main(_args)

