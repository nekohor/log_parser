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

from log_parser_single import main
matplotlib.style.use('ggplot')

plt.rcParams["font.sans-serif"] = ["Microsoft Yahei"]
plt.rcParams["axes.unicode_minus"] = False


# setup parameter
line = 2250

current_dir = "e:/log_test/20180319_SAPH440-P"
main(line, current_dir)
