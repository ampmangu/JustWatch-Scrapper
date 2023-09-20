#!/usr/bin/env python3

import csv
import urllib
import os

import requests
from Levenshtein import distance
from bs4 import BeautifulSoup

JW_BUSCAR = "https://www.justwatch.com/es/buscar?q="


def get_platforms():
    if os.path.isfile("./streaming_platforms.txt"):
        with open('streaming_platforms.txt', 'r') as f_txt:
            return [txt.upper() for txt in f_txt.read().splitlines()]
    else:
        return []


def get_names():
    with open('watchlist.csv', 'r') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        next(csv_reader)  # skip header
        return [row[1] for row in csv_reader]


def search_content(text: str) -> str:
    response = requests.get(JW_BUSCAR + urllib.parse.quote(text))
    if response.status_code == 200:
        return response.text
    else:
        return "FAILED"


def parse_text(html: str, text_input: str):
    soup = BeautifulSoup(html, "html.parser")
    list_html = soup.find_all("span", class_="header-title")
    names = [element.text for element in list_html]
    names_with_score = {}
    for name in names:
        names_with_score[name] = distance(text_input, name)
    if len(names_with_score) == 0:
        print(f'{text_input} can not be found')
        return text_input, "-"
    return text_input, min(names_with_score, key=names_with_score.get)


def find_stream(html: str, text_input: str):
    soup = BeautifulSoup(html, "html.parser")
    found = soup.find("div", class_="title-list-row__row").text
    if "Fijo" in found:
        stream = soup.find("div", class_="buybox-row stream inline")
        if stream is not None:
            stream_text = stream.find("img", class_="offer__icon")['alt']
            print(f'{text_input} can be found in {stream_text}')
            return text_input, stream_text
        else:
            print(f'{text_input} cannot be found streaming')
            return text_input, "-"
    else:
        print(f'{text_input} cannot be found streaming')
        return text_input, "-"


def should_add_to_platform(platforms: list, platform_stream: str):
    if len(platforms) == 0:
        return True  # no platforms were provided
    return any(platform_stream.upper() in string for string in platforms) or any(
        p.upper() in platform_stream.upper() for p in platforms)


def main():
    if not os.path.isfile('./watchlist.csv'):
        print("watchlist.csv file required to be in the same directory as the script")
        exit(1)
    letterboxd_names = get_names()
    platforms = get_platforms()
    result_rows = []
    for name in letterboxd_names:
        results = search_content(name)
        if results != "FAILED":
            found_title, match = parse_text(results, name)
            if match != "-":
                title, platform_stream = find_stream(results, found_title)
                if should_add_to_platform(platforms, platform_stream):
                    result_rows.append([title, platform_stream])
    with open('results.csv', 'w+', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(result_rows)


if __name__ == "__main__":
    main()
