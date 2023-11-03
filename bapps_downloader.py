from bs4 import BeautifulSoup
import requests
import time
import os
import multiprocessing

BASE_URL = 'https://portswigger.net'
WEBPATH = 'bappstore'
DOWNLOAD_DIR = 'bapps'

def download_file(url, name):
    with requests.Session() as session:
        time.sleep(1)
        r = session.get(url, timeout=10)
        soup = BeautifulSoup(r.content, 'html.parser')
        repo_link = soup.find('a', id='RepoLink').get('href')
        download_link = soup.find('a', id='DownloadedLink').get('href')
        repo_name = repo_link.split('/')[-1]
        file_name = f'{DOWNLOAD_DIR}/{repo_name}.bapp'
        print(f"[*] Downloading: {name}")
        response = session.get(download_link)

        if response.status_code == 200:
            with open(file_name, 'wb') as file:
                file.write(response.content)
        else:
            print(f"Failed to download {file_name}!")

def process_extension(extension):
    url, name = extension
    download_file(url, name)

if __name__ == '__main__':
    if not os.path.exists(DOWNLOAD_DIR):
        os.makedirs(DOWNLOAD_DIR)
      
    extensions = []
    r = requests.get(f'{BASE_URL}/{WEBPATH}')
    soup = BeautifulSoup(r.content, 'html.parser')
    table = soup.find('table', id='List-BAppStore-Table')
    rows = table.find_all('tr')
    for row in rows:
        a_tags = row.find_all('a', class_='bapp-label heading-4')
        for a_tag in a_tags:
            ext_url = a_tag.get('href')
            ext_name = a_tag.text
            extensions.append((f'{BASE_URL}{ext_url}', ext_name))

    # Use multiprocessing Pool for parallel execution
    with multiprocessing.Pool(processes=5) as pool:
        pool.map(process_extension, extensions)
