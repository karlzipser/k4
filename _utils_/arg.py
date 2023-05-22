import os
import glob
import re
from pathlib import Path
import time
gg = glob.glob

import numpy as np
from k4.utils.core.paths import *
rnd = np.random.random
rndint = np.random.randint
rndn = np.random.randn
rndchoice = np.random.choice
na = np.array
degrees = np.degrees
arange = np.arange
shape = np.shape
randint = np.random.randint
randn = np.random.randn
zeros = np.zeros
ones = np.ones
reshape = np.reshape
mod = np.mod
array = np.array
sqrt = np.sqrt
sin = np.sin
cos = np.cos
std = np.std
pi = np.pi
#from k4.utils import *

def natural_keys(text):
    '''
    alist.sort(key=natural_keys) sorts in human order
    http://nedbatchelder.com/blog/200712/human_sorting.html
    (See Toothy's implementation in the comments)
    '''
    def atoi(text):
        return int(text) if text.isdigit() else text
    return [ atoi(c) for c in re.split('(\d+)', text) ]

def opj(*args):
    if len(args) == 0:
        args = ['']
    str_args = []
    for a in args:
        str_args.append(str(a))
    return os.path.join(*str_args)

def opjh(*args):
    return opj(home_path,opj(*args))

def opjD(*args):
    return opjh('Desktop',opj(*args))

def sgg(d,r=0):
    return sorted(gg(d,recursive=r),key=natural_keys)

def sggo(d,*args,r=0):
    a = opj(d,*args)
    return sgg(a,r=r)




def read_img_and_get_orientation_correction_degrees(path):
    import exifread
    """https://pypi.org/project/ExifRead/"""
    tags = {}
    with open(path, 'rb') as f:
        tags = exifread.process_file(f, details=False)
    if "Image Orientation" in tags.keys():
        orientation = tags["Image Orientation"]
        val = orientation.values
        if 3 in val:
            return 180
        if 6 in val:
            return 270
        if 8 in val:
            return 90
    return 0

def has_exif(path):
    import exifread
    with open(path,'r') as f:
        l = len(exifread.process_file(f))
    if l:
        return True
    else:
        return False

def load_image_with_orientation(filepath,change_rgb=True):
    from PIL import Image, ExifTags
    from numpy import asarray
    theta = read_img_and_get_orientation_correction_degrees(filepath)
    if theta in [90,180,270]:
        image=Image.open(filepath)
        image = image.rotate(theta, expand=True)
        image = na(image)[:,:,:3]
    else:
        image = imread(filepath)[:,:,:3]
        if change_rgb:
            image = cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
    return image, theta

def zimread(p):
    return load_image_with_orientation(p)[0]


import matplotlib
import matplotlib.pyplot as plt  # the Python plotting package
plt.ion()
plot = plt.plot
hist = plt.hist
xlim = plt.xlim
ylim = plt.ylim
clf = plt.clf
pause = plt.pause
figure = plt.figure
title = plt.title
plt.ion()
plt.show()
PP,FF = plt.rcParams,'figure.figsize'


def mi(
    image_matrix,
    figure_num = 1,
    subplot_array = [1,1,1],
    img_title = '',
    img_xlabel = 'x',
    img_ylabel = 'y',
    cmap = 'gray',
    toolBar = True,
    do_clf = True,
    do_axis = False ):
    """
    My Imagesc, displays a matrix as grayscale image if 2d, or color if 3d.
    Can take different inputs -- e.g.,

        from matrix:

            from k4.vis import *
            mi(np.random.rand(256,256),99,[1,1,1],'random matrix')

        from path:
            mi(opjh('Desktop','conv1'),1,[5,5,0])

        from list:
            l = load_img_folder_to_list(opjh('Desktop','conv5'))
            mi(l,2,[4,3,0])

        from dict:
            mi(load_img_folder_to_dict(opjh('Desktop','conv5')),1,[3,4,0])
    """
    if type(image_matrix) == str:
        l=load_img_folder_to_list(image_matrix)
        mi(l)
        return

    if type(image_matrix) == list:
        l=1.0*array(image_matrix)
        l/=l.max()
        mi(vis_square(l))
        return

    if type(image_matrix) == dict:
        img_keys = sorted(image_matrix.keys(),key=natural_keys)
        l = []
        for k in img_keys:
            l.append(image_matrix[k])
        mi(l)
        return        

    if toolBar == False:
        plt.rcParams['toolbar'] = 'None'
    else:
        plt.rcParams['toolbar'] = 'toolbar2'

    f = plt.figure(figure_num)
    if do_clf:
        #print('plt.clf()')
        plt.clf()

    if True:
        f.subplots_adjust(bottom=0.05)
        f.subplots_adjust(top=0.95)
        f.subplots_adjust(wspace=0.1)
        f.subplots_adjust(hspace=0.1)
        f.subplots_adjust(left=0.05)
        f.subplots_adjust(right=0.95)
    if False:
        f.subplots_adjust(bottom=0.0)
        f.subplots_adjust(top=0.95)
        f.subplots_adjust(wspace=0.0)
        f.subplots_adjust(hspace=0.1)
        f.subplots_adjust(left=0.0)
        f.subplots_adjust(right=1.0)
    f.add_subplot(subplot_array[0],subplot_array[1],subplot_array[2])
    imgplot = plt.imshow(image_matrix, cmap)
    imgplot.set_interpolation('nearest')
    if not do_axis:
        plt.axis('off')
    if len(img_title) > 0:# != 'no title':
        plt.title(img_title)
#
######################



import cv2
imread = cv2.imread


def resize_to_extent(img,extent,interpolation=cv2.INTER_AREA): #INTER_LINEAR):
    if extent != max(shape(img)):
        q = extent / max(shape(img))
        scale_percent = 60 # percent of original size
        width = int(img.shape[1] * q)
        height = int(img.shape[0] * q)
        dim = (width, height)
        return cv2.resize(img, dim, interpolation=interpolation)
    else:
        print('resize_to_extent(): no resizing')
        return img







import argparse

def parse_args_to_dict(dict_in):

	dict_out = {}

	parser = argparse.ArgumentParser()

	for k in dict_in:

		if len(k) == 1:
			dash = '-'
		else:
			dash = '--'

		if type(dict_in[k])is type:
			parser.add_argument(
				dash+k,
				type=dict_in[k],
				required=True,
			)
		else:
			parser.add_argument(
				dash+k,
				nargs='?',
				type=type(dict_in[k]),
				required=False,
				default=dict_in[k],
			)

	args = parser.parse_args()

	for k in vars(args):
		dict_out[k] = vars(args)[k]

	for k in dict_in:
		if k not in dict_out or dict_out[k] is None:
			print(
				'***',
				k,
				'must have value and cannot be None'
			)
			assert(False)

	return dict_out







if __name__ == '__main__':

	dict_in = {
		'x':int,#5,
		'y':2.,
		'hi':str,#'hello'
	}

	print('dict_in:',dict_in)

	dict_out = parse_args_to_dict(dict_in)

	print('dict_out',dict_out)

	print(dict_out['hi'],'Product:', dict_out['x'] * dict_out['y'])


	#EOF
