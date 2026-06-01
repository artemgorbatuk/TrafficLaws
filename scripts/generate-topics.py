#!/usr/bin/env python3
"""Generate topics/*.html and rebuild index.html hub sections."""

from __future__ import annotations

import html
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TOPICS = ROOT / "topics"
SIGNS = ROOT / "TrafficSigns"


def sign_filename(num: str) -> str:
    parts = num.strip().split(".")
    if len(parts) == 2:
        return f"{parts[0].zfill(2)}.{parts[1].zfill(2)}.png"
    if len(parts) == 3:
        return f"{parts[0].zfill(2)}.{parts[1].zfill(2)}.{parts[2].zfill(2)}.png"
    raise ValueError(f"Bad sign number: {num}")


def sign_exists(num: str) -> bool:
    return (SIGNS / sign_filename(num)).is_file()


def esc(text: str) -> str:
    return html.escape(text, quote=True)


Item = dict  # slug, title, refs, signs: list[str]
Group = dict  # title: str | None, items: list[Item]
Section = dict  # id, title, breadcrumb, groups


SECTIONS: list[Section] = [
    {
        "id": "road-types",
        "title": "Виды дорог",
        "breadcrumb": "Дорога",
        "groups": [
            {
                "title": None,
                "items": [
                    {"slug": "avtomagistral", "title": "Автомагистраль", "refs": "ПДД 1.2 · Знак 5.1", "signs": ["5.1"]},
                    {"slug": "dorogi-vne-naselennyh-punktov", "title": "Дороги общего пользования вне населённых пунктов", "refs": "ПДД 1.2 · Знак 5.3", "signs": ["5.3"]},
                    {"slug": "doroga-v-naselennyom-punkte", "title": "Дорога в населённом пункте", "refs": "ПДД 10.2 · Знаки 5.23.1, 5.23.2, 5.25", "signs": ["5.23.1", "5.23.2", "5.25"]},
                    {"slug": "doroga-dlya-avtomobiley", "title": "Дорога для автомобилей", "refs": "ПДД 1.2 · Знак 5.3", "signs": ["5.3"]},
                    {"slug": "zhilaya-zona", "title": "Жилая зона", "refs": "ПДД 17.1 · Знак 5.21", "signs": ["5.21"]},
                    {"slug": "velosipednaya-zona", "title": "Велосипедная зона", "refs": "ПДД 24.1 · Знак 5.33", "signs": ["5.33"]},
                    {"slug": "vydelennye-polosy-obshchestvennogo-transporta", "title": "Выделенные полосы для общественного транспорта", "refs": "ПДД 18.2 · Знак 5.14.1", "signs": ["5.14.1"]},
                ],
            }
        ],
    },
    {
        "id": "road-elements",
        "title": "Элементы дороги",
        "breadcrumb": "Дорога",
        "groups": [
            {
                "title": None,
                "items": [
                    {"slug": "trotuary-ili-obochiny", "title": "Тротуары или обочины", "refs": "ПДД 1.2", "signs": []},
                ],
            },
            {
                "title": "Проезжие части",
                "items": [
                    {"slug": "polosy-dvizheniya", "title": "Полосы движения", "refs": "ПДД 1.2", "signs": []},
                    {"slug": "polosy-razgona-tormozheniya-podema", "title": "Полосы разгона, торможения, подъёма, аварийной остановки", "refs": "ПДД 8.10", "signs": []},
                    {"slug": "polosa-marshrutnyh-ts", "title": "Полоса для маршрутных транспортных средств (автобусы, троллейбусы)", "refs": "Знак 5.14", "signs": ["5.14.1", "5.14.2"]},
                    {"slug": "velosipednaya-polosa", "title": "Велосипедная полоса (для велосипедистов, мопедов, СИМ)", "refs": "Знак 5.14.3", "signs": ["5.14.3"]},
                    {"slug": "reversivnaya-polosa", "title": "Реверсивная полоса движения", "refs": "Знаки 5.15.1, 5.15.2 · Разметка 1.9", "signs": ["5.15.1", "5.15.2"]},
                    {"slug": "doroga-odnostoronnego-dvizheniya", "title": "Дорога с односторонним движением", "refs": "Знаки 5.5, 5.6", "signs": ["5.5", "5.6"]},
                ],
            },
            {
                "title": None,
                "items": [
                    {"slug": "tramvajnye-puti", "title": "Трамвайные пути", "refs": "ПДД 9.6", "signs": []},
                ],
            },
            {
                "title": "Разделительная полоса",
                "items": [
                    {"slug": "sploshnaya-liniya", "title": "Сплошная линия", "refs": "Разметка 1.2", "signs": []},
                    {"slug": "preryvistaya-liniya", "title": "Прерывистая линия", "refs": "Разметка 1.5", "signs": []},
                    {"slug": "ostrovok-bezopasnosti", "title": "Островок безопасности", "refs": "Разметка 1.16.1—1.16.3", "signs": []},
                ],
            },
        ],
    },
    {
        "id": "road-intersections",
        "title": "Места пересечения и взаимодействия",
        "breadcrumb": "Дорога",
        "groups": [
            {
                "title": "Перекрёсток",
                "items": [
                    {"slug": "reguliruemyj-perekrestok", "title": "Регулируемый перекрёсток", "refs": "ПДД 13.3", "signs": []},
                    {"slug": "nereguliruemyj-perekrestok", "title": "Нерегулируемый перекрёсток", "refs": "ПДД 13.11", "signs": []},
                    {"slug": "glavnaya-i-vtorostepennaya-doroga", "title": "Главная и второстепенная дорога", "refs": "ПДД 13.11", "signs": ["2.3.1", "2.4", "2.1"]},
                    {"slug": "perekrestok-ravnoznachnyh-dorog", "title": "Перекрёсток равнозначных дорог", "refs": "ПДД 13.11", "signs": []},
                ],
            },
            {
                "title": "Пешеходная инфраструктура",
                "items": [
                    {"slug": "peshehodnyj-perehod", "title": "Пешеходный переход", "refs": "Знаки 5.19.1, 5.19.2", "signs": ["5.19.1", "5.19.2"]},
                    {"slug": "peshehodnaya-dorozhka", "title": "Пешеходная дорожка", "refs": "Знак 4.5", "signs": ["4.5"]},
                    {"slug": "peshehodnaya-zona", "title": "Пешеходная зона", "refs": "Знак 5.34", "signs": ["5.34"]},
                ],
            },
            {
                "title": None,
                "items": [
                    {"slug": "zheleznodorozhnyj-pereezd", "title": "Железнодорожный переезд", "refs": "ПДД 15.1 · Знаки 1.1—1.4", "signs": ["1.1", "1.2", "1.3", "1.4"]},
                ],
            },
        ],
    },
    {
        "id": "road-structures",
        "title": "Искусственные сооружения",
        "breadcrumb": "Дорога",
        "groups": [
            {
                "title": None,
                "items": [
                    {"slug": "tonnel", "title": "Тоннель", "refs": "ПДД 11.7", "signs": []},
                    {"slug": "most", "title": "Мост", "refs": "ПДД 1.2", "signs": []},
                    {"slug": "estakada", "title": "Эстакада", "refs": "ПДД 1.2", "signs": []},
                    {"slug": "puteprovod", "title": "Путепровод", "refs": "ПДД 1.2", "signs": []},
                ],
            }
        ],
    },
    {
        "id": "road-services",
        "title": "Инфраструктура обслуживания",
        "breadcrumb": "Дорога",
        "groups": [
            {
                "title": None,
                "items": [
                    {"slug": "marshrutnye-ostanovki", "title": "Маршрутные остановки", "refs": "Знак 5.16", "signs": ["5.16"]},
                    {"slug": "parkovki", "title": "Парковки", "refs": "Знак 6.4", "signs": ["6.4"]},
                ],
            }
        ],
    },
    {
        "id": "vehicle-mass",
        "title": "Масса",
        "breadcrumb": "Транспортное средство",
        "groups": [
            {
                "title": None,
                "items": [
                    {"slug": "razreshennaya-maksimalnaya-massa", "title": "Разрешённая максимальная масса", "refs": "ПДД 23.1", "signs": []},
                    {"slug": "fakticheskaya-massa", "title": "Фактическая масса", "refs": "ПДД 23.1", "signs": []},
                    {"slug": "snaryazhennaya-massa", "title": "Снаряжённая масса", "refs": "ПДД 23.1", "signs": []},
                ],
            }
        ],
    },
    {
        "id": "vehicle-lights",
        "title": "Световые приборы",
        "breadcrumb": "Транспортное средство",
        "groups": [
            {
                "title": None,
                "items": [
                    {"slug": "fary-blizhnego-dalnego-sveta", "title": "Фары ближнего/дальнего света", "refs": "ПДД 19.1", "signs": []},
                    {"slug": "dnevnye-hodovye-ogni", "title": "Дневные ходовые огни", "refs": "ПДД 19.5", "signs": []},
                    {"slug": "gabaritnye-ogni", "title": "Габаритные огни", "refs": "ПДД 19.1", "signs": []},
                    {"slug": "ukazateli-povorotov", "title": "Указатели поворотов", "refs": "ПДД 19.1", "signs": []},
                    {"slug": "stop-signaly", "title": "Стоп-сигналы", "refs": "ПДД 19.1", "signs": []},
                    {"slug": "fonar-zadnego-hoda", "title": "Фонарь заднего хода", "refs": "ПДД 19.1", "signs": []},
                    {"slug": "protivotumannye-fary", "title": "Противотуманные фары", "refs": "ПДД 19.4", "signs": []},
                ],
            }
        ],
    },
    {
        "id": "vehicle-overtaking",
        "title": "Продольное движение и опережение",
        "breadcrumb": "Транспортное средство",
        "groups": [
            {
                "title": None,
                "items": [
                    {"slug": "obgon", "title": "Обгон", "refs": "ПДД 11.1—11.3", "signs": ["3.20"]},
                    {"slug": "operezhenie", "title": "Опережение", "refs": "ПДД 11.4", "signs": []},
                    {"slug": "perestroenie", "title": "Перестроение", "refs": "ПДД 8.4", "signs": []},
                ],
            }
        ],
    },
    {
        "id": "vehicle-start-turns",
        "title": "Изменение направления и начало движения",
        "breadcrumb": "Транспортное средство",
        "groups": [
            {
                "title": None,
                "items": [
                    {"slug": "nachalo-dvizheniya", "title": "Начало движения", "refs": "ПДД 8.1", "signs": []},
                    {"slug": "povoroty-napravo-nalevo", "title": "Повороты направо/налево", "refs": "ПДД 8.5", "signs": ["4.1.1", "4.1.2", "4.1.3", "4.1.4"]},
                    {
                        "slug": "razvorot",
                        "title": "Разворот",
                        "refs": "ПДД 8.5, 8.8, 8.11, 16.1, 16.3",
                        "signs": [
                            "3.18.2",
                            "3.19",
                            "4.1.1",
                            "4.1.2",
                            "4.1.3",
                            "4.1.4",
                            "4.1.5",
                            "4.1.6",
                            "4.3",
                            "5.1",
                            "5.2",
                            "5.3",
                            "5.5",
                            "5.6",
                            "5.7.1",
                            "5.7.2",
                            "5.15.1",
                            "5.15.2",
                            "5.16",
                            "5.19.1",
                            "5.19.2",
                            "6.3.1",
                            "6.3.2",
                            "1.31",
                            "1.1",
                            "1.2",
                            "1.3.1",
                            "1.4",
                            "1.12.1",
                            "1.18",
                        ],
                    },
                    {"slug": "dvizhenie-zadnim-hodom", "title": "Движение задним ходом", "refs": "ПДД 8.12", "signs": []},
                    {"slug": "krugovoe-dvizhenie", "title": "Движение по круговым развязкам («круг»)", "refs": "ПДД 13.9—13.12", "signs": ["4.3"]},
                ],
            }
        ],
    },
    {
        "id": "vehicle-stop-parking",
        "title": "Остановка и стоянка",
        "breadcrumb": "Транспортное средство",
        "groups": [
            {
                "title": None,
                "items": [
                    {"slug": "ostanovka", "title": "Остановка", "refs": "ПДД 12.1—12.3", "signs": ["3.27"]},
                    {"slug": "stoyanka", "title": "Стоянка", "refs": "ПДД 12.1—12.3", "signs": ["3.28"]},
                    {"slug": "vynuzhdennaya-ostanovka", "title": "Вынужденная остановка", "refs": "ПДД 12.6", "signs": []},
                    {"slug": "tormozhenie", "title": "Торможение (включая экстренное)", "refs": "ПДД 10.5", "signs": []},
                ],
            }
        ],
    },
    {
        "id": "vehicle-interaction",
        "title": "Правила взаимодействия и общие понятия",
        "breadcrumb": "Транспортное средство",
        "groups": [
            {
                "title": None,
                "items": [
                    {"slug": "preimuschestvo", "title": "Преимущество (приоритет)", "refs": "ПДД 1.2", "signs": []},
                    {"slug": "ustupit-dorogu", "title": "Требование уступить дорогу", "refs": "ПДД 1.2", "signs": ["2.4"]},
                    {"slug": "vstrechnyj-razezd", "title": "Встречный разъезд", "refs": "ПДД 11.7", "signs": []},
                    {"slug": "opasnoe-vozhdenie", "title": "Опасное вождение", "refs": "ПДД 2.7", "signs": []},
                ],
            }
        ],
    },
    {
        "id": "vehicle-speed",
        "title": "Скоростной режим",
        "breadcrumb": "Транспортное средство",
        "groups": [
            {
                "title": "Предельно допустимая скорость",
                "items": [
                    {"slug": "skorost-gorod", "title": "Городские улицы", "refs": "ПДД 10.2", "signs": ["3.24"]},
                    {"slug": "skorost-trassa", "title": "Трассы", "refs": "ПДД 10.3", "signs": ["3.24"]},
                    {"slug": "skorost-avtomagistral", "title": "Автомагистрали", "refs": "ПДД 10.3", "signs": ["3.24"]},
                ],
            },
            {
                "title": "Специальные ограничения скорости",
                "items": [
                    {"slug": "skorost-shkoly", "title": "Школы", "refs": "ПДД 10.1", "signs": ["3.24"]},
                    {"slug": "skorost-zhilaya-zona", "title": "Жилые зоны", "refs": "ПДД 10.2", "signs": ["5.21"]},
                    {"slug": "skorost-opasnye-uchastki", "title": "Опасные участки", "refs": "ПДД 10.1", "signs": ["3.24", "1.13"]},
                ],
            },
        ],
    },
    {
        "id": "participants-vehicles-mechanical",
        "title": "Механические транспортные средства",
        "breadcrumb": "Участники движения",
        "groups": [
            {
                "title": None,
                "items": [
                    {"slug": "legkovye-avtomobili", "title": "Легковые автомобили (до 3,5 тонн)", "refs": "ПДД 1.2", "signs": []},
                    {"slug": "gruzovye-avtomobili", "title": "Грузовые автомобили (более 3,5 тонн)", "refs": "ПДД 1.2", "signs": []},
                    {"slug": "avtopoezda", "title": "Автопоезда (тягачи с прицепами)", "refs": "ПДД 1.2", "signs": []},
                    {"slug": "mopedy", "title": "Мопеды", "refs": "ПДД 1.2", "signs": []},
                    {"slug": "mototsikly", "title": "Мотоциклы", "refs": "ПДД 1.2", "signs": []},
                    {"slug": "kvadritsikly", "title": "Квадрициклы", "refs": "ПДД 1.2", "signs": []},
                ],
            }
        ],
    },
    {
        "id": "participants-vehicles-sim",
        "title": "Средства индивидуальной мобильности (СИМ)",
        "breadcrumb": "Участники движения",
        "groups": [
            {
                "title": None,
                "items": [
                    {"slug": "elektrosamokaty", "title": "Электросамокаты", "refs": "ПДД 1.2", "signs": []},
                    {"slug": "monokolesa", "title": "Моноколёса", "refs": "ПДД 1.2", "signs": []},
                    {"slug": "kvadrotsikly", "title": "Квадроциклы", "refs": "ПДД 1.2", "signs": []},
                ],
            }
        ],
    },
    {
        "id": "participants-vehicles-muscular",
        "title": "Мускульные транспортные средства",
        "breadcrumb": "Участники движения",
        "groups": [
            {
                "title": None,
                "items": [
                    {"slug": "velosipedy", "title": "Велосипеды", "refs": "ПДД 1.2", "signs": []},
                ],
            }
        ],
    },
    {
        "id": "participants-vehicles-special",
        "title": "Транспортные средства особого статуса",
        "breadcrumb": "Участники движения",
        "groups": [
            {
                "title": "Маршрутные транспортные средства",
                "items": [
                    {"slug": "avtobusy", "title": "Автобусы", "refs": "ПДД 1.2", "signs": []},
                    {"slug": "trollejbusy", "title": "Троллейбусы", "refs": "ПДД 1.2", "signs": []},
                    {"slug": "tramvai", "title": "Трамваи", "refs": "ПДД 1.2", "signs": []},
                ],
            },
            {
                "title": None,
                "items": [
                    {"slug": "shkolnye-avtobusy", "title": "Школьные автобусы", "refs": "ПДД 22.6", "signs": []},
                    {"slug": "taksi", "title": "Такси", "refs": "ПДД 1.2", "signs": []},
                    {"slug": "organizovannaya-kolonna", "title": "Организованная транспортная колонна", "refs": "ПДД 2.7", "signs": ["1.30"]},
                ],
            },
        ],
    },
    {
        "id": "participants-individuals",
        "title": "Индивидуальные участники",
        "breadcrumb": "Участники движения",
        "groups": [
            {
                "title": None,
                "items": [
                    {"slug": "voditeli", "title": "Водители", "refs": "ПДД 1.2", "signs": []},
                    {"slug": "passazhiry", "title": "Пассажиры", "refs": "ПДД 5.1", "signs": []},
                    {"slug": "peshehody", "title": "Пешеходы", "refs": "ПДД 1.2", "signs": []},
                    {"slug": "organizovannaya-peshehodnaya-kolonna", "title": "Организованная пешеходная колонна", "refs": "Знак 1.29", "signs": ["1.29"]},
                ],
            }
        ],
    },
    {
        "id": "participants-transportation",
        "title": "Перевозка грузов и пассажиров",
        "breadcrumb": "Участники движения",
        "groups": [
            {
                "title": None,
                "items": [
                    {"slug": "passazhiry", "title": "Пассажиры", "refs": "ПДД 22.1—22.9", "signs": []},
                    {"slug": "gruzy", "title": "Грузы", "refs": "ПДД 23.5", "signs": []},
                    {"slug": "opasnye-gruzy", "title": "Опасные грузы", "refs": "ПДД 23.5", "signs": []},
                ],
            }
        ],
    },
    {
        "id": "participants-regulation",
        "title": "Регулирование дорожного движения",
        "breadcrumb": "Участники движения",
        "groups": [
            {
                "title": None,
                "items": [
                    {"slug": "svetofory", "title": "Сигналы светофоров", "refs": "ПДД 6.2—6.5", "signs": []},
                    {"slug": "regulirovschik", "title": "Действия регулировщика", "refs": "ПДД 6.10—6.15", "signs": []},
                    {"slug": "dorozhnye-znaki", "title": "Дорожные знаки", "refs": "ПДД 5.1—8.26", "signs": []},
                    {"slug": "gorizontalnaya-razmetka", "title": "Горизонтальная разметка", "refs": "ПДД 1.1—1.26", "signs": []},
                ],
            }
        ],
    },
    {
        "id": "participants-conditions",
        "title": "Условия дорожного движения",
        "breadcrumb": "Участники движения",
        "groups": [
            {
                "title": None,
                "items": [
                    {"slug": "nedostatochnaya-vidimost", "title": "Недостаточная видимость", "refs": "ПДД 1.2", "signs": []},
                    {"slug": "ogranichennaya-vidimost", "title": "Ограниченная видимость", "refs": "ПДД 1.2", "signs": []},
                    {"slug": "prepyatstvie", "title": "Препятствие", "refs": "ПДД 1.2", "signs": []},
                    {"slug": "svetloe-vremya-sutok", "title": "Светлое время суток", "refs": "ПДД 19.1", "signs": []},
                    {"slug": "temnoe-vremya-sutok", "title": "Тёмное время суток", "refs": "ПДД 19.1", "signs": []},
                    {"slug": "pogodnye-usloviya", "title": "Погодные условия", "refs": "ПДД 10.1", "signs": []},
                ],
            }
        ],
    },
]


