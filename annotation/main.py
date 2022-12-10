from __future__ import print_function
import json
import argparse
import os
import numpy as np
def json2json(json_path,images_number):
    if not os.path.exists('json'):
        os.mkdir('json')
    json_file=json_path
    data=json.load(open(json_file,'r'))
    for i in range(images_number):
        data_2={}
        data_2['info']=data['info']
        data_2['licenses']=data['licenses']
        data_2['images']=[data['images'][i]] # 只提取第一张图片
        data_2['categories']=data['categories']
        annotation=[] # 通过imgID 找到其所有对象
        imgID=data_2['images'][0]['id']
        file_name=data_2['images'][0]['file_name']
        for ann in data['annotations']:
            if ann['image_id']==imgID:
                annotation.append(ann)
        data_2['annotations']=annotation # 保存到新的JSON文件，便于查看数据特点
        a = filter(str.isdigit, file_name)
        b = list(a)
        c = "".join(b)
        # print('%s' % (annotation))
        json.dump(data_2,open('json/'+'%s.json'%(c),'w'),indent=4) # indent=4 更加美观显示

def json2txt():
    if not os.path.exists('../coco128_seg(pothole)/labels/test'):
        os.mkdir('../coco128_seg(pothole)/labels/test')
    m = 0
    filepath = 'json'
    for file in os.listdir(filepath):
        with open(filepath + os.sep + file, 'r') as f:
            dict = json.load(f)
        images_value = dict.get("images")  # 得到某个键下对应的值
        annotations_value = dict.get("annotations")  # 得到某个键下对应的值
        lis = []
        for i in images_value:
            imgid = str(i.get("file_name"))
            a = filter(str.isdigit, imgid)
            b = list(a)
            imgID = "".join(b)
            open('../coco128_seg(pothole)/labels/test/%s.txt' % (imgID), 'w')
            lis.append(i.get("id"))
        # print("######################################")
        # print('%s' % (imgID))
        for i in lis:
            for j in annotations_value:
                # if j.get("image_id") == i:
                # bbox标签归一化处理
                num = (j.get('bbox'))
                numO = np.array(num[::2])
                numE = np.array(num[1::2])
                # print('numO:%s' % (numO))
                # print('numE:%s' % (numE))
                for i in images_value:
                    w = int(i.get('width'))
                    h = int(i.get('height'))
                numO[0] = numO[0] + numO[1] / 2
                numE[0] = numE[0] + numE[1] / 2
                c = np.around(numO / w, decimals=6)
                d = np.around(numE / h, decimals=6)
                from itertools import chain

                num_0 = list(chain.from_iterable(zip(c, d)))
                # print(num_0)
                #
                newbbox_3 = ' '.join(str(i) for i in num_0)
                # print(newbbox_3)
                seg = (j.get('segmentation'))
                seg1 = seg[0]
                # print(len(seg))
                # print(len(seg1))
                # # print(newbbox)
                # print(w, h)
                # print('num:%s' % (num))
                # print('seg1:%s' % (seg1))
                segO = np.array(seg1[::2])
                segE = np.array(seg1[1::2])
                c = np.around(segO / w, decimals=6)
                d = np.around(segE / h, decimals=6)
                seg_0 = list(chain.from_iterable(zip(c, d)))
                # print(seg_0)
                newseg_3 = ' '.join(str(i) for i in seg_0)
                # print(newseg_3)
                newlis = newbbox_3 + ' ' + newseg_3
                # print(newlis)
                # print(0, newbbox_3)
                # print(0, newseg_3)
                with open('../coco128_seg(pothole)/labels/test/%s.txt' % (imgID), 'a') as file1:  # 写入txt文件中
                #     #      # print(j.get("category_id"), newbbox_3, file=file1)
                    print(0, newseg_3, file=file1)

def parse_opt():
        parser = argparse.ArgumentParser()
        parser.add_argument('--source', type=str, default="instances_val2017.json",help='file')
        parser.add_argument('--number', type=int, default="100",help='file')
        # parser.add_argument('--output', type=str, default="val",help='file')
        opt = parser.parse_args()
        print(opt)
        return opt

if __name__ == "__main__":
        opt = parse_opt()
        json2json(opt.source,opt.number)
        json2txt()