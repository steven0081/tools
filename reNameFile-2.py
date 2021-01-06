#coding=utf-8

#文件改名程序 对下载的 都挺好 视频文件重命名

import shutil, os
import re

file_dir =r'D:\360安全浏览器下载'
file_list = os.listdir(file_dir)
#print (file_list)
for file_name in file_list:
    if file_name.endswith("mp"):
        pos = file_name.rfind('-')
        name_replace = '都挺好'+file_name[pos:-1]
        old_filename = file_dir + '\\' + file_name
        new_filename = file_dir + '\\' + name_replace +'p4'
        print('old = ', old_filename)
        print ('new = ', new_filename)
        shutil.move(old_filename, new_filename)