HUB_BLOCKS = [
    {
        "id": "road",
        "title": "Дорога",
        "sections": ["road-types", "road-elements", "road-intersections", "road-structures", "road-services"],
    },
    {
        "id": "vehicle",
        "title": "Транспортное средство (ТС)",
        "sections": [
            "vehicle-mass",
            "vehicle-lights",
            "vehicle-overtaking",
            "vehicle-start-turns",
            "vehicle-stop-parking",
            "vehicle-interaction",
            "vehicle-speed",
        ],
    },
    {
        "id": "participants",
        "title": "Участники дорожного движения",
        "sections": [
            "participants-vehicles-mechanical",
            "participants-vehicles-sim",
            "participants-vehicles-muscular",
            "participants-vehicles-special",
            "participants-individuals",
            "participants-transportation",
            "participants-regulation",
            "participants-conditions",
        ],
    },
]


NAV_TREE = [
    {
        "id": "road",
        "title": "Дорога",
        "children": [
            {"section": "road-types"},
            {"section": "road-elements"},
            {"section": "road-intersections"},
            {"section": "road-structures"},
            {"section": "road-services"},
        ],
    },
    {
        "id": "vehicle",
        "title": "Транспортное средство (ТС)",
        "children": [
            {
                "label": "Характеристики",
                "children": [{"section": "vehicle-mass"}, {"section": "vehicle-lights"}],
            },
            {
                "label": "Движение и маневрирование",
                "children": [
                    {"section": "vehicle-overtaking"},
                    {"section": "vehicle-start-turns"},
                    {"section": "vehicle-stop-parking"},
                    {"section": "vehicle-interaction"},
                    {"section": "vehicle-speed"},
                ],
            },
        ],
    },
    {
        "id": "participants",
        "title": "Участники дорожного движения",
        "children": [
            {
                "label": "Транспортные средства (ТС)",
                "children": [
                    {"section": "participants-vehicles-mechanical"},
                    {"section": "participants-vehicles-sim"},
                    {"section": "participants-vehicles-muscular"},
                    {"section": "participants-vehicles-special"},
                ],
            },
            {"section": "participants-individuals"},
            {"section": "participants-transportation"},
            {"section": "participants-regulation"},
            {"section": "participants-conditions"},
        ],
    },
]


