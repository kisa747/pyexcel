#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
说明文档
"""
__author__ = 'kevin'
__date__ = '2022/10/30'

import logging
import re
from pathlib import Path

import xlwings as xw


def to_xlsx(wb, xlsx_path):
    wb.save(xlsx_path)
    logging.info(f'--> 转换为xlsx成功：{xlsx_path}')


def to_pdf(wb, pdf_path: str | Path, ziliao=False):
    pdf_path = pdf_path if isinstance(pdf_path, Path) else Path(pdf_path)
    if not ziliao:
        wb.to_pdf(pdf_path)
        logging.info(f'--> 转换为pdf成功：{pdf_path}')
    else:
        for sheet in wb.sheets:
            if re.match(r'\(\d+\)', sheet.name):
                logging.debug(f'{sheet.name=}')
                pdf_path_sheet = pdf_path.with_stem(f'{pdf_path.stem}_{sheet.name}')
                sheet.to_pdf(pdf_path_sheet)
                logging.info(f'--> 转换为pdf成功：{pdf_path_sheet}')


def drop_formula(wb, xlsx_without_formula_path: str | Path):
    for sht in wb.sheets:
        # sht.used_range 工作表中用过的区域
        # 如果整张表为空，则返回A1单元格
        # 关于used_range的范围判定，我截取了网上的一段解释：
        # UsedRange属性返回工作表中所有已使用范围的单元格区域，而不管该区域数据间是否有空行或空格。
        # 特别注意：UsedRange属性返回工作表中所有已使用范围的单元格区域是指：
        # 单元格中有数值、公式、单元格格式化设置（例如：单元格字体设置、边框设置等等）
        logging.debug(f'{sht.used_range.shape}')
        sht.used_range.value = sht.used_range.value
        logging.debug(f'{sht.name=} 已处理')
    wb.save(xlsx_without_formula_path)
    logging.info(f'--> 清除公式成功：{xlsx_without_formula_path}')


def merge(excel_dir: str | Path):
    excel_dir = Path(excel_dir) if isinstance(excel_dir, str) else excel_dir
    if not excel_dir.exists():
        raise FileNotFoundError('目录不存在！')
    if not excel_dir.is_dir():
        raise ValueError('参数必须是目录，不能是文件或其它！')
    excel_list = list(excel_dir.glob('*.xlsx'))
    if excel_list:
        logging.info(f'--> 共计 {len(excel_list)} 个工作簿')
        with xw.App(visible=False, add_book=False) as app:
            wb_new = app.books.add()
            sht_new = wb_new.sheets[0]
            for excel in excel_list:
                wb = app.books.open(excel)
                for sht in wb.sheets:
                    sht.copy(sht_new)
                wb.close()
                logging.info(f'--> 合并了 {excel.name}')
            sht_new.delete()
            wb_new.sheets[0].activate()
            excel_new_name = f'{excel_dir.stem}_merge.xlsx'
            wb_new.save(excel_dir.with_name(excel_new_name))
            wb_new.close()
            # app.quit()
        logging.info(f'--> 成功合并至 {excel_new_name}')
    else:
        xls_list = list(excel_dir.glob('*.xls'))
        if xls_list:
            logging.warning(f'--> 请先将 xls 文件转换为 xlsx 文件！')
        else:
            logging.warning('没有发现任何 excel 文件！')


def split(excel_file: str | Path):
    excel_file = Path(excel_file) if isinstance(excel_file, str) else excel_file
    if not excel_file.exists():
        raise FileNotFoundError(f'{excel_file} 不存在！')
    if not excel_file.is_file():
        raise ValueError(f'参数只能是文件，不能是目录或其它！')
    excel_dir = excel_file.with_name(excel_file.stem)
    excel_dir.mkdir(parents=True, exist_ok=True)
    with xw.App(visible=False, add_book=False) as app:
        wb = app.books.open(excel_file)
        for sht in wb.sheets:
            wb_new = app.books.add()
            sht_new = wb_new.sheets[0]
            sht.copy(sht_new)
            sht_new.delete()
            wb_new_path = excel_dir / f'{sht.name}.xlsx'
            wb_new.save(wb_new_path)
            wb_new.close()
            logging.info(f'--> 拆分出： {sht.name}.xlsx')
        wb.close()
        # app.quit()
    logging.info(f'--> 成功拆分至 {excel_dir.name} 文件夹')
