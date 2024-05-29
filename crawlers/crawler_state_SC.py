from bs4 import BeautifulSoup
import json
import requests
import time #BS Addition!

#As it stands right now, the scaper is unthrottled. See what you think about doing this responsibly.
#https://365datascience.com/tutorials/python-tutorials/limit-rate-requests-web-scraping/
# Adding some code from this resource to throttle the requests.

#This is the main page for SC General Statutes
BASEURL = "https://scstatehouse.gov/"
PARENTURL= 'https://www.scstatehouse.gov/code/statmast.php' #Does not look like a valid URL to me! 
#would think this to be the URL after searching it out: https://www.scstatehouse.gov/code/statmast.php

title_list= []
chapter_list = []

def get_titles(url):
    #This goes to the main page and makes a list of title urls
    response = requests.get(url=url)
    if response.status_code == 200:
        html_content = response.text

        soup= BeautifulSoup(html_content, 'html.parser')
        items = soup.find_all('a', href=True)
        for item in items:
            href = item['href']
            #There is probably a more elegant way to figure out which urls should go into the title list, but this is what I figured out.
            if "title" in href:
                title_list.append(href) #BS Notes: Finding all links on the top page, and appending those that have "title" in that href tag to the list. 
    
def get_chapters(url):
    #This goes to the title page to make a list of chapter urls
    response = requests.get(url=url)
    if response.status_code == 200:
        html_content = response.text

        soup = BeautifulSoup(html_content, 'html.parser')
        items = soup.find_all('a', href=True)

        for item in items:
            href = item['href']
            if "code/t" in href:
                chapter_list.append(BASEURL+href)

    else:
        print(f"Failed to retrieve the chapter website. Status code: {response.status_code}")

def parse_statute (url):
    #This takes a chapter url and returns a json with each section 
    response = requests.get(url=url)
    html_content = response.text

    soup = BeautifulSoup(html_content, 'html.parser')
    spans = soup.find_all('span')
    statutes = {}

    for span in spans:
        time.sleep(.01) #BS Notes: Forcing the for loop to sleep for 1/100 of a second at each iteration, effectively throttling the requests. 
        trimmed_content = ''
        try:
            a_tag = span.find('a')
            name = a_tag.get('name')
            text = span.get_text()
            trimmed_content += str(text)
            for sibling in span.next_siblings:
                if sibling.name == 'span':
                    break
                else:
                    trimmed_content += str(sibling)
            statutes[name]=trimmed_content.strip()

        except AttributeError:
            "not this span"

    #A little validation to make sure we are getting the data we expect
    print(list(statutes.keys())[0])

    #This is the file name that the statutes will be saved to, per statute 
    file_name = "SC_" + url.split('/')[-1].split('.')[0]  #was: url[34:-4]
    with open(f"{file_name}.json", 'w') as file:
        json.dump(statutes, file, indent=4)

get_titles(PARENTURL) #populates the title list with the URLs of the titles

for title in title_list:
    get_chapters(BASEURL+title) #populates the chapter list with the URLs of the chapters

for chapter in chapter_list:
    parse_statute(chapter) #parses the statutes and writes them to a json file

#future: save to a database before (or after) vectorizing the statutes for NLP


