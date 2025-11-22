import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

CSS_DIR = 'css'


def ensure_dir(path: str) -> str:
    os.makedirs(path, exist_ok=True)
    return path


def filename_from_url(url: str, fallback: str = 'style.css') -> str:
    parsed = urlparse(url)
    name = os.path.basename(parsed.path)
    return name or fallback


def download_css(url: str, folder: str) -> str:
    ensure_dir(folder)
    destination = os.path.join(folder, filename_from_url(url, 'style.css'))

    if os.path.exists(destination):
        return destination

    resp = requests.get(url)
    resp.raise_for_status()

    with open(destination, 'wb') as f:
        f.write(resp.content)

    print(f"[CSS] Saved {url} -> {destination}")
    return destination


def download_landing_page(url: str, output_filename: str) -> None:
    ensure_dir(CSS_DIR)

    resp = requests.get(url)
    resp.raise_for_status()

    soup = BeautifulSoup(resp.text, 'html.parser')

    # Collect CSS links, download them, then strip all external assets and scripts
    css_links = soup.find_all('link', rel='stylesheet')
    for link in css_links:
        href = link.get('href')
        if href:
            download_css(urljoin(url, href), CSS_DIR)
        link.decompose()

    for tag in soup.find_all(['script', 'style', 'link']):
        tag.decompose()

    html_content = soup.prettify()
    with open(output_filename, 'w', encoding='utf-8') as f:
        f.write(html_content)

    print(f"Saved HTML of {url} -> {output_filename}")


if __name__ == '__main__':
    url = 'https://cocosolis.com/bg/'
    output_file = 'cocosolis_bg_landing.html'
    download_landing_page(url, output_file)
