from seleniumwire import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from functions import search_in_page_error, search_in_page_ta, rtime
import time


# поиск точки входа
def find_point_enter(db_point_in, driver, db_cp):
    db_point_in_w_lp = []
    db_cp_w = []
    for i in db_point_in:
        try:
            driver.find_element(By.CSS_SELECTOR, i)
            db_point_in_w_lp.append(i)
            for j in range(len(db_cp)):
                try:
                    driver.find_element(By.NAME, db_cp[j])
                    db_cp_w.append(db_cp[j])
                    break
                except Exception:
                    driver.find_element(By.ID, db_cp[j])
                    db_cp_w.append(db_cp[j])
                    break
        except Exception:
            continue
    return db_point_in_w_lp, db_cp_w


# for dvwa
def dvwa(driver):
    driver.find_element(By.NAME, "username").send_keys("admin")
    driver.find_element(By.NAME, "password").send_keys("password")
    # time.sleep(rtime())
    driver.find_element(By.CSS_SELECTOR, "input[type='submit']").click()
    time.sleep(rtime())
    driver.find_element(By.XPATH, "/html/body/div/div[2]/div/ul[2]/li[7]/a").click()
    # time.sleep(rtime())


# main function
def sql_find_in_ef(url, k_conf, sqli):
    options = Options()
    options.headless = True

    db_point_in = ["input[type='login']", "input[type='log']", "input[type='user']", "input[type='username']",
                   "input[type='text']", "input[type='password']", "input[type='pass']"]
    db_point_in_w_ta = []
    db_return = []
    db_cp = ["confirm_password", "password-retype"]
    db_error = ["error-header", "error-label", "error-detail"]
    db_access = ["Logout"]
    db_s = ["\'", "\\", "\"", "<", ">", "/"]
    db_s_mini = ["<", ">", "\\", "/", "="]
    db_button_in = ["input[type='submit']", "button[type='submit']"]
    db_button_in_w = []
    time_0 = 0

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )
    try:
        driver.get(url=url)
        key_find_textarea = 0
        db_point_in_w_lp, db_cp_w = find_point_enter(db_point_in, driver, db_cp)
        page = driver.page_source
        try:
            driver.find_element(By.NAME, search_in_page_ta(page, db_s_mini)[1:-1])
            db_point_in_w_ta.append(search_in_page_ta(page, db_s_mini)[1:-1])
        except Exception:
            a = 0
        for i in db_button_in:
            try:
                driver.find_element(By.CSS_SELECTOR, i)
                db_button_in_w.append(i)
            except Exception:
                continue
        # попытка вставки sql инъекции
        key_check_find_or_empty = 0
        db_new = db_point_in_w_lp + db_point_in_w_ta

        for i_sqli in range(len(sqli)):
            for i in range(len(db_new)):
                driver.get(url=url)
                if len(db_point_in_w_lp) > 0:
                    for j in range(len(db_point_in_w_lp)):
                        if i == j:
                            driver.find_element(By.CSS_SELECTOR, db_point_in_w_lp[j]).send_keys(sqli[i_sqli])
                        else:
                            driver.find_element(By.CSS_SELECTOR, db_point_in_w_lp[j]).send_keys("AaBbCcD0")

                if len(db_cp_w) > 0:
                    if i == len(db_point_in_w_lp) - 1:
                        try:
                            driver.find_element(By.NAME, db_cp_w[0]).send_keys(sqli[i_sqli])
                        except Exception:
                            driver.find_element(By.ID, db_cp_w[0]).send_keys(sqli[i_sqli])
                    else:
                        try:
                            driver.find_element(By.NAME, db_cp_w[0]).send_keys("AaBbCcD0")
                        except Exception:
                            driver.find_element(By.ID, db_cp_w[0]).send_keys("AaBbCcD0")

                if len(db_point_in_w_ta) > 0:
                    for k in range(len(db_point_in_w_ta)):
                        if i == (k + len(db_point_in_w_lp)):
                            driver.find_element(By.NAME, db_point_in_w_ta[k]).send_keys(sqli[i_sqli])
                            key_find_textarea = 3
                        else:
                            driver.find_element(By.NAME, db_point_in_w_ta[k]).send_keys("AaBbCcD0")
                time_1 = time.time()
                driver.find_element(By.CSS_SELECTOR, db_button_in_w[0]).click()
                page2 = driver.page_source
                if time.time() - time_1 > time_0:
                    time_0 = time.time() - time_1

                # обработка кода ошибки
                if k_conf.find("1") != -1:
                    for request in driver.requests:
                        if request.response:
                            if int(request.response.status_code) > 404:
                                key_check_find_or_empty = 1
                                if key_find_textarea != 3:
                                    db_return.append("1" + db_new[i][12:-2])
                                    break
                                else:
                                    db_return.append("1textarea")
                                    break

                # обработка страницы ошибки
                if k_conf.find("2") != -1:
                    key_page_error_check = 0
                    try:
                        try:
                            key_page_error_check = search_in_page_error(page2, db_s, db_error, key_page_error_check)
                            if key_page_error_check > 0:
                                key_check_find_or_empty = 1
                                if key_find_textarea != 3:
                                    db_return.append("2" + db_new[i][12:-2])
                                else:
                                    db_return.append("2textarea")
                        except Exception:
                            try:
                                key_page_error_check = search_in_page_error(page2, db_s, db_access,
                                                                            key_page_error_check)
                                if key_page_error_check > 0:
                                    key_check_find_or_empty = 1
                                    if key_find_textarea != 3:
                                        db_return.append("ACCESSWARNING2" + db_new[i][12:-2])
                                    else:
                                        db_return.append("ACCESSWARNING2textarea")
                            except Exception:
                                print("-2")
                    except Exception:
                        print("-1")
            print(db_return)
            # search time problem
            if k_conf.find("3") != -1:
                driver.get(url=url)
                if len(db_point_in_w_lp) > 0:
                    for j in range(len(db_point_in_w_lp)):
                        driver.find_element(By.CSS_SELECTOR, db_point_in_w_lp[j]).send_keys("AaBbCcD0")
                if len(db_cp_w) > 0:
                    try:
                        driver.find_element(By.NAME, db_cp_w[0]).send_keys("AaBbCcD0")
                    except Exception:
                        driver.find_element(By.ID, db_cp_w[0]).send_keys("AaBbCcD0")
                if len(db_point_in_w_ta) > 0:
                    for k in range(len(db_point_in_w_ta)):
                        driver.find_element(By.NAME, db_point_in_w_ta[k]).send_keys("AaBbCcD0")
                time_2 = time.time()
                driver.find_element(By.CSS_SELECTOR, db_button_in_w[0]).click()
                if abs(time_0 - (time.time() - time_2)) > 0.1:
                    db_return.append("3")
                    key_check_find_or_empty = 1
            # exit if search
            if key_check_find_or_empty == 1:
                break
        # вывод
        if key_check_find_or_empty == 0:
            db_return.append("0")
        return db_return

    except Exception as ex:
        print("sqli[i_sqli]_enter form")
    finally:
        driver.close()
        driver.quit()