def iter_items(section: Section):
    for group in section["groups"]:
        for item in group["items"]:
            yield group.get("title"), item


def all_items(section: Section) -> list[Item]:
    return [item for _, item in iter_items(section)]


def section_by_id(section_id: str) -> Section:
    for section in SECTIONS:
        if section["id"] == section_id:
            return section
    raise KeyError(section_id)


def render_signs(signs: list[str]) -> str:
    parts = []
    for num in signs:
        if sign_exists(num):
            fn = sign_filename(num)
            parts.append(
                f'        <img class="sign" src="../TrafficSigns/{esc(fn)}" '
                f'alt="Знак {esc(num)}" title="{esc(fn)}" loading="lazy" />'
            )
    if not parts:
        return ""
    return "\n".join(parts) + "\n"


BREADCRUMB_HUB = {
    "Дорога": "road",
    "Транспортное средство": "vehicle",
    "Участники движения": "participants",
}


def render_topic_page(section: Section) -> str:
    sid = section["id"]
    title = section["title"]
    crumb = section["breadcrumb"]
    hub_id = BREADCRUMB_HUB[crumb]
    count = len(all_items(section))

    nav_items = []
    articles = []

    for group in section["groups"]:
        gtitle = group.get("title")
        if gtitle:
            articles.append(f'      <h4 class="topic-group">{esc(gtitle)}</h4>')

        for item in group["items"]:
            slug = item["slug"]
            ititle = item["title"]
            refs = item["refs"]
            nav_items.append(f'        <li><a href="#{esc(slug)}">{esc(ititle)}</a></li>')
            signs_html = render_signs(item.get("signs", []))
            articles.append(
                f"""      <article id="{esc(slug)}" class="topic-card">
        <header class="topic-card__header">
          <h3>{esc(ititle)}</h3>
          <p class="refs">{esc(refs)}</p>
        </header>
        <div class="signs">{signs_html.rstrip()}</div>
        <div class="notes"></div>
      </article>"""
            )

    nav_block = "\n".join(nav_items)
    articles_block = "\n".join(articles)

    return f"""<!doctype html>
<html lang="ru">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>{esc(title)} — ПДД</title>
    <link rel="stylesheet" href="../index.css" />
  </head>
  <body id="top" class="topic-page">
    <header class="page-header">
      <nav class="breadcrumb" aria-label="Навигация">
        <a class="breadcrumb__link" href="../index.html">Содержание</a>
        <span class="breadcrumb__sep" aria-hidden="true">›</span>
        <a class="breadcrumb__link" href="../index.html#{esc(hub_id)}">{esc(crumb)}</a>
        <span class="breadcrumb__sep" aria-hidden="true">›</span>
        <a class="breadcrumb__link breadcrumb__link--current" href="#top" aria-current="page">{esc(title)}</a>
      </nav>
      <h1>{esc(title)}</h1>
      <p class="page-meta">{count} {"пункт" if count == 1 else "пункта" if 2 <= count <= 4 else "пунктов"}</p>
    </header>

    <div class="topic-layout">
      <nav class="topic-nav" aria-label="Пункты раздела">
        <h2>На этой странице</h2>
        <ul>
{nav_block}
        </ul>
      </nav>

      <main class="topic-main">
{articles_block}
      </main>
    </div>

    <a class="back-to-top" href="#top" aria-label="Наверх">↑</a>
    <script src="../scripts/sign-tooltips.js" defer></script>
  </body>
</html>
"""


