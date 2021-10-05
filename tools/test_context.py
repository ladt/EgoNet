import os
from pathlib import Path
import random

def calc_new_box(img_arr, old_box):
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
        old_box = choose_box(img_src_path, label_path)
        new_box = calc_new_box(img_arr, old)


def create_train_file(dir):
    # TODO sorted
    pass

def cmp_alpha(src, dst):
    pass

if __name__=='__main__':

    orig_dir = '/home/elad/Data/KITTI/training'
    stat_dir = '/home/elad/Data/KITTI/training_stat_blck'
    shift_dir= '/home/elad/Data/KITTI/training_shift_blck'

    in_dir = orig_dir
    out_dir = stat_dir
    new_imgs(in_dir, out_dir, mode='stat', num_files=10)
    create_train_file(out_dir)

    # TODO run network

    orig_pred_dir = '/home/PycharmProjects/EgoNet/tools/YOUR_OUTPUT_DIR'
    stat_pred_dir = '/home/PycharmProjects/EgoNet/tools/YOUR_STAT_DIR'
    shift_pred_dir = '/home/PycharmProjects/EgoNet/tools/YOUR_SHIFT_DIR'
    cmp_alpha(orig_pred_dir, dst=stat_pred_dir)
