## confuse

本仓库包含汉语**字级别**（同音字、近音字、形近字）和**词语级别**（同音词）的混淆集。

### char

- `char/basic_hanzi_2500.txt`：2500 个常用汉字

- `char/basic_hanzi_3500.txt`：3500 个常用汉字

- `char/confusion_set.txt`：近音字混淆集

- `char/sound_confusion.txt`：同音字混淆集

- `char/shape_confusion.txt`：形近字混淆集

`char/confusion_set.txt`来自于

 https://github.com/aopolin-lv/ECSpell/tree/main/Data/confusion

`char/sound_confusion.txt`和`char/shape_confusion.txt`主要来自于

https://github.com/liushulinle/PLOME/tree/main/pre_train_src/confusions

### jieba

基于 jieba 词典提取得到的同音词混淆集，每个词语中包含两个汉字。

```shell
cd jieba/
python get_jieba_homophones.py \
    --input jieba_dict.txt \
    --minCount 50 > jieba_homophones_min_count_50.txt
```

`minCount`参数表示 jieba 词典中词语出现的最小次数。

`jieba/jieba_homophones_min_count_50.txt`数据形式如下：

```context
世间 事件 始建 实践 时间 识见
事件 世间 始建 实践 时间 识见
始建 世间 事件 实践 时间 识见
实践 世间 事件 始建 时间 识见
时间 世间 事件 始建 实践 识见
识见 世间 事件 始建 实践 时间
```

如要确保每一行第一个词语与其他词语的编辑距离为 1：

```shell
python postprocess.py --input jieba_homophones_min_count_50.txt > jieba_edit_distance_1.txt
```

`jieba/jieba_edit_distance_1.txt`数据形式如下：

```context
世间 时间
时间 世间
世面 市面
市面 世面
丛中 从中
从中 丛中 从重
从重 从中
```

### sgns

基于 [Chinese-Word-Vectors](https://github.com/Embedding/Chinese-Word-Vectors) 仓库中搜狗新闻和百度百科词向量数据的共有词语，再合并 jieba 词典中的非人名地名词语，提取得到了同音词混淆集`sgns/sgns_homophones.txt`

```shell
cd sgns/
python merge.py --ltp_model /data/wangzejun/models/LTP-legacy --output sgns_words.txt
python get_sgns_homophones.py --input sgns_words.txt > sgns_homophones.txt
```

```context
事件 实践 诗笺 十间 世间 食监 尸检 失检 饰件 石坚 十件 拾捡 识见 始建 时见 时艰 时间 试剑 试件
识见 实践 诗笺 十间 世间 食监 尸检 失检 饰件 石坚 十件 拾捡 事件 始建 时见 时艰 时间 试剑 试件
始建 实践 诗笺 十间 世间 食监 尸检 失检 饰件 石坚 十件 拾捡 事件 识见 时见 时艰 时间 试剑 试件
时见 实践 诗笺 十间 世间 食监 尸检 失检 饰件 石坚 十件 拾捡 事件 识见 始建 时艰 时间 试剑 试件
时艰 实践 诗笺 十间 世间 食监 尸检 失检 饰件 石坚 十件 拾捡 事件 识见 始建 时见 时间 试剑 试件
时间 实践 诗笺 十间 世间 食监 尸检 失检 饰件 石坚 十件 拾捡 事件 识见 始建 时见 时艰 试剑 试件
```

如要确保每一行第一个词语与其他词语的编辑距离为 1：

```shell
python postprocess.py --input sgns_homophones.txt > sgns_edit_distance_1.txt
```

`sgns/sgns_edit_distance_1.txt`数据形式如下：

```context
世间 十间 时间
尸检 失检
失检 尸检
饰件 十件 事件 试件
十件 十间 饰件 事件 试件
事件 饰件 十件 试件
识见 时见
时见 识见 时艰 时间
```
