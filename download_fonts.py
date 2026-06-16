import urllib.request
import os

def download_fonts():
    fonts = {
        "Cairo-Regular.ttf": "https://cdn.jsdelivr.net/gh/Gue3bara/Cairo@master/fonts/ttf/Cairo-Regular.ttf",
        "Cairo-Bold.ttf": "https://cdn.jsdelivr.net/gh/Gue3bara/Cairo@master/fonts/ttf/Cairo-Bold.ttf"
    }

    os.makedirs("assets/fonts", exist_ok=True)

    for name, url in fonts.items():
        path = os.path.join("assets/fonts", name)
        print(f"Downloading {name} from {url}...")
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req) as response, open(path, 'wb') as out_file:
                out_file.write(response.read())
            print(f"Successfully downloaded {name}")
        except Exception as e:
            print(f"Failed to download {name}: {e}")

if __name__ == "__main__":
    download_fonts()
