## Dataset Creator
#### General description 
Writing a script that can automatically download images from 'Google Images' and generate a dataset for Bonnet.

#### Requirements
- This script can generate different types of dataset according to user-specified keywords/key-phrases.
- This script can be invoked from another python file.
- The generated dataset follows the standard dataset formats of Bonnet (generating a configuration document data.yaml).

#### Next step (TODO)
clean up the outliers in the data using an unsupervised clustering

## How to run
#### Install the Google Images Download
##### This script is based on the Google Images Download, so please have a look at the Google Images Download package first before using this script.
- If you want to adjust all the parameters in the generated configuration yaml file. You have to download the whole package, because I did some modification in the original Google Images Download package.

```sh
$ git clone https://github.com/Chen-Xieyuanli/google-images-download.git
```

- If you only need to create a configuration yaml file which can automatically generate dataset list and the label/color maps, you could only download this script and install the Google Images Download using pip as below.

```sh
$ pip install google_images_download
```
#### Other dependencies

- I created this script using Ubuntu14.04 and python2.7.6
- Please install 'pyyaml' and 'ruamel.yaml' by typing:

```sh
$ pip install pyyaml  
$ pip install ruamel.yaml
```

- During the development, I also get the error of "ImportError: cannot import name get_column_letter
". I solved this problem by reinstalling the latest openpyxl. Then it works.

#### Run a sample demo

- You could directly run a demo using commands below, in the folder witch contains this script.

```sh
$ python Creat_Dataset.py --keywords "bears,cats,birds" --limit 20 
```

- You could change all the parameters in the generated configuration yaml file, and run a demo using commands below.

```sh
$ python Creat_Dataset.py --keywords "bears,cats,birds" --limit 5 --Y_img_prop_height 360 --Y_force_remap True --Y_color_map "0:[0,0,0] 20:[64,0,0] 40:[128,0,0]"
```

- If you are in the same situation as me which cannot directly visit iamge.google.com ;-), you could run this script using the proxy. It would be like:

```sh
$ python Creat_Dataset.py --keywords "bears,cats,birds" --limit 20 --proxy 127.0.0.1:8123
```
