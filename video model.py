#!/usr/bin/env python
# coding: utf-8

# In[1]:


import os
# set current working directory
os.chdir("/Users/xiteng/Desktop/Tony's Research/video sentiment analysis materials/Models/Video-Sentiment-Analysis-master")


# In[2]:


import sys
import os
import numpy as np
from predictemt import pred, removeout, vidframe, ssimscore1
# from flask import Flask, request, render_template, flash, redirect
# from werkzeug.utils import secure_filename
# import shutil
from tensorflow.keras.models import model_from_json
import cv2
import tensorflow as tf
from tensorflow.keras.preprocessing import image
# from matplotlib import pyplot as plt
# import io
# import base64
# import urllib
from skimage.metrics import structural_similarity


# In[3]:


facec = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')   #load face detection cascade file


# In[ ]:


#codes of following blocks used for analyzing entire videos


# In[7]:


# create two lists: a list of video names represented by their ticks, and a list of file paths
path = "/Users/xiteng/Desktop/Tony's Research/video sentiment analysis materials/Models/Video-Sentiment-Analysis-master/video data"
filelist = []
filename = []
for root, dirs, files in os.walk(path):
    for name in files:
        if ".xls" not in name:
            if ".DS_Store" not in name:
                filelist.append(os.path.join(root, name))
                filename.append(name.replace('.MP4',''))
print(filename)
for f in filelist:
    print(f)
    print(type(f))


# In[5]:


# this functions is used to calculate posture scores
def ssimscore1(im1,im2):
    im1=im1.reshape(48, 48, 1).astype('float32')   #reshaping the flattened image array
    im2=im2.reshape(48, 48, 1).astype('float32')
    (score, diff) = structural_similarity(im1, im2, full=True,multichannel=True) #comparing the image for finding difference using compare_ssim function 
    return score


# In[6]:


# this block of codes is used to analyze video files from 'filelist'
# it returns a list with ticks, emotions and postures
emotions_counts = []
posture_lst = []
for f, name in zip(filelist, filename):
    result, face = vidframe(f) #running vidframe with the uploaded video
    ssimscore=[ssimscore1(i,j) for i, j in zip(face[: -1],face[1 :])]  # calculating similarityscore for images
    if np.mean(ssimscore)<0.6:
        posture="Not Good"
    else:
        posture="Good"
    counts = [name, result.count('angry'),result.count('disgust'),result.count('fear'),
              result.count('happy'),result.count('sad'), posture]
    emotions_counts.append(counts)
print(emotions_counts)


# In[ ]:


#codes of following blocks used for analyzing clips


# In[6]:


# create two lists: a list of video names represented by their ticks, and a list of file paths
clips_path = '/Users/xiteng/Desktop/video sentiment analysis materials/Models/Video-Sentiment-Analysis-master/clips'
filelist_clips = []
filename_clips = []
for root, dirs, files in os.walk(clips_path):  # 对文件夹进行遍历
    for name in files:
        if ".xls" not in name:
            if ".DS_Store" not in name:
                filelist_clips.append(os.path.join(root, name))
                filename_clips.append(name.replace('.MP4','')) # creat a list with file name'
print(filename_clips)
for i in filelist_clips:
    print(i)


# In[8]:


# this block of codes is used to analyze video clips from 'filelist_clips'
# it returns a list with ticks, emotions and postures
clips_lst=[]
for f, name in zip(filelist_clips, filename_clips):
    result, face = vidframe(f) #running vidframe with the uploaded video
    ssimscore=[ssimscore1(i,j) for i, j in zip(face[: -1],face[1 :])]  # calculating similarityscore for images
    if np.mean(ssimscore)<0.6:
        posture="Not Good"
    else:
        posture="Good"
    
    ##os.remove(file_path)  #removing the video as we dont need it anymore
    counts = [name, result.count('angry'),result.count('disgust'),result.count('fear'),
              result.count('happy'),result.count('sad'), posture]
    counts #angry,disgust,fear,happy,sad
    clips_lst.append(counts)
print(clips_lst)


# In[13]:


# the codes below used to write video yielded results into excel
# when test = clips_lst, write clips results; when test = emotions_counts, write full video results
test  = clips_lst
emotion = ['Tick','angry','disgust','fear','happy','sad','posture']
container = []
for l in test:
    d = {}
    for i,j in zip(l, emotion):
        d[j] = i
    container.append(d)

import csv
myFile = open('clips_results.csv', 'w') #the file name need to match the test variable
writer = csv.DictWriter(myFile, fieldnames=['Tick','angry','disgust','fear','happy','sad','posture'])
writer.writeheader()
writer.writerows(container)
myFile.close()
myFile = open('clips_results.csv', 'r') #the file name need to match the test variable
print("The content of the csv file is:")
print(myFile.read())
myFile.close()

