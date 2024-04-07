#!/usr/bin/env python
# coding: utf-8

# In[1]:


from tensorflow import keras
import librosa
import numpy as np
import streamlit as st
import os


# In[2]:


# set working directory to where tensorflow models are saved
os.chdir('/Users/xiteng/Desktop/speech-emotion-webapp-master')
model = keras.models.load_model("model3.h5")


# In[9]:


CAT6 = ['fear', 'angry', 'neutral', 'happy', 'sad', 'surprise']
CAT7 = ['fear', 'disgust', 'neutral', 'happy', 'sad', 'surprise', 'angry']
CAT3 = ["positive", "neutral", "negative"]


# In[10]:


# this function used in 3 and 6 emotions codes
def get_title(predictions, categories):
#     title = f"Detected emotion: {categories[predictions.argmax()]} \
#     - {predictions.max() * 100:.2f}%"
#     return title
    title = categories[predictions.argmax()] # only return the emotions information
    return title


# In[19]:


# create filename and filelist
# change audio path to '/Users/xiteng/Desktop/speech-emotion-webapp-master/large audios' for full audios;
# change audio path to '/Users/xiteng/Desktop/speech-emotion-webapp-master/clips' for audio clips.
audio_path = '/Users/xiteng/Desktop/speech-emotion-webapp-master/large audios'
filelist = []
filename = []
for root, dirs, files in os.walk(audio_path):
    for name in files:
        if ".xls" not in name:
            if ".DS_Store" not in name:
                filelist.append(os.path.join(root, name))
                filename.append(name.replace('.mp3','')) # creat a list with file name'
print(filename)
for f in filelist:
    print(f)
print(len(filelist))


# In[36]:


print(filelist[56])


# In[5]:


# # small files
import soundfile as sf
def get_mfccs(audio, limit):
    y, sr = librosa.load(audio, sr=44100)
    a = librosa.feature.mfcc(y, n_mfcc=40,sr=sr)
    if a.shape[1] > limit:
        mfccs = a[:, :limit]
    elif a.shape[1] < limit:
        mfccs = np.zeros((a.shape[0], limit))
        mfccs[:, :a.shape[1]] = a
    return mfccs


# In[6]:


# samll audio files
place_holder = np.zeros((6,))
results_small = []
for small in filelist:
    mfccs_small = get_mfccs(small, model.input_shape[-1])
    mfccs_small = mfccs_small.reshape(1, *mfccs_small.shape)
    pred_small = model.predict(mfccs_small)[0]
    pred_small = np.add(pred_small, place_holder)
    results_small.append(pred_small)
print(results_small)


# In[7]:


print(len(results_small))
print(results_small)


# In[11]:


#small files
# codes used to get emotions from 3 emotion category
three_emotions = []
for result in results_small:
    pos = result[3] + result[5] * .5
    neu = result[2] + result[5] * .5 + result[4] * .5
    neg = result[0] + result[1] + result[4] * .5
    data3 = np.array([pos, neu, neg])

# 3 emotions  
#     txt_3 = "MFCCs\n" + get_title(data3, CAT3)
    txt_3 = get_title(data3, CAT3)# only return the emotions information
    three_emotions.append(txt_3)
print(three_emotions)
print(len(three_emotions))

# codes used to get emotions from 6 emotion category
six_emotions = []
for result in results_small:
    txt_6 = "MFCCs\n" + get_title(result, CAT6)
    txt_6 = get_title(result, CAT6) # only return the emotions information
    six_emotions.append(txt_6)
print(six_emotions)
print(len(six_emotions))


# In[12]:


# using 7 emotions
# small files
os.chdir('/Users/xiteng/Desktop/speech-emotion-webapp-master')
results_small_seven = []
place_holder_l = np.zeros((7,))
seven_emotions = []
model_ = keras.models.load_model("model4.h5")

for small in filelist:
    mfccs_ = get_mfccs(small, model_.input_shape[-2])
    mfccs_ = mfccs_.T.reshape(1, *mfccs_.T.shape)
    pred_ = model_.predict(mfccs_)[0]
    pred_ = np.add(pred_, place_holder_l)
    results_small_seven.append(pred_)

for result in results_small_seven:
    txt_7 = get_title(result, CAT7) # only return the emotions information
    seven_emotions.append(txt_7)
print(seven_emotions)


