import requests
from bs4 import BeautifulSoup
import json
import time

def get_etymology(word):
    url = f'https://www.etymonline.com/word/{word}'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    etymology_section = soup.find('section', {'class': 'word__defination--2q7ZH'})

    if etymology_section:
        etymology_text = ''
        for paragraph in etymology_section.find_all('p'):
            etymology_text += str(paragraph)

        cleaned_etymology = BeautifulSoup(etymology_text, 'html.parser')
        response_text = cleaned_etymology.get_text(strip=True)
        return {"prompt": word, "response": response_text}
    else:
        return None

def load_words(file_name):
    with open(file_name, 'r') as f:
        words = [word.strip() for word in f.readlines()]
    return words

def load_scraped_data(output_file):
    try:
        with open(output_file, 'r') as f:
            scraped_data = json.load(f)
    except FileNotFoundError:
        scraped_data = []
    return scraped_data

def save_scraped_data(output_file, scraped_data):
    with open(output_file, 'w') as f:
        json.dump(scraped_data, f, ensure_ascii=False, indent=2)

def main(words_file, output_file):
    words = load_words(words_file)
    scraped_data = load_scraped_data(output_file)

    if scraped_data:
        last_word = scraped_data[-1]['prompt']
        start_index = words.index(last_word) + 1
    else:
        start_index = 0

    for word in words[start_index:]:
        etymology = get_etymology(word)
        if etymology:
            scraped_data.append(etymology)
            print(f'Scraped etymology for {word}')
        else:
            print(f'Etymology not found for {word}')

        save_scraped_data(output_file, scraped_data)
        time.sleep(1)  # To avoid overloading the server

if __name__ == '__main__':
    main('words.txt', 'etymology_data.json')
