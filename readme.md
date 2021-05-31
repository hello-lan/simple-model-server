### 简单的模型服务部署方案

采用Flask框架作为服务框架，利用double buffer机制实现模型热更新，具体实现说明参见[模型热更新小记](https://mp.weixin.qq.com/s/TMcj-X5SmOqOgh6Ljkb3sw)。

本代码中，简单将用含数值内容的txt文件代替序列化的模型保，具体运用中，可根据实际情况采用如scikit-learn等序列化模型文件，对应的模型加载方法也需要修改。



###### install

```s
$ pip install -r requirements.txt
```

###### usage

```s
$ flask run
```

