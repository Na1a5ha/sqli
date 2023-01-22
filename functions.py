import random


def search_in_page_error(page, db):
    # for i in db_s:
    #     page = page.replace(i, " ")
    # page2 = page.split(" ")
    for i in db:
        if page.find(i) != -1:
            return 1
    return 0

def search_in_page_ta(page, db_s):
    key = 0
    for i in db_s:
        page = page.replace(i, " ")
    for i in page.split(" "):
        if i == "textarea":
            key = 1
        if key == 1:
            if i == "name":
                key = 2
                continue
        if key == 2 and i != " ":
            name = i
            return name

def rtime ():
    return random.randint(3, 6)

