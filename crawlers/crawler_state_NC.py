from bs4 import BeautifulSoup
import json
import requests
import time #BS Addition!

#As it stands right now, the scaper is unthrottled. See what you think about doing this responsibly.
#https://365datascience.com/tutorials/python-tutorials/limit-rate-requests-web-scraping/
# Adding some code from this resource to throttle the requests.

#This is the main page for SC General Statutes
BASEURL = "https://www.ncleg.gov"
PARENTURL= 'https://www.ncleg.gov/Laws/GeneralStatutesTOC' #Does not look like a valid URL to me! 
#would think this to be the URL after searching it out: https://www.scstatehouse.gov/code/statmast.php

chapter_list = []
    
def get_chapters(url):
    #This goes to the title page to make a list of chapter urls
    response = requests.get(url=url)
    if response.status_code == 200:
        html_content = response.text

        soup = BeautifulSoup(html_content, 'html.parser')
        items = soup.find_all('a', href=True)

        for item in items:
            href = item['href']
            if "/EnactedLegislation/Statutes/HTML/ByChapter/" in href:
                chapter_list.append(href)
                print(BASEURL+href)

    else:
        print(f"Failed to retrieve the chapter website. Status code: {response.status_code}")

    
def parse_statute(url):
    #This takes a chapter url and returns a json with each section 
    response = requests.get(url=url)
    html_content = response.text

    soup = BeautifulSoup(html_content, 'html.parser')
    p_tags = soup.find_all('p')  # Change this to 'p'
    statutes = {}

    for p in p_tags:  # Change this to 'p'
        trimmed_content = ''
        try:
            a_tag = p.find('span')  # Find 'span' tag within 'p' tag
            name = a_tag.get('name')
            text = p.get_text()  # Get text from 'p' tag
            trimmed_content += str(text)
            for sibling in p.next_siblings:
                if sibling.name == 'p':  # Break if next sibling is a 'p' tag
                    break
                else:
                    trimmed_content += str(sibling)
            statutes[name] = trimmed_content.strip()

        except AttributeError:
            "not this p tag"

    #A little validation to make sure we are getting the data we expect
    print(list(statutes.keys())[0])

    #This is the file name that the statutes will be saved to, per statute 
    file_name = "NC_" + url.split('/')[-1].split('.')[0] #Splitting the URL by '/' and '.' to get the file name.
    with open(f"{file_name}.json", 'w') as file:
        json.dump(statutes, file, indent=4)

def parse_statute_copilot_suggestion(url): #tired and turning in.  This is a suggestion from copilot that i don't have the energy to test
    response = requests.get(url=url)
    html_content = response.text

    soup = BeautifulSoup(html_content, 'html.parser')
    tags = soup.find_all(['p', 'h3', 'span'])  # Find 'p', 'h3', and 'span' tags
    statutes = {}
    current_chapter = ''
    current_subchapter = ''
    current_article = ''

    for tag in tags:
        if tag.name == 'h3' and 'article' in tag.get_text().lower():
            current_article = tag.get_text()
        elif tag.name == 'p' and '§' in tag.get_text():
            section_info = tag.get_text().split('.')
            current_chapter = section_info[0]
            current_subchapter = section_info[1] if len(section_info) > 1 else ''
        elif tag.name == 'span':
            definition = tag.get_text().strip()
            name = f"{current_chapter}.{current_subchapter}"
            statutes[name] = {
                'chapter': current_chapter,
                'subchapter': current_subchapter,
                'article': current_article,
                'definition': definition
            }

    print(list(statutes.keys())[0])

    file_name = url.split('/')[-1].split('.')[0]
    with open(f"{file_name}.json", 'w') as file:
        json.dump(statutes, file, indent=4)

#get_titles(PARENTURL) #populates the title list with the URLs of the titles

#for title in title_list:
get_chapters(PARENTURL) #populates the chapter list with the URLs of the chapters

for chapter in chapter_list:
    time.sleep(.01) #BS Notes: Forcing the for loop to sleep for 1/100 of a second at each iteration, effectively throttling the requests. 
    parse_statute(BASERURL+chapter) #parses the statutes and writes them to a json file

#future: save to a database before (or after) vectorizing the statutes for NLP


