import requests
from bs4 import BeautifulSoup
import re

def save_to_file(items, filename):
    with open(filename, 'w') as f:
        for item in items:
            f.write(item + '\n')

def scrape_website(url, save_links, save_emails, save_pdf, save_xlsx, save_phone_numbers):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    scraped_links = []
    scraped_emails = []
    scraped_pdf = []
    scraped_xlsx = []
    scraped_phone_numbers = []

    if save_links:
        for link in soup.find_all('a', href=True):
            href = link['href']
            if href.startswith('http') or href.startswith('https'):
                scraped_links.append(href)
        save_to_file(scraped_links, 'links.txt')
        print(f'Scraped {len(scraped_links)} links')

    if save_emails:
        emails = re.findall(r'\S+@\S+', soup.get_text())
        scraped_emails.extend(emails)
        save_to_file(scraped_emails, 'emails.txt')
        print(f'Scraped {len(scraped_emails)} emails')

    if save_pdf:
        for link in soup.find_all('a', href=True):
            href = link['href']
            if href.endswith('.pdf'):
                scraped_pdf.append(href)
                pdf_response = requests.get(href)
                with open(href.split('/')[-1], 'wb') as f:
                    f.write(pdf_response.content)
        save_to_file(scraped_pdf, 'pdf_links.txt')
        print(f'Scraped {len(scraped_pdf)} PDF files')

    if save_xlsx:
        for link in soup.find_all('a', href=True):
            href = link['href']
            if href.endswith('.xlsx'):
                scraped_xlsx.append(href)
                xlsx_response = requests.get(href)
                with open(href.split('/')[-1], 'wb') as f:
                    f.write(xlsx_response.content)
        save_to_file(scraped_xlsx, 'xlsx_links.txt')
        print(f'Scraped {len(scraped_xlsx)} XLSX files')

    if save_phone_numbers:
        phone_numbers = re.findall(r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b', soup.get_text())
        scraped_phone_numbers.extend(phone_numbers)
        save_to_file(scraped_phone_numbers, 'phone_numbers.txt')
        print(f'Scraped {len(scraped_phone_numbers)} phone numbers')


if __name__ == '__main__':
    print('''
         __   ______                              
   _____/ /__/ ____/_______  ___  ____  ___  _____
  / ___/ //_/ /   / ___/ _ \/ _ \/ __ \/ _ \/ ___/
 (__  ) ,< / /___/ /  /  __/  __/ /_/ /  __/ /    
/____/_/|_|\____/_/   \___/\___/ .___/\___/_/     
                              /_/    
            written by virtuoso :)             
    ''')
    url = input('Enter the website URL: ')
    save_links = input('Scrape links? (y/n): ').lower() == 'y'
    save_emails = input('Scrape emails? (y/n): ').lower() == 'y'
    save_pdf = input('Scrape PDF files? (y/n): ').lower() == 'y'
    save_xlsx = input('Scrape XLSX files? (y/n): ').lower() == 'y'
    save_phone_numbers = input('Scrape phone numbers? (y/n): ').lower() == 'y'

    scrape_website(url, save_links, save_emails, save_pdf, save_xlsx, save_phone_numbers)
