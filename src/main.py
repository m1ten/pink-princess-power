import sys
import os
from findtarget import ft_main
import json


def main():
    # distance from top left fiducial to bottom right fiducial (center to center) in mm
    fid_dis_left_to_right = 190  # millimeters
    fid_diameter = 61  # millimeters
    avg_fl = 1234  # millimeters

    args = sys.argv[1:]

    img_path = input('Path to a image (Y/y to take picture): ')
    if img_path == 'Y' or img_path == 'y':
        # take a picture from android
        # and save it to img_path
        pass
    else:
        # check if the path is valid
        if not os.path.isfile(img_path):
            print('Invalid path')
            exit()

        img_details = ft_main(img_path, True, avg_fl, fid_dis_left_to_right, None)

    # write the details to a json file
    with open('img_details.json', 'w') as f:
        data = json.dumps(img_details.__dict__, indent=4)
        f.write(data)

    print(img_details.__dict__)


if __name__ == '__main__':
    main()
