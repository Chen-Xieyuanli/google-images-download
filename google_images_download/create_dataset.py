# Creating dataset for Bonnet

import google_images_download  # Importing the library
import time  # Importing the time library to check the time of code execution

from ruamel.yaml import YAML  # for comments
import os
from collections import OrderedDict  # To keep the output order


def deafault_yaml():
    deafault_yaml = """\
# dataset cfg file
name: "general"
data_dir: "/cache/datasets/persons/dataset"
buff: True            # if this is true we buffer buff_n images in a fifo
buff_nr: 3000         # number of images to keep in fifo (prefetch batch) <-should be bigger than batch size to make sense
img_prop:
  width: 512
  height: 512
  depth: 3            # number of channels in original image
force_resize: True    # if dataset contains images of different size, it should be True
force_remap: False
label_map:
  0: "background"
color_map: # bgr
  0: [0, 0, 0]
label_remap:          # for softmax (it must be an index of the onehot array)
  0: 0
"""
    return deafault_yaml


# create yaml Files
def create_yaml_files(arguments, paths):

    yaml = YAML()
    dataset = yaml.load(deafault_yaml())

    # All the parameters in yaml could be given by users
    if arguments['Y_name']:
        dataset['name'] = arguments['Y_name']

    if arguments['Y_data_dir']:
        dataset['data_dir'] = arguments['Y_data_dir']

    if arguments['Y_buff']:
        dataset['buff'] = arguments['Y_buff']

    if arguments['Y_buff_nr']:
        dataset['buff_nr'] = arguments['Y_buff_nr']

    if arguments['Y_img_prop_width']:
        dataset['img_prop']['width'] = arguments['Y_img_prop_width']

    if arguments['Y_img_prop_height']:
        dataset['img_prop']['height'] = arguments['Y_img_prop_height']

    if arguments['Y_img_prop_depth']:
        dataset['img_prop']['depth'] = arguments['Y_img_prop_depth']

    if arguments['Y_force_resize']:
        dataset['force_resize'] = arguments['Y_force_resize']

    if arguments['Y_force_remap']:
        dataset['force_remap'] = arguments['Y_force_remap']

    if arguments['Y_label_map']:
        dataset['label_map'] = arguments['Y_label_map']

    if arguments['Y_color_map']:
        dataset['color_map'] = arguments['Y_color_map']

    if arguments['Y_label_remap']:
        dataset['label_remap'] = arguments['Y_label_remap']

    # automatically generate the direction of the dataset
    key_num = 0  # count for keys
    label_num = 0  # count for labels
    color_num_1 = 0  # count for colormap
    color_num_2 = 0  # count for colormap
    color_num_3 = 0  # count for colormap

    # for each key create a yaml unit.
    for keys in paths:

        # automatically generate the data_dir for each label
        lists = list(paths[keys])
        raw_dir = lists[0]
        print("_raw_dir:", raw_dir)

        if not arguments['Y_data_dir']:
            dataset['data_dir'] = os.path.dirname(os.path.dirname(raw_dir))

        raw_data_dir = os.path.dirname(raw_dir)
        print("data_dir:", raw_data_dir)
        filename = 'label' + str(key_num)
        data_dir = "data_dir" + str(key_num)
        dataset[filename] = keys
        dataset[data_dir] = raw_data_dir

        # automatically generate the relative maps
        if not arguments['Y_label_map']:
            dataset['label_map'][label_num] = keys

        if not arguments['Y_color_map']:
            dataset['color_map'][label_num] = [
                color_num_1, color_num_2, color_num_3]
            if color_num_1 < 192:
                color_num_1 += 64
            elif color_num_2 < 192:
                color_num_2 += 64
            elif color_num_3 < 192:
                color_num_3 += 64
            else:
                print("Color Map Overflow!!!")

        if not arguments['Y_label_remap']:
            dataset['label_remap'][label_num] = key_num

        key_num += 1
        label_num += 20

    # create yaml
    if arguments['Y_directory']:
        _folder = arguments['Y_directory']  # use the specific direction
    else:
        _folder = 'cfg/'  # default direction

    if arguments['Y_filename']:
        _filename = arguments['Y_filename']  # use the specific direction
    else:
        _filename = 'dataset'  # default direction

    if not os.path.exists(_folder):
        os.makedirs(_folder)
    yaml_file = open(_folder + _filename + '.yaml', 'wb+')
    yaml.dump(dataset, yaml_file)
    yaml_file.close()

    return


# Main Program
def main():
    records = google_images_download.user_input()
    for arguments in records:

        if arguments['single_image']:  # Download Single Image using a URL
            response = google_images_download.googleimagesdownload()  # class instantiation
            response.single_image(arguments['single_image'])
        else:  # or download multiple images based on keywords/keyphrase search
            t0 = time.time()  # start the timer
            response = google_images_download.googleimagesdownload()  # class instantiation
            # wrapping response in a variable just for consistency
            paths = response.download(arguments)
            print("\nEverything downloaded!")

            create_yaml_files(arguments, paths)
            print("\nYaml files created!")

            t1 = time.time()  # stop the timer
            # Calculating the total time required to crawl, find and download
            # all the links of 60,000 images
            total_time = t1 - t0
            print("Total time taken: " + str(total_time) + " Seconds")


if __name__ == "__main__":
    main()
