from bs4 import BeautifulSoup
import json
import requests

#As it stands right now, the scaper is unthrottled. See what you think about doing this responsibly.

#This is the main page for SC General Statutes
PARENTURL= 'South Carolina Code of Laws.html'
COURT_RULES_URL = 'https://www.sccourts.org/courtReg/'

def get_titles():
    #Open the file and get all URLs
    with open(PARENTURL, 'r', encoding='utf-8') as file:
        html_content= file.read()
    soup= BeautifulSoup(html_content, 'html.parser')
    items = soup.find_all('a', href=True)
    for item in items:
        href = item['href']
        #There is probably a more elegant way to figure out which urls should go into the title list, but this is what I figured out.
        if "title" in href:
            title_list.append(href)

def get_chapters(url):
    #This goes to the main page of each title and makes a list of chapter urls
    response = requests.get(url=url)
    if response.status_code == 200:
        html_content = response.text
        soup = BeautifulSoup(html_content, 'html.parser')
        items = soup.find_all('a', href=True)

        for item in items:
            href = item['href']
            #Again, there is probably a more elegant way to figure out which urls should be put in our final workload, but this is what I came up with in a pinch.
            if "code/t" in href:
                chapter_list.append('scstatehouse.gov'+href)

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

    print(list(statutes.keys())[0])

    file_name = url[34:-4]
    with open(f"{file_name}json", 'w') as file:
        json.dump(statutes, file, indent=4)

def get_court_rules():
    response= requests.get(url=COURT_RULES_URL)
    if response.status_code == 200:
        html_content= response.text
        soup = BeautifulSoup(html_content, 'html.parser')
        items = soup.find_all('a', href=True)

        for item in items:
            if 'ruleID' in item['href']:
                court_rule_list.append(item['href'])

    else:
        print(f"Failed to retrieve the rule links. Status code: {response.status_code}")

def court_rules_from_html():
    with open('SC court rules.html', 'r', encoding='utf-8') as file:
        html_content = file.read()
        soup = BeautifulSoup(html_content, 'html.parser')
        items = soup.find_all('a', href=True)

    for item in items:
        if 'ruleID' in item.get('href'):
            print(item.get('href'))


title_list= []
chapter_list = []
court_rule_list = []


court_rules_from_html()
