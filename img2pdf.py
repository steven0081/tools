#安装 pip install reportlab
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch, cm
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Image, PageBreak
from reportlab.lib.pagesizes import A4,A3,A2,A1, legal, landscape
from reportlab.lib.utils import ImageReader
import PIL.Image,PIL.ExifTags
from os import listdir
import os, re
import time
from reportlab.lib.units import inch

#将图片转换为PDF文件

#获得目录中所有图片文件列表
def getFilelist(path):
    #print(path)
    files = []
    for a, b, c in os.walk(path):
        print(c)
    for i in c:
        f = os.path.join(path, i)
        if f.endswith("jpeg"):
            # print(f)
            files.append(f)
    return files

#调整图片方向
def rotate_img_to_proper(image):
    try:
        #image = Image.open(filename)
        if hasattr(image, '_getexif'):  # only present in JPEGs
            for orientation in PIL.ExifTags.TAGS.keys():
                if PIL.ExifTags.TAGS[orientation] == 'Orientation':
                    break
            e = image._getexif()  # returns None if no EXIF data
            if e is not None:
                #log.info('EXIF data found: %r', e)
                exif = dict(e.items())
                orientation = exif[orientation]
                # print('found, ',orientation)

                if orientation == 3:
                    image = image.transpose(Image.ROTATE_180)
                elif orientation == 6:
                    image = image.transpose(Image.ROTATE_270)
                elif orientation == 8:
                    image = image.rotate(90,expand=True)
    except:
        pass
    return image

def main(myPath):
    files = []
    #获取文件列表
    files = getFilelist(myPath)
    print(files)
    #设置输出文件名
    output_file_name = 'out_1.pdf'
    # save_file_name = 'ex.pdf'
    # doc = SimpleDocTemplate(save_file_name, pagesize=A1,
    #                     rightMargin=72, leftMargin=72,
    #                     topMargin=72, bottomMargin=18)
    imgDoc = canvas.Canvas(output_file_name)  # pagesize=letter
    imgDoc.setPageSize(A4)
    document_width, document_height = A4
    for image in files:
        try:
            image_file = PIL.Image.open(image)
            #image_file = rotate_img_to_proper(image_file)
            image_width, image_height = image_file.size
            print('img size:', image_file.size)
            if not (image_width > 0 and image_height > 0):
                raise Exception
            image_aspect = image_height / float(image_width)
            # Determins the demensions of the image in the overview
            print_width = document_width
            print_height = document_height
            #是否等比例缩放
            imgDoc.drawImage(ImageReader(image_file), document_width - print_width,
                             document_height - print_height, width=print_width,
                             height=print_height, preserveAspectRatio=False)
            # inform the reportlab we want a new page
            imgDoc.showPage()
        except Exception as e:
            print('error:', e, image)
    imgDoc.save()
    print('Done')

if __name__ == '__main__':
    #设置图片路径
    path = r'G:\PythonProject\WebCrawler\img'
    #调用主函数
    main(path)