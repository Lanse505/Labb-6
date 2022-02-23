import os
import urllib.request
import time
from selenium import webdriver  # needs to be whitelisted

# r (raw string) => https://stackoverflow.com/questions/52360537/i-know-of-f-strings-but-what-are-r-strings-are-there-others
CROME_DRIVER_PATH = r'C:\temp\chromedriver.exe'
BASE_SAVE_FOLDER = 'images/'
URL_PREFIX = 'https://www.google.com.sg/search?q='
# https://simply-python.com/tag/google-images/
URL_POSTFIX = '&source=lnms&tbm=isch&sa=X&ei=0eZEVbj3IJG5uATalICQAQ&ved=0CAcQ_AUoAQ&biw=939&bih=591'


def main():
    if not os.path.exists(BASE_SAVE_FOLDER):
        os.mkdir(BASE_SAVE_FOLDER)
    download_images()


def download_images():
    topic = input('What do you want to search for? ')
    n_images = int(input('How many images do you want? '))

    save = input('In what subdir do you want to save the images? ')
    saving = BASE_SAVE_FOLDER + save
    if not os.path.exists(saving):
        os.mkdir(saving)

    search_url = URL_PREFIX + topic + URL_POSTFIX
    #print(search_url)

    driver = webdriver.Chrome(CROME_DRIVER_PATH)
    driver.get(search_url)

    value = 0
    for i in range(3):
        driver.execute_script('scrollBy('+str(value)+',+1000);')
        value += 1000
        time.sleep(1)

    elem1 = driver.find_element_by_id('islmp')
    sub = elem1.find_elements_by_tag_name('img')

    j=0
    for j, i in enumerate(sub):
        if j < n_images:
            src = i.get_attribute('src')
            try:
                if src is not None:
                    src = str(src)
                    print(src)
                    urllib.request.urlretrieve(src, os.path.join(saving, topic + str(j) + '.jpg'))
                else:
                    raise TypeError
            except Exception as ex:       # catches type error along with other errors
                print(f'fail with error {ex}')

    driver.close()

if __name__ == "__main__":
    main()