def render_nav_item(item: Item, section_id: str) -> str:
    label = f'{item["title"]} [{item["refs"]}]'
    return (
        f'<li><a href="topics/{esc(section_id)}.html#{esc(item["slug"])}">'
        f"{esc(label)}</a></li>"
    )


def render_nav_node(node) -> str:
    if "section" in node:
        section = section_by_id(node["section"])
        lines = [
            f'<li><a class="nav-section" href="topics/{esc(section["id"])}.html">'
            f'{esc(section["title"])}</a>:',
            "<ul>",
        ]
        for item in all_items(section):
            lines.append(render_nav_item(item, section["id"]))
        lines.append("</ul></li>")
        return "\n".join(lines)

    label = node.get("label") or node["title"]
    href = f'#"{node["id"]}"' if "id" in node and "label" not in node else None
    if "id" in node and "label" not in node:
        open_tag = f'<li><a href="#{esc(node["id"])}">{esc(label)}</a>:'
    else:
        open_tag = f"<li><span class=\"nav-group\">{esc(label)}</span>:"

    lines = [open_tag, "<ul>"]
    for child in node["children"]:
        lines.append(render_nav_node(child))
    lines.append("</ul></li>")
    return "\n".join(lines)


def render_hub_cards() -> str:
    sections_map = {s["id"]: s for s in SECTIONS}
    blocks = []
    for block in HUB_BLOCKS:
        cards = []
        for sid in block["sections"]:
            section = sections_map[sid]
            count = len(all_items(section))
            cards.append(
                f"""          <a class="section-card" href="topics/{esc(sid)}.html">
            <span class="section-card__title">{esc(section["title"])}</span>
            <span class="section-card__meta">{count} {"тема" if count == 1 else "темы" if 2 <= count <= 4 else "тем"}</span>
          </a>"""
            )
        cards_html = "\n".join(cards)
        blocks.append(
            f"""      <section id="{esc(block["id"])}" class="hub-block">
        <h2>{esc(block["title"])}</h2>
        <div class="section-cards">
{cards_html}
        </div>
      </section>"""
        )
    return "\n".join(blocks)


