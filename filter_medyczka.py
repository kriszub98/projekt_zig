import json
import re
import csv
import regex


def filter_empty(unfiltered_list):
    filtered_list = [d for d in unfiltered_list if "content" in d]
    filtered_list = [d for d in filtered_list if not d['content'] == ""]
    return filtered_list


def filter_cyrillic(unfiltered_list):
    # Define a regular expression pattern that matches Cyrillic letters
    cyrillic_pattern = re.compile('[\u0400-\u04FF]')
    filtered_list = [d for d in unfiltered_list if not cyrillic_pattern.search(d['title'])]
    filtered_list = [d for d in filtered_list if not cyrillic_pattern.search(d['content'])]
    return filtered_list


def filter_korean(unfiltered_list):
    filtered_list = [d for d in unfiltered_list if not regex.search(r'\p{IsHangul}', d['title'])]
    filtered_list = [d for d in filtered_list if not regex.search(r'\p{IsHangul}', d['content'])]
    return filtered_list


def filter_words(unfiltered_list):
    words_to_exclude = ["SPRZEDAM", "Sprzedam", "sprzedam",
                        "SPRZEDAJE", "Sprzedaje", "sprzedaje",
                        "SPRZEDAJĄ", "Sprzedają", "sprzedają",
                        "SPRZEDAJEMY", "Sprzedajemy", "sprzedajemy"
                        "SPRZEDAŻ", "Sprzedaż", "sprzedaż",
                        "SPRZEDAZ", "Sprzedaz", "sprzedaz",
                        "SPRZEDANIA", "Sprzedania", "sprzedania",
                        "WYSYŁKA", "Wysyłka", "wysyłka",
                        "WYSYLKA", "Wysylka", "wysylka", "Where", "How to",
                        "everprof", "chat", "cam", "porn", "sex", "buy", "Buy", "BUY", "website", "video",
                        "tits", "ass", "pussy"]
    filtered_list = [d for d in unfiltered_list if not any(word in d["content"] for word in words_to_exclude)]
    filtered_list = [d for d in filtered_list if not any(word in d["title"] for word in words_to_exclude)]
    return filtered_list


def filter_author(unfiltered_list):
    authors_to_exclude = ["fahij76111", "Kegankar", "calebjames", "brila", "WitekZoobseics", "Witeklallwappy", "chptiepthi6", "huongviet3933", "Robertbot"]
    filtered_list = [d for d in unfiltered_list if not any(author in d["author"] for author in authors_to_exclude)]
    return filtered_list


def save_to_csv(filtered_list, file):
    writer = csv.writer(file)
    writer.writerow(["source", "date", "title", "content"])
    for d in filtered_list:
        writer.writerow(['medyczka', d['date'], d['title'], d['content']])


with open('medyczka.json', 'r', encoding="utf-8") as fr:
    data = json.load(fr)
data = filter_empty(data)
data = filter_author(data)
data = filter_cyrillic(data)
data = filter_korean(data)
data = filter_words(data)

# with open('filtered_medyczka.json', 'w', encoding="utf-8") as fw:
#     json.dump(data, fw, ensure_ascii=False)

with open('filtered_medyczka.csv', 'w', encoding="utf-8", newline='') as fw:
    save_to_csv(data, fw)

