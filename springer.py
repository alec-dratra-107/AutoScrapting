import requests
from requests.exceptions import RequestException

from bs4 import BeautifulSoup

import os
import re

import urllib.parse
from urllib.parse import urlparse
from urllib.parse import urljoin

cookies = {
    'idp_session': 'sVERSION_1ca5aced8-214f-41e5-9e4d-e55a6cf8b186',
    'idp_session_http': 'hVERSION_19d0be7e2-9dac-4037-beef-64101c9d83e5',
    'idp_marker': '31540fc4-6eca-4bd4-98a2-d7b1d55c92e9',
    'user.uuid.v2': '"e8286aa4-01c6-4405-8078-4f981d6da898"',
    'sncc': 'P%3D17%3AV%3D57.0.0%26C%3DC01%2CC02%2CC03%2CC04%26D%3Dtrue',
    '_ga': 'GA1.1.698258708.1746925157',
    'permutive-id': 'a97bcd28-1d68-4ead-8ecf-79c3926d40cf',
    'trackid': '"mh4cgj494zt31jqt4zcjd60r3"',
    'ajs_anonymous_id': 'fcfb98d4-6404-4e48-89ad-47e12c4eb9a1',
    'optimizelyEndUserId': 'oeu1746925495360r0.052291082820738466',
    '__gads': 'ID=a2575d57b92f1292:T=1746925374:RT=1746925374:S=ALNI_MbdGFZbDi6UPrstkJpSJprjpgrcwA',
    '__gpi': 'UID=000010a943fa9c80:T=1746925374:RT=1746925374:S=ALNI_MY8ueweqrIRME_HC057AcMYM85iJw',
    '__eoi': 'ID=db58186e17f6394f:T=1746925374:RT=1746925374:S=AA-AfjYebvmABAyZkIze7qDTjWkD',
    '_hjSessionUser_5176038': 'eyJpZCI6ImY5NjQ0MGNhLWY1YzgtNWUyNS1hN2E2LWY4Zjc5MTJjNjdkYSIsImNyZWF0ZWQiOjE3NDY5MjUxNjM3MjUsImV4aXN0aW5nIjp0cnVlfQ==',
    '_fbp': 'fb.1.1747028279864.898122418226924071',
    'sim-inst-token': '""',
    '_hjSession_5176038': 'eyJpZCI6IjE2Mjk0ZTI3LTlkNjAtNGY5NS1hNzMyLTc4YWY2ZjJlYzM0MiIsImMiOjE3NDcwMjkwNDkxNDYsInMiOjAsInIiOjAsInNiIjowLCJzciI6MCwic2UiOjAsImZzIjowLCJzcCI6MX0=',
    'cto_bundle': 'm9EFRV91N3RBWk1nMkhPUXBza1pMZEs2JTJGTGdQT3FVSUl6dWxWU0FHb3VxanplRzJTeXV5WjN3TGRzJTJGWVQxMWxzaFhRNm1idkl6dXVwaDJkJTJGdzkyQyUyRjQ1YjlFN1VCbzVOU0t3NSUyRldKTklRRVJwY0s4c09uQk94YTh6M05ONlJUZU1Pd3Q5aCUyRjhWSG01UHd6eHMyVGclMkJWUHBweE5vV09JJTJGWkdJQ0VBczJ2Q3RDT3djJTNE',
    'permutive-session': '%7B%22session_id%22%3A%22e544df0b-3a6f-4650-a672-1b600db30181%22%2C%22last_updated%22%3A%222025-05-12T05%3A55%3A30.636Z%22%7D',
    '_ga_B3E4QL2TPR': 'GS2.1.s1747028275$o6$g1$t1747029330$j53$l0$h0',
    '_ga_5V24HQ1XD5': 'GS2.1.s1747028278$o6$g1$t1747029330$j0$l0$h0',
    'amp_72dea4': 'pcCI3O4-t8sgAtEkyt9WZ1...1ir1g00ag.1ir1h02s6.4c.5.4h',
    '_uetsid': '2bb014102e0311f0b89f6199da8db2da',
    '_uetvid': '2bb03e002e0311f097d225feffcda80f',
}

headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'en-US,en;q=0.9',
    'cache-control': 'max-age=0',
    'priority': 'u=0, i',
    'referer': 'https://link.springer.com/search?new-search=true&query=ocean+energt',
    'sec-ch-ua': '"Chromium";v="136", "Google Chrome";v="136", "Not.A/Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36',
    # 'cookie': 'idp_session=sVERSION_1ca5aced8-214f-41e5-9e4d-e55a6cf8b186; idp_session_http=hVERSION_19d0be7e2-9dac-4037-beef-64101c9d83e5; idp_marker=31540fc4-6eca-4bd4-98a2-d7b1d55c92e9; user.uuid.v2="e8286aa4-01c6-4405-8078-4f981d6da898"; sncc=P%3D17%3AV%3D57.0.0%26C%3DC01%2CC02%2CC03%2CC04%26D%3Dtrue; _ga=GA1.1.698258708.1746925157; permutive-id=a97bcd28-1d68-4ead-8ecf-79c3926d40cf; trackid="mh4cgj494zt31jqt4zcjd60r3"; ajs_anonymous_id=fcfb98d4-6404-4e48-89ad-47e12c4eb9a1; optimizelyEndUserId=oeu1746925495360r0.052291082820738466; __gads=ID=a2575d57b92f1292:T=1746925374:RT=1746925374:S=ALNI_MbdGFZbDi6UPrstkJpSJprjpgrcwA; __gpi=UID=000010a943fa9c80:T=1746925374:RT=1746925374:S=ALNI_MY8ueweqrIRME_HC057AcMYM85iJw; __eoi=ID=db58186e17f6394f:T=1746925374:RT=1746925374:S=AA-AfjYebvmABAyZkIze7qDTjWkD; _hjSessionUser_5176038=eyJpZCI6ImY5NjQ0MGNhLWY1YzgtNWUyNS1hN2E2LWY4Zjc5MTJjNjdkYSIsImNyZWF0ZWQiOjE3NDY5MjUxNjM3MjUsImV4aXN0aW5nIjp0cnVlfQ==; _fbp=fb.1.1747028279864.898122418226924071; sim-inst-token=""; _hjSession_5176038=eyJpZCI6IjE2Mjk0ZTI3LTlkNjAtNGY5NS1hNzMyLTc4YWY2ZjJlYzM0MiIsImMiOjE3NDcwMjkwNDkxNDYsInMiOjAsInIiOjAsInNiIjowLCJzciI6MCwic2UiOjAsImZzIjowLCJzcCI6MX0=; cto_bundle=m9EFRV91N3RBWk1nMkhPUXBza1pMZEs2JTJGTGdQT3FVSUl6dWxWU0FHb3VxanplRzJTeXV5WjN3TGRzJTJGWVQxMWxzaFhRNm1idkl6dXVwaDJkJTJGdzkyQyUyRjQ1YjlFN1VCbzVOU0t3NSUyRldKTklRRVJwY0s4c09uQk94YTh6M05ONlJUZU1Pd3Q5aCUyRjhWSG01UHd6eHMyVGclMkJWUHBweE5vV09JJTJGWkdJQ0VBczJ2Q3RDT3djJTNE; permutive-session=%7B%22session_id%22%3A%22e544df0b-3a6f-4650-a672-1b600db30181%22%2C%22last_updated%22%3A%222025-05-12T05%3A55%3A30.636Z%22%7D; _ga_B3E4QL2TPR=GS2.1.s1747028275$o6$g1$t1747029330$j53$l0$h0; _ga_5V24HQ1XD5=GS2.1.s1747028278$o6$g1$t1747029330$j0$l0$h0; amp_72dea4=pcCI3O4-t8sgAtEkyt9WZ1...1ir1g00ag.1ir1h02s6.4c.5.4h; _uetsid=2bb014102e0311f0b89f6199da8db2da; _uetvid=2bb03e002e0311f097d225feffcda80f',
}