# In[13]:


print(len(seven_emotions))
print(seven_emotions)


# In[14]:


# get the gender reulst
# small files
gmodel = keras.models.load_model("model_mw.h5")
gplace_holder = np.zeros((2,))
gender = []

for small in filelist:
    gmfccs = get_mfccs(small, gmodel.input_shape[-1])
    gmfccs = gmfccs.reshape(1, *gmfccs.shape)
    gpred = gmodel.predict(gmfccs)[0]
    gpred = np.add(gpred, gplace_holder)
    gdict = [["female", "woman.png"], ["male", "man.png"]]
    ind = gpred.argmax()
    txt_gender = gdict[ind][0]
    gender.append(txt_gender)
print(gender)


# In[15]:


print(gender)
print(len(gender))


# In[9]:


# Codes in the fllowing blocks used to analyze full audio files.


# In[21]:


# process audio files and returns a list of arrays as inputs for 3 and 6 emotions models 
sr = 44100
place_holder = np.zeros((6,))
limit = model.input_shape[-1]
three_emotions = []
six_emotions = []

for l_path in filelist:
    try:
        stream = librosa.stream(l_path,
                                block_length=256,
                                frame_length=2048,
                                hop_length=2048)
        for y_block in stream:
            m_block = librosa.feature.mfcc(y=y_block, sr=sr,
                                                         n_mfcc=40,
                                                         hop_length=2048,
                                                         n_fft=512,
                                                         center=False)
            if m_block.shape[1] > limit:
                mfccs = m_block[:, :limit]
            elif m_block.shape[1] < limit:
                mfccs = np.zeros((m_block.shape[0], limit))
                mfccs[:, :m_block.shape[1]] = m_block

            mfccs = mfccs.reshape(1, *mfccs.shape)
            pred = model.predict(mfccs)[0]
            pred = np.add(pred, place_holder)
            pos = pred[3] + pred[5] * .5
            neu = pred[2] + pred[5] * .5 + pred[4] * .5
            neg = pred[0] + pred[1] + pred[4] * .5
            data3 = np.array([pos, neu, neg])
            txt_3 = get_title(data3, CAT3) # only return the emotions information
            txt_6 = get_title(pred, CAT6) # only return the emotions information
        three_emotions.append(txt_3)
        six_emotions.append(txt_6)
    except:
        txt_3 = 'None'
        txt_6 = 'None'
        three_emotions.append(txt_3)
        six_emotions.append(txt_6)


# In[28]:


print(three_emotions)
print(len(three_emotions))
print(six_emotions)
print(len(six_emotions))


# In[25]:


# codes used to get emotions from 3 emotion category
# three_emotions = []
# for result in results:
#     pos = result[3] + result[5] * .5
#     neu = result[2] + result[5] * .5 + result[4] * .5
#     neg = result[0] + result[1] + result[4] * .5
#     data3 = np.array([pos, neu, neg])

# # 3 emotions  
# #     txt_3 = "MFCCs\n" + get_title(data3, CAT3)
#     txt_3 = get_title(data3, CAT3)# only return the emotions information
#     three_emotions.append(txt_3)
# print(three_emotions)
# print(len(three_emotions))


# In[24]:


# codes used to get emotions from 6 emotion category
# six_emotions = []
# for result in results:
#     txt_6 = "MFCCs\n" + get_title(result, CAT6)
#     txt_6 = get_title(result, CAT6) # only return the emotions information
#     six_emotions.append(txt_6)
# print(six_emotions)
# print(len(six_emotions))


# In[29]:


# the codes below used to get 7  emotions results
os.chdir('/Users/xiteng/Desktop/speech-emotion-webapp-master') # set working directory to where models are saved
model_ = keras.models.load_model("model4.h5")
place_holder_l = np.zeros((7,))
limit_l = model_.input_shape[-2]
seven_emotions = []

