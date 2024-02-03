# Understanding the OpenAI assistant response.
# we use a saved response, model_dict.pkl to examine the object

import pickle

# Path to the pickle file
pickle_file_path = 'model_dict.pkl'

# Open the pickle file and load the content
with open(pickle_file_path, 'rb') as file:
    model_dict = pickle.load(file)

print(type(model_dict))