session = requests.Session()

BASE_URL = "https://link.springer.com"

def search_springer(query, page):
    # search_url = f'https://link.springer.com/search?new-search=true&query={query.replace(' ', '+')}&content-type=article&content-type=research&content-type=review&content-type=news&sortBy=relevance&page={page}'
    search_url = f'https://link.springer.com/search?new-search=true&query={query.replace(' ', '+')}&content-type=Article&sortBy=relevance&page={page}'
    # search_url = f'https://link.springer.com/search?new-search=true&query={query.replace(' ', '+')}&content-type=Article&language=En&date=custom&dateFrom=2020&dateTo=2025&sortBy=relevance&page={page}'
    # search_url = f'https://link.springer.com/search?new-search=true&query={query.replace(' ', '+')}&content-type=Article&facet-discipline=%22Life+Sciences%22&facet-discipline=%22Environment%22&facet-discipline=%22Engineering%22&facet-discipline=%22Computer+Science%22&facet-discipline=%22Geography%22&facet-discipline=%22Economics%22&facet-discipline=%22Materials+Science%22&facet-discipline=%22Energy%22&date=custom&dateFrom=2015&dateTo=2020&sortBy=relevance&page={page}'
    # search_url = f'https://link.springer.com/search?new-search=true&query={query.replace(' ', '+')}&content-type=Article&facet-sub-discipline=%22Agriculture%22&facet-sub-discipline=%22Plant+Sciences%22&facet-sub-discipline=%22Ecology%22&facet-sub-discipline=%22Plant+Pathology%22&facet-sub-discipline=%22Plant+Physiology%22&facet-sub-discipline=%22Plant+Genetics+and+Genomics%22&facet-sub-discipline=%22Ecotoxicology%22&facet-sub-discipline=%22Monitoring%2FEnvironmental+Analysis%22&facet-sub-discipline=%22Biotechnology%22&taxonomy=%22Agriculture%22&taxonomy=%22Agronomy%22&taxonomy=%22Plant+Pathology%22&taxonomy=%22Agricultural+Geography%22&taxonomy=%22Plant+Biotechnology%22&taxonomy=%22Subsistence+Agriculture%22&taxonomy=%22Plant+Science%22&taxonomy=%22Agroecology%22&taxonomy=%22Agricultural+Biotechnology%22&taxonomy=%22Organic+Farming%22&taxonomy=%22Environmental+Impact%22&taxonomy=%22Agricultural+Economics%22&date=custom&dateFrom=2020&dateTo=2025&sortBy=relevance&page={page}'
    # search_url = f'https://link.springer.com/search?new-search=true&query={query.replace(' ', '+')}&content-type=Article&advancedSearch=true&title=%22disease%22+OR+%22pest%22&date=custom&dateFrom=2015&dateTo=2025&sortBy=relevance&page={page}'
    
    try:
        response = session.get(
            search_url, 
            cookies=cookies,
            headers=headers,
        )
        soup = BeautifulSoup(response.text, 'html.parser')

        results = []
        articles = soup.select("li.app-card-open")

        # articles = soup.select("h3.app-card-open__heading")
        if len(articles):
            for article_info in articles:
                if len(article_info.select('svg.app-entitlement__icon--full-access')) == 0:
                    continue

                article = article_info.select_one('h3.app-card-open__heading')
                title_tag = article.find('a', class_="app-card-open__link")
                if title_tag:
                    title = title_tag.text.strip()
                    detail_link = title_tag.get('href')
                    download_link = f'https://link.springer.com/content/pdf/{detail_link.split('/article/')[1]}.pdf'
                    # if txt == "Download PDF":
                    #     print(download_link)
                    results.append((title, download_link))
                    # # /article/
                    # try:
                    #     response = session.get(
                    #         detail_page_url,
                    #         cookies=cookies,
                    #         headers=headers,
                    #     )
                    #     soup = BeautifulSoup(response.text, 'html.parser')

                    #     parent_tag = soup.find('div', class_="c-pdf-container")
                    #     child_tag = parent_tag.find('div', class_="c-pdf-download")

                    #     download_buttion_tag = child_tag.find('a', class_="u-button")
                    #     if download_buttion_tag:
                    #         span_tag = download_buttion_tag.find('span', class_="c-pdf-download__text")
                    #         if span_tag:
                    #             txt = span_tag.text.strip()
                    #             download_link = BASE_URL + download_buttion_tag.get('href')
                    #             if txt == "Download PDF":
                    #                 print(download_link)
                    #                 results.append((title, download_link))
                    # except requests.exceptions.Timeout as e:
                    #     print("\ntime exceed error: ", e)
                    # except requests.ConnectTimeout as e:
                    #     print("\nconnenction time exceed error: ", e)
                    # except requests.ReadTimeout as e:
                    #     print("\nread time exceed error: ", e)
                    # except requests.exceptions.RequestException as e:
                    #     print("\nrequest error: ", e)
                    # except Exception as e:
                    #     print("\nglobal error: ", e)
                    # except KeyboardInterrupt:
                    #     print("\nprogram stopped because of Ctrl+C.")
    except requests.exceptions.Timeout as e:
        print("\ntime exceed error: ", e)
    except requests.ConnectTimeout as e:
        print("\nconnenction time exceed error: ", e)
    except requests.ReadTimeout as e:
        print("\nread time exceed error: ", e)
    except requests.exceptions.RequestException as e:
        print("\nrequest error: ", e)
    except Exception as e:
        print("\nglobal error: ", e)
    except KeyboardInterrupt:
        print("\nprogram stopped because of Ctrl+C.")

    return results

