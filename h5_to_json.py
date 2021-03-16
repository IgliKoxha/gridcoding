import numpy as np
import h5py
import os
import json

file_name = input('Enter the file name: ')
file_path = f'{os.path.dirname(__file__)}\{file_name}'
output_path = os.path.dirname(__file__) + '\output.json'

#h5 file which we want to convert the data to json format
root = h5py.File(file_path, 'r')

#Recursive function to create a nested dictionary with data from the "Hierarchical Data Format" H5 file
def nested_dict(group):
    d = {}
    print(f'Reading all items in group: {group.name}')
    print(f'Item list {list(group.keys())}')

    #Looping through all items inside current group
    for key in group.keys():

        #Checking if item is a subgroup, if it is we make a recursive call to nested_dict function
        if(isinstance(group.get(key), h5py.Group)):
            nested_data = nested_dict(group.get(key))
        
        #Else the item is a dataset, we retrive the values
        else:
            print(f'Retriving data from dataset: {group.get(key).name}')
            nested_data = list(np.array(group.get(key)[:]).astype(float))

        #Populating the key with the nested_data (subgroup or dataset)
        d[key] = nested_data
    return d

#Starting the nested_dict recursive function from root
data = nested_dict(root)

with open(output_path, 'w', encoding='utf-8') as f:
    #Converting the nested dictionary to json and writing to file
    json.dump(data, f, ensure_ascii=True, indent=4)