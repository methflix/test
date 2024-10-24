#!/usr/bin/python
# -*-coding:utf8;-*-
#!/usr/bin/env python3
import urllib.request
import urllib.error
from bs4 import BeautifulSoup as bs
from time import sleep as slp
import requests as rq
from humanfriendly import format_timespan
import time
import subprocess
import base64
import ssl
import re
import os
import inquirer
from tqdm import tqdm
import argparse
from colorama import Fore, Style
clear = lambda: subprocess.call('cls||clear', shell=True)

# Start record processing time
begin_time = time.time()
headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'en-US,en;q=0.9',
    'priority': 'u=0, i',
    'sec-ch-ua': '"Google Chrome";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'none',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36'
}

cwd = os.getcwd()
art = '''
     ██╗ ░█████╗ ░██╗░░░██╗
     ██║ ██╔══██╗ ██║░░░██║
     ██║ ███████║ ╚██╗░██╔╝
██╗░██║█ █╔══ ██║░ ╚████╔╝░
╚█████╔╝ ██║░░██║ ░░╚██╔╝░░
░╚════╝░ ╚═╝░░╚═╝ ░░░╚═╝░░░
        scrapper0.4
            m3uEdition
'''

def center_text(text, width):
    lines = text.split('\n')
    centered_lines = [line.center(width) for line in lines]
    return '\n'.join(centered_lines)

width = 160  # Adjust width as needed
centered_art = center_text(art, width)
print(Fore.GREEN + centered_art + Style.RESET_ALL)

#####################################################################################

def main():
    parser = argparse.ArgumentParser(description='JAV Scrapper')
    parser.add_argument('site', choices=['ma', 'jg'], help='ma = MissAv.com, jg = JavGuru')
    parser.add_argument('mode', choices=['1', '2', '3'], help='Mode selection: 1 = Keyword Mode, 2 = Link Mode, 3 = Single Page Mode')
    parser.add_argument('--https_proxy', help='Optional HTTPS proxy in the format: https://user:pass@proxy:port')
    args = parser.parse_args()

    if args.site == "jg":
        return None

