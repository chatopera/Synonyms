# Synonyms
Chinese Synonyms for Natural Language Processing and Understanding.

```synonyms```可以用于自然语言理解的很多任务：文本对齐，推荐算法，相似度计算，语义偏移等。

![](https://camo.githubusercontent.com/ae91a5698ad80d3fe8e0eb5a4c6ee7170e088a7d/687474703a2f2f37786b6571692e636f6d312e7a302e676c622e636c6f7564646e2e636f6d2f61692f53637265656e25323053686f74253230323031372d30342d30342532306174253230382e32302e3437253230504d2e706e67)

# Welcome

```
pip install -U synonyms
```

## Usage

### synonyms#nearby
```
import synonyms
print("人脸: %s" % (synonyms.nearby("人脸")))
print("识别: %s" % (synonyms.nearby("识别")))
print("NOT_EXIST: %s" % (synonyms.nearby("NOT_EXIST")))
```

```synonyms.nearby(WORD)```返回一个list，list中包含两项：```[[nearby_words], [nearby_words_score]]```，```nearby_words```是WORD的近义词们，也以list的方式存储，并且按照距离的长度由近及远排列，```nearby_words_score```是```nearby_words```中**对应位置**的词的距离的分数，分数在(0-1)区间内，越接近于1，代表越相近。比如:

```
synonyms.nearby(人脸) = [
    ["图片", "图像", "通过观察", "数字图像", "几何图形", "脸部", "图象", "放大镜", "面孔", "Mii"], 
    [0.597284, 0.580373, 0.568486, 0.535674, 0.531835, 0.530
095, 0.525344, 0.524009, 0.523101, 0.516046]]
```

在OOV的情况下，返回  ```[[], []]```。

## PCA (主成分析)

![](assets/1.png)

## More samples

![](assets/2.png)

## Similarity Demo
```
$ pip install -r Requirements.txt
$ python demo.py
>> Synonyms on loading ...
>> Synonyms vocabulary size: 125792
Model loaded succeed
人脸: [['图片', '图像', '通过观察', '数字图像', '几何图形', '脸部', '图象', '放大镜', '面孔', 'Mii'], [0.597284, 0.580373, 0.568486, 0.535674, 0.531835, 0.530
095, 0.525344, 0.524009, 0.523101, 0.516046]]
识别: [['辨识', '辨别', '辨认', '标识', '鉴别', '标记', '识别系统', '分辨', '检测', '区分'], [0.872249, 0.764099, 0.725761, 0.702918, 0.68861, 0.678132, 0.663
829, 0.661863, 0.639442, 0.611004]]
```

## Data
```
words.nearby.gz # 近义词汇源数据
words.wc.gz     # 词频统计
```
View data with ```zmore```, ```zgrep```, ```zcat```.

data is built based on https://github.com/Samurais/wikidata-corpus.


## 声明
[Synonyms](https://github.com/shuzi/insuranceQA)发布证书 GPL 3.0。数据和程序可用于研究和商业产品，必须注明引用和地址，比如发布的任何媒体、期刊、杂志或博客等内容。
```
@online{Synonyms:hain2017,
  author = {Hai Liang Wang, Hu Ying Xi},
  title = {中文近义词工具包Synonyms},
  year = 2017,
  url = {https://github.com/huyingxi/Synonyms},
  urldate = {2017-09-27}
}
```

任何基于[Synonyms](https://github.com/huyingxi/Synonyms)衍生的数据和项目也需要开放并需要声明一致的“声明”。

# References

[wikidata-corpus](https://github.com/Samurais/wikidata-corpus)

[word2vec原理推导与代码分析](http://www.hankcs.com/nlp/word2vec.html)

# License
[GPL3.0](./LICENSE)