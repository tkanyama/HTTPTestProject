import pandas as pd
import requests
import io

# URL
url = "https://www8.cao.go.jp/chosei/shukujitsu/syukujitsu.csv"
r = requests.get(url).content
# print(r.decode('shift_jis'))
df = pd.read_csv(io.StringIO(r.decode('shift_jis')), sep=",",header=0)
print(df.iloc[0:1,0:2])

list1 = df.to_numpy().tolist()
print(list1[0:2][0:2])