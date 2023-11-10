# -*- coding: utf-8 -*-
from logging import getLogger, config, StreamHandler, DEBUG
import os

# import sys
from logutil import LogUtil
from importenv import ImportEnvKeyEnum

from util.sample import Util

import json

PYTHON_APP_HOME = os.getenv('PYTHON_APP_HOME')
LOG_CONFIG_FILE = ['config', 'log_config.json']

logger = getLogger(__name__)
log_conf = LogUtil.get_log_conf(os.path.join(PYTHON_APP_HOME, *LOG_CONFIG_FILE))
config.dictConfig(log_conf)
handler = StreamHandler()
handler.setLevel(DEBUG)
logger.setLevel(DEBUG)
logger.addHandler(handler)
logger.propagate = False

FORMAT_PATH = os.path.join(PYTHON_APP_HOME, *['format', 'format.txt'])
REPLACE_DICT_PATH = os.path.join(PYTHON_APP_HOME, *['format', 'replace_dict.json'])
EXPORT_PATH = os.path.join(PYTHON_APP_HOME, *['export', 'export.txt'])

def import_format():
    """
    フォーマットファイルを読み込む
    """
    return_list = []
    with open(FORMAT_PATH, 'r') as f:
        for line in f.read().splitlines():
            return_list.append(line)
    return return_list

def import_replace_dict():
    """
    変換用辞書ファイルを読み込む
    """
    with open(REPLACE_DICT_PATH, 'r') as d:
        replace_dict = json.load(d)
    logger.debug(type(replace_dict))
    return replace_dict

def format_replace(format_list: list, replace_dict: dict) -> list:
    """format_listをreplace_dictで変換して返す。

    Args:
        format_list (list): 変換前
        replace_dict (dict): 変換用辞書

    Returns:
        list: 変換後文字列
    """

    return_list = []
    for line in format_list:
        for key, value in replace_dict.items():
            line = line.replace(key, value)
        return_list.append(line)
    return return_list

def export(string_list: list):
    """ファイルを出力する。

    Args:
        string_list (list): 出力文字列
    """
    with open(EXPORT_PATH, 'w') as f:
        for line in string_list:
            f.write(line + '\n')

if __name__ == '__main__':
    # 起動引数の取得
    # args = sys.argv
    # args[0]はpythonのファイル名。
    # 実際の引数はargs[1]から。
    
    # print('Hello Python on Docker!!')
    # logger.info('This is logger message!!')

    # .envの取得
    # print(ImportEnvKeyEnum.SAMPLE.value)

    # Util.print()
    
    logger.info('Start.')
    
    logger.info(f'Format : {FORMAT_PATH}')
    format = import_format()
    logger.info(format)
    
    replace_dict = import_replace_dict()
    logger.info(f'Replace dict : {REPLACE_DICT_PATH}')
    logger.info(replace_dict)
    
    replaced = format_replace(format, replace_dict)
    logger.info(f'replaced : {replaced}')

    logger.info(f'Export : {EXPORT_PATH}')
    export(replaced)
    ｓ