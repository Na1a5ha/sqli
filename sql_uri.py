from selenium.webdriver.chrome.options import Options
from seleniumwire import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

def sql_in_uri(uri, k_conf, sqli):
    options = Options()
    options.headless = True
    db_error = ["error-header", "error-label", "error-detail", "mysqli_sql_exception:", "mysql_fetch_array()"]
    db_return = []
    key_page_error_check = 0
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )

    try:
        driver.get(url=uri)
        url_1 = driver.current_url
        c_url = url_1 + "?id=1&Submit=Submit#"
        try:
            time_1 = time.time()
            driver.get(url=c_url)
            time_1 = time.time()-time_1
        except Exception:
            print("ex")
        for i_sqli in range(len(sqli)):
            c_url = url_1 + "?id=" + sqli[i_sqli] + "&Submit=Submit#"
            try:
                time_2 = time.time()
                driver.get(url=c_url)
                page = driver.page_source
                time_2 = time.time()-time_2
                #status code
                if k_conf.find("1") != -1:
                    for request in driver.requests:
                        if request.response:
                            if int(request.response.status_code) > 404:
                                db_return.append("1" + str(i_sqli))
                                key_page_error_check = 1
                                break
                #page error
                if k_conf.find("2") != -1:
                    for i in db_error:
                        if page.find(i) != -1:
                            db_return.append("2" + str(i_sqli))
                            key_page_error_check = 1
                            break
                #time
                if k_conf.find("3") != -1:
                    if abs(time_1 - time_2) > 0.1:
                        db_return.append("3" + str(i_sqli))
                        key_page_error_check = 1
            except Exception:
                print("sql_uri1")
        # вывод
        if key_page_error_check == 0:
            db_return.append("0")
        return db_return
    except Exception:
        print("sql_uri")





