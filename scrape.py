import urllib.request
from serpapi import GoogleSearch
import json
import ssl
import socket

def get_image():
    image_res = []

    spice = ['fresh cardamom']

    for query in spice:
        parameter = {
            "engine": "google",
            'q': query,
            'tbm': 'isch',
            'num': 100,
            'start': 0,
            'ijn': 0,
            'api_key': '7099757cf368b9d19cf48cca874cd3694adaa20d670c2b7e10beb96a1d6fb155'
        }

        search = GoogleSearch(parameter)
        flag = True
        while flag:
            results = search.get_dict()

            if 'error' not in results:
                for img in results['images_results']:
                    if img['original'] not in image_res:
                        image_res.append(img['original'])
                parameter['ijn'] += 1
            else:
                print(results['error'])
                flag = False

    for index, image in enumerate(image_res, start=1):
        print(f'Downloading {index} image...')
        
        opener = urllib.request.build_opener()
        opener.addheaders = [("User-Agent","Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.114 Safari/537.36")]
        urllib.request.install_opener(opener)

        filename = f'cardamom{index}.jpg'

        try:
            with urllib.request.urlopen(image, timeout=30) as response:
                with open(f'Data2/Cardamom/{filename}', 'wb') as out_file:
                    out_file.write(response.read())
                    print(f'Downloaded {index} image.')
        except (urllib.error.URLError, socket.timeout) as e:
            print(f'Error downloading {index} image: {str(e)}')
            continue

    print(json.dumps(image_res, indent=2))
    print(len(image_res))

# Disable SSL certificate verification
ssl._create_default_https_context = ssl._create_unverified_context

get_image()
