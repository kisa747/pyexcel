#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
利用 xlwings 操作 Excel
"""

__author__ = "kevin"
__date__ = "2021/2/3"

import logging

# import os
from pathlib import Path
from typing import Literal

import xlwings as xw

from pyexcel import utils
from pyexcel.excel import Excel


def _convert_file(
    file_input: str | Path,
    newfile: str | Path = "",
    method: Literal["to_xlsx", "to_pdf", "dropformula"] = "to_xlsx",
):
    """
    内部使用，调用请使用 convert 方法。
    转换文件
    :param file: 输入的文件
    :param method: 要使用的转换方法，可以使用 to_xlsx, to_pdf, dropformula
    :return: None
    """
    file_input = file_input if isinstance(file_input, Path) else Path(file_input)
    if not file_input.exists():
        raise FileNotFoundError(f"{file_input} 文件不存在！")
    method_dict = {
        "to_xlsx": file_input.with_suffix(".xlsx"),
        "to_pdf": file_input.with_suffix(".pdf"),
        "dropformula": file_input.with_name(f"{file_input.stem}_without_formula.xlsx"),
    }
    newfile = newfile or method_dict[method]
    with Excel(file_input) as ex:
        if method == "to_xlsx":
            ex.to_xlsx(newfile)
        elif method == "to_pdf":
            ex.to_pdf(newfile)
        elif method == "dropformula":
            ex.drop_formula(newfile)
        else:
            raise ValueError(f"method 参数：{method} 传递错误，不在指定列表中。")


def _convert_dir(
    folder: str | Path, method: Literal["to_xlsx", "to_pdf", "dropformula"] = "to_xlsx"
):
    """
    内部使用，调用请使用 convert 方法。
    传入一个目录，将目录内的所有 xls 转换为 xlsx 或 pdf 文件。

    :param folder: 输入的目录
    :param method: 要使用的转换方法，可以使用 to_xlsx, to_pdf, dropformula
    :return: None
    """
    folder = folder if isinstance(folder, Path) else Path(folder)
    if not folder.exists():
        raise FileNotFoundError(f"{folder} 目录不存在！")
    length = len(folder.parents)
    if method == "to_xlsx":
        xls_path_list = folder.rglob("*.xls")
    else:
        xls_path_list = folder.rglob("*.xlsx")
    newfile_dir_dict = {
        "to_xlsx": f"{folder.name}_xlsx",
        "to_pdf": f"{folder.name}_pdf",
        "dropformula": f"{folder.name}_without_formula",
    }
    newfile_suffix = ".pdf" if method == "to_pdf" else ".xlsx"
    excel_file_num = 0
    with xw.App(visible=False, add_book=False) as app:
        for excel_file_num, file in enumerate(xls_path_list, 1):
            file_parts = list(file.parts)
            file_parts[length - 1] = newfile_dir_dict[method]
            newfile = Path.joinpath(*file_parts).with_suffix(newfile_suffix)
            # newfile = Path(os.path.join(*file_parts)).with_suffix(newfile_suffix)
            newfile.parent.mkdir(parents=True, exist_ok=True)
            wb = app.books.open(file)
            if method == "to_xlsx":
                utils.to_xlsx(wb, newfile)
            elif method == "to_pdf":
                utils.to_pdf(wb, newfile)
            elif method == "dropformula":
                utils.drop_formula(wb, newfile)
            else:
                raise ValueError(f"method 参数：{method} 传递错误，不在指定列表中。")
    if not excel_file_num:
        logging.warning("没有发现 excel 文件！")


def convert(
    path: str | Path, method: Literal["to_xlsx", "to_pdf", "dropformula"] = "to_xlsx"
):
    """
    :param path: 输入的文件或目录
    :param method: 要使用的转换方法，可以使用 to_xlsx, to_pdf, dropformula
    :return: None
    """
    path = path if isinstance(path, Path) else Path(path)
    if path.is_dir():
        _convert_dir(path, method=method)
    elif path.is_file():
        _convert_file(path, method=method)
    else:
        logging.warning(f"{path} 不是是个合法的地址！")
