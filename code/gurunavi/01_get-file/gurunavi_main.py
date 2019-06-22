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
Key = "xxx"							#取得したキーを入力
FP = r"xxx"							#jsonファイルのフルパス指定（ファイル名含む）

#init
url_PS = "https://api.gnavi.co.jp/master/PrefSearchAPI/v3/" 	#都道府県コードAPI
url_RS = "https://api.gnavi.co.jp/RestSearchAPI/v3/" 		#店舗情報取得API
url_OS = "https://api.gnavi.co.jp/PhotoSearchAPI/v3/" 		#応援口コミAPI
THC = 0
num = 1

#ファイルが存在したら削除
if os.path.isfile(FP) == True:
    os.remove(FP)


#都道府県パラメータの設定
params_PS={}
params_PS["keyid"] = Key

#都道府県エリア情報のデータフレーム化
result_api_A = requests.get(url_PS, params_PS)
result_api_A = result_api_A.json()
result_api_A = result_api_A["pref"]
result_api_A = pd.DataFrame(result_api_A)

#店舗情報取得パラメータの設定
counter1 = 1
params_RS={}
params_RS["keyid"] = Key
params_RS["hit_per_page"] = 100
params_RS["area"] = result_api_A["area_code"][12]

#口コミ情報取得パラメータの設定
params_OS={}
params_OS["keyid"] = Key
params_OS["hit_per_page"] = 50

#口コミ情報取得処理
while counter1 < 10 and THC < 2000:
    print(counter1)
    params_RS["offset"] = 100 * counter1 - 99
    result_api_T = requests.get(url_RS, params_RS)
    result_api_T = result_api_T.json()
    result_api_T = result_api_T["rest"]
    result_api_T = pd.DataFrame(result_api_T)
    result_api_T = result_api_T["id"]
    counter2 = 0

    while counter2 < 100 and THC < 2000:
        time.sleep(2)
        params_OS["shop_id"] = result_api_T[counter2]
        print(params_OS["shop_id"])
        result_api_K = requests.get(url_OS, params_OS)
        result_api_K = result_api_K.json()

        if "gnavi" in result_api_K:
            pass
        else:
            upper = result_api_K["response"]["total_hit_count"]
            if upper > 50:
                upper = 50
            THC += upper
            print('THC={0}'.format(THC))
            counter3 = 0
            result_api_K_s = {}

            while counter3 < upper:
                s_counter3 = str(counter3)
                num_str = "response" + str(num)
                result_api_K_s[num_str] = result_api_K["response"][s_counter3]["photo"]
                num += 1
                counter3 += 1
            f = open(FP, 'a')
            json.dump(result_api_K_s, f, ensure_ascii=False)

        counter2 += 1

    counter1 += 1

#ファイル内容をjson形式に調整
f = open(FP,"r")
data = f.read()
data = data.replace('}}}}{','}}},')
f = open(FP,"w")
f.write(data)
f.close()