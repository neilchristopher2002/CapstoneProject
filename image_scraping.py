import requests
import urllib.request
import re
from bs4 import BeautifulSoup
import socket

# Set timeout 30 detik biar ga error
socket.setdefaulttimeout(30)

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
    path = 'D:\Kuliah\Bangkit\Capstone\CapstoneProject\Dataset\Cinnamon_5'
    image_index = 1 # Set index gambar biar berurutan

    while len(google_images) < num_images:
        parameter['start'] = start_index
        html = requests.get("https://www.google.com/search", params=parameter, headers=headers, timeout=30) # Tambah timeout
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

        for metadata, thumbnail, original in zip(
                soup.select('.isv-r.PNCib.MSM1fd.BUooTd'), thumbnails, full_res_images):
            google_images.append({
                "title": metadata.select_one(".VFACy.kGQAp.sMi44c.lNHeqe.WGvvNb")["title"],
                "link": metadata.select_one(".VFACy.kGQAp.sMi44c.lNHeqe.WGvvNb")["href"],
                "source": metadata.select_one(".fxgdke").text,
                "thumbnail": thumbnail,
                "original": original
            })

            print(f'Downloading {image_index} image...')

            try:
                # Implementasi timeout
                response = requests.get(original, timeout=30) # Tambah timeout
                with open(f'{path}\\cinnamon_{image_index}.jpg', 'wb') as file:
                    file.write(response.content)
            except requests.exceptions.RequestException as e:
                print('Error:', e)

            image_index += 1

            if len(google_images) == num_images:
                break

        start_index += 100

    print('end')
    return google_images

# Cleaning
def clean_data(data):
    cleaned_data = []
    unique_titles = set()

    for item in data:
        cleaned_item = {
            'title': item['title'],
            'link': item['link'],
            'source': item['source'],
            'thumbnail': item['thumbnail'],
            'original': item['original']
        }

        if cleaned_item['title'] not in unique_titles:
            cleaned_data.append(cleaned_item)
            unique_titles.add(cleaned_item['title'])

    for item in cleaned_data:
        print("Title:", item['title'])
        print("Link:", item['link'])
        print("Source:", item['source'])
        print("Thumbnail:", item['thumbnail'])
        print("Original:", item['original'])
        print()

    return cleaned_data


html = requests.get("https://www.google.com/search", params=parameter, headers=headers, timeout=30) # Tambah timeout
soup = BeautifulSoup(html.text, "lxml")

search_data(soup)

raw_data = get_image(headers, parameter)
cleaned_data = clean_data(raw_data)