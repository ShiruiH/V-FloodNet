import os
from glob import glob
import argparse
from datetime import datetime
from myutils.Process_EXIF import *


def get_parser():
    parser = argparse.ArgumentParser(description='The date to be process')
    parser.add_argument('--date-str', type=str, required=True,
                        help='Date string YYYY-MM-DD')

    return parser.parse_args()


# Usage
def main(args):

    parent_path = f'/home/shirui_hao/V-FloodNet-SH/nhd_data'
    sub_folders = glob(os.path.join(parent_path, 'lavenders_bridge', f'{args.date_str}'))
    for each_folder in sub_folders:
        all_files = glob(os.path.join(each_folder, '*.jpg'))
        for f in all_files:
            print(f)
            rename_with_date_taken(f, 'string')


if __name__ == '__main__':

    _args = get_parser()
    print(_args)

    main(_args)

