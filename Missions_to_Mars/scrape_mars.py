import pandas as pd
from splinter import Browser
from bs4 import BeautifulSoup 
from webdriver_manager.chrome import ChromeDriverManager
import requests
import time

def init_browser():
    executable_path={'executable_path':ChromeDriverManager().install()}
    return Browser('chrome', **executable_path, headless=False)

mars_data = {}

def scrape_info():
    browser = init_browser()


    url='https://mars.nasa.gov/news/'
    browser.visit(url)

    html=browser.html
    soup=BeautifulSoup(html, 'html.parser')
    latest_news = soup.find_all('div', class_="list_text")

# Get the latest news    
    news = latest_news[0]
    news_title=news.find('div', class_="content_title").text
    news_p=soup.find('div', class_="article_teaser_body").text

    mars_data["news_title"] = news_title
    mars_data["news_p"] = news_p

#Featured Image
    base_url='https://www.jpl.nasa.gov/images/'
    base_1='https://www.jpl.nasa.gov'
    browser.visit(base_url)
    img_html=browser.html
    soup=BeautifulSoup(img_html, 'html.parser')
    latest_img = soup.find_all('div', class_="SearchResultCard")
    img=latest_img[0]
    latest=img.find('a')["href"]
    new_url=base_1+latest
    browser.visit(new_url)
    img_html=browser.html
    soup=BeautifulSoup(img_html, 'html.parser')
    large_image=soup.find_all('div', class_="BaseImagePlaceholder")
    large_img=large_image[0]
    full_size=large_img.find('img')["src"]

    mars_data["full_size"]=full_size

    #Mars Table

    facts_url='https://space-facts.com/mars/'
    browser.visit(facts_url)

    tables = pd.read_html(facts_url)

    Mars_facts=tables[0]

    Mars_facts.columns=['Description', 'Mars']
    Mars_facts.set_index('Description', inplace=True)

    mars_html=Mars_facts.to_html(classes='table table-striped')
    mars_html=mars_html.replace('<tr style="text-align: right;">','<tr style="text-align: left;">')

    mars_data["mars_html"]=mars_html

    #Hemisphere

    #Not working Link below
    hemisphere_url='https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    #hemisphere_url='https://webcache.googleusercontent.com/search?q=cache:Ljops39QW5MJ:https://astrogeology.usgs.gov/search/results%3Fq%3Dhemisphere%2Benhanced%26k1%3Dtarget%26v1%3DMars+&cd=2&hl=en&ct=clnk&gl=us'
    browser.visit(hemisphere_url)

    hem_url='https://astrogeology.usgs.gov'
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    hemisphere_image_urls = []
    results=soup.find_all('div',class_='item')
    for result in results:   
        hem=result.find('h3').text
        image=result.find('a')["href"]
        hem_url2=hem_url+image
        browser.visit(hem_url2)
        img_html=browser.html
        soup=BeautifulSoup(img_html, 'html.parser')
        image=soup.find('img', class_='wide-image')['src']
        new_url=hem_url+image
        hemis_dict = {"title": hem, "img_url":new_url}
        hemisphere_image_urls.append(hemis_dict)
         
        mars_data["hemisphere_image_urls"]=hemisphere_image_urls
    #mars_data={
        #"news_title": news_title,  
        #"news_p" : news_p,  
        #"full_size": full_size,
        #"mars_html": mars_html,
        #"hemisphere_image_urls": hemisphere_image_urls
        # }
    browser.quit()

    # Return results
    return mars_data