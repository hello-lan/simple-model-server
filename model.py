#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@create Time:2021-05-19

@author:LHQ

【double buffer】

中文叫做双备份机制，这个机制的原理并不复杂。就是对于要更新的部分，如模型、配置，
在运行过程中用两个变量来保存，一个变量用于正常运行，给预测的请求用，另一个则用
来更新模型，模型更新完以后，把带着新模型的变量用来进行预测。

这样做能完美满足上面模型热更新的3个细节需求：

 - 原子化。真正更换模型的过程其实是把调用的指针从指着带有原模型的变量转为带有新
   模型的变量，这个指针转化的过程就是原子化的。

 - 模型加载更新过程服务不可终止。加载模型过程是另一个线程在做的，可最终更新模型
   只是一个指针的更换，所以影响面压缩的非常小，终止情况大大减少。

 - 两块内容进行，本身就能够保证回滚。
 
"""
from collections import namedtuple


def singleton(cls):
    """单例装饰器
    """
    _instance = {}

    def inner(*args):
        if cls not in _instance:
            _instance[cls] = cls(*args)
        return _instance[cls]

    return inner


ModelMeta = namedtuple("ModelMeta", ["obj", "info"])


@singleton
class Model:
    """
    采用double buffer机制来设计模型类, 就是对于要更新的部分，
    如模型、配置，在运行过程中用两个变量来保存，一个变量用于
    正常运行，给预测的请求用，另一个则用来更新模型，模型更新
    完以后，把带着新模型的变量用来进行预测。
    """
    def __init__(self,config):
        self.config = config
        init_model = self.load_model()
        self.models = [init_model, init_model]
        self.cur_run_model_idx = 0

    def load_model(self):
        with open(self.config["model_path"]) as f:
            for line in f:
                obj = float(line.strip())
                model = ModelMeta(obj=obj, info=line.strip())
        return model

    def update_model(self):
        """
        update_model方法更新模型的核心，首先用一个临时局部变量存着新模型，
        当然新模型在文件上需要覆盖原模型；然后把家再好的模型赋值给没有在使
        用的那个模型里面，最后再修改cur_run_model_idx为新模型。
        """
        new_model = self.load_model()
        next_idx = (self.cur_run_model_idx + 1) % 2
        self.models[next_idx] = new_model
        self.cur_run_model_idx = next_idx
        return new_model.info

    def predict(self, x):
        return self.models[self.cur_run_model_idx].obj * x


def init_model():
    global model
    model = Model({"model_path": "./data/model.txt"})


def predict(x):
    return model.predict(x)


def update_model():
    return model.update_model()


if __name__ == "__main__":
    init_model()
    x = 3
    y = predict(x)
    print(x, y)

