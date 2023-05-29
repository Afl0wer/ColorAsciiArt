#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
'A tool to convert pictures into colorful character paintings'
'Created on Thur May 25 20:08:16 2023'
__author__ = 'Af10wer'
"""
import os
import sys
import argparse
import textwrap

import numpy as np
from tqdm import tqdm
from PIL import Image, ImageDraw, ImageFont

class CharImageConvert:

    def __init__(self):
        # 设置彩色字符画中显示的字符集
        self.char_set = r"$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'.*"
        '''
        设置font路径,此处将要生成的彩色字符画中的字符设置为黑体
        在 Windows 上: C:\\Windows\\Fonts
        在 MAC_OSX 上: /Library/Fonts and /System/Library/Fonts
        在 Linux 上: /usr/share/fonts/truetype
        '''
        self.font_path = 'C:\\Windows\\Fonts\\simhei.ttf'  

    ''' 将原图每个像素点的RGBA映射到字符集中的每个字符 '''
    def get_char(self,r,g,b,alpha=256):
        self.gray = int(0.2126 * r + 0.7152 * g + 0.0722 * b)
        self.unit = (255.0 + 1)/len(self.char_set)
        self.alpha = alpha
        if self.alpha == 0:
            return ' '
        else:
            return self.char_set[int(self.gray/self.unit)]
            
    '''生成彩色字符画'''
    def CharPic(self): 
        # 创建一个font对象
        self.font = ImageFont.truetype(self.font_path, font_size)
        self.img = Image.open(origin_image)
        #self.img = self.img.resize((int(self.img.size[0]*0.4),int(self.img.size[1]*0.4)),Image.Resampling.LANCZOS)
        self.w, self.h = self.img.size
        # 创建一个与原图尺寸相同、背景为白色的Image对象
        self.new_img = Image.new("RGBA", (self.w, self.h),'white')
          
        for i in tqdm(range(0, self.h, font_size)):
            for j in range(0, self.w, font_size):
                # 创建一个ImageDraw对象，以便下一步在新图上绘制文本字符
                self.draw = ImageDraw.Draw(self.new_img) 
                # 绘制文本字符
                self.draw.text((j, i), self.get_char(*(self.img.getpixel((j, i)))), fill=self.img.getpixel((j, i)), font=self.font) 
        
        self.new_img_arr = np.array(self.new_img)
        self.text_rows,self.text_cols,self.channel = self.new_img_arr.shape
        
        # 针对生成的新图是RGB格式的情况，处理RGBA转RGB
        if newImageName.endswith('.jpg') or newImageName.endswith('.jpeg'):
            self.rgb = np.zeros((self.text_rows,self.text_cols,3),dtype='float32')
            self.r,self.g,self.b,self.a = self.new_img_arr[:,:,0],self.new_img_arr[:,:,1],self.new_img_arr[:,:,2],self.new_img_arr[:,:,3]
            self.a = np.array(self.a,dtype='float32')/255.0
            self.rgb[:,:,0] = self.r * self.a + (1.0 - self.a)* 255
            self.rgb[:,:,1] = self.g * self.a + (1.0 - self.a)* 255
            self.rgb[:,:,2] = self.b * self.a + (1.0 - self.a)* 255
            self.new_img = Image.fromarray(np.array(self.rgb,dtype='uint8'))

        # 针对原图与生成的新图都是RGBA格式的情况，将两者的alpha保持一致    
        if self.img.mode in ('RGBA','CMYK') and not (newImageName.endswith('.jpg') or newImageName.endswith('.jpeg')): 
            self.img_arr = np.array(self.img)
            self.rgb = np.zeros((self.text_rows,self.text_cols,4),dtype='float32')
            self.rgb[:,:,0] = self.new_img_arr[:,:,0]
            self.rgb[:,:,1] = self.new_img_arr[:,:,1]
            self.rgb[:,:,2] = self.new_img_arr[:,:,2]
            self.rgb[:,:,3] = self.img_arr[:,:,3]
            self.new_img = Image.fromarray(np.array(self.rgb,dtype='uint8'))

        # 将绘制好的彩色字符画保存本地
        self.new_img.save(new_char_image) 


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description = 'Convert pictures to color character paintings',
        formatter_class = argparse.RawDescriptionHelpFormatter,
        epilog = textwrap.dedent('''Example:
            color_ascii_art.py -i origin_image -o new_char_image [--fontsize 8]
            ''')
        )
    parser.add_argument('-i','--inputImage',required=True,help='The path of the image file to be converted')
    parser.add_argument('-o','--outputImage',required=True,help='The path of the color character painting to be generated')
    parser.add_argument('--fontsize',type=int,default=6,help='Sets the size of characters in color character paintings')

    args = parser.parse_args()
    origin_image = args.inputImage
    new_char_image = args.outputImage
    newImageName = os.path.basename(new_char_image)
    font_size = args.fontsize

    charImage = CharImageConvert()
    charImage.CharPic()
