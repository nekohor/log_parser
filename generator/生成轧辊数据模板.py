# coding:utf-8
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import numpy as np
import os
import sys
# import seaborn as sns  # 学院派风格的话，这个用不到
import docx   # 注意是python-docx
from docx.shared import Inches
import re
matplotlib.style.use('ggplot')

plt.rcParams["font.sans-serif"] = ["Microsoft Yahei"]
plt.rcParams["axes.unicode_minus"] = False

# sns.set(color_codes=True)
# sns.set(rc={'font.family': [u'Microsoft YaHei']})
# sns.set(rc={'font.sans-serif': [u'Microsoft YaHei', u'Arial',
#                                 u'Liberation Sans', u'Bitstream Vera Sans',
#                                 u'sans-serif']})


def max_segment(line):
    if line == 1580:
        return 76
    elif line == 2250:
        return 102
    else:
        return 0


def c_segment(line):
    return (max_segment(line) / 2)


def out(f, content):
    f.write(content)
    # f.write("\n")


# setup parameter
line_list = [1580, 2250]
std_list = [1, 2, 3, 4, 5, 6, 7]


for line in line_list:
    with open("%d日志轧辊数据模板.txt" % line, "w") as f:
        for std in std_list:
            f.write(
                " Roll Object:f%d_stdrollpr       TOP ROLL                                                    BOTTOM ROLL" % std)
            f.write("\n")
            f.write("   Seg  Pos        Surf Temp           Wear          Expansion      Profile          Surf Temp     Wear        Expansion")
            f.write("\n")
            for i in range(max_segment(line) + 1):
                if i == c_segment(line):
                    f.write(" C %3d" % i)
                else:
                    f.write("%6d" % i)
                f.write(" (?P<F%d_Pos_%03d>.{8,8}?) mm (?P<F%d_Top_Roll_Surf_Temp_%03d>.{7,7}}?) C (?P<F%d_Top_Roll_Wear_%03d>.{12,12}?) mm (?P<F%d_Top_Roll_Expans_%03d>.{12,12}?) mm (?P<F%d_Profile_%03d>.{20,20}?) (?P<F%d_Bot_Roll_Surf_Temp_%03d>.{8,8}?) C (?P<F%d_Bot_Roll_Wear_%03d>.{12,12}?) mm (?P<F%d_Bot_Roll_Expans_%03d>.{12,12}?) mm" % (
                    std, i, std, i, std, i, std, i, std, i, std, i, std, i, std, i))
                f.write("\n")
            f.write("\n")
            f.write("\n")
