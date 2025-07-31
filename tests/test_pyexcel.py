#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试单元
"""
__author__ = 'kevin'
__date__ = '2022/11/4'

import unittest

import pytest

from pyexcel import Excel, convert, merge, split


class TestPyexcel(unittest.TestCase):
    def setUp(self):
        self.ex = Excel(r"E:\test\pyexcel\Excel\test.xls")

    # @unittest.skip('跳过')
    def test_excel_to_xlsx(self):
        self.ex.to_xlsx(r"E:\test\pyexcel\Excel\test_xlsx.xlsx")

    def test_excel_to_pdf(self):
        self.ex.to_pdf(r"E:\test\pyexcel\Excel\test_pdf.pdf")

    def test_excel_drop_formula(self):
        self.ex.drop_formula(r"E:\test\pyexcel\Excel\test_drop_formula.xlsx")

    def tearDown(self):
        self.ex.close()


@pytest.mark.parametrize(
    'path', [r'E:\test\pyexcel\converts\folder', r"E:\test\pyexcel\converts\test.xls"]
)
@pytest.mark.parametrize('method', ['to_xlsx', 'to_pdf', 'dropformula'])
def test_converts_convert(path, method):
    convert(path, method)  # type: ignore


def test_merge():
    merge(r"E:\test\pyexcel\merge\folder")


def test_split():
    split(r"E:\test\pyexcel\split\split.xlsx")


if __name__ == '__main__':
    unittest.main()