def render_index() -> str:
    nav_nodes = "\n".join(render_nav_node(node) for node in NAV_TREE)
    hub = render_hub_cards()

    return f"""<!doctype html>
<html lang="ru">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>Правила дорожного движения</title>
    <link rel="stylesheet" href="index.css" />
  </head>
  <body id="top" class="home-page">
    <header class="site-header">
      <p class="site-tagline">Справочник и личные заметки</p>
      <h1>Правила дорожного движения</h1>
    </header>

    <div class="home-layout">
      <nav id="TableContents" class="toc-panel" aria-label="Содержание">
        <h2>Содержание</h2>
        <ul class="toc-tree">
{nav_nodes}
        </ul>
      </nav>

      <main class="hub-main">
        <p class="hub-intro">Выберите раздел для просмотра тем и заметок. Оглавление слева — для быстрого перехода к любому пункту.</p>
{hub}
      </main>
    </div>

    <a class="back-to-top" href="#top" aria-label="Наверх">↑</a>
  </body>
</html>
"""


def main() -> None:
    TOPICS.mkdir(exist_ok=True)
    missing_signs: list[str] = []

    for section in SECTIONS:
        for item in all_items(section):
            for num in item.get("signs", []):
                if not sign_exists(num):
                    missing_signs.append(f'{section["id"]}/{item["slug"]}: {num}')

        path = TOPICS / f'{section["id"]}.html'
        path.write_text(render_topic_page(section), encoding="utf-8")
        print(f"Wrote {path.relative_to(ROOT)}")

    index_path = ROOT / "index.html"
    index_path.write_text(render_index(), encoding="utf-8")
    print(f"Wrote {index_path.relative_to(ROOT)}")

    if missing_signs:
        print("\nMissing signs (skipped images):")
        for line in sorted(set(missing_signs)):
            print(f"  - {line}")


if __name__ == "__main__":
    main()
