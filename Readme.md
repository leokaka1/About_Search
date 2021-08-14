# 基于语义进行知识图谱搜索算法的项目说明

##  写在前面

这是一篇关于我调研和开发知识图谱搜索算法的说明文档，公司现在知识图谱的需求是要通过一定的语义来进行搜索任务，因为之前我开发过一个相对简单的用通用模板进行匹配搜索的算法，但是那种方法相对来说比较容易，对语义的识别也不是太好，所以下决心还是开发一个更为深层次的基于语义理解方法的搜索方法，因为公司没有语料，所以用NER等任务抽取句子中的三元组的做法就不太合适了，我一度想过很多种方式，但是很多的方式都会基于模型或者深度学习的方式，所以被迫放弃，突然有一天发现了一篇很好的paper，这篇paper让我思路突然重整了。在看了很多遍这篇paper之后，我打算基于这篇paper对其中的方式进行复现试试。结果进行复现之后发现相对第一种模板匹配的方式来说，太过于复杂，代码量过大，我现在的项目还不足以支撑所有的语境，但是就效果来说和灵活度来说比第一种方式要优秀，只能两种方式有利有弊把，没有绝对好的方法，每种方式都只能不停的去迭代，最后趋于一个平稳的水平，现阶段NLP还不能做到理解每一种说辞。这是必须要说明的。



## 开发进度

2021.8.3 - 2021.8.6   	知识调研，搜索相关的paper和资料，为开发做准备

2021.8.9 - 2021.8.13	 Demo的开发，出一个1.0的出版，可以使用，但是有Bug。跟最终版本相比还是需要不停迭代。

未完待续....



## 项目目录

```
├── createCypher.py
├── main.py
├── resources
│   ├── attributes
│   ├── disambiguation
│   ├── entities
│   ├── relations
│   ├── type
│   ├── user_dicts
│   └── user_former_dict
├── searchNeo4j.py
├── segmentationAndPostag.py
├── semanticGraph.py
├── semanticVertexModel.py
├── sematicAnalysisModel.py
├── sematicPosModel.py
├── sematicSetting.py
└── tools.py
```



## 框架选择说明

在解析框架的选择上，我考虑过用HanLP和jieba等分词语法解析工具，但是发现效果并不是很好，再三斟酌选用了

[baidu/DDParser: 百度开源的依存句法分析系统 ](https://github.com/baidu/DDParser)

[baidu/lac: 百度NLP：分词，词性标注，命名实体识别，词重要性](https://github.com/baidu/lac)

这两个库，百度的套件还是相当好用的！