#!/usr/bin/env python
# _*_ coding:utf-8 _*_
import csv
import logging
import os
import pandas as pd
import openpyxl
from xmind2testcase.utils import get_xmind_testcase_list, get_absolute_path


"""
Convert XMind fie to Zentao testcase csv file 

Zentao official document about import CSV testcase file: https://www.zentao.net/book/zentaopmshelp/243.mhtml 
"""


def xmind_to_zentao_csv_file(xmind_file):
    """Convert XMind file to a zentao csv file"""
    xmind_file = get_absolute_path(xmind_file)
    logging.info('Start converting XMind file(%s) to zentao file...', xmind_file)
    testcases = get_xmind_testcase_list(xmind_file)

    # fileheader = ["所属模块", "用例标题", "前置条件", "步骤", "预期", "关键词", "优先级", "用例类型", "适用阶段"]
    fileheader = ["所属模块", "相关需求", "用例标题", "前置条件", "优先级", "用例类型", "适用阶段", "步骤", "预期", "关键词", "用例状态"]
    zentao_testcase_rows = [fileheader]
    for testcase in testcases:
        row = gen_a_testcase_row(testcase)
        zentao_testcase_rows.append(row)

    zentao_file = xmind_file[:-6] + '.csv'
    if os.path.exists(zentao_file):
        os.remove(zentao_file)
        # logging.info('The zentao csv file already exists, return it directly: %s', zentao_file)
        # return zentao_file

    with open(zentao_file, 'w', encoding='utf8') as f:
        writer = csv.writer(f)
        writer.writerows(zentao_testcase_rows)
        logging.info('Convert XMind file(%s) to a zentao csv file(%s) successfully!', xmind_file, zentao_file)

    # pdata = pd.read_csv(zentao_file)
    # zentao_xlsx_file = zentao_file[:-4] + '.xlsx'
    # if os.path.exists(zentao_xlsx_file):
    #     os.remove(zentao_xlsx_file)
        # logging.info('The zentao csv file already exists, return it directly: %s', zentao_file)
        # return zentao_file
    # pdata.to_excel(zentao_xlsx_file, index=False)

    return zentao_file


# 兼容导出为xlsx格式文件，
def xmind_to_zentao_xlsx_file(xmind_file):
    zentao_file = xmind_to_zentao_csv_file(xmind_file)
    pdata = pd.read_csv(zentao_file)
    zentao_xlsx_file = zentao_file[:-4] + '.xlsx'
    if os.path.exists(zentao_xlsx_file):
        os.remove(zentao_xlsx_file)
        # logging.info('The zentao csv file already exists, return it directly: %s', zentao_file)
        # return zentao_file
    pdata.to_excel(zentao_xlsx_file, index=False)

    return zentao_xlsx_file




def gen_a_testcase_row(testcase_dict):
    """
    """
    case_module = gen_case_module(testcase_dict['suite'])
    case_requirements = testcase_dict['product']
    case_title = testcase_dict['name']
    case_precontion = testcase_dict['preconditions']
    case_step, case_expected_result = gen_case_step_and_expected_result(testcase_dict['steps'])
    case_keyword = ''
    case_priority = gen_case_priority(testcase_dict['importance'])
    case_type = gen_case_type(testcase_dict['execution_type'])
    case_apply_phase = '功能测试阶段'
    row = [case_module, case_requirements, case_title, case_precontion,  case_priority, case_type, case_apply_phase, case_step, case_expected_result, case_keyword]
    return row


def gen_case_module(module_name):
    if module_name:
        module_name = module_name.replace('（', '(')
        module_name = module_name.replace('）', ')')
    else:
        module_name = '/'
    return module_name


def gen_case_step_and_expected_result(steps):
    case_step = ''
    case_expected_result = ''

    for step_dict in steps:
        case_step += str(step_dict['step_number']) + '. ' + step_dict['actions'].replace('\n', '').strip() + '\n'
        case_expected_result += str(step_dict['step_number']) + '. ' + \
            step_dict['expectedresults'].replace('\n', '').strip() + '\n' \
            if step_dict.get('expectedresults', '') else ''

    return case_step, case_expected_result


def gen_case_priority(priority):
    mapping = {"高": 1, "中": 2, "低": 3}
    if priority in mapping.keys():
        return mapping[priority]
    else:
        return 3


def gen_case_type(case_type):
    mapping = {1: '功能测试', 2: '性能测试', 3: '接口测试', 4: '单元测试'}
    if case_type in mapping.keys():
        return mapping[case_type]
    else:
        return '功能测试'


def gen_case_requirements(case_requirements):
    return None


if __name__ == '__main__':
    xmind_file = '../docs/zentao_testcase_template.xmind'
    zentao_csv_file = xmind_to_zentao_csv_file(xmind_file)
    print('Conver the xmind file to a zentao csv file succssfully: %s', zentao_csv_file)