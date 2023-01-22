from seleniumwire import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from functions import search_in_page_error, search_in_page_ta, rtime
import time

# поиск точки входа
def find_point_enter(list_of_input_selectors,driver, list_type):
    try:
        name = []
        id = []
        list_key_find = 0
        a = 0
        for j in range(len(list_of_input_selectors)):
            page2 = driver.page_source
            a3 = 0
            while page2.find(list_of_input_selectors[j]) != -1:
                a+=1
                enter_input = page2.find(list_of_input_selectors[j])
                end_enter_input = page2[enter_input:].find(">") + enter_input
                for k in list_type:
                    if page2[enter_input:end_enter_input].find(k) != -1:
                        list_key_find = 1
                        if k == "type=\"text\"":
                            a1 = "11"
                        elif k == "type=\"password\"":
                            a1 = "12"
                        elif k == "type=\"button\"" or k == "type=\"submit\"":
                            a1 = "20"
                        else:
                            a1 = ""
                        break
                if list_key_find == 1:
                    enter_name = page2[enter_input:end_enter_input].find(" name=") # первое вхождение name
                    enter_id = page2[enter_input:end_enter_input].find(" id=")  #первое вхождение id
                    #detected textarea = 13
                    if list_of_input_selectors[j] != "<input ":
                        a1 = "13"
                    if enter_name != -1:
                        enter_name += enter_input + 7
                        for i in range(enter_name, enter_name + 50):
                            if page2[i] != "\"":
                                a1 += page2[i]
                            else:
                                break
                        a1_db = []
                        a1_db.append(str(a3 + enter_name))
                        a1_db.append(a1)
                        name.append(a1_db)
                    elif enter_id != -1:
                        enter_id += enter_input + 5
                        for i in range(enter_id, enter_id + 50):
                            if page2[i] != "\"":
                                a1 += page2[i]
                            else:
                                break
                        a1_db = []
                        a1_db.append(str(a3 + enter_name))
                        a1_db.append(a1)
                        id.append(a1_db)
                a3 += end_enter_input
                page2 = page2[end_enter_input:]
        name.sort()
        id.sort()
        for i in range(len(name)):
            name[i][0] = i
        return name, id
    except Exception:
        print("find_point_enter_warning")


uri = "http://test.com/mutillidae/index.php?page=register.php"
options = Options()
options.headless = True
driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    options=options
)

list_of_input_selectors = ["<input ", "<textarea "]
list_type = ["type=\"text\"", "type=\"button\"", "type=\"submit\"", "type=\"password\""]

try:
    driver.get(url=uri)
    list_of_input_name, list_of_input_id = find_point_enter(list_of_input_selectors,driver,list_type)
    print(list_of_input_id)
    print(list_of_input_name)
    #распределение точек входа на поля и кнопки


except Exception as ex:
    print("sqli[i_sqli]_enter form_warning")
finally:
    driver.close()
    driver.quit()