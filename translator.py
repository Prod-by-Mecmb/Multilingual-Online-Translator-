from bs4 import BeautifulSoup
import requests, sys

all_languages = ['arabic', 'german', 'english', 'spanish', 'french', 'hebrew', 'japanese', 'dutch', 'polish', 'portuguese', 'romanian', 'russian', 'turkish']
args = sys.argv

yourLanguage = args[1]
toLanguage = args[2]
word = args[3]

if toLanguage not in all_languages and toLanguage != 'all':
    print(f'Sorry, the program doesn\'t support {toLanguage}')
    exit()
elif toLanguage != 'all':
    linkus = "https://context.reverso.net/translation/{}-{}/{}".format(yourLanguage, toLanguage, word)
    timeout = 5
    try:
        r = requests.get(linkus, headers={'User-Agent': 'Mozilla/5.0'})
    except (requests.ConnectionError, requests.Timeout) as exception:
        print("Something wrong with your internet connection")
        exit()
    soup = BeautifulSoup(r.content, 'html.parser')
    words = [i.text.strip('\n " "') for i in soup.find_all('a', {'class': "translation"})]
    phrases_list = [(i.text.strip('\n " " []')) for i in soup.select("#examples-content .text")]
    print(f'{toLanguage.capitalize()} Translations:')
    print(words[1])
    print(f'\n{toLanguage.capitalize()} Examples:')
    print("\n".join(phrases_list[0]))
elif toLanguage == 'all':
    with open(f'{word}.txt', 'w', encoding="utf-8") as ftw:
        for i in all_languages:
            if i != yourLanguage:
                link_us = "https://context.reverso.net/translation/{}-{}/{}".format(yourLanguage, i, word)
                timeout = 5
                try:
                    r = requests.get(link_us, headers={'User-Agent': 'Mozilla/5.0'})
                except (requests.ConnectionError, requests.Timeout) as exception:
                    print("Something wrong with your internet connection")
                    exit()
                soup = BeautifulSoup(r.content, 'html.parser')
                words = [i.text.strip() for i in soup.find_all('a', {'class': "translation"})]
                phrases_list = [i.text.strip() for i in soup.select("#examples-content .text")]
                print(f'{i.capitalize()} Translations:')
                try:
                    print(words[1])
                except IndexError:
                    print(f'Sorry, unable to find {word}')
                    exit()
                ftw.write(f'{i.capitalize()} Translations:' + '\n' + words[1] + '\n\n')
                print(f'\n{i.capitalize()} Examples:')
                print("\n".join(phrases_list[0:2]))
                print()
                ftw.write(f'{i.capitalize()} Examples:' + '\n' + phrases_list[0])
            else:
                continue