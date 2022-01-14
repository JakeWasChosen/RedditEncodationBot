import csv
import json
from os.path import dirname, abspath

# Opening JSON file and loading the data
# into the variable data
file = f'{dirname(abspath(__file__))[:-17]}'

with open(f'{file}data\db.json') as json_file:
    data = json.load(json_file)

requests = data['requests']

# now we will open a file for writing
data_file = open(f'{file}data\\requests.csv', 'w+')

# create the csv writer object
csv_writer = csv.writer(data_file)

# Counter variable used for writing
# headers to the CSV file
count = 0
for nums, req in enumerate(list(requests)):
    ContainedDict = requests[str(nums + 1)]
    if count == 0:
        # Writing headers of CSV file
        header = ContainedDict.keys()
        csv_writer.writerow(header)
        count += 1

    # Writing data of CSV file
    csv_writer.writerow(ContainedDict.values())

data_file.close()
