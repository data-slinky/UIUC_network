from bs4 import BeautifulSoup # To scrape html
from urllib.request import urlopen # To navigate to urls
import re # To use regular expression

# Webpage of the Gray Book
weblink = "http://www.trustees.uillinois.edu/trustees/resources/15-16-Graybook/"

# Open webpage to navigate
webpage = urlopen(weblink + "KP.html")

# Parse the HTML from the webpage
soup = BeautifulSoup(webpage, "html.parser")

# Navigate to the summary table for UIUC
mydivs = soup.findAll("table", { "summary" : re.compile(".*Urbana-Champaign.*")})

# Pull out the link from the div class
for div in mydivs:
    links = div.findAll('a')

f = open("uiucData_sample.txt", "w+")

# Navigate to each link
for a in links:
    subpage = urlopen(weblink + a['href'])

    # Each page contains a table we need to pull the data from
    soup2 = BeautifulSoup(subpage, "html.parser")

    # Locate the salary table
    table = soup2.find("table", {"summary": "Table of Salary Ranges"})

    for row in table.findAll("th", {"class": ["dept-heading", "empl"]}):
        if re.match("\d+\s-\s", row.text):
            department = re.sub("\d+\s-\s", "", row.text)
        else:
            prof = row.text.strip()
            print(department+"\t"+prof, file=f)
f.close()


'''
# If you want the result as a dictionary to output as a JSON directly
result = {}
for row in table.findAll("th", {"class": ["dept-heading", "empl"]}):
    if re.match("\d+\s-\s", row.text):
        department = row.text
        result[department] = []
    else:
        result[department].append(row.text)
'''