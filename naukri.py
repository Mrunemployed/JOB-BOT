from selenium import webdriver
import pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
import requests
from concurrent.futures import ThreadPoolExecutor
import re
import time
import logging
import json
from bs4 import BeautifulSoup

#Chapno25

class naukri():

    def __init__(self) -> None:
        self.options = webdriver.ChromeOptions()
        self.options.add_argument("--start-maximized")
        self.driver = webdriver.Chrome(options=self.options)
        self.driver.get("https://naukri.com")
        with open("input_data.json","r") as input_file:
            self.data = json.load(input_file)
        print(self.data)
        if self.data["filters"]["freshness-days"]["value"] != "":
            self.filter_freshness = self.data["filters"]["freshness-days"]["value"]
            self.filter_freshness_name = self.data["filters"]["freshness-days"]["filter-name"]
        else:
            self.filter_freshness = 7

    def login_handler(self,**kwargs):
        try:
            login_button = self.driver.find_element(By.ID,"login_Layer")
        except Exception:
            WebDriverWait(self.driver,10).until(EC.presence_of_element_located((By.LINK_TEXT,"login")))
            login_button = self.driver.find_element(By.LINK_TEXT,"login")
        except:
            WebDriverWait(self.driver,10).until(EC.presence_of_all_elements_located((By.TAG_NAME,"a")))
            login_buttons = self.driver.find_elements(By.TAG_NAME,"a")
            # login_button = [x for x in login_buttons if x.get_attribute('title') == "Jobseeker Login"]
            login_button = [x for x in login_buttons if x.text == "Login"][0]
            print(login_button,login_button.text)
            
        login_button.click()
        time.sleep(3)

        try:
            WebDriverWait(self.driver,10).until(EC.presence_of_all_elements_located((By.TAG_NAME,"input")))
            input_fields = self.driver.find_elements(By.TAG_NAME,"input")
            username_field = [x for x in input_fields if re.search("USERNAME",x.get_attribute("placeholder").upper())][0]
            print(username_field.get_attribute('placeholder'))
            username_field.send_keys(self.data["username"])
            pass_field = [x for x in input_fields if re.search("PASSWORD",x.get_attribute("placeholder").upper())][0]
            pass_field.send_keys(self.data["pasw"])
        except Exception as err:
            print("not found",err)

        try:
            login_buttons = self.driver.find_elements(By.CLASS_NAME, "loginButton")
            print(login_button.text)
            login_button = [x for x in login_buttons if re.search("SUBMIT",x.get_attribute("type").upper())][0]
            login_button.click()
        except Exception as err:
            print(err)

    def sign_out(self):
        try:
            WebDriverWait(self.driver,10).until(EC.presence_of_element_located((By.CLASS_NAME,"nI-gNb-drawer__icon")))
            log_out_menu = self.driver.find_element(By.CLASS_NAME,"nI-gNb-drawer__icon")
            log_out_menu.click()
            log_out_buttons = self.driver.find_elements(By.TAG_NAME,"a")
            log_out_button = [x for x in log_out_buttons if re.search("LOGOUT",x.get_attribute("title").upper())][0]
            log_out_button.click()
        except:
            print("Log out button not found")

    def change_profile_headline(self,sample_text):
        if sample_text.endswith("."):
            sample_text = sample_text[:len(sample_text)-1]
        else:
            sample_text+="."
        return sample_text

    def update_profile(self):
        try:
            time.sleep(3)
            # WebDriverWait(self.driver,10).until(EC.visibility_of_all_elements_located((By.TAG_NAME,"a")))
            a_elements = self.driver.find_elements(By.TAG_NAME,"a")
            update_profile_link = [x for x in a_elements if re.search("complete * profile",x.text.lower())][0]
            update_profile_link.click()
            WebDriverWait(self.driver,30).until(EC.visibility_of_element_located((By.TAG_NAME,"span")))
            time.sleep(3)
            divs = self.driver.find_elements(By.CLASS_NAME,"widgetHead")
            for i in range(len(divs)):
                print(divs[i].text)
                if re.search("RESUME",divs[i].text.upper()):
                    spans_in_div = divs[i].find_elements(By.TAG_NAME,"span")[1]
                    spans_in_div.click()

                    break
            resume_headline = self.driver.find_element(By.ID,"resumeHeadlineTxt")
            resume_headline_text = resume_headline.text
            print(resume_headline_text)
            
            resume_headline.clear()
            changed_headline = self.change_profile_headline(resume_headline_text)
            resume_headline.send_keys(changed_headline) 

            WebDriverWait(self.driver,10).until(EC.presence_of_element_located((By.XPATH,"/html/body/div[6]/div[8]/div[2]/form/div[3]/div/button")))
            save_resume_headline_btn = self.driver.find_element(By.XPATH,"/html/body/div[6]/div[8]/div[2]/form/div[3]/div/button")
            WebDriverWait(self.driver,10).until(EC.element_to_be_clickable((By.XPATH,"/html/body/div[6]/div[8]/div[2]/form/div[3]/div/button")))
            save_resume_headline_btn.click()

        except Exception as err:
            print("Error at update profile:",err)

    def search_matching_jobs(self,jobs_parameters:dict):
        try:
            jobs_parameters_search = [jobs_parameters[x] for x in jobs_parameters if isinstance(jobs_parameters[x],list)][0]
            jobs_parameters_search_str = ",".join(jobs_parameters_search)

            WebDriverWait(self.driver,10).until(EC.presence_of_element_located((By.CSS_SELECTOR,"span.nI-gNb-sb__placeholder")))
            search_box = self.driver.find_element(By.CSS_SELECTOR,"span.nI-gNb-sb__placeholder")
            search_box.click()
            WebDriverWait(self.driver,10).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR,"input.suggestor-input")))
            search_box_search = self.driver.find_elements(By.CSS_SELECTOR,"input.suggestor-input")
            # search_box_search[0] for jobs search_box_search[1] for locations
            search_box_search[0].send_keys(jobs_parameters_search_str,Keys.RETURN)
            time.sleep(5)
            return self.driver.current_url,self.driver

        except TypeError as err:
            return err
        except Exception as err:
            return err
        
    def view_job_post(self,df):
        pass

    def parse_job_search_page(self):
        time.sleep(3)
        page_content = self.driver.page_source 
        # sour = BeautifulSoup(page_content,"html.parser")
        # job_header_text = sour.find("div","jobs-list-header").find("span")['title']
        # Un-commenting this will cause the bot to fetch all the matching jobs that matched the search
        # Which may result in subsequent blocking of the Naukri ID/IP.
        # self.get_all_matching_jobs(job_header_text,sour) 
        page_url = self.driver.current_url
        filter_uri = page_url+"&"+self.filter_freshness_name+"="+str(self.filter_freshness)
        print(filter_uri)
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.80 Safari/537.36',
            'Content-Type': 'text/html',
        }
        req = requests.get(url=filter_uri,verify=False,headers=headers)
        print(req.status_code)
        # req = json.loads(req.text)
        req = req.text
        with open("out.html","w") as file:
            file.writelines(req)
        sour_candy = BeautifulSoup(req,"html.parser") 
        all_divs = sour_candy.find_all("div","row1")
        all_a_tags = [x.find("a") for x in all_divs if x.find("a") is not None]
        all_a_tag_hrefs = [x['href'] for x in all_a_tags]
        print(all_a_tag_hrefs)
        all_a_tags_text = [x.text for x in all_a_tags]
        print()
        df = pd.DataFrame(columns=["Job_post","Job_link"])
        df["Job_post"] = all_a_tags_text
        df["Job_link"] = all_a_tag_hrefs
        df.to_excel("job-data.xlsx")



        


    def get_all_matching_jobs(self,job_header_text,sour:BeautifulSoup):
        job_header_results = int(job_header_text.split("of")[1].strip())
        #total pages to be requested
        tpr = int(job_header_results/20)
        if tpr > 10 : tpr = 20
        while (tpr>1):
            page_content = requests.get()
            all_divs = sour.find_all("div","row1")
            all_a_tags = [x.find("a") for x in all_divs if x.find("a") is not None]
            all_a_tag_hrefs = [x['href'] for x in all_a_tags]
            print(all_a_tag_hrefs)
            df = pd.DataFrame(columns=["Job_post","Job_link"])
        
            

nauk1 = naukri()
nauk1.login_handler()
nauk1.update_profile()
current_uri = nauk1.search_matching_jobs(nauk1.data)
print(current_uri)
nauk1.parse_job_search_page()

nauk1.sign_out()
time.sleep(30)
    # self.driver.quit()