#coding=utf-8

#读取特定目录下的所有文件

import shutil, os
import re

file_dir = os.path.join('/mnt', 'download', 'TDDOWNLOAD')
filedata_dir = os.path.join('/var/www/html', 'moviesite', 'data')
filedata = filedata_dir+'movieName.txt'
print(filedata)
file_list = os.listdir(file_dir)
#print (file_list)
nameList =[]
fileList = []
#获取目录内的所有文件名
for file_name in file_list:
    #拼接  正则表达式
    #print(file_name)
    name_patten = re.compile('.mp4|.mkv|.rmvb')
    movieList = name_patten.split(file_name)
    nameList.append(movieList[0])
    fileList.append(file_name)
#将文件名排序后写入数据文件
nameList.sort()
fileList.sort()
with open(filedata, 'w') as movie_name:
    for i, j in nameList, fileList:
        filmname = i+'+'+j
        print(filmname)
        movie_name.write(filmname + '\n')

'''
with open(filedata, 'w') as movie_name:
    for file_name in file_list:
        #拼接  正则表达式
        #print(file_name)
        name_patten = re.compile('.mp4|.mkv|.rmvb')
        movieList = name_patten.split(file_name)
        #print(movieList[0])
        movie_name.write(movieList[0] + '\n')


    #name_replace = name_reg.sub('', file_name)

    #print(name_replace)
    #old_filename = file_dir+'/'+file_name
    #new_filename = file_dir+'/'+name_replace
    #print (new_filename)
    #shutil.move(old_filename, new_filename)
'''
