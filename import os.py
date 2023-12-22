import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def download_pdfs(base_url, save_folder):
    try:
        # Fetch the HTML content of the website
        response = requests.get(base_url)
        response.raise_for_status()

        # Parse the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find all links within elements with class "title" (assuming these are the links)
        article_links = soup.find_all('a', href=True)

        for link in article_links:
            if '/article/view/' in link['href']:
                article_url = urljoin(base_url, link['href'])
                print(f'Downloading article from URL: {article_url}')

                # Fetch the HTML content of the article page
                article_response = requests.get(article_url)
                article_response.raise_for_status()

                # Parse the HTML content of the article page
                article_soup = BeautifulSoup(article_response.text, 'html.parser')

                # Find the link to download (assuming it's a direct PDF link)
                pdf_link = article_soup.find('a', string='PDF', href=True)

                if pdf_link:
                    pdf_url = urljoin(article_url, pdf_link['href'])
                    print(f'Downloading PDF from URL: {pdf_url}')

                    # Download the PDF content
                    pdf_response = requests.get(pdf_url, allow_redirects=True)
                    pdf_response.raise_for_status()

                    # Extract the filename from the PDF URL
                    filename = os.path.join(save_folder, f'article_{link["href"].split("/")[-1]}.pdf')

                    # Save the PDF content to the file
                    with open(filename, 'wb') as pdf_file:
                        pdf_file.write(pdf_response.content)

                    print(f'Saved PDF to: {filename}')

    except requests.exceptions.HTTPError as http_err:
        print(f'HTTP error occurred while accessing {base_url}: {http_err}')

    except Exception as err:
        print(f'An error occurred while accessing {base_url}: {err}')

# Example usage
base_url = "https://mpaeds.my/journals/index.php/MJPCH/index"
save_folder = 'myjpch'

# Create the save folder if it doesn't exist
os.makedirs(save_folder, exist_ok=True)

download_pdfs(base_url, save_folder)
