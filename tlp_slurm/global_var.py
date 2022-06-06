#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys

global_var = {}
desc_var = {}  # Global variable Description


# use_slurm

def set_global(var, val):
    global_var[var] = val


def get_global(var):
    return global_var.get(var, None)


def set_default_value(var, val, desc):
    """
    default settings
    """
    global_var[var] = val
    desc_var[var] = desc


def set_default():
    set_global('slurm_info', None)
    set_default_value('use_slurm', '1', "if 'true', execute using slurm; if 'false', run locally; default 'true'")

