# -*- coding: utf-8 -*-

from collections import OrderedDict

COUNTRIES_LIST = [
    ("MU", "Московский университет МВД России"),
    ("KU", "Краснодарский университет МВД России"),
    ("PU", "Санкт-Петербургский университет МВД России"),
    ("VA", "Волгоградская академия МВД России"),
    ("NA", "Нижегородская академия МВД России"),
    ("OA", "Омская академия МВД России"),
    ("TI", "Тюменский юридический институт МВД России"),
    ("BI", "Барнаульский юридический институт МВД России"),
    ("BG", "Белгородский юридический институт МВД России"),
    ("VI", "Воронежский институт МВД России"),
    ("VS", "Восточно-Сибирский институт МВД России"),
    ("VU", "Дальневосточный юридический институт МВД России"),
    ("KI", "Казанский юридический институт МВД России"),
    ("OI", "Орловский юридический институт МВД России"),
    ("RI", "Ростовский юридический институт МВД России"),
    ("SI", "Сибирский юридический институт МВД России"),
    ("UR", "Уральский юридический институт МВД России"),
    ("UI", "Уфимский юридический институт МВД России"),
]

# Nicely titled (and translatable) country names.
COUNTRIES_DICT = OrderedDict(COUNTRIES_LIST)


def get_countries():
    return COUNTRIES_DICT


def lookup_country_code(country_code):
    return COUNTRIES_DICT.get(country_code)