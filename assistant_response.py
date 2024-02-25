# Understanding the OpenAI assistant response.
# we use a saved response, model_dict.pkl to examine the object

import pickle

# helper functions
def inspect_structure(element, indent=0, counter=[1]):
    if isinstance(element, dict):
        for key, value in element.items():
            print(f"{counter[0]}. " + ' ' * indent + f"Key: {key}, Value Type: {type(value)}")
            counter[0] += 1  # Increment the counter
            if isinstance(value, (list, dict)):
                inspect_structure(value, indent + 2, counter)
    elif isinstance(element, list):
        for item in element:
            print(f"{counter[0]}. " + ' ' * indent + f"List item type: {type(item)}")
            counter[0] += 1  # Increment the counter
            if isinstance(item, (list, dict)):
                inspect_structure(item, indent + 2, counter)                

def inspect_structure_and_values(element, indent=0, counter=[1]):
    if isinstance(element, dict):
        for key, value in element.items():
            print(f"{counter[0]}. " + ' ' * indent + f"Key: {key}, Value Type: {type(value)}, Value: {value}")
            counter[0] += 1
            if isinstance(value, (list, dict)):
                inspect_structure_and_values(value, indent + 2, counter)
    elif isinstance(element, list):
        for item in element:
            # This ensures every item in the list, regardless of type, is accounted for in the counter.
            print(f"{counter[0]}. " + ' ' * indent + f"List item type: {type(item)}")
            counter[0] += 1  # Increment the counter right away for uniformity
            if isinstance(item, (list, dict)):
                # Recursively inspect if the item is a list or dict, without repeating the counter increment here
                inspect_structure_and_values(item, indent + 2, counter)
            
# Path to the pickle file
pickle_file_path = 'model_dict.pkl'

# Load the pickle file
with open(pickle_file_path, 'rb') as file:
    model_dict = pickle.load(file)

# print structure
inspect_structure(model_dict, indent=0, counter=[1])
inspect_structure_and_values(model_dict, indent=0, counter=[1])

# print objects of interest
print(model_dict['data'][1]['content'][0]['text']['annotations'][0]['file_citation']['quote']) # 29. 
print(model_dict['data'][1]['content'][0]['text']['annotations'][1]['file_citation']['quote']) # 37. 
print(model_dict['data'][1]['content'][0]['text']['value']) # 41. 

# lengths
print(len(model_dict['data'][1]['content'][0]['text']['annotations'][0]['file_citation']['quote'])) # 1645
print(len(model_dict['data'][1]['content'][0]['text']['annotations'][1]['file_citation']['quote'])) # 4360
print(len(model_dict['data'][1]['content'][0]['text']['value'])) # 1553







