
import requests
from bs4 import BeautifulSoup
import pandas as pd

def extract_text(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    if soup.find("div", attrs={"class": "td-post-content tagdiv-type"}):
        title = soup.find('h1' ,attrs = {"class":"entry-title"}).get_text()
        
        div_element = soup.find("div", attrs={"class": "td-post-content tagdiv-type"})
        p_elements = div_element.children
        t = []
        for p in p_elements:
           t.append(p.text)
        text = ' '.join(t)

                  
    elif soup.find("article").find("p").parent:
        title = soup.find('h1' ,attrs = {"class":"tdb-title-text"} ).get_text()
        text = soup.find("article").find("p").parent.get_text(' ',strip=True)
    else:
        text = None
    return text, title



if __name__ == "__main__":
    df = pd.read_excel(R'C:\Users\Desktop\input.xlsx')
# Iterate over the rows in the DataFrame
    for row in df.iterrows():
    # Get the URL and ID of the article
        url = row[1]["URL"]
        id = row[1]["URL_ID"]
        with open(f"{id}.txt", "w", encoding="utf-8") as f:
       
             text , title= extract_text(url)
             f.write("Title: " + str(title)+"\n")
             f.write(text)
             
