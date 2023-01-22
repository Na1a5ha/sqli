from seleniumwire import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import time
from statistics import mean

#fun find point enter
def find_point_enter(db_point_in, db_button_in, driver):
    db_point_in_w = []
    db_button_in_w = []
    for i in range(len(db_point_in)):
        if len(driver.find_elements(By.CSS_SELECTOR, db_point_in[i])) != 0:
            a = []
            a.append(driver.find_elements(By.CSS_SELECTOR, db_point_in[i]))
            a.append(db_point_in[i])
            db_point_in_w.append(a)
    for i in range(len(db_button_in)):
        if len(driver.find_elements(By.CSS_SELECTOR, db_button_in[i])) != 0:
            db_button_in_w.append(driver.find_elements(By.CSS_SELECTOR, db_button_in[i]))
    return db_button_in_w, db_point_in_w

#fun sql enter
def sql_find_in_ef(url, k_conf, sqli):
    options = Options()
    options.add_experimental_option("prefs", {"profile.block_third_party_cookies": True})
    options.headless = True
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )
    db_point_in = ["input[type='login']", "input[type='log']", "input[type='user']", "input[type='username']",
                   "input[type='text']", "input[type='password']", "input[type='pass']", "textarea[name='my_signature']", "textarea[name='blog_entry']"]
    db_button_in = ["input[type='submit']", "button[type='submit']"]
    db_error = ["error-header", "error-label", "error-detail"]
    db_access = ["Logout", "Username=", "Password="]
    db_return = []
    time_list = []
    try:
        driver.get(url=url)
        db_button_in_w, db_point_in_w = find_point_enter(db_point_in, db_button_in, driver)
        db_button_in_w_len, db_point_in_w_len = db_button_in_w, db_point_in_w
        key_check_find_or_empty = 0
        #расширяем точки входа для проверки типа all
        db_point_in_w.append(["1"])
        for i_sqli in range(len(sqli)):
            for r_i in range(len(db_point_in_w_len)):
                for i in range(len(db_button_in_w_len)):
                    driver.delete_all_cookies()
                    driver.get(url=url)
                    db_button_in_w, db_point_in_w = find_point_enter(db_point_in, db_button_in, driver)
                    #все заполненные формы
                    a3 = ''
                    if r_i == len(db_point_in_w):
                        if len(db_point_in_w) != 1:
                            for r_i2 in range(len(db_point_in_w)):
                                a = db_point_in_w[r_i2]
                                if len(a[0]) > 1:
                                    a = a[0]
                                    for k in range(len(a)):
                                        a[k].send_keys(sqli[i_sqli])
                                else:
                                    a = a[0]
                                    a[0].send_keys(sqli[i_sqli])
                                a = db_point_in_w[r_i2]
                                a3 = "all"
                            a2 = ["", a3]
                            a = db_button_in_w[i]
                            # блок проверки времени
                            if k_conf.find("3") != -1:
                                time_0 = time.time()
                            a[0].click()
                            if k_conf.find("3") != -1:
                                time_list.append(time.time() - time_0)
                    #основные итерации проверки
                    else:
                        db_point_in_w.insert(0, db_point_in_w[r_i])
                        a = db_point_in_w[0]
                        a2 = a
                        if len(a[0])>1:
                            a = a[0]
                            for k in range(len(a)):
                                a[k].send_keys(sqli[i_sqli])
                        else:
                            a = a[0]
                            a[0].send_keys(sqli[i_sqli])
                        db_point_in_w.pop(0)
                        db_point_in_w.pop(r_i)
                        for j2 in range(len(db_point_in_w)):
                            a = db_point_in_w[j2]
                            if len(a[0]) > 1:
                                a = a[0]
                                for k in range(len(a)):
                                    a[k].send_keys("a1")
                            else:
                                a = a[0]
                                a[0].send_keys("a1")
                        a = db_button_in_w[i]
                        if k_conf.find("3") != -1:
                            time_0 = time.time()
                        a[0].click()
                        if k_conf.find("3") != -1:
                            time_list.append(time.time() - time_0)
                    #!проверки
                    # обработка кода ошибки
                    if k_conf.find("1") != -1:
                        for request in driver.requests:
                            if request.response:
                                if int(request.response.status_code) > 404:
                                    db_return.append("1" + a2[1] + str(i_sqli))
                                    key_check_find_or_empty = 1
                                    break
                    # обработка страницы ошибки
                    page = driver.page_source
                    if k_conf.find("2") != -1:
                        key_page_error_check = 0
                        #find error
                        for i in db_error+db_access:
                            if page.find(i) != -1:
                                key_page_error_check = 1
                                break
                        if key_page_error_check > 0:
                                db_return.append("2" + a2[1] + str(i_sqli))
                                key_check_find_or_empty = 1
            #проверка времени
            if k_conf.find("3") != -1:
                abs_time = mean(time_list)
                time_list = []
                for i in range(len(db_button_in_w)):
                    driver.delete_all_cookies()
                    driver.get(url=url)
                    db_button_in_w, db_point_in_w = find_point_enter(db_point_in, db_button_in, driver)
                    for r_i2 in range(len(db_point_in_w)):
                        a = db_point_in_w[r_i2]
                        if len(a[0]) > 1:
                            a = a[0]
                            for k in range(len(a)):
                                a[k].send_keys("a")
                        else:
                            a = a[0]
                            a[0].send_keys("a")
                    # блок проверки времени
                    if k_conf.find("3") != -1:
                        time_0 = time.time()
                    a = db_button_in_w[i]
                    a[0].click()
                    if k_conf.find("3") != -1:
                        time_list.append(time.time() - time_0)
                if abs(mean(time_list) - abs_time) > 0.1:
                    db_return.append("3" + str(i_sqli))
                    key_check_find_or_empty = 1
        if key_check_find_or_empty == 0:
            db_return.append("0")
        return db_return
    except Exception as ex:
        print("sqli[i_sqli]_enter form_warning")
    finally:
        driver.close()
        driver.quit()