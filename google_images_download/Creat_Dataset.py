#Creating dataset for Bonnet

import google_images_download # Importing the library
import time # Importing the time library to check the time of code execution

from ruamel.yaml import YAML # for comments
import os
from collections import OrderedDict # To keep the output order


def Deafault_yaml():
    Deafault_yaml = """\
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
    return Deafault_yaml


# Creat Yaml Files
def Creat_Yaml_Files(arguments, paths):

    yaml = YAML()
    Dataset = yaml.load(Deafault_yaml())

    # All the parameters in yaml could be given by users
    if arguments['Y_name']:
        Dataset['name'] = arguments['Y_name']

    if arguments['Y_data_dir']:
        Dataset['data_dir'] = arguments['Y_data_dir']

    if arguments['Y_buff']:
        Dataset['buff'] = arguments['Y_buff']

    if arguments['Y_buff_nr']:
        Dataset['buff_nr'] = arguments['Y_buff_nr']

    if arguments['Y_img_prop_width']:
        Dataset['img_prop']['width'] = arguments['Y_img_prop_width']

    if arguments['Y_img_prop_height']:
        Dataset['img_prop']['height'] = arguments['Y_img_prop_height']

    if arguments['Y_img_prop_depth']:
        Dataset['img_prop']['depth'] = arguments['Y_img_prop_depth']

    if arguments['Y_force_resize']:
        Dataset['force_resize'] = arguments['Y_force_resize']

    if arguments['Y_force_remap']:
        Dataset['force_remap'] = arguments['Y_force_remap']

    if arguments['Y_label_map']:
        Dataset['label_map'] = arguments['Y_label_map']

    if arguments['Y_color_map']:
        Dataset['color_map'] = arguments['Y_color_map']

    if arguments['Y_label_remap']:
        Dataset['label_remap'] = arguments['Y_label_remap']

    # automatically generate the direction of the dataset
    _key_num = 0 # count for keys
    _label_num = 0 # count for labels
    _color_num_1 = 0  # count for colormap
    _color_num_2 = 0  # count for colormap
    _color_num_3 = 0  # count for colormap

    # for each key create a yaml unit.
    for _key in paths:

        # automatically generate the data_dir for each label
        _lists = list(paths[_key])
        _raw_dir = _lists[0]
        print("_raw_dir:", _raw_dir)

        if not arguments['Y_data_dir']:
            Dataset['data_dir'] = os.path.dirname(os.path.dirname(_raw_dir))

        Data_Dir = os.path.dirname(_raw_dir)
        print("data_dir:", Data_Dir)
        _name = 'label'+str(_key_num)
        _data_dir = "data_dir"+str(_key_num)
        Dataset[_name]= _key
        Dataset[_data_dir] = Data_Dir

        # automatically generate the relative maps
        if not arguments['Y_label_map']:
            Dataset['label_map'][_label_num] = _key

        if not arguments['Y_color_map']:
            Dataset['color_map'][_label_num] = [_color_num_1, _color_num_2, _color_num_3]
            if _color_num_1 < 192:
                _color_num_1 += 64
            elif _color_num_2 < 192:
                _color_num_2 += 64
            elif _color_num_3 < 192:
                _color_num_3 += 64
            else:
                print("Color Map Overflow!!!")

        if not arguments['Y_label_remap']:
            Dataset['label_remap'][_label_num] = _key_num

        _key_num += 1
        _label_num += 20

    # create yaml
    _folder = 'cfg'
    if not os.path.exists(_folder):
        os.makedirs(_folder)
    Yaml_File = open('cfg/dataset.yaml', 'wb+')
    yaml.dump(Dataset, Yaml_File)

    Yaml_File.close()
    return

# Main Program
def main():
    records = google_images_download.user_input()
    for arguments in records:

        if arguments['single_image']:  # Download Single Image using a URL
            response = google_images_download.googleimagesdownload() # class instantiation
            response.single_image(arguments['single_image'])
        else:  # or download multiple images based on keywords/keyphrase search
            t0 = time.time()  # start the timer
            response = google_images_download.googleimagesdownload() # class instantiation
            paths = response.download(arguments)  # wrapping response in a variable just for consistency
            print("\nEverything downloaded!")

            Creat_Yaml_Files(arguments,paths)
            print("\nYaml files created!")

            t1 = time.time()  # stop the timer
            total_time = t1 - t0  # Calculating the total time required to crawl, find and download all the links of 60,000 images
            print("Total time taken: " + str(total_time) + " Seconds")

if __name__ == "__main__":
    main()