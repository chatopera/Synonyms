# 3.10
* 计算编辑距离时去停用词

# 3.9
* fix bug

# 3.8
* 获得一个分词后句子的向量，向量以BoW方式组成


```
    sentence: 句子是分词后通过空格联合起来
    ignore: 是否忽略OOV，False时，随机生成一个向量
```


# 3.7
* change import path of utils in word2vec.py to local path
* expose vector fn

# 3.6
* Fix Bug: compare 保证交换两个句子后分数一致 [#60](https://github.com/huyingxi/Synonyms/issues/60)

# 3.5
* 根据实际情况，降低向量距离对近似度分数的影响

# 3.3
* 增加分词接口
* 优化分词器初始化加载字典
* 使用jieba分词源码
* 使用 glog 作为日志输出模块

# 3.2
* 将发布证书改为MIT

# 3.1
* 对空间临近词的邻居进行缓存，提高返回速度
* nearby中处理OOV，返回 ([], [])

# 3.0 - 更简单的定制和配置，增加了额外的开销
* 去掉nearby words, 使用 kdtree检索空间词汇的最近临
* 增加了对sk-learn的依赖，但是减少了对词向量的预处理
* 优化了分词所使用的字典，也可以使用环境变量声明主字典
* 支持自定义word2vec模型，使用环境变量声明

# 2.5
* 使用空间距离近的词汇优化编辑距离计算

# 2.3
* 计算相似度时增加平滑策略

# v1.6
* use ```jieba``` instead of ```thulac``` as tokeninzer.
* refine console log for Jupyter notebook.