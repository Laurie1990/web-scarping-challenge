from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
import time
from webdriver_manager.chrome import ChromeDriverManager



def scrape():
    executable_path = {"executable_path": "chromedriver"}
    browser = Browser("chrome", **executable_path, headless=False)

        ######### 1 MARS NEWS

    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    time.sleep(1)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    top_item = soup.select_one('ul.item_list ')
    header=top_item.find("div", class_= "content_title")
    header=header.text.strip()
    header

    html = browser.html
    soup = BeautifulSoup(html, "html.parser")

    par_text=top_item.find("div", class_= "article_teaser_body")
    par_text=par_text.text.strip()
    par_text


    ####### 2 MARS IMAGES

    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)
    time.sleep(1)

    se = browser.find_by_id('full_image')
    se.click()  

    #Click the button that says "more info", by looking for xml path associated with "more info" button
    look_for_text = '//*[@id="fancybox-lock"]/div/div[2]/div/div[1]/a[2]'

    matching_elements = browser.find_by_xpath(look_for_text)
    
    #Click on the box that says "more info"
    matching_elements.click()
    
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    #We know that the mian image that we want is of the image class, "main image"
    images = soup.find_all("img", { "class" : "main_image" })

    for image in images:
        image_href = f"{image['src']}"

    #We have our stem url, and we also have the src that takes us to the large scale image. Combine into a single link.
    stem_url = 'https://www.jpl.nasa.gov'
    main_image_url=stem_url+image_href


    ###### 3 MARS FACTS

    url = 'https://space-facts.com/mars/'

    dfs = pd.read_html(url)
    for df in dfs:
        try:
            df = df.rename(columns={0:"Fact", 1:"Data"})
            df = df.set_index("Fact")
            marstable_html=df.to_html()
            break
        except:
            continue



    ####### 4 MARS HEMISPHERES

    url='https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    stem_url= 'https://astrogeology.usgs.gov'

    browser.visit(url)
    time.sleep(1)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')


    pages = soup.find_all('div', class_='item')

    links = []
    titles = []
    for page in pages:
        links.append(stem_url + page.find('a')['href'])
        titles.append(page.find('h3').text.strip())



    browser.visit(links[0])
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    finalurl = stem_url+soup.find('img',class_='wide-image')['src']
    finalurl


    browser.visit(links[0])
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    finalurl = stem_url+soup.find('img',class_='wide-image')['src']
    finalurl

    img_url = []

    for finalurl in links:
        browser.visit(finalurl)
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')
        finalurl = stem_url+soup.find('img',class_='wide-image')['src']
        img_url.append(finalurl)

    hemisphere_image_urls = []

    for i in range(len(titles)):
        hemisphere_image_urls.append({'title':titles[i],'img_url':img_url[i]})

    
    marsinfo = {}
    marsinfo["news_header"] = header
    marsinfo["news_text"] = par_text
    marsinfo["featured_image_url"] = main_image_url
    marsinfo["marsfacts_html"] = marstable_html
    marsinfo["hemisphere_image_urls"] = hemisphere_image_urls

    return marsinfo
    
