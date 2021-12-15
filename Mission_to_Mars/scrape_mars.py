# import dependancies 
from splinter import Browser
from bs4 import BeautifulSoup as bs
import time
import pandas as pd
from flask import Flask, render_template, redirect
from webdriver_manager.chrome import ChromeDriverManager

def scrape_all():
    # initiate driver
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)   

    # run all scraping functions
    url1 = 'https://redplanetscience.com/'
    browser.visit(url1)
    html=browser.html
    soup = bs(html, 'html.parser')
    news1head = soup.find_all('div', class_='content_title')[0].text
    new1con = soup.find_all('div', class_='article_teaser_body')[0].text

    url2 = 'https://spaceimages-mars.com/'
    browser.visit(url2)
    html = browser.html
    soup = bs(html, 'html.parser')
    featured_image_url = soup.find("img", {"class": "headerimage"})['src']
    final_image = (url2 + featured_image_url)

    url3 = 'https://galaxyfacts-mars.com/'
    browser.visit(url3)
    mars_table = pd.read_html(url3)
    columns=['Description', 'Mars', 'Earth']
    table1= mars_table[0]
    table2 = table1.to_html(index=False)
    #table1.to_html("Table.html", index=False))

    url4 = 'https://marshemispheres.com/'
    browser.visit(url4)
    html = browser.html
    soup = bs(html, 'html.parser')
    marshemispheres = soup.find_all("div", {"class":"item"})

    hemisphere = []
    for x in marshemispheres:
        ref = url4 + x.find("a", {"class": "itemLink"})["href"]
        browser.visit(ref)
        time.sleep(1)
    
        html = browser.html
        soup = bs(html, "html.parser")
    
        img_url = url4 + soup.find("img", {"class", "wide-image"})["src"]
        title = soup.find("h2", {"class", "title"}).text
    
        images_title = {"title":title,
                    "img_url":img_url}
    
        hemisphere.append(images_title)

    # store results
    mars_data = {
        "news1head": news1head,
        "new1con": new1con,
        "final_image": final_image,
        "table2": table2,
        "hemisphere": hemisphere
    }
    print("Data:", mars_data)

    browser.quit()

    return mars_data

if __name__ == "__main__":

    print(scrape_all())