import os
from pathlib import Path
import random
from distutils.dir_util import copy_tree
import shutil
from shutil import copy
from PIL import Image
import numpy as np

def calc_new_box(img_path, old_box):
    # returns a box - float list (left, top, right, bottom) == (x1, y1, x2, y2)
    pass

def choose_line(img_pth, label_path):
    # returns a line
    # if no match - return None
    pass

def new_img(img_arr, old_box, new_box):
    # returns a new image array
    pass

def new_imgs(in_dir, out_dir, mode, num_files):

    # create sub directories - assuming no files in parent dir
    for dir_name in os.listdir(in_dir):
        Path(out_dir, dir_name).mkdir(parents=True, exist_ok=True)

    # choose files randomly - assuming no dirs in subdirs
    imgs_filenames = random.sample(os.listdir(Path(in_dir, 'ImageSets')), num_files)

    for img_filename in imgs_filenames:

        img_src_path = Path(in_dir, 'ImageSets', img_filename)
        img_dst_path = Path(out_dir, 'ImageSets', img_filename)
        label_src_path = Path(in_dir, 'label_2', img_filename.split('.')[0] + '.txt')
        label_dst_path = Path(out_dir, 'label_2', img_filename.split('.')[0] + '.txt')

        old_line = choose_line(img_src_path, label_src_path) # label line
        if old_line is None: continue
        line_elemns = old_line.split(' ')
        old_box = [float(elem) for elem in line_elemns[4: 8]]
        new_box = calc_new_box(img_src_path, old_box) if mode == 'shift' else old_line # float list

        # copy calib file
        calib_src_path = Path(in_dir, 'calib', str(label_src_path).split('/')[-1])
        copy(calib_src_path, str(Path(out_dir, 'calib')))

        # write new label file
        line_elemns[4: 8] = ['{:3f}'.format(elem) for elem in new_box]
        new_line = (' ').join(line_elemns)
        with open(label_dst_path, 'w') as label_file:
            label_file.write(new_line + '\n')

        # change image file
        img = Image.open(img_src_path)
        img_arr = np.array(img)
        new_arr = new_img(img_arr, old_box, new_box)
        new_img = Image.fromarray(new_arr)
        new_img.save(img_dst_path)


def create_test_file(dir):
    file_path = Path(dir, 'ImageSets', 'test.txt')
    file_names = sorted([file for file in os.listdir(str(Path(dir, 'image2'))) if file.endswith('.png')])
    with open(file_path, 'w') as test_file:
        for txt_filename in file_names:
            test_file.write(txt_filename.split('.')[0] + '\n')

def cmp_alpha(src, dst):
    pass

def quant(src, dst):
    Path(dst, 'calib').mkdir(parents=True, exist_ok=True)
    copy_tree(str(Path(src, 'calib')), str(Path(dst,'calib')))
    Path(dst, 'image2').mkdir(parents=True, exist_ok=True)
    copy_tree(str(Path(src, 'image_2')), str(Path(dst, 'image2')))
    Path(dst, 'ImageSets').mkdir(parents=True, exist_ok=True)
    copy(str(Path(src, 'ImageSets', 'trainval.txt')), str(Path(dst, 'ImageSets')))
    shutil.move(str(Path(dst, 'ImageSets', 'trainval.txt')), str(Path(dst, 'ImageSets', 'test.txt')))
    Path(dst, 'label_2').mkdir(parents=True, exist_ok=True)
    for filename in os.listdir(Path(src, 'label_2')):
        src_file_path = Path(src, 'label_2', filename)
        dst_file_path = Path(dst, 'label_2', filename)
        with open(src_file_path, 'r') as src_file:
            lines = src_file.read().splitlines()
            with open(dst_file_path, 'w') as dst_file:
                for line in lines:
                    elems = line.split(' ')
                    quant_box = ['{:3f}'.format(int(float(elem))) for elem in elems[4: 8]]
                    new_line_list = [elems[0], *[-1] * 2, -10, *quant_box, *[-1] * 3,
                                     *[-1000] * 3, -10, '{:8f}'.format(0)]
                    new_line = (' ').join([str(elem) for elem in new_line_list])
                    dst_file.write(new_line + '\n')


if __name__=='__main__':

    '''
    Want to use kitti's ground truth data to examine alpha.
    In order to be able to change images - have to quantisize 2D boxes and use them as predictions, and run the network on them.
    Goal is (only on chosen files):
        - (compare quantizied predictions (under 'tools' - output dirs) to original ones: make sure network is running OK)
        - compare static (black) images to quantizied (relevant boxes)
        - compare shifted (black) images to quantizied (relevant boxes)
    '''

    '''
    'resources' dir - put bboxes predictions
    '_OUTPUT_DIR' dir - output: submission data (labels with alpha&yaw, same bboxes as input) & images with bboxes (different resolution! compare boxes against original input)
    '''

    # put all KITTI's quantizied GT data in new data folder - under testing
    # put KITTI's testing folder labels under 'resources'
    kitti_orig_dir = '/home/elad/Data/KITTI/training'
    kitti_quant_dir = '/home/elad/Data/KITTI_QUANTIZIED/testing'
    quant(kitti_orig_dir, kitti_quant_dir)
    Path('../resources', 'KITTI_QUANT_test_boxes').mkdir(parents=True, exist_ok=True)
    copy_tree(str(Path(kitti_quant_dir, 'label_2')), str(Path('../resources', 'KITTI_QUANT_test_boxes')))

    kitti_stat_dir = '/home/elad/Data/KITTI_STAT/testing'
    kitti_shift_dir= '/home/elad/Data/KITTI_SHIFT/testing'

    in_dir = kitti_quant_dir
    out_dir = kitti_stat_dir
    new_imgs(in_dir, out_dir, mode='stat', num_files=10)
    create_test_file(out_dir)

    Path('../resources', 'KITTI_STAT_test_boxes').mkdir(parents=True, exist_ok=True)
    copy_tree(str(Path(kitti_stat_dir, 'label_2')), str(Path('../resources', 'KITTI_STAT_test_boxes')))
    Path('../resources', 'KITTI_SHIFT_test_boxes').mkdir(parents=True, exist_ok=True)
    copy_tree(str(Path(kitti_shift_dir, 'label_2')), str(Path('../resources', 'KITTI_SHIFT_test_boxes')))
    #
    # # TODO run network
    #
    # orig_pred_dir = '/home/PycharmProjects/EgoNet/tools/YOUR_OUTPUT_DIR'
    # stat_pred_dir = '/home/PycharmProjects/EgoNet/tools/YOUR_STAT_DIR'
    # shift_pred_dir = '/home/PycharmProjects/EgoNet/tools/YOUR_SHIFT_DIR'
    # cmp_alpha(orig_pred_dir, dst=stat_pred_dir) # TODO cmp alpha also between GT and pred for sanity check
