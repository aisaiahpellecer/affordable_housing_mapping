from bs4 import BeautifulSoup
import requests
from concurrent.futures import ThreadPoolExecutor
import pandas as pd
import os

url = 'https://chicago.urbanize.city/neighborhoods'

def scrape_section(section):
    try:
        response = requests.get(section)
        html_content = response.content
        bsObj = BeautifulSoup(html_content, 'html.parser')

        content = bsObj.find_all("div", {'class': 'content'})

        article_links = []
        for elements in content:
            try:
                individual_article_elements = elements.find_all("a")

                for article_link in individual_article_elements:
                    link = article_link.get('href')
                    article_links.append('https://chicago.urbanize.city/' + link)

            except Exception as e:
                print(f"Inner loop error: {e}")

        return article_links

    except Exception as e:
        print(f"Outer loop error: {e}")
        return []

def scrape_article(link):
    try:
        response = requests.get(link)
        html_content = response.content

        bsObj = BeautifulSoup(html_content, 'html.parser')
        neighborhood = bsObj.find('div', {'class': 'neighborhood-tag'}).get_text()
        article_name = bsObj.find('h1', {'class': 'article-title'}).get_text()
        body_div = bsObj.find('div', {'class': 'article-body'})
        content = ''
        if body_div:
            paragraphs = body_div.find_all('p')

            filtered_paragraphs = [p for p in paragraphs if not p.find('span', {'class': 'caption'})]

            for paragraph in filtered_paragraphs:
                content += paragraph.getText() + " "
            return {'article_name':article_name,'content': content, 'neighborhood': neighborhood}

        else:
            print("Div with class 'article-body' not found.")
            return {}

    except Exception as e:
        print(f"Outer loop error: {e}")
        return {}

if __name__ == '__main__':
    with ThreadPoolExecutor() as executor:
        section_links = [link.get('href') for link in
                         BeautifulSoup(requests.get(url).content, 'html.parser').find_all('a',
                                                                                           href=lambda x: x and 'neighborhood' in x)]

        section_links = ['https://chicago.urbanize.city/' + link for link in section_links]

        batches = [section_links[i:i + 5] for i in range(0, len(section_links), 5)]
        article_links = []

        with ThreadPoolExecutor() as executor:
            for batch in batches:
                results = executor.map(scrape_section, batch)
                article_links.extend([link for sublist in results for link in sublist])

        with ThreadPoolExecutor() as executor:
            data = list(executor.map(scrape_article, article_links))


path = "data/"
isExist = os.path.exists(path)
if not isExist:
    os.makedirs(path)


df = pd.DataFrame(data)
df.to_csv(os.path.join(path,'urbanize.csv'), index=False)
