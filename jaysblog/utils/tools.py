# !/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
 @Time    : 2019/9/24 15:10
 @Author  : Jay Chen
 @FileName: tools.py
 @GitHub  : https://github.com/cRiii
 @Desc    : 工具文件
"""
import random


# 生成随机的手机号码
def random_mobile():
    mobile_header_list = ["130", "131", "132", "133", "134", "135", "136", "137", "138", "139", "147", "150", "151",
                          "152", "153", "155", "156", "157", "158", "159", "186", "187", "188"]
    random_header = random.choice(mobile_header_list)
    rest_num = "".join(random.choice("0123456789") for i in range(8))
    mobile_num = random_header + rest_num
    return mobile_num
