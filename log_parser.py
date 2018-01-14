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
import asyncio
import aiofiles
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


def compile_pattern(pf_name):
    pattern_list = []
    with open(pf_name, 'r') as pf:
        for p in pf.readlines():
            # 因为没有对字符串p加r，
            # 所以模式文件中的正则项目如果用到\,需要打两个。
            pattern_list.append(re.compile(p))
    return pattern_list


def parse_operation(col_id, df, p, s):
    if s.startswith("|"):
        pass
    if s.startswith("!"):
        pass
    mobj = p.match(s)
    print(p)
    print(s)
    if mobj.groups == ():
        pass
    else:
        # tag = "\<(.*?)\>"
        print(mobj.groupdict())
        for k, v in mobj.groupdict().items():
            df.loc[col_id, k] = v


async def fetch(col_id, df, p_list, sf_name):
    sf = await aiofiles.open(sf_name, 'r')
    try:
        for p in p_list:
            s = await sf.readline()
            parse_operation(col_id, df, p, s)
    finally:
        await sf.close()


def parse_data(col_id, df, p_list, sf_name):
    with open(sf_name, 'r') as sf:
        for p in p_list:
            s = sf.readline()
            if s.startswith("|"):
                continue
            if s.startswith("!"):
                continue
            mobj = p.match(s)
            print(p)
            print(s)
            if mobj.groups == ():
                continue
            else:
                # tag = "\<(.*?)\>"
                print(mobj.groupdict())
                for k, v in mobj.groupdict().items():
                    df.loc[col_id, k] = v


def parse_data_old(col_id, df, pf_name, sf_name):
    i = 0
    with open(pf_name, 'r') as pf, open(sf_name, 'r') as sf:
        for p in pf.readlines():
            s = sf.readline()
            if s.startswith("|"):
                continue
            if s.startswith("!"):
                continue
            # 因为没有对字符串p加r，所以模式文件中的正则项目如果用到\,需要打两个。
            mobj = re.match(p, s)
            # mobj = re.match(r"%s" % p, s)
            # mobj = re.match(re.escape(p), s)
            # 第i行
            i = i + 1
            print(i)
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
        return ('pattern/%d/shape_pattern%d.txt' % (line, line))


def sample_select(line, kind):
    if kind == "ssu":
        return ('pattern/%d/shape_sample%d.txt' % (line, line))


# --- new func ---
# setup parameter
kind = "ssu"
root_dir = "i:/1580log/GSM"


line = 1580
month = 201711
day = 3

# pattern file
p_list = compile_pattern(pattern_select(line, kind))

# 当前目录
current_dir = generate_path(root_dir, str(month), month_day(month, day))
current_dir = "e:/log_test/"

# 批量汇总文件和卷号
file_list = [x for x in os.listdir(current_dir) if x.startswith(
    filename_head(kind, line)) if x.endswith(filename_end())]
coil_id_list = [x.split("_")[1] for x in file_list]

print([x for x in os.listdir(current_dir)])
# --- 单卷测试 ---
# df = pd.DataFrame()
# sf_name = sample_select(line, kind)
# parse_data(coil_id_list[0], df, p_list, sf_name)

# --- 同步 ---
df = pd.DataFrame()
for file in file_list:
    print(file)
    coil_id = file.split("_")[1]
    sf_name = "/".join([current_dir, file])
    parse_data(coil_id, df, p_list, sf_name)


# --- 异步 如果从网络上读取，可能用这种方式实现更快 ---
# df = pd.DataFrame()
# tasks = []
# for file in file_list:
#     print(file)
#     coil_id = file.split("_")[1]
#     sf_name = "/".join([current_dir, file])
#     tasks.append(fetch(coil_id, df, p_list, sf_name))
# loop = asyncio.get_event_loop()
# loop.run_until_complete(asyncio.wait(tasks))
# loop.close()
# ------------

# 保存DataFrame
dest_dir = (current_dir +
            "data/result_%d_%s.xlsx" % (line, month_day(month, day))
            )
df.to_excel(dest_dir)
df = pd.read_excel(dest_dir)

# 记录数据类型
with open("type%d.txt" % line, "w") as f:
    for idx, tp in zip(df.dtypes.index, df.dtypes):
        f.write("%30s : %20s \n" % (str(idx), str(tp)))

df.to_excel(dest_dir)
