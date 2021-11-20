########################################################################
##
##  Web Scraping Homework - Mission to Mars
##
##       Author: George Alonzo
##     Due Date: November 20, 2021
##
########################################################################
from splinter import Browser
from bs4 import BeautifulSoup
import time
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd


def scrape_info():

    print("==========================================")
    print(" BEGINNING SCRAPE_MARS.PY")
    print("==========================================")

    # Set up Splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    mars_data=[]

    ######################################################################################
    ##
    ##  BEGIN SCRAPE FOR FEATURED IMAGE
    ##
    ######################################################################################
    
    print("**** BEGIN SCRAPE FOR FEATURED IMAGE ****")

    url = 'https://spaceimages-mars.com/'
    browser.visit(url)

    time.sleep(1)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')   

    results = soup.find_all('div', class_='header')

    for result in results:
        featured_image = result.find('img', class_='headerimage fade-in')['src']
        featured_image_url = "https://spaceimages-mars.com/"+featured_image
      
    mars_data_dict = {
    "featured_img": featured_image_url
    }
    mars_data.append(mars_data_dict)

    print("**** END SCRAPE FOR FEATURED IMAGE ****")

    ######################################################################################
    ##
    ##  END SCRAPE FOR FEATURED IMAGE
    ##
    ######################################################################################




    ######################################################################################
    ##
    ##  BEGIN SCRAPE FOR MARS FACTS
    ##
    ######################################################################################
    
    print("**** BEGIN SCRAPE FOR MARS FACTS ****")

    url = 'https://galaxyfacts-mars.com/'
    #browser.visit(url)

    time.sleep(1)

    tables = pd.read_html(url)
    html_table = tables[0]
    html_table = html_table.rename(columns={0:"Description",1:"Mars",2:"Earth"})
    html_table
    html_table = html_table.set_index("Description")
    html_table = html_table.iloc[1:,:]

    html_table = html_table.to_html()

    #Strip newlines
    html_table = html_table.replace("\n", "")

    mars_data_dict = {
    "mars_facts": html_table
    }
    mars_data.append(mars_data_dict)

    print("**** END SCRAPE FOR MARS FACTS ****")

    ######################################################################################
    ##
    ##  END SCRAPE FOR MARS FACTS
    ##
    ######################################################################################




    ######################################################################################
    ##
    ##  BEGIN SCRAPE FOR HEMISPHERES
    ##
    ######################################################################################
    
    print("**** BEGIN SCRAPE FOR HEMISPHERES ****")
    
    url = 'https://marshemispheres.com/'
    browser.visit(url)

    time.sleep(1)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    results = soup.find_all('div', class_='item')


    sub_urls=[]
    hemisphere_image_list =[]
    for result in results:
        # look for clickable links
        href = result.find('a')['href']
        LinkName = result.find('h3').text
        sub_urls.append(url+href)
        
        browser.click_link_by_partial_text(LinkName)
        clicked_html = url+browser.html
        clicked_soup = BeautifulSoup(clicked_html, 'html.parser')
        clicked_results = clicked_soup.find_all('div', class_='cover')
        for clicked_result in clicked_results:

            hem_title = LinkName.rsplit(' ', 1)[0]
            hem_hi_res = url+clicked_result.find('a')['href']
            mars_data_dict = {
                "hem_title": hem_title,
                "hem_hi_res": hem_hi_res
                }
            
            mars_data.append(mars_data_dict)

        browser.click_link_by_partial_text('Back')

    print("**** END SCRAPE FOR HEMISPHERES ****")

    ######################################################################################
    ##
    ##  END SCRAPE FOR HEMISPHERES
    ##
    ######################################################################################




    ######################################################################################
    ##
    ##  BEGIN SCRAPE FOR HEADLINES
    ##
    ######################################################################################
    
    print("**** BEGIN SCRAPE FOR HEADLINES ****")

    url = 'https://redplanetscience.com/'
    browser.visit(url)

    time.sleep(1)

    # Scrape page into Soup
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    # Retrieve the parent divs for all articles
    results = soup.find_all('div', class_='list_text')

    # loop over results to get article data

    # NOT GOING TO ATTEMPT TRYING TO CLICK THE 'MORE' BUTTON AS IT IS NOT ENABLED ON THE PAGE

    for result in results:
        # scrape the article header 
        title=(result.find('div', class_='content_title').text)

        # scrape the article subheader
        paragraph=(result.find('div', class_='article_teaser_body').text)

        # Store data in a dictionary
        mars_data_dict = {
        "news_title": title,
        "paragraph_text": paragraph
        }
        mars_data.append(mars_data_dict)

    print("**** END SCRAPE FOR HEADLINES ****")

    ######################################################################################
    ##
    ##  END SCRAPE FOR HEADLINES
    ##
    ######################################################################################

    time.sleep(1)

    # Close the browser after scraping
    browser.quit()

    print("==========================================")
    print(" ENDING SCRAPE_MARS.PY")
    print("==========================================")
    
    # Return results
    return mars_data
