import os
import cv2
import numpy as np
import glob
import argparse
import shutil
from datetime import datetime


def get_parser():
    parser = argparse.ArgumentParser(description='Check the water mask and overlay')
    parser.add_argument('--seg-path', type=str, required=True,
                        help='Path to the segmentation folder')

    return parser.parse_args()


def main(args):

    mask_files = glob.glob(os.path.join(args.seg_path, 'mask', '*.png'))
    overlay_dir = os.path.join(args.seg_path, 'overlay')
    output_overlay_dir = os.path.join(f'{args.seg_path}_filtered', 'overlay')
    os.makedirs(output_overlay_dir, exist_ok=True)
    output_mask_dir = os.path.join(f'{args.seg_path}_filtered', 'mask')
    os.makedirs(output_mask_dir, exist_ok=True)

    ### Check the water mask
    # Threshold area
    area_threshold = 30000 # 35000

    # Position to check if it is included in the river mask (row, col)
    pos = (133, 486)

    image_areas = {}
    eliminated_area = {}

    for mfile in mask_files:
        # Read image in grayscale
        mask = cv2.imread(mfile, cv2.IMREAD_GRAYSCALE)

        binary_mask = (mask > 0).astype(np.uint8)

        # Find connected components
        num_labels, labels = cv2.connectedComponents(binary_mask)

        # Find the label of the component that contains this position
        component_label = labels[pos]

        if component_label == 0:
            area = 0  # position is in background
            eliminated_image_name = os.path.basename(mfile)
            eliminated_area[eliminated_image_name] = area
        else:
            area = np.sum(labels == component_label)

        image_name = os.path.basename(mfile)
        image_name_no_ext = os.path.splitext(image_name)[0]
        image_areas[image_name_no_ext] = area
        print('image_name', image_name)
        print('area', area)

        overlay_path_img = os.path.join(overlay_dir, image_name)

        # Copy image if area exceeds threshold
        if area <= area_threshold:
            os.remove(mfile)
            os.remove(overlay_path_img)
            print(f'{image_name} removed, area: {area}')


if __name__ == '__main__':

    _args = get_parser()
    print(_args)

    main(_args)
