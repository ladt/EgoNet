import os





def new_img(img_arr, old_box, new_box):
    pass

def new_imgs(paths_in, out_dir, mode):
    pass

def create_train_file(dir):
    # TODO sorted
    pass

def cmp_alpha(src, dst):
    pass

if __name__=='__main__':

    orig_dir = '/home/elad/Data/KITTI/training'
    stat_dir = '/home/elad/Data/KITTI/training_stat_blck'
    shift_dir= '/home/elad/Data/KITTI/training_shift_blck'

    num_files = 10
    out_dir = stat_dir
    paths_in = [os.path.join(stat_dir, filename) for filename in os.listdir(orig_dir)[:num_files]]
    new_imgs(paths_in=paths_in, out_dir=out_dir, mode='stat')
    create_train_file(out_dir)

    # TODO run network

    orig_pred_dir = '/home/PycharmProjects/EgoNet/tools/YOUR_OUTPUT_DIR'
    stat_pred_dir = '/home/PycharmProjects/EgoNet/tools/YOUR_STAT_DIR'
    shift_pred_dir = '/home/PycharmProjects/EgoNet/tools/YOUR_SHIFT_DIR'
    cmp_alpha(orig_pred_dir, dst=stat_pred_dir)
