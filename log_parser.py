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


def month_day(month, day):
    return str(month * 100 + day)


def generate_path(root_dir, month, day):
    return "/".join([root_dir, str(month), month_day(month, day)])


def filename_head(kind, line):
    if line == 1580:
        head = "M"
    else:
        head = "H"
    return "_".join([kind, head])


def filename_end():
    return "fbk.txt"


def parse_data(col_id, df, pf_name, sf_name):
    i = 0
    with open(pf_name, 'r') as pf, open(sf_name, 'r') as sf:
        for p in pf.readlines():
            s = sf.readline()
            if s.startswith("|"):
                continue
            if s.startswith("!"):
                continue
            mobj = re.match(p, s)
            # mobj = re.match(r"%s" % p, s)
            # mobj = re.match(re.escape(p), s)
            print(i)
            i = i + 1
            print(p)
            print(s)
            if mobj.groups == ():
                continue
            else:
                tag = "\<(.*?)\>"
                col_list = re.findall(tag, p)
                print(mobj.groups())
                print(col_list)
                for i in range(len(col_list)):
                    df.loc[col_id, col_list[i]] = mobj.groups()[i]


def pattern_select(line, kind):
    if kind == "ssu":
        return 'pattern/shape_pattern_non_space.txt'
        # return 'pattern/2250/shape_pattern2250.txt'


def sample_select(kind):
    if kind == "ssu":
        return 'pattern/shape_sample.txt'
        # return 'pattern/2250/shape_sample2250.txt'


# --- new func ---
# setup parameter
kind = "ssu"
root_dir = "C:/document/GSM/GSM/Out"


line = 1580
month = 201709
day = 1


# pattern file
pf_name = pattern_select(line, kind)
# sample file
# sf_name = 'pattern/shape_sample.txt'


current_dir = generate_path(root_dir, month, day)

file_list = [x for x in os.listdir(current_dir) if x.startswith(
    filename_head(kind, line)) if x.endswith(filename_end())]

col_id_list = [x.split("_")[1] for x in file_list]

df = pd.DataFrame()
sf_name = sample_select(kind)

parse_data(col_id_list[0], df, pf_name, sf_name)


# df = pd.DataFrame()
# for file in file_list:
#     print(file)
#     col_id = file.split("_")[1]
#     sf_name = "/".join([current_dir, file])
#     parse_data(col_id, df, pf_name, sf_name)

df.to_excel("test_result.xlsx")


df = pd.read_excel("test_result.xlsx")


with open("type%d.txt" % line, "w") as f:
    for idx, tp in zip(df.dtypes.index, df.dtypes):
        f.write("%30s : %20s \n" % (str(idx), str(tp)))
