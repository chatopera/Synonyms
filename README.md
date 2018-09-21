# Synonyms
Chinese Synonyms for Natural Language Processing and Understanding.

最好的中文近义词工具包。

```synonyms```可以用于自然语言理解的很多任务：文本对齐，推荐算法，相似度计算，语义偏移，关键字提取，概念提取，自动摘要，搜索引擎等。

[![chatoper banner][co-banner-image]][co-url]

[co-banner-image]: https://user-images.githubusercontent.com/3538629/42383104-da925942-8168-11e8-8195-868d5fcec170.png
[co-url]: https://www.chatopera.com

# Table of Content:

* [Install](https://github.com/huyingxi/Synonyms#welcome)
* [Usage](https://github.com/huyingxi/Synonyms#usage)
* [Quick Get Start](https://github.com/huyingxi/Synonyms#quick-get-start)
* [Valuation](https://github.com/huyingxi/Synonyms#valuation)
* [Benchmark](https://github.com/huyingxi/Synonyms#benchmark)
* [Statement](https://github.com/huyingxi/Synonyms#statement)
* [References](https://github.com/huyingxi/Synonyms#references)
* [Frequently Asked Questions](https://github.com/huyingxi/Synonyms#frequently-asked-questions-faq)
* [License](https://github.com/huyingxi/Synonyms#license)

# Welcome

```
pip install -U synonyms
```
兼容py2和py3，当前稳定版本 [v3.x](https://github.com/huyingxi/Synonyms/releases)。

![](./assets/3.gif)

**Node.js 用户可以使用 [node-synonyms](https://www.npmjs.com/package/node-synonyms)了。**

```
npm install node-synonyms
```

本文档的配置和接口说明面向python工具包， node版本查看[项目](https://www.npmjs.com/package/node-synonyms)。 

## Usage

支持使用环境变量配置分词词表和word2vec词向量文件。

| 环境变量 | 描述 |
| --- | --- |
| *SYNONYMS_WORD2VEC_BIN_MODEL_ZH_CN* | 使用word2vec训练的词向量文件，二进制格式。 |
| *SYNONYMS_WORDSEG_DICT* | 中文分词[**主字典**](https://github.com/fxsjy/jieba#%E5%BB%B6%E8%BF%9F%E5%8A%A0%E8%BD%BD%E6%9C%BA%E5%88%B6)，格式和使用[参考](https://github.com/fxsjy/jieba#%E8%BD%BD%E5%85%A5%E8%AF%8D%E5%85%B8) | 

### synonyms#seg
中文分词
```
import synonyms
synonyms.seg("中文近义词工具包")
```

分词结果，由两个list组成的元组，分别是单词和对应的词性。
```
(['中文', '近义词', '工具包'], ['nz', 'n', 'n'])
```

**该分词不去停用词和标点。**


### synonyms#nearby
```
import synonyms
print("人脸: %s" % (synonyms.nearby("人脸")))
print("识别: %s" % (synonyms.nearby("识别")))
print("NOT_EXIST: %s" % (synonyms.nearby("NOT_EXIST")))
```

```synonyms.nearby(WORD)```返回一个元组，元组中包含两项：```([nearby_words], [nearby_words_score])```，```nearby_words```是WORD的近义词们，也以list的方式存储，并且按照距离的长度由近及远排列，```nearby_words_score```是```nearby_words```中**对应位置**的词的距离的分数，分数在(0-1)区间内，越接近于1，代表越相近。比如:

```
synonyms.nearby(人脸) = (
    ["图片", "图像", "通过观察", "数字图像", "几何图形", "脸部", "图象", "放大镜", "面孔", "Mii"], 
    [0.597284, 0.580373, 0.568486, 0.535674, 0.531835, 0.530
095, 0.525344, 0.524009, 0.523101, 0.516046])
```

在OOV的情况下，返回  ```([], [])```，目前的字典大小: 125,792。

### synonyms#compare
两个句子的相似度比较

```
    sen1 = "发生历史性变革"
    sen2 = "发生历史性变革"
    r = synonyms.compare(sen1, sen2, seg=True)
```

其中，参数 seg 表示 synonyms.compare是否对sen1 和 sen2进行分词，默认为 True。返回值：[0-1]，并且越接近于1代表两个句子越相似。

```
旗帜引领方向 vs 道路决定命运: 0.429
旗帜引领方向 vs 旗帜指引道路: 0.93
发生历史性变革 vs 发生历史性变革: 1.0
```

### synonyms#display
以友好的方式打印近义词，方便调试，```display```调用了 ```synonyms#nearby``` 方法。

```
>>> synonyms.display("飞机")
'飞机'近义词：
  1. 架飞机:0.837399
  2. 客机:0.764609
  3. 直升机:0.762116
  4. 民航机:0.750519
  5. 航机:0.750116
  6. 起飞:0.735736
  7. 战机:0.734975
  8. 飞行中:0.732649
  9. 航空器:0.723945
  10. 运输机:0.720578
```

### synonyms#v
获得一个词语的向量，该向量为numpy的array，当该词语是未登录词时，抛出 KeyError异常。

```
>>> synonyms.v("飞机")
array([-2.412167  ,  2.2628384 , -7.0214124 ,  3.9381874 ,  0.8219283 ,
       -3.2809453 ,  3.8747153 , -5.217062  , -2.2786229 , -1.2572327 ],
      dtype=float32)
```

### synonyms#sv(sentence, ignore=False)
获得一个分词后句子的向量，向量以BoW方式组成

```
    sentence: 句子是分词后通过空格联合起来
    ignore: 是否忽略OOV，False时，随机生成一个向量
```


## PCA
以“人脸”为例主要成分分析：

![](assets/1.png)

## Quick Get Start
```
$ pip install -r Requirements.txt
$ python demo.py
```

## Change logs
更新情况[说明](./CHANGELOG.md)。

## Voice of Users
用户怎么说：

<img src="https://github.com/huyingxi/Synonyms/raw/master/assets/4.png" width="600">

## Data
data is built based on [wikidata-corpus](https://github.com/Samurais/wikidata-corpus).

## Valuation

### 同义词词林
《同义词词林》是梅家驹等人于1983年编纂而成，现在使用广泛的是哈工大社会计算与信息检索研究中心维护的《同义词词林扩展版》，它精细的将中文词汇划分成大类和小类，梳理了词汇间的关系，同义词词林扩展版包含词语7万余条，其中3万余条被以开放数据形式共享。

### 知网, HowNet
HowNet，也被称为知网，它并不只是一个语义字典，而是一个知识系统，词汇之间的关系是其一个基本使用场景。知网包含词语8余条。

国际上对词语相似度算法的评价标准普遍采用 Miller&Charles 发布的英语词对集的人工判定值。该词对集由十对高度相关、十对中度相关、十对低度相关共 30 个英语词对组成,然后让38个受试者对这30对进行语义相关度判断，最后取他们的平均值作为人工判定标准。然后不同近义词工具也对这些词汇进行相似度评分，与人工判定标准做比较，比如使用皮尔森相关系数。在中文领域，使用这个词表的翻译版进行中文近义词比较也是常用的办法。

### 对比
Synonyms的词表容量是125,792，下面选择一些在同义词词林、知网和Synonyms都存在的几个词，给出其近似度的对比：

![](./assets/5.png)

注：同义词林及知网数据、分数[来源](https://github.com/yaleimeng/Final_word_Similarity)。Synonyms也在不断优化中，新的分数可能和上图不一致。

更多[比对结果](./VALUATION.md)。

## Benchmark

Test with py3, MacBook Pro.

```
python benchmark.py
```

++++++++++ OS Name and version ++++++++++

Platform: Darwin

Kernel: 16.7.0

Architecture: ('64bit', '')

++++++++++ CPU Cores ++++++++++

Cores: 4

CPU Load: 60

++++++++++ System Memory ++++++++++

meminfo 8GB

```synonyms#nearby: 100000 loops, best of 3 epochs: 0.209 usec per loop```


## Live Sharing

[52nlp.cn](http://www.52nlp.cn/synonyms-%E4%B8%AD%E6%96%87%E8%BF%91%E4%B9%89%E8%AF%8D%E5%B7%A5%E5%85%B7%E5%8C%85)

[机器之心](https://www.jiqizhixin.com/articles/2018-01-14-3)

[线上分享实录: Synonyms 中文近义词工具包 @ 2018-02-07](http://gitbook.cn/gitchat/activity/5a563545a8b23d387720ccd5)

## Statement

[Synonyms](https://github.com/huyingxi/Synonyms)发布证书 MIT。数据和程序可用于研究和商业产品，必须注明引用和地址，比如发布的任何媒体、期刊、杂志或博客等内容。
```
@online{Synonyms:hain2017,
  author = {Hai Liang Wang, Hu Ying Xi},
  title = {中文近义词工具包Synonyms},
  year = 2017,
  url = {https://github.com/huyingxi/Synonyms},
  urldate = {2017-09-27}
}
```

# References

[wikidata-corpus](https://github.com/Samurais/wikidata-corpus)

[word2vec原理推导与代码分析](http://www.hankcs.com/nlp/word2vec.html)

# Frequently Asked Questions (FAQ)

1. 是否支持添加单词到词表中？

不支持，欲了解更多请看 [#5](https://github.com/huyingxi/Synonyms/issues/5)

2. 词向量的训练是用哪个工具？

Google发布的[word2vec](https://code.google.com/archive/p/word2vec/)，该库由C语言编写，内存使用效率高，训练速度快。gensim可以加载word2vec输出的模型文件。

3. 相似度计算的方法是什么？

[详见 #64](https://github.com/huyingxi/Synonyms/issues/64)

# Authors

[Hai Liang Wang](http://blog.chatbot.io/webcv/)

[Hu Ying Xi](https://github.com/huyingxi/)

# Give credits to

[Word2vec by Google](https://code.google.com/archive/p/word2vec/)

[Wikimedia: 训练语料来源](https://dumps.wikimedia.org/)

[gensim: word2vec.py](https://github.com/RaRe-Technologies/gensim)

[SentenceSim: 相似度评测语料](https://github.com/fssqawj/SentenceSim/)

[jieba: 中文分词](https://github.com/fxsjy/jieba)

# License
[MIT](./LICENSE)
