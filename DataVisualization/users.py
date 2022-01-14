import json
from os.path import dirname, abspath

file = f"{dirname(abspath(__file__))[:-17]}"

with open(f"{file}data\\db.json") as json_file:
    ArgsDict = json.load(json_file)
Arglist = []
for nums, req in enumerate(list(ArgsDict["requests"])):
    Arglist.append((ArgsDict["requests"][str(nums + 1)]["author"]))
AuthorCounts = {}
for entry in Arglist:
    if entry in AuthorCounts.keys():
        AuthorCounts[entry] += 1
    else:
        AuthorCounts[entry] = 1

AuthorCountsList = sorted(AuthorCounts, key=AuthorCounts.get, reverse=True)
IndexMap = {v: i for i, v in enumerate(AuthorCountsList)}
x = sorted(AuthorCounts.items(), key=lambda pair: IndexMap[pair[0]])
print(x)
print(AuthorCountsList)
