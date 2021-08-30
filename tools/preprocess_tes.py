import cv2
import os
import sys

sys.path.append('../')

def vid_to_frame(vid_pth, out_dir_pth):
    if not os.path.exists(out_dir_pth): os.makedirs(out_dir_pth)
    vidcap = cv2.VideoCapture(vid_pth)
    success, image = vidcap.read()
    count = 0
    while success:
        frame_path = os.path.join(out_dir_pth, '{:06d}.png'.format(count))
        print(frame_path)
        cv2.imwrite(frame_path, image)
        count += 1
        success, image = vidcap.read()
        print('Read a new frame: ', success)
    print(count)

'''
upper left corner is (0,0)
tes format: (center_x, center_y, width, height) - all normalized by image dimensions
kitti format: (left, top, right, bottom) == (x1, y1, x2, y2)
'''
def convert_bboxes(tes_file_path, kitti_file_path, img_height, img_width):
    with open(tes_file_path, 'r') as tes_file:
        lines = tes_file.read().splitlines()
        with open(kitti_file_path, 'w') as kitti_file:
            for line in lines:
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

def frame_tes_to_kitti(in_dir, gt_dir, out_dir):
    if not os.path.exists(out_dir): os.makedirs(out_dir)
    split_file_path = os.path.join(os.path.abspath(os.path.join(in_dir, os.pardir)), 'ImageSets', 'test.txt')
    with open(split_file_path, 'w') as split_file:
        for frame_filename in os.listdir(in_dir):
            frame_num = frame_filename.split('.')[0]
            split_file.write(frame_num + '\n')
            frame_img_path = os.path.join(in_dir, frame_filename)
            frame_file_path = os.path.join(gt_dir, gt_dir.split('/')[-1][:-2] + frame_num + '.txt')
            out_file_path = os.path.join(out_dir, frame_num + '.txt')
            img_height, img_width = cv2.imread(frame_img_path, 0).shape
            convert_bboxes(frame_file_path, out_file_path, img_height, img_width)

if __name__=='__main__':
    vid_file_name = '00012_r1_2.mp4'
    vid_path = os.path.join('/home/elad/Data/TES', vid_file_name)
    frame_out_dir = os.path.join(vid_path.split('.')[0], 'testing', 'image_2')
    # vid_to_frame(vid_path, frame_out_dir)
    boxes_out_dir = '../resources/TES_test_boxes'
    gt_dir = os.path.join(('/').join(vid_path.split('/')[:-1]), 'GT_partial_TES', vid_file_name.split('.')[0] + '_gt')
    frame_tes_to_kitti(frame_out_dir, gt_dir, boxes_out_dir)