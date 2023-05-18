import requests
import urllib.request
import re
from bs4 import BeautifulSoup

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.114 Safari/537.36"
}

spice = 'cinnamon stick'
parameter = {
    'q': spice,
    'tbm': 'isch',
    'num': '100',
    'start': 0,
    'ijn': '0' 
}


def search_data(soup):
    suggested_searches = []
    all_script_tags = soup.select('script')
    matched_images = "".join(re.findall(r"AF_initDataCallback\(({key: 'ds:1'.*?)\);</script>", str(all_script_tags)))

    suggested_search_thumbnails = ",".join(re.findall(r'{key(.*?)\[null,\"Size\"', matched_images))
    suggested_search_thumbnail_encoded = re.findall(r'\"(https:\/\/encrypted.*?)\"', suggested_search_thumbnails)

    for suggested_search, suggested_search_fixed_thumbnail in zip(
            soup.select(".PKhmud.sc-it.tzVsfd"), suggested_search_thumbnail_encoded):
        suggested_searches.append({
            "name": suggested_search.select_one(".VlHyHc").text,
            "link": f"https://www.google.com{suggested_search.a['href']}",
            "chips": "".join(re.findall(r"&chips=(.*?)&", suggested_search.a["href"])),
            "thumbnail": bytes(suggested_search_fixed_thumbnail, "ascii").decode("unicode-escape")
        })
    print('start')
    return suggested_searches


def get_image(headers, parameter):
    google_images = []
    num_images = 100
    start_index = 0
    path = 'C:\\Users\\Christopher\\Downloads\\Capstone\\Dataset\\Test'

    while len(google_images) < num_images:
        parameter['start'] = start_index
        html = requests.get("https://www.google.com/search", params=parameter, headers=headers, timeout=30)
        soup = BeautifulSoup(html.text, "lxml")
        
        all_script_tags = soup.select('script')
        matched_images_data = "".join(re.findall(r"AF_initDataCallback\(([^<]+)\);", str(all_script_tags)))
        matched_google_image_data = re.findall(r'\"b-GRID_STATE0\"(.*)sideChannel:\s?{}}', matched_images_data)
        matched_google_images_thumbnails = ", ".join(
            re.findall(r'\[\"(https\:\/\/encrypted-tbn0\.gstatic\.com\/images\?.*?)\",\d+,\d+\]',
                       str(matched_google_image_data))).split(", ")
        thumbnails = [
            bytes(bytes(thumbnail, "ascii").decode("unicode-escape"), "ascii").decode("unicode-escape") for thumbnail in
            matched_google_images_thumbnails
        ]

        removed_matched_google_images_thumbnails = re.sub(
            r'\[\"(https\:\/\/encrypted-tbn0\.gstatic\.com\/images\?.*?)\",\d+,\d+\]', "",
            str(matched_google_image_data))
        matched_google_full_resolution_images = re.findall(r"(?:'|,),\[\"(https:|http.*?)\",\d+,\d+\]",
                                                           removed_matched_google_images_thumbnails)

        full_res_images = [
            bytes(bytes(img, "ascii").decode("unicode-escape"), "ascii").decode("unicode-escape") for img in
            matched_google_full_resolution_images
        ]

        for index, (metadata, thumbnail, original) in enumerate(
                zip(soup.select('.isv-r.PNCib.MSM1fd.BUooTd'), thumbnails, full_res_images), start=start_index + 1):
            google_images.append({
                "title": metadata.select_one(".VFACy.kGQAp.sMi44c.lNHeqe.WGvvNb")["title"],
                "link": metadata.select_one(".VFACy.kGQAp.sMi44c.lNHeqe.WGvvNb")["href"],
                "source": metadata.select_one(".fxgdke").text,
                "thumbnail": thumbnail,
                "original": original
            })
            print(f'Downloading {index} image...')

            opener = urllib.request.build_opener()
            opener.addheaders = [('User-Agent',
                                  'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36')]
            urllib.request.install_opener(opener)

            try: 
                urllib.request.urlretrieve(original, f'{path}\\cinnamon_{index}.jpg')
            except:
                print('error')
            
            if len(google_images) == num_images:
                break

        start_index += 100

    print('end')
    return google_images


html = requests.get("https://www.google.com/search", params=parameter, headers=headers, timeout=30)
soup = BeautifulSoup(html.text, "lxml")

search_data(soup)
get_image(headers, parameter)