from datetime import datetime
from os.path import dirname, abspath

import pandas as pd
from matplotlib import pyplot as plt

from utils import timeConverter

plt.style.use("seaborn-poster")
file = f"{dirname(abspath(__file__))[:-17]}"
df = pd.read_csv(f"{file}data\\requests.csv")
timelist = list(df["time"])

df["time"] = df["time"].map(lambda unix: datetime.fromtimestamp(unix)).replace("-", "/")
df["time"] = df["time"].map(
    lambda datestamp: datetime.strptime(
        str(datestamp).replace("-", "/"), "%Y/%m/%d %H:%M:%S.%f"
    )
)

x = df["time"]
y = df["NumbRequest"]
# plot
"""
Plot the time of day a user did a request

The most popular day

DONE: The most used encryption types (use pie charts)

"""
TimeSeriesHour = []
for tlt, xt in zip(timelist, x):
    TimeSeriesHour.append(xt.hour)

import json
from os.path import dirname, abspath

import matplotlib.pyplot as plt

# get all info for pie charts
import numpy as np

file = f"{dirname(abspath(__file__))[:-17]}"
with open(f"{file}data/db.json") as json_file:
    TimesDict = json.load(json_file)
Arglist = []

count = {
    "1": 0,
    "2": 0,
    "3": 0,
    "4": 0,
    "5": 0,
    "6": 0,
    "7": 0,
    "8": 0,
    "9": 0,
    "10": 0,
    "11": 0,
    "12": 0,
    "13": 0,
    "14": 0,
    "15": 0,
    "16": 0,
    "17": 0,
    "18": 0,
    "19": 0,
    "20": 0,
    "21": 0,
    "22": 0,
    "23": 0,
    "0": 0,
}
for entry in TimeSeriesHour:
    count[str(entry)] += 1
temp = {
    "14": 20,
    "12": 12,
    "15": 4,
    "10": 3,
    "13": 2,
    "1": 0,
    "2": 0,
    "3": 0,
    "4": 0,
    "5": 0,
    "6": 0,
    "7": 0,
    "8": 0,
    "9": 0,
    "11": 0,
    "16": 0,
    "17": 0,
    "18": 0,
    "19": 0,
    "20": 0,
    "21": 0,
    "22": 0,
    "23": 0,
    "0": 0,
}

count = dict(sorted(count.items(), key=lambda x: x[1], reverse=True))
d_count = count.copy()
start = 0
for k, v in d_count.items():
    start += 1
    if v == 0:
        del count[k]


def AddToStart():
    global start
    start += 1
    return str(start - 1)


print([AddToStart() for x in count])
## get all info for pie charts


# pie chart vars

# encode / decode vars
# other args vars
o_explode = (
    0.007,
    0.007,
    0.007,
    0.007,
    0.007,
    0.007,
    0.007,
    0.007,
    0.007,
    0.007,
    0.007,
    0.007,
    0.007,
    0.007,
    0.007,
    0.007,
    0.007,
    0.007,
    0.007,
    0.007,
    0.007,
    0.007,
    0.007,
    0.007,
)
start = 0

o_labels = [
    "1",
    "2",
    "3",
    "4",
    "5",
    "6",
    "7",
    "8",
    "9",
    "10",
    "11",
    "12",
    "13",
    "14",
    "15",
    "16",
    "17",
    "18",
    "19",
    "20",
    "21",
    "22",
    "23",
    "0",
]

o_sizes = np.array([count[num] for num in o_labels if num != 0])
o_colors = [
    "#148d7b",
    "#108577",
    "#0c7d73",
    "#08756f",
    "#006466",
    "#065a60",
    "#0b525b",
    "#144552",
    "#1b3a4b",
    "#212f45",
    "#272640",
    "#312244",
    "#3e1f47",
    "#4d194d",
    "#641654",
    "#7a135a",
    "#a60d66",
    "#d30773",
    "#ff007f",
    "#ff1460",
    "#fe2840",
    "#fe3230",
    "#fe3c20",
    "#fd5000",
]

porcent = 100.0 * o_sizes / o_sizes.sum()
labels = [
    "{0} - {1:1.2f} %".format(timeConverter(int(i)), j)
    for i, j in zip(o_labels, porcent)
]

# Pie chart
fig, others = plt.subplots()
o_wedges, o_labels = others.pie(
    o_sizes, labels=o_labels, colors=o_colors, startangle=90, explode=o_explode
)

plt.legend(
    o_wedges,
    labels,
    loc="center left",
    bbox_to_anchor=(1.2, 0.9),
    fontsize=8,
    frameon=False,
)
samefile = f"{dirname(abspath(__file__))}"
plt.tight_layout()
plt.savefig(f"{samefile}/Generated/MostPopularHour.png")
plt.show()
