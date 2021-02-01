{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "import pandas as pd\n",
    "from splinter import Browser\n",
    "from bs4 import BeautifulSoup \n",
    "from webdriver_manager.chrome import ChromeDriverManager\n",
    "import requests"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {
    "scrolled": true
   },
   "outputs": [],
   "source": [
    "executable_path={'executable_path':ChromeDriverManager().install()}\n",
    "browser=Browser('chrome', **executable_path, headless=False)"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "#NASA Mars News"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "url='https://mars.nasa.gov/news/'\n",
    "browser.visit(url)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "html=browser.html\n",
    "soup=BeautifulSoup(html, 'html.parser')\n",
    "latest_news = soup.find_all('div', class_=\"list_text\")\n",
    "\n",
    "# Get the latest news    \n",
    "news = latest_news[0]\n",
    "news_title=news.find('div', class_=\"content_title\").text\n",
    "\n",
    "print(news_title)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "news_p=soup.find('div', class_=\"article_teaser_body\").text\n",
    "print(news_p)"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "#JPL Mars Space Images - Featured Image"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "base_url='https://www.jpl.nasa.gov/images/'\n",
    "base_1='https://www.jpl.nasa.gov'\n",
    "browser.visit(base_url)\n",
    "img_html=browser.html\n",
    "soup=BeautifulSoup(img_html, 'html.parser')\n",
    "latest_img = soup.find_all('div', class_=\"SearchResultCard\")\n",
    "img=latest_img[0]\n",
    "latest=img.find('a')[\"href\"]\n",
    "new_url=base_1+latest\n",
    "browser.visit(new_url)\n",
    "img_html=browser.html\n",
    "soup=BeautifulSoup(img_html, 'html.parser')\n",
    "large_image=soup.find_all('div', class_=\"BaseImagePlaceholder\")\n",
    "large_img=large_image[0]\n",
    "full_size=large_img.find('img')[\"src\"]\n",
    "print(full_size)"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "#MARS Facts "
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "facts_url='https://space-facts.com/mars/'\n",
    "browser.visit(facts_url)\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "tables = pd.read_html(facts_url)\n",
    "tables"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "Mars_facts=tables[0]\n",
    "Mars_facts"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "Mars_facts.columns=['Description', 'Mars']\n",
    "Mars_facts.set_index('Description', inplace=True)\n",
    "Mars_facts"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {
    "scrolled": true
   },
   "outputs": [],
   "source": [
    "mars_html=Mars_facts.to_html()\n",
    "mars_html"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "#Mars Hemispheres"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "hemisphere_url='https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'\n",
    "browser.visit(hemisphere_url)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "hem_url='https://astrogeology.usgs.gov'\n",
    "html = browser.html\n",
    "soup = BeautifulSoup(html, 'html.parser')\n",
    "hemisphere_image_urls = []\n",
    "results=soup.find_all('div',class_='description')\n",
    "for result in results:\n",
    "    try:    \n",
    "        hem=result.find('h3').text\n",
    "        image=result.find('a')[\"href\"]\n",
    "        hem_url2=hem_url+image\n",
    "        browser.visit(hem_url2)\n",
    "        img_html=browser.html\n",
    "        soup=BeautifulSoup(img_html, 'html.parser')\n",
    "        image=soup.find('img', class_='wide-image')['src']\n",
    "        new_url=hem_url+image\n",
    "        hemis_dict = {\"title\": hem, \"img_url\":new_url}\n",
    "        hemisphere_image_urls.append(hemis_dict)\n",
    "        print(hem)\n",
    "        print(new_url)\n",
    "    except Exception as e:\n",
    "        print(e)    "
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {
    "scrolled": true
   },
   "outputs": [],
   "source": [
    "hemisphere_image_urls"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.8.3"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 4
}
