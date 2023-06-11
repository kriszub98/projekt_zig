import pandas as pd
import os
import csv
import json

dataset = pd.read_csv("final_with_keywords.csv")
result_file = open("keytool_with_data.csv", "w", encoding="utf-8", newline="")
writer = csv.writer(result_file)

header = ['ID', 'Source', 'Title', 'Content', 'Timestamp', 'Ours', 'Voicelab', 'Clarin', 'Textclass', 'Ner']
writer.writerow(header)


for root, dirs, files in os.walk("Keytool"):
    for filename in files:
        with open(f"Keytool/{filename}", encoding="utf-8") as file:
            _id = filename.replace(".txt", "")

            keywords = json.load(file)
            # print(keywords["voicelab"])
            # dataset.loc[dataset["ID"] == int(_id), "Keywords"] = keywords
            dataset.loc[dataset["ID"] == int(_id), "Voicelab"] = "\n".join(keywords['voicelab']['labels'])
            # dataset.loc[dataset["ID"] == int(_id), "Voicelab"] = json.dumps(keywords['voicelab'])
            dataset.loc[dataset["ID"] == int(_id), "Clarin"] = "\n".join(keywords['clarin']['labels'])
            dataset.loc[dataset["ID"] == int(_id), "Textclass"] = "\n".join(keywords['textclass']['labels'])
            dataset.loc[dataset["ID"] == int(_id), "Ner"] = "\n".join(keywords['ner']['labels'])

            search_result = dataset.loc[dataset['ID'] == int(_id)]
            writer.writerow(search_result.values[0])
result_file.close()
