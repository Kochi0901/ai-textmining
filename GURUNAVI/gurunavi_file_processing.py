#汎用関数
import requests
import os
import pprint
import json
import time
from datetime import datetime
import numpy as np
import pandas as pd
import itertools
import math
import time
from numpy import array
from retry import retry
from datetime import datetime
from decimal import *

"""
個人設定
"""
FP = r"xxx"			#ファイル保存先のフルパスを指定（ファイル名含む）



#jsonファイル読み込む
f = open(FP)
data = json.load(f)
f.close()

#データフレーム化→表示
data = pd.DataFrame(data)
print(data)