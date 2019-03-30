#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2019-03-27
# @Author  : jishuzhain
# @Link    :
# @Version : 1.0
import jieba
jieba.load_userdict("namedict.txt")
import jieba.analyse as analyse
from wordcloud import WordCloud
from scipy.misc import imread
import matplotlib.pyplot as plt


# 获取关键词
def get_words(file_name, *stopwords):
    stop_words= []
    with open("name.txt", "r") as file:
        for f in file:
            stop_words.append(f.strip())
    with open(file_name, encoding='utf-8') as f:
        fiction_text = f.read()
    wordList = jieba.cut(fiction_text)  # 分词
    print('小说分词完成...')
    allow_pos = ('nr',)  # 设置筛选参数为”nr“
    tags = jieba.analyse.extract_tags(fiction_text, topK=50, withWeight=False, allowPOS=allow_pos)  # 从原文文本original_text中，筛选词性为”nr“的前30个词汇作为关键词
    print('关键词筛选完成...')
    stags = "/".join(tags)  # 将关键词用‘/’分隔
    with open("stags.txt", "w") as f:
        f.write(stags)  # 将关键词保存到stags.txt文件中（可供调试查看）
    outstr = ''
    for word in wordList:
        if word in stags:  # 与关键词字符串比较，只保留关键词
            if word != '/':
                if word in stop_words: #只有在停止词里的属于人名才统计
                    outstr += word
                    outstr += "/"
                else:
                    pass
    return outstr


# 绘制词云
def draw_wordcloud(strwords):
    backgroud_Image = plt.imread('backpic.png')
    cloud = WordCloud(width=1024, height=768,
                      background_color='white', mask=backgroud_Image,
                      font_path='kaitiGBK.ttf', collocations=False,
                      max_font_size=400, random_state=50)
    word_cloud = cloud.generate(strwords)                # 生成词云数据
    return word_cloud


if __name__ == '__main__':
    file_name = 'yitian.txt'
    outstr = get_words(file_name)
    word_cloud = draw_wordcloud(outstr)
    plt.imshow(word_cloud)
    plt.axis('off')
    plt.show()
    word_cloud.to_file('yitian.jpg')
