from bs4 import BeautifulSoup
import requests
from webdriver_manager.chrome import ChromeDriverManager
from splinter import Browser
from selenium import webdriver
import pandas as pd

def init_browser():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    return Browser('chrome', **executable_path, headless=False)


def scrape():
    #Mars News Headline and Description
    url = 'https://mars.nasa.gov/news/'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    news_header = soup.find('div', class_='content_title').text
    news_paragraph = soup.find('div', class_='rollover_description_inner').text

    #Featured Image
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)
    url = 'https://spaceimages-mars.com/'
    browser.visit(url)
    browser.links.find_by_partial_text('FULL').click()
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    feature_img_url = soup.find('img', class_='fancybox-image').get('src')
    feature_img_url = url + feature_img_url
    browser.quit()

    #Mars Facts
    table_url = 'https://space-facts.com/mars/'
    tables = pd.read_html(table_url)
    mars_df = tables[1]
    html_table = mars_df.to_html()
    html_table.replace('\n', '')

    #Mars Hemispheres
    mars_url = "https://marshemispheres.com/"
    hemisphere_urls = []
    response = requests.get(mars_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    link_m = soup.find_all('a', class_='itemLink product-item')

    for i in range(0, len(link_m)-1, 2):    
        link = link_m[i]['href']
        link_full = mars_url + link
        hemisphere_urls.append(link_full)
    
    #Visit hemisphere_urls and save image urls and title
    img_url_full = ""
    hemisphere_image_urls = {"img_url": [], "title": []}
    hemisphere_names = []
    hemisphere_images = []
    for url in hemisphere_urls:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        title = soup.find('h2', class_='title').text
        image_url = soup.find('div', class_='downloads').a['href']
        image_url_full = mars_url + image_url
        hemisphere_images.append(image_url_full)
        hemisphere_image_urls["title"].append(title)
        hemisphere_image_urls["img_url"].append(image_url_full)
    
    info = {"news_header": news_header,
        "news_paragraph": news_paragraph,
        "feature_img_url": feature_img_url,
        "hemisphere_image_urls": hemisphere_image_urls,
        "html_table": html_table
    }
    
    return info

