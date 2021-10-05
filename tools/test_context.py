import os
from pathlib import Path
import random

def calc_new_box(img_path, old_line):
    pass

def choose_box(img_pth, label_path):
    # if no match - return None
    pass

def new_img(img_arr, old_box, new_box):
    pass

def new_imgs(in_dir, out_dir, mode, num_files):

    # create sub directories - assuming no files in parent dir
    for dir_name in os.listdir(in_dir):
        new_dir_path = os.path.join(out_dir, dir_name)
        Path(new_dir_path).mkdir(parents=True, exist_ok=True)

    imgs_dirname = 'ImageSets'
    # choose files randomly - assuming no dirs in subdirs
    imgs_filenames = random.sample(os.listdir(os.path.join(in_dir, imgs_dirname)), num_files)

    for img_filename in imgs_filenames:
        img_src_path = os.path.join(in_dir, imgs_dirname, img_filename)
        img_dst_path = os.path.join(out_dir, imgs_dirname, img_filename)
        label_path = os.path.join(in_dir, 'label_2', img_filename)
        old_line = choose_box(img_src_path, label_path) # label line
        if old_line is None: continue
        new_line = calc_new_box(img_src_path, old_line) if mode == 'shift' else old_line

        # change image file
        with open(img_src_path, 'r') as img_src_file:
            lines = img_src_file.read().splitlines()
            for line in lines:
                elems = line.split(' ')
                cls, trunc, occ
                cls, center_x, center_y, width, height = [float(elem) for elem in line.split(' ')]
                if int(cls) !=3: continue
                abs_center_x, abs_center_y = img_width * center_x, img_height * center_y
                abs_width, abs_height = img_width * width, img_height * height
                left, right = abs_center_x - abs_width / 2, abs_center_x + abs_width / 2
                top, bottom = abs_center_y - abs_height / 2, abs_center_y + abs_height / 2
                kitti_box = (left, top, right, bottom)
                new_line_list = ['Car', * [-1] * 2, -10, * ['{:3f}'.format(elem) for elem in kitti_box], * [-1] * 3, * [-1000] * 3, -10, '{:8f}'.format(0)]
                new_line = (' ').join([str(elem) for elem in new_line_list])
                kitti_file.write(new_line + '\n')


def create_test_file(dir):
    # TODO sorted
    pass

def cmp_alpha(src, dst):
    pass

if __name__=='__main__':

    '''
    Want to use kitti's ground truth data to examine alpha.
    In order to be able to change images - have to quantisize 2D boxes and use them as predictions, and run the network on them.
    Goal is (only on chosen files):
        - (compare quantizied predictions (under 'tools' - output dirs) to original ones: make sure network is running OK)
        - compare static (black) images to quantizied (relevant boxes)
        - compare shifted (black) images to quantizied (relevant boxes)
    '''

    # TODO write a function to put all KITTI's quantizied GT data in new data folder - under testing
    # put KITTI's testing folder labels + other datasets under 'resources'

    orig_dir = '/home/elad/Data/KITTI_QUANTIZIED/testing'
    stat_dir = '/home/elad/Data/KITTI_QUANTIZIED/testing'
    shift_dir= '/home/elad/Data/KITTI_QUANTIZIED/testing'

    in_dir = orig_dir
    out_dir = stat_dir
    new_imgs(in_dir, out_dir, mode='stat', num_files=10)
    create_train_file(out_dir)

    # TODO run network

    orig_pred_dir = '/home/PycharmProjects/EgoNet/tools/YOUR_OUTPUT_DIR'
    stat_pred_dir = '/home/PycharmProjects/EgoNet/tools/YOUR_STAT_DIR'
    shift_pred_dir = '/home/PycharmProjects/EgoNet/tools/YOUR_SHIFT_DIR'
    cmp_alpha(orig_pred_dir, dst=stat_pred_dir) # TODO cmp alpha also between GT and pred for sanity check
