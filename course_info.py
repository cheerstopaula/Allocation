import os
import pandas as pd



DATA_PATH = os.path.join(os.environ["HOME"], "Desktop", "BCHdata", "BCHdata.csv")

df = pd.read_csv(DATA_PATH)
df["time"] = pd.to_datetime(df["time"],format='%Y-%m-%d %H:%M:%S.%f')
df["time"] = pd.to_datetime(df["time"],unit='secs')