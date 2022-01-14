from datetime import datetime
from os.path import dirname, abspath

import pandas as pd
from matplotlib import pyplot as plt

plt.style.use("seaborn-poster")
file = f"{dirname(abspath(__file__))[:-17]}"
print(file)
df = pd.read_csv(f"{file}data\\requests.csv")
df["time"] = df["time"].map(lambda unix: datetime.fromtimestamp(unix)).replace("-", "/")
df["time"] = df["time"].map(
    lambda datestamp: datetime.strptime(
        str(datestamp).replace("-", "/"), "%Y/%m/%d %H:%M:%S.%f"
    )
)
x = df["time"]
y = df["NumbRequest"]
print(x)
# plot
"""
What am i exactly trying to do.. 

Plot the time of day a user did a request

The most popular day

The most used encrytion types (use pie charts)

"""
plt.xlabel("Date")
plt.ylabel("Requests On That Day")
# beautify the x-labels
plt.gcf().autofmt_xdate()

plt.scatter(x, y)

plt.hist(x, facecolor="#202A44", edgecolor="#918936", bins=len(x))

# plt.hist(x,
#         facecolor='#ff4500',
#         edgecolor='#00baff',
#         bins=len(x),
#         alpha=0.9)
plt.savefig('')
plt.savefig('Generated/Arguments.png')
plt.show()
