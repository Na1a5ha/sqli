from selenium.webdriver.chrome.options import Options
from seleniumwire import webdriver
from selenium.webdriver.chrome.service import Service
from tkinter import *
from webdriver_manager.chrome import ChromeDriverManager

def click_ex_uri(uri):
    options = Options()
    options.headless = True
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )
    try:
        driver.get(url=uri)
        for request in driver.requests:
            if request.response is not None:
                if int(request.response.status_code) < 399:
                    Label(text="URI доступен", font=("Roboto Bold", 12)) \
                        .place(relx=0.2, rely=0.05, relheight=0.05, relwidth=0.5)
                    return True
                else:
                    Label(text="URI не доступен", font=("Roboto Bold", 12)) \
                        .place(relx=0.2, rely=0.05, relheight=0.05, relwidth=0.5)
                    return False
            else:
                Label(text="URI не доступен", font=("Roboto Bold", 12)) \
                    .place(relx=0.2, rely=0.05, relheight=0.05, relwidth=0.5)
                return False
    except Exception:
        Label(text="URI не доступен", font=("Roboto Bold", 12)) \
            .place(relx=0.2, rely=0.05, relheight=0.05, relwidth=0.5)
        return False