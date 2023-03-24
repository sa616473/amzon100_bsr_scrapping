from selenium import webdriver
from bs4 import BeautifulSoup, NavigableString
import pandas as pd
import time
import os

INITIAL_URL = "https://www.amazon.com/Best-Sellers/zgbs/ref=zg_bs_unv_0_boost_1"

def department_scrapping():
    #initializing selium
    driver = webdriver.Chrome()
    driver.get(INITIAL_URL)
    src=driver.page_source
    soup=BeautifulSoup(src,'html.parser')
    list_of_departments = soup.findAll('ul',{'id':'zg_browseRoot'})
    links_to_bsr_dep = []
    dep = []
    for department in list_of_departments:
        a_tag = department.findAll('a')
        for tag in a_tag:
            dep.append(tag.text)
    #         print(tag['href'])
            links_to_bsr_dep.append(tag['href'])
        dep_dict = {'department': dep, 'URL': links_to_bsr_dep}
        temp = pd.DataFrame(dep_dict)
        if not os.path.exists("./departments"):
            os.makedirs("./departments")
            temp.to_csv("./departments/department.csv")
        else:
            temp.to_csv("./departments/department.csv")

def category_scrapping():
    df = pd.read_csv('./departments/department.csv')
    driver = webdriver.Chrome()
    for department,url in zip(df['department'],df['URL']):
#         print(url)
        driver.get(url)
        src=driver.page_source
        soup=BeautifulSoup(src,'html.parser')
        list_of_cat = soup.findAll('ul',{'id':'zg_browseRoot'})
        cat_text = []
        cat_links = []
        for cat in list_of_cat:
            cat_tag = cat.findAll('a')
            for cat in cat_tag[1:]:
                cat_text.append(cat.text)
                cat_links.append(cat['href'])
            cat_dict = {'category': cat_text, 'URL': cat_links}
            temp = pd.DataFrame(cat_dict)
            if not os.path.exists("./categories"):
                os.makedirs("./categories")
                temp.to_csv("./categories/{}.csv".format(department))
            else:
                temp.to_csv("./categories/{}.csv".format(department))

def sub_category_scrapping():
    departments = pd.read_csv("./departments/department.csv")
    driver = webdriver.Chrome()
    for dep in departments["department"]:
        df = pd.read_csv("./categories/{}.csv".format(dep))
        for cat,url in zip(df["category"],df["URL"]):
            print(cat)
            print(url)
            driver.get(url)
            src=driver.page_source
            soup=BeautifulSoup(src,'html.parser')
            list_of_sub_cat = soup.findAll('ul',{'id':'zg_browseRoot'})
            sub_cat_text = []
            sub_cat_links = []

            for sub_cat in list_of_sub_cat:
                sub_cat_tag = sub_cat.findAll('a')

                for sub_cat in sub_cat_tag[1:]:
                    sub_cat_text.append(sub_cat.text)
                    sub_cat_links.append(sub_cat['href'])

                sub_cat_dict = {'category': sub_cat_text, 'URL': sub_cat_links}
                temp = pd.DataFrame(sub_cat_dict)
                if not os.path.exists("./sub_cat/{}".format(cat)):
                    os.makedirs("./sub_cat/{}".format(cat))
                    temp.to_csv("./sub_cat/{}".format(cat) + "/{}.csv".format(cat))
                else:
                    temp.to_csv("./sub_cat/{}".format(cat) + "/{}.csv".format(cat))

def top_100_scrapping():
    sub_categories = os.listdir('./sub_cat/')
    driver = webdriver.Chrome()
    for sub_cat in sub_categories:
        df =pd.read_csv("./sub_cat/{}/{}.csv".format(sub_cat,sub_cat))
        for cat,url in zip(df['category'],df['URL']):
            driver.get(url)
            src=driver.page_source
            soup=BeautifulSoup(src,'html.parser')
            listitem = soup.findAll('ol',{'id':'zg-ordered-list'})
            item_name = []
            item_link = []
            category = []
            for item in listitem:
                item_tag = item.findAll('a',{'class':'a-link-normal'})
#                 print(item_tag[0])
                for item in item_tag:
                    item_name.append(item['href'].split('/')[1])
                    item_link.append(item['href'])
                    category.append(cat)
                item_dict = {'sub_cat':category,'item_name':item_name, 'URL':item_link}
                temp = pd.DataFrame(item_dict)
                if not os.path.exists("./top100/{}".format(cat)):
                    os.makedirs("./top100/{}".format(cat))
                    temp.to_csv("./top100/{}/top_100{}.csv".format(cat,cat))
                else:
                    temp.to_csv("./top100/{}/top_100{}.csv".format(cat,cat))
def main():
    department_scrapping()
    category_scrapping()
    sub_category_scrapping()
    top_100_scrapping()

if __name__ == "__main__":
    main()
