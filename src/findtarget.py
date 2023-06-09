import numpy as np
import cv2 as cv
import glob
import sys
import re


class Image:
    name: str
    focal_length: float
    distance: float
    angle: float

    def __init__(self, name: str, focal_length: float, distance: float, angle: float) -> None:
        self.name = name
        self.focal_length = focal_length
        self.distance = distance
        self.angle = angle


def focal_length(measured_distance, real_width, width_in_rf_image) -> float:
    focal_length_value = (width_in_rf_image * measured_distance) / real_width
    return focal_length_value


def distance_finder(focal_length, real_face_width, face_width_in_frame) -> float:
    distance = (real_face_width * focal_length)/face_width_in_frame
    return distance


def ft_main(fname: str, display: bool, avg_fl: float, fid_dis_left_to_right: float, real_distance: float) -> Image:

    # print(f'\n{fname}')
    img = cv.imread(fname)

    # circle fiducials
    hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)

    # find yellow
    # lower_color = np.array([20, 100, 100])
    # upper_color = np.array([30, 255, 255])

    # find green
    lower_color = np.array([40, 100, 100])
    upper_color = np.array([70, 255, 255])
    mask = cv.inRange(hsv, lower_color, upper_color)
    res = cv.bitwise_and(img, img, mask=mask)

    gray = cv.cvtColor(res, cv.COLOR_BGR2GRAY)

    # filter out noise, there are 4 fiducials +/- 10% of each other
    kernel = np.ones((5, 5), np.uint8)
    mask = cv.morphologyEx(mask, cv.MORPH_OPEN, kernel)
    mask = cv.morphologyEx(mask, cv.MORPH_CLOSE, kernel)

    # find contours
    contours, hierarchy = cv.findContours(
        mask, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

    # find the 4 fiducials
    fiducials = []
    for cnt in contours:
        M = cv.moments(cnt)
        if M['m00'] != 0:
            cx = int(M['m10']/M['m00'])
            cy = int(M['m01']/M['m00'])
            fiducials.append([cx, cy])

    # sort the fiducials
    fiducials = sorted(fiducials, key=lambda x: x[0])
    fiducials = sorted(fiducials, key=lambda x: x[1])

    if len(fiducials) < 4:
        # lower the tolerance and try again
        lower_color = np.array([40, 50, 50])
        upper_color = np.array([70, 255, 255])
        mask = cv.inRange(hsv, lower_color, upper_color)
        res = cv.bitwise_and(img, img, mask=mask)

        gray = cv.cvtColor(res, cv.COLOR_BGR2GRAY)

        # filter out noise, there are 4 fiducials +/- 10% of each other
        kernel = np.ones((5, 5), np.uint8)
        mask = cv.morphologyEx(mask, cv.MORPH_OPEN, kernel)
        mask = cv.morphologyEx(mask, cv.MORPH_CLOSE, kernel)

        # find contours
        contours, hierarchy = cv.findContours(
            mask, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

        # find the 4 fiducials
        fiducials = []
        for cnt in contours:
            M = cv.moments(cnt)
            if M['m00'] != 0:
                cx = int(M['m10']/M['m00'])
                cy = int(M['m01']/M['m00'])
                fiducials.append([cx, cy])

        # sort the fiducials
        fiducials = sorted(fiducials, key=lambda x: x[0])
        fiducials = sorted(fiducials, key=lambda x: x[1])

    # show the fiducials
    for fiducial in fiducials:
        cv.circle(img, (fiducial[0], fiducial[1]), 5, (0, 0, 255), -1)

    # find the center of the fiducials, which is the target
    target = [0, 0]
    for fiducial in fiducials:
        target[0] += fiducial[0]
        target[1] += fiducial[1]
    target[0] = int(target[0] / len(fiducials))
    target[1] = int(target[1] / len(fiducials))

    # show the target
    cv.circle(img, (target[0], target[1]), 5, (0, 255, 0), -1)

    # show the image
    if display:
        # resize the image by 50% to fit
        show_img = cv.resize(img, (0, 0), fx=0.5, fy=0.5)
        cv.imshow(f'{fname} modified', show_img)
        cv.waitKey(0)
        cv.destroyAllWindows()

    # distance from top left fiducial to bottom right fiducial (center to center) in pixels
    fid_dis_left_to_right_pixels = np.sqrt(
        (fiducials[0][0] - fiducials[3][0])**2 + (fiducials[0][1] - fiducials[3][1])**2)

    # print('fid_dis_left_to_right_pixels = ', fid_dis_left_to_right_pixels)

    if real_distance is not None:
        fl = focal_length(real_distance, fid_dis_left_to_right, fid_dis_left_to_right_pixels)
        avg_fl = fl

    found_distance = distance_finder(
        avg_fl, fid_dis_left_to_right, fid_dis_left_to_right_pixels)

    # print(f"Real distance: {real}mm")
    # print(f"Found distance: {found_distance} mm")

    # determine the angle of the target
    center_of_image = img.shape[1] / 2
    angle = np.arctan((target[0] - center_of_image) / avg_fl)
    # convert to degrees
    angle = angle * 180 / np.pi
    # print(f"Angle: {angle} degrees")

    return Image(fname, avg_fl, found_distance, angle)

    # reals.pop(0)

# average the focal lengths
# raw_fls = []
# for _, fl in fls:
#     raw_fls.append(fl)
# average_fl = sum(raw_fls) / len(raw_fls)
# print(f"Average focal length: {average_fl}")


if __name__ == '__main__':
    dirt = 'delta/*mm.jpg'

    # command line arguments, 1st is the file path, 2nd is whether or not to display the images
    args = sys.argv[1:]
    if len(args) < 2 or len(args) > 2:
        args = [dirt, False]
    elif len(args) == 2:
        if args[0] == '*':
            args[0] = dirt

        match = re.match(r'^(true|false)$', args[1], re.IGNORECASE)
        if match:
            args[1] = match.group(1).lower() == 'true'
        else:
            args = [dirt, False]

    images = glob.glob(args[0])

    if len(images) == 0:
        print('No images found')
        exit()

    # distance from top left fiducial to bottom right fiducial (center to center) in mm
    fid_dis_left_to_right = 190  # millimeters
    fid_diameter = 61  # millimeters

    # this is only true for images in delta/
    avg_fl = 1234  # millimeters

    #real_distances = [500, 1000, 1500, 2000, 2500, 3000, 3500]
    real_distances = []
    imgs = []
    for image in images:
        img = ft_main(image, args[1], avg_fl, fid_dis_left_to_right, None if len(real_distances) == 0 else real_distances[0])
        imgs.append(img)
        try:
            real_distances.pop(0)
        except:
            pass

    # sort the images by distance
    imgs = sorted(imgs, key=lambda x: x.distance)

    for img in imgs:
        print(f"{img.name}\tfocal length: {img.focal_length}mm\tdistance: {img.distance}mm\tangle: {img.angle} degrees")

    # find the average focal length but remove any outliers
    fls = []
    for img in imgs:
        fls.append(img.focal_length)
    fls = sorted(fls)
    fls.pop(0)
    fls.pop(-1)
    avg_fl = sum(fls) / len(fls)
    print(f"Average focal length: {avg_fl}")
