import os
import xml.etree.ElementTree as ET
import requests
from urllib.parse import urlparse

# Function to extract HTML content from a URL
def extract_html(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        else:
            print(f"Failed to fetch {url}: {response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return None

# Function to parse XML file and extract URLs
def extract_urls_from_xml(xml_file):
    urls = []
    try:
        tree = ET.parse(xml_file)
        root = tree.getroot()
        ns = {"ns": "http://www.sitemaps.org/schemas/sitemap/0.9"}
        for url in root.findall("ns:url/ns:loc", ns):
            urls.append(url.text.strip())
    except ET.ParseError as e:
        print(f"Error parsing XML file: {e}")
    return urls

# Function to save HTML content to a file
def save_html_to_file(html_content, file_path):
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(html_content)

# Main function to read XML file, extract URLs, fetch HTML content, and save to corresponding folders
def main(xml_file):
    urls = extract_urls_from_xml(xml_file)
    for url in urls:
        print(f"Extracting HTML content from {url}")
        html_content = extract_html(url)
        if html_content:
            # Create folder structure based on URL route
            parsed_url = urlparse(url)
            folder_path = os.path.join(*parsed_url.netloc.split("/"), *parsed_url.path.split("/")[:-1])
            os.makedirs(folder_path, exist_ok=True)  # Create folder if it doesn't exist
            file_name = "base.html" if not os.path.splitext(os.path.basename(parsed_url.path))[1] else os.path.basename(parsed_url.path)
            file_path = os.path.join(folder_path, file_name)
            save_html_to_file(html_content, file_path)
            print(f"HTML content saved to {file_path}")
        print("-" * 50)

# Example usage
if __name__ == "__main__":
    xml_file = "sitemap.xml" 
    main(xml_file)
