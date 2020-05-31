import requests
from lxml import html
import json
from os import path, mkdir
from consts import *
from time import sleep
import re


def intersection(lst1, lst2):
    return set(lst1).intersection(lst2) 


def correc_filename(filename):
    filename = filename.replace("*", "(star)")
    filename = filename.replace('"', "``")
    filename = filename.replace('/', "_")
    return filename


def get_page(url, filename):
    r = requests.get(url, headers=headers)
    text = r.text
    filename = correc_filename(filename)
    with open(filename, 'wb') as output_file:
        output_file.write(text.encode(encoding=default_encoding))
    return html.fromstring(text)


def parse_itinerary(text):
    regexpr = r"\([^)]*\)"
    text = re.sub(regexpr, '', text)
    stopes = text.split(' - ')
    stopes = [stop.strip().lower()
                          .replace(";", "")
                          .replace(")", "")
              for stop in stopes]
    return stopes


def save_json(ob, filename):
    with open(filename, 'wt', encoding=default_encoding) as f:
        f.write(json.dumps(ob))


def load_json(filename):
    with open(filename, 'rt', encoding=default_encoding) as f:
        json_string = f.read()
        return json.loads(json_string)


def load_html(filename):
    with open(filename, 'rt', encoding=default_encoding) as f:
        html_str = f.read()
        page = html.fromstring(html_str)
    return page


def sure_folder_exists(folder_name):
    if (not path.exists(folder_name)):
        mkdir(folder_name)


def get_or_load_page(url, filename):
    filename = correc_filename(filename)
    if (path.exists(filename)):
        page = load_html(filename)
    else:
        page = get_page(url, filename)
        sleep(sleep_time)
    return page


def save_graph_csv(graph, filename):
    with open(filename, 'wt', encoding=default_encoding) as f:
        for edge in graph.edges:
            f.write(f'{edge[0]}, {edge[1]}\n')
