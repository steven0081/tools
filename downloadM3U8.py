import os
import sys
import requests
import datetime
import time
from Crypto.Cipher import AES
from binascii import b2a_hex, a2b_hex

# pip install pycrypto
"""
下载M3U8文件里的所有片段
"""

#sys.setdefaultencoding('utf-8')
headers = {
    'referer':'https://www.66s.cc/e/DownSys/play/?classid=17&id=11662&pathid2=0&bf=1',
    'user-agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
}

def download(url):
    download_path = os.getcwd() + "\download"
    if not os.path.exists(download_path):
        os.mkdir(download_path)
    # 获取M3U8的文件内容
    all_content = requests.get(url, headers=headers).text
    print('返回内容：{}'.format(all_content))

    # 通过判断文件头来确定是否是M3U8文件
    if "#EXTM3U" not in all_content:
        raise BaseException(u"非M3U8的链接")
    if "EXT-X-STREAM-INF" in all_content:  # 第一层
        file_line = all_content.split("\n")
        print(file_line)
        for line in file_line:
            if '.m3u8' in line:
                url = url.rsplit("/", 1)[0] + "/" + line  # 拼出第二层m3u8的URL
                all_content = requests.get(url).text

    file_line = all_content.split("\n")
    unknow = True
    key = ""
    print(file_line)
    for index, line in enumerate(file_line):  # 第二层
        if "#EXT-X-KEY" in line:  # 找解密Key
            method_pos = line.find("METHOD")
            comma_pos = line.find(",")
            method = line[method_pos:comma_pos].split('=')[1]
            print("Decode Method：", method)

            uri_pos = line.find("URI")
            quotation_mark_pos = line.rfind('"')
            key_path = line[uri_pos:quotation_mark_pos].split('"')[1]

            key_url = url.rsplit("/", 1)[0] + "/" + key_path  # 拼出key解密密钥URL
            res = requests.get(key_url)
            key = res.content
            print("key：", key)

        if "EXTINF" in line:  # 找ts地址并下载
            unknow = False
            pd_url = url.rsplit("/", 1)[0] + "/" + file_line[index + 1]  # 拼出ts片段的URL
            #pd_url = 'https://youku.pmkiki.com/' + file_line[index + 1]  # 拼出ts片段的URL
            print(pd_url)
            time.sleep(2)
            res = requests.get(pd_url, headers=headers)
            c_fule_name = file_line[index + 1].rsplit("/", 1)[-1]

            if len(key):  # AES 解密
                cryptor = AES.new(key, AES.MODE_CBC, key)
                with open(os.path.join(download_path, c_fule_name + ".mp4"), 'ab') as f:
                    f.write(cryptor.decrypt(res.content))
            else:
                with open(os.path.join(download_path, c_fule_name), 'ab') as f:
                    f.write(res.content)
                    f.flush()
                    print('1')
    if unknow:
        raise BaseException("未找到对应的下载链接")
    else:
        print("下载完成")

    merge_file(download_path)


def merge_file(path):
    os.chdir(path)
    cmd = "copy /b * new.tmp"
    os.system(cmd)
    os.system('del /Q *.ts')
    os.system('del /Q *.mp4')
    os.rename("new.tmp", "new.mp4")

if __name__ == '__main__':
    download("https://youku.pmkiki.com/20190807/pxPG3Eiy/1000kb/hls/index.m3u8")