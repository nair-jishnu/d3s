import os

import cv2
import numpy as np
from glob import glob 
def save_video():
    text_file = open("boxes.txt", "r")
    lines = text_file.readlines()

    img_array = []
    for j , i in enumerate(sorted(glob(r"C:\Users\Dell\Desktop\d3s\pytracking\save-mask-path\sequence1\*"))):
        img = cv2.imread(i)
        try:
            state = lines [j]
            state_1= state.split(",")
            cv2.rectangle(img, (int(state_1[0][1:]), int(state_1[1])), (int(state_1[2]) + int(state_1[0][1:]), int(state_1[3][:-2]) + int(state_1[1])),(0, 255, 0), 5)
        except:
            pass
        height, width, layers = img.shape
        size = (width,height)
        img_array.append(img)
        
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter('./output1.mp4', fourcc, 10, size)
    
    for i in range(len(img_array)):
        out.write(img_array[i])
    out.release()

def save_mask(image,mask, mask_real, segm_crop_sz, bb, img_w, img_h, masks_save_path, sequence_name, frame_name):



    if mask is not None:
        M_sel = cv2.dilate(mask, np.ones((7, 7), np.uint8), iterations=1)
        mask_resized = (cv2.resize((M_sel * mask_real).astype(np.float32), (segm_crop_sz, segm_crop_sz),
                                   interpolation=cv2.INTER_LINEAR) > 0.5).astype(np.uint8)
    else:
        mask_resized = (cv2.resize(mask_real.astype(np.float32), (segm_crop_sz, segm_crop_sz),
                                   interpolation=cv2.INTER_LINEAR) > 0.5).astype(np.uint8)
    image_mask = np.zeros((img_h, img_w), dtype=np.uint8)
    # patch coordinates
    xp0 = 0
    yp0 = 0
    xp1 = mask_resized.shape[0]
    yp1 = mask_resized.shape[1]
    # image coordinates
    xi0 = int(round((bb[0] + bb[2] / 2) - mask_resized.shape[1] / 2))
    yi0 = int(round((bb[1] + bb[3] / 2) - mask_resized.shape[0] / 2))
    xi1 = int(round(xi0 + mask_resized.shape[1]))
    yi1 = int(round(yi0 + mask_resized.shape[0]))
    if xi0 < 0:
        xp0 = -1 * xi0
        xi0 = 0
    if xi0 > img_w:
        xp0 = (mask_resized.shape[1]) - (xi0 - img_w)
        xi0 = img_w
    if yi0 < 0:
        yp0 = -1 * yi0
        yi0 = 0
    if yi0 > img_h:
        yp0 = (mask_resized.shape[0]) - (yi0 - img_h)
        yi0 = img_h
    if xi1 < 0:
        xp1 = -1 * xi1
        xi1 = 0
    if xi1 > img_w:
        xp1 = (mask_resized.shape[1]) - (xi1 - img_w)
        xi1 = img_w
    if yi1 < 0:
        yp1 = -1 * yi1
        yi1 = 0
    if yi1 > img_h:
        yp1 = (mask_resized.shape[0]) - (yi1 - img_h)
        yi1 = img_h

    image_mask[yi0:yi1, xi0:xi1] = mask_resized[yp0:yp1, xp0:xp1]

    mask_save_dir = os.path.join(masks_save_path, sequence_name)
    if not os.path.exists(mask_save_dir):
        os.mkdir(mask_save_dir)
    mask_save_path = os.path.join(mask_save_dir, '%s.png' % frame_name)

    cv2.imwrite(mask_save_path, image_mask*255)
    img_mask_save = cv2.imread(mask_save_path)
    result = cv2.bitwise_or(image, img_mask_save)
    cv2.imwrite(mask_save_path, result)


    return result
