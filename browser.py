import os, sys, requests
from _collections import deque
from bs4 import BeautifulSoup
from colorama import init, Fore

dir_name = sys.argv[1]
back_stack = deque()
back_puffer = None

if os.path.exists(dir_name) == False:
    os.mkdir(dir_name)

def get_page(url):
    if url.startswith("https://") == False:
        url = "https://"+url
    r = requests.get(url)
    soup = BeautifulSoup(r.content, "html.parser")(["p","h1","h2","a","ul","ol","li"])
    for tag in soup:
        if tag.name == "a":
            print(Fore.BLUE + tag.get_text())
        else:
            print(tag.get_text())
    return soup


def check_if_exists(path, url):
    global back_puffer
    if os.path.exists(path):
        with open(path) as file:
            print(file.read())
        back_puffer = url
        browser()
    elif not "." in url:
        print("Error, please type in a valid URL")
        browser()

def browser():
    global back_puffer
    while True:
        url = input()
        if url == "exit":
            sys.exit()
        elif url == "back" and len(back_stack) > 0 :
            url = back_stack.pop()
        back_stack.append(back_puffer)
        path = os.path.join(dir_name, url.strip(".com").strip(".org").strip("www."))
        check_if_exists(path, url)
        try:
            text = get_page(url)
            with open(path, "w") as ufile:
                for tag in text:
                    ufile.write(tag.get_text())
            back_puffer = url
        except KeyError:
            print("Error 404: URL not found")
            continue

browser()

