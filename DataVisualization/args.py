import json
from os.path import dirname, abspath

import matplotlib.pyplot as plt
## get all info for pie charts
import numpy as np

file = f"{dirname(abspath(__file__))[:-17]}"
with open(f"{file}data/db.json") as json_file:
    ArgsDict = json.load(json_file)
Arglist = []
for nums, req in enumerate(list(ArgsDict["requests"])):
    Arglist.append((ArgsDict["requests"][str(nums + 1)]["Args"]))
count = {
    "encode": 0,
    "decode": 0,
    "base32": 0,
    "base64": 0,
    "rot13": 0,
    "hex": 0,
    "base85": 0,
    "ascii85": 0,
    "morse": 0,
    "binary": 0,
    "text": 0,
}
for entry in Arglist:
    for k, v in entry.items():
        if v:
            count[k] += 1
## get all info for pie charts


# pie chart vars

# encode / decode vars
en_de_explode = (0.007, 0.007)
en_de_sizes = [count["encode"], count["decode"]]
en_de_labels = ["Encode", "Decode"]
en_de_colors = ["#3E5D74", "#a5487d"]
# other args vars
o_explode = (0.007, 0.007, 0.007, 0.007, 0.007, 0.007, 0.007, 0.007, 0.007)
o_sizes = np.array(
    [
        count["base32"],
        count["base64"],
        count["rot13"],
        count["hex"],
        count["base85"],
        count["ascii85"],
        count["morse"],
        count["binary"],
        count["text"],
    ]
)
o_labels = [
    "base32",
    "base64",
    "rot13",
    "hex",
    "base85",
    "ascii85",
    "morse",
    "binary",
    "text",
]
o_colors = [
    "#f72585",
    "#b5179e",
    "#7209b7",
    "#560bad",
    "#480ca8",
    "#3a0ca3",
    "#3c35c0",
    "#4361ee",
    "#4895ef",
    "#4cc9f0",
]
porcent = 100.0 * o_sizes / o_sizes.sum()
labels = ["{0} - {1:1.2f} %".format(i, j) for i, j in zip(o_labels, porcent)]

# Pie chart
fig, (en_de, others) = plt.subplots(1, 2)
en_de_wedges, en_de_labels, en_de_autopct = en_de.pie(
    en_de_sizes,
    labels=en_de_labels,
    colors=en_de_colors,
    autopct="%1.1f%%",
    startangle=90,
    explode=en_de_explode,
)
o_wedges, o_labels = others.pie(
    o_sizes, labels=o_labels, colors=o_colors, startangle=90, explode=o_explode
)

plt.legend(
    o_wedges, labels, loc="best", bbox_to_anchor=(0.8, 1.0), fontsize=8, frameon=False
)
plt.tight_layout()
plt.savefig('Generated/Arguments.png')
plt.show()
