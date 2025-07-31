#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
利用 xlwings 操作 Excel
"""
__author__ = 'kevin'
__date__ = '2021/2/3'

import argparse
import logging

from .converts import convert
from .utils import merge, split


def main() -> None:
    r"""
    可以直接在命令行使用的工具，底层使用 xlwings 模块。

    Examples
    --------
    将目录内的所有 xls 文件批量转换为 xlsx 文件，导出至 "D:\Excel_xlsx"
    python -m pyexcel -x "D:\Excel"
    将指定的 xls 文件转换为 xlsx 文件，导出至文件同目录
    python -m pyexcel -x "D:\test.xls"

    将目录内的所有 xlsx 文件批量导出为 pdf 文件，导出至 "D:\Excel_pdf"
    python -m pyexcel -p "D:\Excel"
    将指定的 xlsx 文件导出为 pdf 文件，导出至文件同目录
    python -m pyexcel -p  "D:\test.xls"

    :return: None
    """
    # action='store'，默认为 store，所以可以省略。, type=str，默认为字符串，也可以省略。
    arg_parser = argparse.ArgumentParser(prog='pyexcel', description='使用xwings处理excel文件')
    arg_parser.add_argument('-x', '--xlsx', metavar='目录或文件', help='将xls文件或目录转换为xlsx')
    arg_parser.add_argument('-p', '--pdf', metavar='目录或文件', help='将excel文件转换为pdf（所有工作表）')
    arg_parser.add_argument('-d', '--dropformula', metavar='目录或文件', help='将excel文件的公式清除')
    arg_parser.add_argument(
        '-m', '--merge', metavar='目录', help='合并文件夹下所有excel文件至一个excel文件'
    )
    arg_parser.add_argument('-s', '--split', metavar='文件', help='将excel文件的工作表拆分至不同的工作簿')
    args = arg_parser.parse_args()
    if args.xlsx:
        logging.debug(f'args.convert参数是：{args.xlsx}')
        convert(args.xlsx, method='to_xlsx')
    if args.pdf:
        convert(args.pdf, method='to_pdf')
    if args.dropformula:
        convert(args.dropformula, method='dropformula')
    if args.merge:
        merge(args.merge)
    if args.split:
        split(args.split)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

    main()
