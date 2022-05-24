from selenium import webdriver
from bs4 import BeautifulSoup
import requests
import time
import csv
START_URL = "https://en.wikipedia.org/wiki/List_of_brown_dwarfs"
browser = webdriver.Chrome("/Users/adrianbacherer/Desktop/Python/WebScraping2.0/chromedriver.isc")
browser.get(START_URL)
time.sleep(10)
headers = ["Star", "Constellation", "Right_ascencion", "Declination", "Distance", "Brown_drawf", "hyperlink", "history", "theory", "observations", "formation_and_evolution", "galleryd"]
brownDwarf_data = []
new_brownDwarf_data = []
def scrape():
    for i in range(1, 430):
        while True:
            time.sleep(2)
            soup = BeautifulSoup(browser.page_source, "html.parser")
            current_page_num = int(soup.find_all("input", attrs={"class", "page_num"})[0].get("value"))
            if current_page_num < i:
                browser.find_element_by_xpath('//*[@id="mw-content-text"]/div[1]/table[4]/thead/tr/th[2]/a').click()
            elif current_page_num > i:
                browser.find_element_by_xpath('//*[@id="mw-content-text"]/div[1]/table[4]/thead/tr/th[1]/a').click()
            else:
                break
        for ul_tag in soup.find_all("ul", attrs={"class", "wikipedia"}):
            li_tags = ul_tag.find_all("li")
            temp_list = []
            for index, li_tag in enumerate(li_tags):
                if index == 0:
                    temp_list.append(li_tag.find_all("a")[0].contents[0])
                else:
                    try:
                        temp_list.append(li_tag.contents[0])
                    except:
                        temp_list.append("")
            hyperlink_li_tag = li_tags[0]
            temp_list.append("https://en.wikipedia.org/wiki/List_of_brown_dwarfs?action=edit"+hyperlink_li_tag.find_all("a", href=True)[0]["href"])
            brownDwarf_data.append(temp_list)
        browser.find_element_by_xpath('//*[@id="mw-content-text"]/div[1]/table[4]/thead/tr/th[2]/a').click()
        print(f"{i} page done 1")
def scrape_more_data(hyperlink):
    try:
        page = requests.get(hyperlink)
        soup = BeautifulSoup(page.content, "html.parser")
        temp_list = []
        for tr_tag in soup.find_all("tr", attrs={"class": "fact_row"}):
            td_tags = tr_tag.find_all("td")
            for td_tag in td_tags:
                try:
                    temp_list.append(td_tag.find_all("div", attrs={"class": "value"})[0].contents[0])
                except:
                    temp_list.append("")
        new_brownDwarf_data.append(temp_list)
    except:
        time.sleep(1)
        scrape_more_data(hyperlink)
    scrape()
for index, data in enumerate(brownDwarf_data):
    scrape_more_data(data[5])
    print(f"{index+1} page done 2")
final_brownDwarf_data = []
for index, data in enumerate(brownDwarf_data):
    new_brownDwarf_data_element = new_brownDwarf_data[index]
    new_brownDwarf_data_element = [elem.replace("\n", "") for elem in new_brownDwarf_data_element]
    new_brownDwarf_data_element = new_brownDwarf_data_element[:7]
    final_brownDwarf_data.append(data + new_brownDwarf_data_element)
with open("final.csv", "w") as f:
        csvwriter = csv.writer(f)
        csvwriter.writerow(headers)
        csvwriter.writerows(final_brownDwarf_data)
