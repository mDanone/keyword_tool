# импорт системных библиотек
import time
import random
import csv
import os

# импорт пакетов Selenium для скрапинга
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

# импорт библиотеки для работы с буфером обмена
import pyperclip

# Создаем экземпляр настроек для браузера и добавляем нужные плагины
options = Options()
options.binary_location = "C:/Program Files (x86)/Google/Chrome/Application/chrome.exe"
options.add_extension(os.getcwd() + "\\Keyword_tool.crx")
PATH = f"{os.getcwd()}\\browser`s drivers\\chromedriver.exe"


# delay нам нужен чтобысайт не работали слишком быстро (изза этого происходят частые ошибки)
def delay():
    return time.sleep(random.randint(2, 5))


def siteEntry(driver, username, password, ToolKit):
    '''Входим на сайт keywordtools'''

    try:
        login = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="navbar"]/ul[2]/li/a'))
        )
        login.click()
    except:
        driver.quit()

    driver.find_element_by_xpath("//*[@id='UserName']").send_keys(username)
    driver.find_element_by_xpath("//*[@id='Password']").send_keys(password)
    driver.find_element_by_xpath('/html/body/div/div[2]/div/div/div[2]/form/div[6]/button').click()

    '''Данный словарь нам понадобится чтобы определить в какой поисковой системе хотим искать ключевые слова'''
    KeywordTools = {
        'amazon': "/html/body/div[1]/div[1]/div/div[1]/a/i",
        'ebay': "/html/body/div[1]/div[1]/div/div[2]/a",
        'etsy': "/html/body/div[1]/div[1]/div/div[3]/a",
        'walmart': "/html/body/div[1]/div[1]/div/div[4]/a",
        'youtube': "/html/body/div[1]/div[1]/div/div[6]/a",
        'bing': "/html/body/div[1]/div[1]/div/div[7]/a",
        'google shopping': "/html/body/div[1]/div[1]/div/div[8]/a",
    }

    if ToolKit in KeywordTools:
        driver.find_element_by_xpath(KeywordTools[ToolKit]).click()


def getTempMail(driver):
    '''Получаем временную почту с сайта Temp-Mail'''

    # Нужен pyperclip (pip install pyperclip)
    driver.get("https://temp-mail.org/ru/")
    delay()
    try:
        while not driver.find_element_by_xpath('//*[@id="click-to-copy"]').get_attribute("disabled") == "disabled":
            time.sleep(2)
            driver.find_element_by_xpath('//*[@id="click-to-copy"]').click()
            break
        mail = pyperclip.paste()
    except:
        driver.quit()
    return mail


def searchForElems(driver, KeyWord):
    '''Данная функция ищет элементы после входа на сайт keywordtols.com (Использовать после siteEntry)'''

    driver.find_element_by_xpath("//*[@id='txtKeywordInput']").send_keys(KeyWord)
    delay()
    driver.find_element_by_xpath("//*[@id='lnkSearch']/i").click()
    delay()
    try:
        WebDriverWait(driver, 1000).until_not(EC.visibility_of_element_located((By.ID, "processing-text")))
    except:
        pass
    words = [i.text for i in driver.find_elements_by_class_name("keyword-text")]
    return words


def siteRegister(driver, username, password, mail):
    '''Используем данную функцию для заполнения полей регистрации и ее выполнения'''

    registerButton = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="navbar"]/form/button')))
    registerButton.click()

    driver.find_element_by_xpath('//*[@id="UserName"]').send_keys(username)
    driver.find_element_by_xpath('//*[@id="Password"]').send_keys(password)
    driver.find_element_by_xpath('//*[@id="ConfirmPassword"]').send_keys(password)
    driver.find_element_by_xpath('//*[@id="EmailAddress"]').send_keys(mail)
    driver.find_element_by_xpath('/html/body/div/div[2]/div/div/div[2]/form/div[8]/button').click()

    return username


def ConfirmRegistration(driver):
    '''
        Эта функция нужна для подтверждения регистрации пользователя на сайте keywordtools.com
        Используем javascript скрипт для того чтобы прокрутить страницу вниз
        так как на странице временной почты в нижней части экрана появляется реклама и мешает нажимать на ссылки
    '''

    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    delay()
    WebDriverWait(driver, 50).until(EC.presence_of_element_located((By.XPATH, '//*[@id="tm-body"]/main/div[1]/div/div[2]/div[2]/div/div[1]/div/div[4]/ul/li[2]/div[1]/a'))).click()
    time.sleep(1)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    delay()
    driver.find_element_by_xpath('//*[@id="tm-body"]/main/div[1]/div/div[2]/div[2]/div/div[1]/div/div[2]/div[3]/a').click()


def Run(username, keyWord, service):
    '''
        Данная функция запускает весь рабочий процесс скрапинга информации с сайта keywordtools для одного элемента
        В каждом цикле создаем новый экземпляр Браузера
        Так как если этого не делать выйдет ошибка urllib3.exceptions.MaxRetryError
    '''
    driver = webdriver.Chrome(chrome_options=options, executable_path=PATH)

    # Получаем почту
    mail = getTempMail(driver)
    delay()
    driver.execute_script('''window.open("https://www.keywordtooldominator.com/","_blank");''')
    delay()
    driver.switch_to_window(driver.window_handles[1])

    # Используем регистрацию
    siteRegister(driver, username, 'Denchikalloha001', mail)
    driver.switch_to_window(driver.window_handles[0])
    delay()

    # Подтверждение регистрации
    ConfirmRegistration(driver)
    delay()
    driver.find_element_by_xpath('/html/body/div/div[1]/div/a/img').click()

    # Вход на сайт
    siteEntry(driver, username, 'Denchikalloha001', service)

    # Поиск ключевых слов
    words = searchForElems(driver, keyWord)

    # Выгружаем ключевые слова в csv файл
    with open("{}.csv".format(keyWord), 'w', newline='', encoding='utf-8') as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=' ',
                               quoting=csv.QUOTE_MINIMAL)
        for keyword in words:
            csvwriter.writerow([keyword])
    driver.quit()
