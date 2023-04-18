import sys
from findtarget import ft_main

def main():
    args = sys.argv[1:]

    img_path = input('Path to a image (Y/y to take picture): ')
    if img_path == 'Y' or img_path == 'y':
        # take picture
        pass
    else:
       img_details = ft_main(img_path, True)

if __name__ == '__main__':
    main()