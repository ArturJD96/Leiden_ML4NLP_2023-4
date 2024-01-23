import json
import random

# Read the JSON file
with open('data/McKay_presentation_types.json', 'r') as json_file:
    presentation_types = list(json.load(json_file).keys())

# # Extract the specified entries
# selected_entries = list(data.keys())

# Read the list of random score titles from labels.txt
with open('data/4_parts/test_labels.txt', 'r') as labels_file:
    test_score_labels = [line.strip() for line in labels_file]

print(len(test_score_labels))

labels_annotated = {}
for label in test_score_labels:
    labels_annotated[label] = random.choice(presentation_types)



# # Assign random score titles to the extracted entries
# for entry_key in presentation_types:
#     presentation_types[entry_key]["score_title"] = random.choice(score_titles)

# # Print or use the updated entries as needed
# for entry_key, entry_value in data.items():
#     print(f"{entry_value['score_title']} - {entry_value['description']} - {entry_key}")