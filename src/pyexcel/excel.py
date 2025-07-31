#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
利用 xlwings 操作 Excel
"""

__author__ = "kevin"
__date__ = "2021/2/3"

from pathlib import Path
from typing import Self

import xlwings as xw

from . import utils


class Excel:
    """
    创建一个 xlwings.app() 实例，支持上下文管理。

    :param xls_path: 要处理的 excel 文件路径
    """

    def __init__(self, xls_path: str | Path):
        self.xls_path = xls_path if isinstance(xls_path, str) else Path(xls_path)
        self.app = xw.App(visible=False, add_book=False)
        self.wb = self.app.books.open(xls_path)

    def __enter__(self, *args, **kwargs) -> Self:  # 上下文管理，进入时执行
        return self  # 返回的对象为 as 后的变量。

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def close(self):
        self.wb.close()
        self.app.quit()
        # 参考 App() 类的源代码，windows 下需要app.kill() 方法才能彻底杀死进程
        self.app.kill()
        # 参考：https://github.com/xlwings/xlwings/issues/814
        # the technology that xlwings/pywin32 uses under the hood,
        # only releases the Excel process if there are no more references to it from Python.
        # This means, you'd either need to del app at the end of your code or use app.kill() instead.

    def to_xlsx(self, xlsx_path: str | Path) -> None:
        """
        转换成 xlsx

        :param xlsx_path: 要处理的excel文件
        :return: None
        """
        utils.to_xlsx(self.wb, xlsx_path)

    def to_pdf(self, pdf_path: str | Path, ziliao=False):
        utils.to_pdf(self.wb, pdf_path, ziliao)

    def drop_formula(self, xlsx_without_formula_path: str | Path):
        utils.drop_formula(self.wb, xlsx_without_formula_path)
