import pandas as pd
import os
import csv
import json

dataset = pd.read_csv("final_dataset.csv")
result_file = open("keytool_with_data.csv", "w", encoding="utf-8", newline="")
writer = csv.writer(result_file)

for root, dirs, files in os.walk("Keytool"):
    for filename in files:
        with open(f"Keytool/{filename}", encoding="utf-8") as file:
            _id = filename.replace(".txt", "")

            keywords = file.readline()
            dataset.loc[dataset["ID"] == int(_id), "Keywords"] = keywords

            search_result = dataset.loc[dataset['ID'] == int(_id)]
            writer.writerow(search_result.values[0])
result_file.close()
