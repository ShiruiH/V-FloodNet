import os
import pandas as pd
import argparse
import shutil
from datetime import timedelta
import matplotlib.pyplot as plt


def get_parser():
    parser = argparse.ArgumentParser(description='Estimate Water Level')
    parser.add_argument('--estimate-path', type=str, required=True,
                        help='Path to the water level estimation')

    return parser.parse_args()


def main(args):

    convert_file = f'px_to_meter_202411.txt'

    shutil.copy(os.path.join(f'/home/shirui_hao/V-FloodNet-SH', convert_file), os.path.join(args.estimate_path, convert_file))

    estimate_file = f'waterlevel.csv'
    estimate_csv = os.path.join(args.estimate_path, estimate_file)

    convert_txt = os.path.join(args.estimate_path, convert_file)

    output_csv = os.path.join(args.estimate_path, 'waterlevel_with_metre.csv')

    # --- Step 1: Read modeled estimation in px ---
    df1 = pd.read_csv(estimate_csv)
    df1.rename(columns={df1.columns[0]: 'datetime'}, inplace=True)
    df1['datetime'] = pd.to_datetime(df1['datetime'], dayfirst=True, errors='coerce')
    df1 = df1.rename(columns={'datetime': 'datetime_estimate'})

    # --- Step 2: Read constants from txt ---
    with open(convert_txt, 'r') as f:
        line = f.read().strip()
    a, b = map(float, line.split())
    # Compute estimated_height
    df1['estimated_height'] = df1['est_ref0_px'] * a + b

    df1 = df1.sort_values('datetime_estimate')

    df1.to_csv(output_csv, index=False)
    print(f'Water level in metre is updated, csv file is saved.')


if __name__ == '__main__':

    _args = get_parser()
    print(_args)

    main(_args)