def download_pdf(title, download_link, save_folder):
    """PDF download"""
    try:
        # filename = re.sub(r'[\\/*?:"<>|]', "", title.string.split("|")[0].strip()) + ".pdf"
        filename = os.path.basename(urlparse(download_link).path)
        os.makedirs(save_folder, exist_ok=True)
        filepath = os.path.join(save_folder, filename)

        filepath1 = os.path.join('Biodynamic cultivation', filename)
        filepath2 = os.path.join('Mycorrhizal inoculation techniques', filename)
        filepath3 = os.path.join('Hydroponic essential oil crops', filename)
        filepath4 = os.path.join('Precision aromatic agriculture', filename)

        if os.path.isfile(filepath1) or os.path.isfile(filepath2) or os.path.isfile(filepath3)or os.path.isfile(filepath4):
            print(f"ℹ️ this file was already downloaded: {filename}")
        else:
            pdf_response = session.get(
                download_link,
                cookies=cookies,
                headers=headers,
            )
            content_type = pdf_response.headers.get('Content-Type', '')
            print('content_type =>', content_type)
            
            if 'application/pdf' in content_type.lower():
                with open(filepath, 'wb') as f:
                    f.write(pdf_response.content)

            print(f"✅ download finished: {filename}")
    except requests.exceptions.Timeout as e:
        print("\ntime exceed error: ", e)
    except requests.ConnectTimeout as e:
        print("\nconnection time exceed error: ", e)
    except requests.ReadTimeout as e:
        print("\nread time exceed error: ", e)
    except requests.exceptions.RequestException as e:
        print("\nrequest error: ", e)
    except Exception as e:
        print("\nglobal error: ", e)
    except KeyboardInterrupt:
        print("\nprogram stopped because of Ctrl+C.")

def main():
    query = input("input a keyword to search: ")
    page_count = input("input search result page count: ")
    for page in range(1, int(page_count) + 1):
        results = search_springer(query, page)
        if not results:
            print(f"{page}Page: 🔍 Cannot find open-access file.")
            continue

        print(f"\n{page}Page: 🔎 Start download searched PDF file...\n")
        for title, link in results:
            print(f"➡ Doc: {title}")
            download_pdf(title, link, "Precision aromatic agriculture")

if __name__ == "__main__":
    main()
