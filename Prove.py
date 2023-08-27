import pandas as pd
import time
import numpy as np

pathRep = 'C:/Users/fernando/Documents/NTH/Products/CloudGaming/data4cg/Results'
datFile = 'blob-dat.csv'

datDf = pd.read_csv(f'{pathRep}/{datFile}', sep=',', delimiter=None, na_values=[''], dtype=str, low_memory=True)

#vect = pd.isna(datDf['gameStartTime'])

datDf['gameStartTime']=(pd.to_datetime(datDf['gameStartTime'],unit='ms'))

#datDf = datDf['gameStartTime'].astype(int)

#datDf['gameStartTime'] = datDf['gameStartTime'].apply(
#        lambda x: time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(x) / 1000)) datDf['gameStartTime'].notna())

#datDf['gameStartTime'] = np.where(datDf[datDf['gameStartTime'].notna()],
#                                  time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(datDf['gameStartTime'].astype(int) / 1000)),
#                                  datDf['gameStartTime'])

print(datDf)