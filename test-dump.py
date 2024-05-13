sampl = {

    'jobs': ["Rpa","something else", "windows"],
    'username': "abcsxxx",
    'pasw': "somefa"
}

sampl1 = [sampl[x] for x in sampl if isinstance(sampl[x],list)][0]
sampl1 = ",".join(sampl1)
print(sampl1,type(sampl1))




from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import re
import time

options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
driver = webdriver.Chrome(options=options)
driver.get("https://google.com")
search_box = driver.find_elements(By.TAG_NAME,"textarea")
search_box = [x for x in search_box if re.search("SEARCH",x.get_attribute("title").upper())][0]
search_box.send_keys("Cats",Keys.RETURN)
time.sleep(5)
content = driver.page_source
soup = BeautifulSoup(content,"html.parser")
# print(soup.prettify())
with open("out.html","wb") as outp:
    outp.write(soup.prettify("UTF-8"))

# for i in soup.find_all("div","kb0PBd"):
#     if i.find_all("a") != []:
#         all_a_tags = i.find_all("a")[0]
#         all_a_tag_hrefs = all_a_tags['href']
#         print(all_a_tag_hrefs)
    

all_divs = soup.find_all("div","kb0PBd")
all_a_tags = [x.find("a") for x in all_divs if x.find("a") is not None]
all_a_tag_hrefs = [x['href'] for x in all_a_tags]
all_a_tags_text = [x.text for x in all_a_tags]
print(all_a_tag_hrefs)

import pandas as pd

df = pd.DataFrame(columns=["job_post","job_link"])
df["job_post"] = all_a_tags
df["job_link"] = all_a_tag_hrefs
# for i in range(len(all_a_tags)):
    # df.loc["job_post"]
print(df)
df.to_excel("usefuldata.xlsx")