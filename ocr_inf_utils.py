from glob import glob
from tqdm import tqdm
from PIL import Image
import json
import cv2
import os
import re
import random
import easyocr

def make_1line(result, cv_img = None): # bbox 그린 이미지가 필요하면 cv_img 받기
    # make tmp_dict
    tmp_dict = {}     
    height_lst, y_center_lst = [], []
    for idx, data in enumerate(result):
        coors = data[0]
        text = data[1]
        conf = data[2]
        
        y_lst = []
        
        for coor in coors:
            coor[0] = int(coor[0])
            coor[1] = int(coor[1])
            
            y_lst.append(coor[1])
            
        # cv_img = cv2.rectangle(cv_img, coors[0], coors[2], (0, 255, 0), 2) # bbox 그린 이미지가 필요하면 주석해제
            
        height = max(y_lst) - min(y_lst)
        y_center = int(min(y_lst) + (height/2))
        
        data_dict = {
            'height': height,
            'y_center': y_center,
            'text': text
        }
                
        tmp_dict[idx] = data_dict
        
    # make exist_next_lst
    exist_next_lst = []

    for i in range(len(tmp_dict)-1):
        target_height = tmp_dict[i]['height']
        target_y_center = tmp_dict[i]['y_center']

        next_y_center = tmp_dict[i+1]['y_center']

        exist_next = target_y_center - int(target_height/4) <= next_y_center <= target_y_center + int(target_height/4)

        if exist_next:
            exist_next_lst.append(i)
    exist_next_lst = sorted(exist_next_lst)
    
    # make final_index_lst
    origin_index_lst = sorted([i for i in range(len(tmp_dict))])

    final_index_lst = []
    tmp_index_lst = []

    for integ in origin_index_lst:
        if integ not in exist_next_lst: # 다음에 이어지는게 없는 경우
            final_index_lst.append([integ])

        else: # 다음에 이어지는게 있는 경우
            if integ + 1 not in exist_next_lst: # 다음에 이어지는게 1개인 경우
                if len(tmp_index_lst) == 0: # 그동안 쌓인게 없는 경우
                    final_index_lst.append([integ, integ+1])
                    origin_index_lst.remove(integ+1)
                else: # 그동안 쌓인게 있는 경우
                    tmp_index_lst.append(integ)
                    tmp_index_lst.append(integ+1)
                    tmp_index_lst = sorted(tmp_index_lst)
                    final_index_lst.append(tmp_index_lst)
                    origin_index_lst.remove(integ+1)
                    tmp_index_lst = []
            else: # 다음에 이어지는게 2개 이상인 경우
                tmp_index_lst.append(integ)
                
    # make final_text_lst
    final_text_lst = []
    for tmp_i in final_index_lst:
        tmp_str = ''
        for j in tmp_i:
            tmp_str += tmp_dict[j]['text'] + ' '
        tmp_str = tmp_str[:-1]
        final_text_lst.append(tmp_str)
        
    return final_text_lst # bbox 그린 이미지가 필요하면 cv_img retrun하기

def fix_text(final_text_lst, fix_dict_lst):
    final_result_lst = []
    for fix_text in final_text_lst:
        for _, target_dict in fix_dict_lst.items():
            for fix_dst, fix_target_lst in target_dict.items():
                for fix_target in fix_target_lst:
                    fix_text = fix_text.replace(fix_target, fix_dst)
        final_result_lst.append(fix_text)
        
    return final_result_lst