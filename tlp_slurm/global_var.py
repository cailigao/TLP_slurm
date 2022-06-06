#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys

global_var = {}
desc_var = {}  # 全局变量说明


# use_slurm

def set_global(var, val):
    global_var[var] = val


def get_global(var):
    return global_var.get(var, None)


def set_default_value(var, val, desc):
    """
    设置默认值
    """
    global_var[var] = val
    desc_var[var] = desc


def set_default():
    set_global('slurm_info', None)
    set_default_value('use_slurm', '1', "如果为‘true’，使用slurm执行；如果为‘false’，在本地运行；默认为‘true’")

