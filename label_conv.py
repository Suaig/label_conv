import os
import sys
from bs4 import BeautifulSoup
from tqdm import tqdm
import argparse


classes = []

def convert(size, box):
    #xyxy to xywh
    dw = 1./(size[0])
    dh = 1./(size[1])
    x = (box[0] + box[1])/2.0 - 1
    y = (box[2] + box[3])/2.0 - 1
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x*dw
    w = w*dw
    y = y*dh
    h = h*dh
    return (x,y,w,h)

def convert_annotation(xlm_in, txt_out):
    with open(xlm_in, 'rb') as in_file:
        try:
            soup = BeautifulSoup(in_file, 'lxml')
        except:
            
            print('open xml fail on {}'.format(xlm_in))
            return
        else:
            w, h, _=map(float, soup.find('size').text.split())

            if w == 0.0 or h == 0.0: #检查是否图片尺寸有误
                print('size error on {}'.format(xlm_in))
                return
            with open(txt_out, 'w') as out_file:
                objs = soup.find_all('object')
                for obj in objs:
                    cls_name = obj.find('name').text
                    difficult = int(obj.find('difficult').text)
                    bdbox = list(map(float, obj.find('bndbox').text.split()))

                    if cls_name not in classes or int(difficult)==1:
                        print("{} not in list:".format(cls_name))
                        return
                    
                    if cls_name not in copy_class: #不在要转化的列表里
                        continue

                    cls_id = copy_class.index(cls_name)

                    b = (bdbox[0], bdbox[2], bdbox[1], bdbox[3]) #xmin,xmax to xmin,ymin
                    bb = convert((w,h), b)
                    out_file.write(str(cls_id) + " " + " ".join([str(a) for a in bb]) + '\n')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--xml', type=str, default='F:/VOC2019/Annotations', help='input xml file Annotations')  #input xml file Annotations
    parser.add_argument('--cls', type=str, default='F:/n.names', help='class names file')  #names class names file
    parser.add_argument('--txt', type=str, default='F:/VOC2019/out', help='output txt file Darknet for yolo')  #output txt file Darknet for yolo
    parser.add_argument('--dis-cls', type=str, default='1,2,3,4', help='dislodge some class. 0 is all 1 2 3 is index in class.names')  #用来设置不需要转化的标签，可以让多类变单类别训练

    opt = parser.parse_args()

    #读取类别文件中的类
    with open(opt.cls, 'r', encoding='utf-8') as csn:
        classes = list(map(lambda s: s.strip() , csn.readlines()))
        copy_class = classes.copy()
        if opt.dis_cls == '0':
            print('class:{}'.format(copy_class)) #打印找到的类别
        else:
            dis_index = list(map(int, opt.dis_cls.split(',')))
            dis_index = list(map(lambda x: x-1, dis_index))
            for isn in dis_index:
                copy_class.remove(classes[isn])
            print('class:\n{}'.format(copy_class))

    #开始遍历xml文件
    files = os.listdir(opt.xml)
    for f in tqdm(files):
        #转换对应标签写入txt
        convert_annotation(os.path.join(opt.xml, f), os.path.join(opt.txt, f.replace('xml', 'txt')))
    print('converted!')