import json
import re


def filter_empty(unfiltered_list):
    filtered_list = [d for d in unfiltered_list if "content" in d]
    return filtered_list


def filter_cyrillic(unfiltered_list):
    # Define a regular expression pattern that matches Cyrillic letters
    cyrillic_pattern = re.compile('[\u0400-\u04FF]')
    filtered_list = [d for d in unfiltered_list if not cyrillic_pattern.search(d['title'])]
    filtered_list = [d for d in filtered_list if not cyrillic_pattern.search(d['content'])]
    return filtered_list


def filter_sellers(unfiltered_list):
    words_to_exclude = ["SPRZEDAM", "Sprzedam", "sprzedam",
                        "SPRZEDAJE", "Sprzedaje", "sprzedaje",
                        "SPRZEDAJĄ", "Sprzedają", "sprzedają",
                        "SPRZEDAJEMY", "Sprzedajemy", "sprzedajemy"
                        "SPRZEDAŻ", "Sprzedaż", "sprzedaż",
                        "SPRZEDAZ", "Sprzedaz", "sprzedaz",
                        "SPRZEDANIA", "Sprzedania", "sprzedania",
                        "WYSYŁKA", "Wysyłka", "wysyłka",
                        "WYSYLKA", "Wysylka", "wysylka"]
    filtered_list = [d for d in unfiltered_list if not any(word in d["content"] for word in words_to_exclude)]
    return filtered_list


with open('medyczka.json', 'r', encoding="utf-8") as fr:
    data = json.load(fr)
data = filter_empty(data)
data = filter_cyrillic(data)
data = filter_sellers(data)

with open('filtered_medyczka.json', 'w', encoding="utf-8") as fw:
    json.dump(data, fw, ensure_ascii=False)
