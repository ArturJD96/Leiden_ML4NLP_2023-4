import json
import pathlib
import random

data_dir = pathlib.Path('data/4_parts/')

# Read the JSON file
with open('data/MacKay_presentation_types.json', 'r') as json_file:
    presentation_types = list(json.load(json_file).keys())

# # Extract the specified entries
# selected_entries = list(data.keys())

# Read the list of random score titles from labels.txt
test_labels = (data_dir/'test_labels.txt').read_text().splitlines()

labels_annotated = {}
for label in test_labels:
    labels_annotated[label] = random.choice((presentation_types[0], presentation_types[1]))
    #presentation_types[0]
    #random.choice(presentation_types)

json_annotations = json.dumps(labels_annotated, indent=1)
(data_dir/'labels_annotated.json').write_text(json_annotations)

# # Assign random score titles to the extracted entries
# for entry_key in presentation_types:
#     presentation_types[entry_key]["score_title"] = random.choice(score_titles)

# # Print or use the updated entries as needed
# for entry_key, entry_value in data.items():
#     print(f"{entry_value['score_title']} - {entry_value['description']} - {entry_key}")