#MISSAV HERE
    if args.site == "ma":
        base_url = 'https://missav.com/'
        search = 'fil/search/'
        print(f"+INFO: Scrapping MissAv")

        if args.mode == "1":
            keyword = input(f'+ACTION: Enter your keyword: ')
            print(f'+INFO: Start fetching link with keyword :',keyword)
            begin_fetch_result_page = time.time()
            link = base_url + search + keyword
            req = urllib.request.Request(link, headers=headers)
            with urllib.request.urlopen(req) as response:
                fetch_content = response.read()
            soup = bs(fetch_content, "html.parser", from_encoding='utf-8')
            beginpage = 1
            lastpage_element = soup.find("span", {"class": "text-gray-500", "id": "price-currency"})
            if lastpage_element:
                    lastpage = int(lastpage_element.text.strip().split("/")[1].strip())
            else:
                lastpage = 1
            end_fetch_result_page = time.time() - begin_fetch_result_page
            print(Fore.GREEN + F'+INFO: Found total ' + str(lastpage) + ' page(s)' + Style.RESET_ALL)
            begin_fetch_movie_link = time.time()
            page_links = []
            movie_links = []
            count = movie = skip = 0
            if int(lastpage) > 1:
                for i in range(int(beginpage),int(lastpage + 1)):
                    url = ('{}{}{}?page={}'.format(base_url, search, keyword, i))
                    page_links.append(url)
            else:
                page_links.append(link)

        elif args.mode == "2":
            link_url = input("+ACTION: Enter URL: ")

            # Check if the URL ends with ?filters=individual
            if not (link_url.endswith("?filters=individual") or '?' not in link_url):
                print("Error: The URL must end with '?filters=individual' or not have any query string.")
                return

            print(f'+INFO: Start fetching pages with link:', link_url)
            req = urllib.request.Request(link_url, headers=headers)
            with urllib.request.urlopen(req) as response:
                print(response)
                fetch_content = response.read()
            soup = bs(fetch_content, "html.parser", from_encoding='utf-8')
            beginpage = 1
            lastpage_element = soup.find("span", {"class": "text-gray-500", "id": "price-currency"})
            if lastpage_element:
                    lastpage = int(lastpage_element.text.strip().split("/")[1].strip())
            else:
                lastpage = 1
            print(Fore.GREEN + f'+INFO: Found total ' + str(lastpage) + ' page(s)' + Style.RESET_ALL)
            print('+INFO: Extracting URLs from ' + str(lastpage) + ' page(s)')
            begin_fetch_movie_link = time.time()
            page_links = []
            movie_links = []
            count = movie = skip = 0
            base_url = '/'.join(link_url.split('/')[:-2])
            params1 = link_url.split('/')[-2]
            params2 = link_url.split('/')[-1].split('?')[0]  # Get the part before the query string

            if int(lastpage) > 1:
                for i in range(int(beginpage), int(lastpage + 1)):
                    # Append filters=individual only if the original URL does not have it
                    if link_url.endswith("?filters=individual"):
                        url = f'{base_url}/{params1}/{params2}?page={i}&filters=individual'
                    else:
                        url = f'{base_url}/{params1}/{params2}?page={i}'  # No filters
                    page_links.append(url)
            else:
                page_links.append(link_url)

        elif args.mode == "3":
            link_url = input("+ACTION: Enter URL: ")
            begin_fetch_result_page = time.time()
            req = urllib.request.Request(link_url, headers=headers)
            with urllib.request.urlopen(req, context=context) as response:
                fetch_content = response.read()
            soup = bs(fetch_content, "html.parser", from_encoding='utf-8')
            beginpage = 1
            lastpage = 1
            end_fetch_result_page = time.time() - begin_fetch_result_page
            print('+INFO: Extracting URLs from ' + str(lastpage) + ' page(s)')
            begin_fetch_movie_link = time.time()
            page_links = []
            movie_links = []
            count = movie = skip = 0
            if int(lastpage) > 1:
                base_url = '/'.join(link_url.split('/')[:-1])
                search = '/'.join(link_url.split('/')[-1:])
                for i in range(2, int(lastpage) + 1):
                    url = f'{base_url}/page/{i}/{search}'
                    page_links.append(url)
            else:
                page_links.append(link_url)

        for link in page_links:
            req = urllib.request.Request(link, headers=headers)
            with urllib.request.urlopen(req) as response:
                fetch_content = response.read()
            soup = bs(fetch_content, "html.parser")
            movie_divs = soup.find_all("div", {"class": "thumbnail group"})
            for div in movie_divs:
                link = div.find("a")['href']
                movie_links.append(link)

        end_fetch_movie_link = time.time() - begin_fetch_movie_link
        print(Fore.GREEN + f'+INFO: Found total '+ str(len(movie_links)) + ' url(s)' + Style.RESET_ALL)

        total_urls = len(movie_links)
        m3u_link = []
        for index, link in enumerate(tqdm(movie_links, desc="+INFO: Processing", total=total_urls), start=1):
            begin_scraping = time.time()
            try:
                true_title = link.split("/")[-1]
                req = urllib.request.Request(link, headers=headers)
                with urllib.request.urlopen(req) as response:
                    fetch_content = response.read()
                soup = bs(fetch_content, "html.parser", from_encoding='utf-8')
                script_tags = soup.find_all("script", {"type": "text/javascript"})
                if len(script_tags) >= 3:
                    script_text = script_tags[2].get_text()  # Extract the text of the third script tag (index 2)
                    uuid_pattern = r'[\da-f]{8}-[\da-f]{4}-[\da-f]{4}-[\da-f]{4}-[\da-f]{12}'
                    uuid_match = re.search(uuid_pattern, script_text)
                    if uuid_match:
                        uuid = uuid_match.group()  # Extract the matched UUID
                        m3u8 = f'https://surrit.com/{uuid}/playlist.m3u8'
                        m3u_link.append({'title': true_title, 'url': m3u8})
                end_scraping = time.time()
            except Exception as e:
                tqdm.write(f'Error scraping: {e}')
        print(Fore.GREEN + f'+INFO: Extracted '+ str(len(m3u_link)) + ' url(s)' + Style.RESET_ALL)

        # Define the download folder path
        download_folder_name = "/media/Backup/others/missav/"
        downloads_folder = os.path.join(download_folder_name)

        # Ensure the download directory exists
        if not os.path.exists(downloads_folder):
            os.makedirs(downloads_folder)

        # Path to the download log file
        log_file_path = '/home/meth/script/download_log.txt'

        # Read already downloaded titles from the log file
        if os.path.exists(log_file_path):
            with open(log_file_path, 'r') as log_file:
                downloaded_titles = {line.strip() for line in log_file}
        else:
            downloaded_titles = set()

        # Keywords to exclude
        exclude_keywords = ['uncensored-leak', 'chinese-subtitle']

        # Define the full path to the N_m3u8DL-RE executable
        n_m3u8dl_re_path = '/home/meth/script/N_m3u8DL-RE'

        if m3u_link:
            true_titles = [
                item['title'] for item in m3u_link
                if not any(keyword in item['title'] for keyword in exclude_keywords) and item['title'] not in downloaded_titles  # Exclude titles containing any of the keywords and already downloaded titles
            ]
            questions = [
                inquirer.Checkbox('titles',
                                message="Select titles to download",
                                choices=true_titles,
                                default=true_titles,
                                ),
            ]
            answers = inquirer.prompt(questions)
            selected_titles = answers['titles']

            # Log the downloaded titles
            with open(log_file_path, 'a') as log_file:
                for title in selected_titles:
                    log_file.write(f"{title}\n")

            with tqdm(total=len(selected_titles), desc="+INFO: Downloading") as pbar:
                for title in selected_titles:
                    for item in m3u_link:
                        if item['title'] == title:
                            extracted_url = item['url']
                            try:
                                process = subprocess.Popen([
                                    n_m3u8dl_re_path,  # Use the full path here
                                    f'{extracted_url}',
                                    '--log-level', 'ERROR',
                                    '-M', 'format=mkv:muxer=mkvmerge',
                                    '-H', 'origin: https://missav.com',
                                    '--binary-merge',
                                    '--live-perform-as-vod', 'True',
                                    '--live-real-time-merge',
                                    '--no-date-info', 'True',
                                    '--del-after-done',
                                    '-sa', 'best',
                                    '-sv', 'best',
                                    '--save-dir', downloads_folder,
                                    '--save-name', f'"{title}"',
                                    '-mt', 'TRUE'
                                ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                                for line in process.stdout:
                                    pass

                                for line in process.stderr:
                                    print(line.decode().strip())

                            except Exception as e:
                                print(f"Error occurred while downloading {title}: {e}")
                    pbar.update(1)
        else:
            print("No m3u links found to download.")
if __name__ == "__main__":
    main()
