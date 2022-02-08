from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException, \
    TimeoutException, ElementNotInteractableException
from time import sleep
from database import dbBrainly
import config

def get_browser():
    opts = Options()
    opts.add_argument("--disable-dev-shm-usage")
    opts.add_argument("--no-sandbox")
    driver = Chrome(executable_path='chromedriver.exe', options=opts)
    return driver

def check_pop_up(driver):
    pop_up_elem = '/html/body/div[2]/div/div[3]'
    driver.implicitly_wait(5)
    try:
        driver.find_element_by_xpath(pop_up_elem).click()
        print('udah di close')
    except NoSuchElementException:
        print('tidak muncul')
        pass
    except ElementNotInteractableException:
        print('tidak ada popup')
        pass

def get_info(driver, url):
    driver.get(url)
    sleep(3)
    check_pop_up(driver)


# Text Pertanyaan
    try:
        text_elem = '/html/body/div[2]/div/div[2]/div[1]/div[1]/div[1]/article/div/div/div[2]/div/div/h1'
        text = driver.find_element_by_xpath(text_elem).text
    except NoSuchElementException:
        text = ''

    # Penjawab
    try:
        penjawab_elem = '//*[@id="question-sg-layout-container"]/div[1]/div[2]/div[2]/div/div[1]/div[2]/div/div[2]/div[1]/span'
        penjawab = driver.find_element_by_xpath(penjawab_elem).text
    except NoSuchElementException:
        penjawab = ''

    # Status Terjawab
    try:
        button_style = 'span.sg-button__text'
        content = driver.find_element_by_id('question-sg-layout-container')
        span_text = content.find_element_by_css_selector(button_style).text

        if 'LIHAT JAWABAN' in span_text:
            terjawab = True
        else:
            terjawab = False

    except NoSuchElementException:
        terjawab = ''

    # Jawaban terverifikasi
    try:
        verif_elem = '/html/body/div[5]/div/div[4]/div[1]/div[1]/div[4]/div/div[1]/div/div[1]/div/div[1]/div[2]/h3'
        verif = driver.find_element_by_tag_name("h3").text
        if 'Jawaban terverifikasi ahli' in verif:
            terverifikasi = True
        else:
            terverifikasi = False

    except NoSuchElementException:
        terverifikasi = ''

    data = {
        'url': url,
        'text_soal': text,
        'penjawab': penjawab,
        'terjawab': terjawab,
        'terverifikasi': terverifikasi
        }
    return data

def get_subject_links(driver):
    driver.implicitly_wait(5)
    xpath_load = '//*[@id="loadMore"]'
    for i in range(10):
        driver.find_element_by_xpath(xpath_load).click()
        sleep(3)
        print('load ke {}'.format(i))
    questions = driver.find_elements_by_xpath('/html/body/div[6]/div/div[2]/div[3]/div') 
    href_list = []
    i = 1
    for q in questions:
        xpath_answer = '//*[@id="questions"]/div[{}]/div/div/div/a'.format(i) 
        href = q.find_element_by_xpath(xpath_answer).get_attribute('href')
        href_list.append(href)
        i+=1
    return href_list

if __name__ == '__main__':
    db = dbBrainly('brainlydb')
    driver = get_browser()

    geografi = config.MAPEL[5]
    # GET URL
    url = 'https://id.brainly.vip/unanswered/{}.html'.format(geografi)

    driver.get(url)
    links = get_subject_links(driver)
    print('scraping for details....')
    for url in links:
        try:
            
            collected = get_info(driver, url)
            collected['mapel'] = 'geografi'
            db.insert_info('geografi', collected)
            print('data {} inserted'.format(geografi))
            sleep(3)

        except NoSuchElementException as no_element:
            print(no_element)
            pass
    print('done')

    # indonesia = config.MAPEL[0]
    # # GET URL
    # url = 'https://id.brainly.vip/unanswered/b-indonesia.html'

    # driver.get(url)
    # links = get_subject_links(driver)
    # print('scraping for details....')
    # for url in links:
    #     try:
    #         collected = get_info(driver, url)
    #         collected['mapel'] = 'bahasa indonesia'
    #         db.insert_info('bahasa indonesia', collected)
    #         print('data {} inserted'.format(indonesia))
    #         sleep(3)