for l_path in filelist:
    try:
        stream = librosa.stream(l_path,
                                    block_length=256,
                                    frame_length=2048,
                                    hop_length=2048)
        for y_block in stream:
            m_block = librosa.feature.mfcc(y=y_block, sr=sr,
                                                             n_mfcc=40,
                                                             n_fft=512,
                                                             hop_length=2048,
                                                             center=False)
            if m_block.shape[1] > limit_l:
                mfccs_ = m_block[:, :limit_l]
            elif m_block.shape[1] < limit_l:
                mfccs_ = np.zeros((m_block.shape[0], limit_l))
                mfccs_[:, :m_block.shape[1]] = m_block
            mfccs_ = mfccs_.T.reshape(1, *mfccs_.T.shape)
            pred_ = model_.predict(mfccs_)[0]
            pred_ = np.add(pred_, place_holder_l)
            txt_7 = get_title(pred_, CAT7) # only return the emotions information
        seven_emotions.append(txt_7)
    except:
        txt_7 = 'None'
        seven_emotions.append(txt_7)
print(seven_emotions)


# In[30]:


print(len(seven_emotions))
print(seven_emotions)


# In[31]:


# get the gender reulst
gplace_holder = np.zeros((2,))
gmodel = keras.models.load_model("model_mw.h5")
limit_g = gmodel.input_shape[-1]
gender = []

for l_path in filelist:
    try:
        stream = librosa.stream(l_path,
                                    block_length=256,
                                    frame_length=2048,
                                    hop_length=2048)
        for y_block in stream:
            m_block = librosa.feature.mfcc(y=y_block, sr=sr,
                                                         n_mfcc=40,
                                                         n_fft=512,
                                                         hop_length=2048,
                                                         center=False)
            if m_block.shape[1] > limit_g:
                gmfccs = m_block[:, :limit_g]
            elif m_block.shape[1] < limit_g:
                gmfccs = np.zeros((m_block.shape[0], limit_g))
                gmfccs[:, :m_block.shape[1]] = m_block
            gmfccs = gmfccs.reshape(1, *gmfccs.shape)
            gpred = gmodel.predict(gmfccs)[0]
            gpred = np.add(gpred, gplace_holder)
            gdict = [["female", "woman.png"], ["male", "man.png"]]
            ind = gpred.argmax()
            txt_gender = gdict[ind][0]
        gender.append(txt_gender)
    except:
        txt_gender = 'None'
        gender.append(txt_gender)

print(gender)


# In[32]:


print(len(gender))
print(gender)


# In[33]:


#create nested list of emotions, each sublist contains three emtoions, six emotions, seven emotions, and gender information. 
agg_lst = []
for i in zip(filename, three_emotions,six_emotions,seven_emotions,gender):
    agg_lst.append(i)
print(agg_lst)
print(len(agg_lst))


# In[34]:


#create a dataframe of emotions
import pandas as pd
headers= ['Tick','three_emotions','six_emotions','seven_emotions','gender']
df = pd.DataFrame(agg_lst, columns=headers)
print(df)


# In[35]:


#append audio eomotional reults to video results file
#set working directory to where 'full_results.csv' is saved
#the input in read_csv and to_csv funtions need to match audio paths: 'full_results.csv' is entire audio, 
#'clips_results.csv' is audio clips
os.chdir('/Users/xiteng/Desktop/video sentiment analysis materials/Models/Video-Sentiment-Analysis-master')
pd.concat([pd.read_csv('full_results458.csv'), df], axis=1) \
  .to_csv('full_results458.csv', header=True, index=False)


# In[58]:


#process the final csv files
df_agg = pd.read_csv('clips_results95.csv')
df_agg['Tick_b'] = df_agg['Tick_b'].apply(lambda x: x.replace('sub_',''))
print(df_agg.to_string())


# In[64]:


df_agg_1 = df_agg.iloc[:,0:7]
df_agg_1 = df_agg_1.dropna().reset_index(drop = True)
df_agg_1['Tick_a'] = df_agg_1['Tick_a'].apply(lambda x: x.replace('clips_', ''))
df_agg_1_sorted = df_agg_1.sort_values('Tick_a')
print(df_agg_1_sorted.to_string())


# In[77]:


df_agg_2 = df_agg.iloc[:,7:]
df_agg_2_sorted = df_agg_2.sort_values('Tick_b')
print(df_agg_2_sorted.to_string())


# In[72]:


df_clips_merge = pd.concat([df_agg_1_sorted,df_agg_2_sorted], axis=1)
print(df_clips_merge.to_string())


# In[74]:


df_agg_1_sorted.to_csv('clips_agg.csv')


# In[76]:


pd.concat([pd.read_csv('clips_agg.csv'), df_agg_2_sorted], axis=1) \
  .to_csv('clips_agg.csv', header=True)

