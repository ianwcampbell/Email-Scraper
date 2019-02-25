# emailparser.py
# By Ian Campbell
# This program scrapes emails from a given URL and spiders 
# to find them!!!
# vers 2.0.0 02/07/19

#imports
import re
from bs4 import BeautifulSoup
import requests
import requests.exceptions
from urllib.parse import urlsplit
from collections import deque

#queue of urls and take input
print('Welcome to emailparser.py!\n')
print('Full url example "http://domainname.com/"')
start = input('Enter target url: ')
new_urls = deque([start])

#setting up sets for emails and URLs
processed_urls = set()
emails = set()

while len(new_urls):
    url = new_urls.popleft()
    processed_urls.add(url)

    parts = urlsplit(url)
    #formatting URL
    base_url = "{0.scheme}://{0.netloc}".format(parts)
    if parts.scheme != 'mailto' and parts.scheme != '#':
        path = url[:url.rfind('/')+1] if '/' in parts.path else url
    else:
        continue


    print("Processing %s" % url)
    try:
        response = requests.get(url)
    except (requests.exceptions.MissingSchema, requests.exceptions.ConnectionError,requests.exceptions.InvalidURL):
        continue

    #regex to find emails even mildly obfuscated
    new_emails = set(re.findall(r"[a-z0-9\.\-+_]+(?:@|\(at\)|\[at\])[a-z0-9\.\-+_]+(?:\.|\(dot\)|\[dot\])[a-z]+",
        response.text, re.I))
    emails.update(new_emails)

    #Add a bsOBJ to get that damn html
    soup = BeautifulSoup(response.text, 'lxml')

    #determine spidering links
    for anchor in soup.find_all("a"):
        link = anchor.attrs["href"] if "href" in anchor.attrs and anchor.attrs["href"].find("mailto") == -1 and anchor.attrs["href"].find("tel") == -1 and anchor.attrs["href"].find("#") == -1 else ''

        if link.startswith('/'):
            link = base_url + link
        elif not link.startswith('http'):
            link = path + link
        if not link in new_urls and not link in processed_urls and not link.find(start) == -1:
            new_urls.append(link)

#prints apparantly valid emails
print("\n EMAILS FOUND \n")
for e in emails:
    if e.endswith(".png") or e.endswith(".gif") or e.endswith(".jpeg") or e.endswith("dwt") or e.startswith("www"):
        continue
    else:
        print(e)
