#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
利用 xlwings 操作 Excel
"""
__author__ = 'kevin'
__date__ = '2021/2/3'

try:
    from .__version__ import __version__, __version_tuple__
except ImportError:
    __version__ = version = '0.1.0'
    __version_tuple__ = version_tuple = (0, 1, 0)
from .converts import convert  # 转换 excel 文件
from .excel import Excel
from .utils import merge, split
