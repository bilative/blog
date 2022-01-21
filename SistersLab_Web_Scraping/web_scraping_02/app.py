import requests #!pip install requests
from bs4 import BeautifulSoup #!pip install beautifulsoup4
import time
from libs.helpies import sendTweet

URLs = 'https://sisterslab.co/blog/'

def get_soup(TARGET_URL):
    page = requests.get(TARGET_URL)
    soup = BeautifulSoup(page.content, 'html.parser', from_encoding="utf-8")
    return soup

OLD_blog_list = []

while (True):
    soup_blog_list = get_soup(URLs)

    NEW_blog_list = [] # Listelenen blog yazılarının url'lerini topluyoruz
    for i in soup_blog_list.find_all('div', attrs={'class':"content-inner"}):
        for j in i.find_all('a', href=True, attrs={'rel':"bookmark"}):
            if j['href'] != 'https://sisterslab.co/steam/':
                NEW_blog_list.append(j['href'])

    NEW_description = [] # Listelenen blog yazılarının giris cümlelerini topluyoruz
    for i in soup_blog_list.find_all('div', attrs={'class':"entry-description"}):
        NEW_description.append(i.text)

    NEW_image = [] # Listelenen blog yazılarının kapak fotolarını topluyoruz
    for i in soup_blog_list.find_all('div', attrs={'class':"post-thumbnail"}):
        for j in i.find_all('img', attrs={'class':'attachment-oxpitan_medium size-oxpitan_medium wp-post-image'}):
            NEW_image.append(j['src'])

    if (NEW_blog_list != OLD_blog_list): # Eğer bugün ve dünün blog listesi aynı değilse bu yeni yazılar yayınlandığına işarettir
        for url, text, img in zip(NEW_blog_list, NEW_description, NEW_image):
            if i not in OLD_blog_list:
                if (len(text) > (280 - 23)): # Bir tweet 280 karakterden uzun olamaz 
                    text = text[:255]
                time.sleep(2)
                sendTweet(img, text, url)       # sendTweet() fonksiyonu kendi tanımladığım bir fonksiyon
                print(url, text, img, '\n\n')   # sendTweet() ile dağınıklığı engellemeyi hedefledik

        OLD_blog_list = NEW_blog_list # yarın tekrar karşılaştırmak için blog listesini güncelliyoruz
    
    else:
        print('Bugün yeni blog yazısı yayınlanmadı')
    time.sleep(24 * 60 * 60) # 1 gun bekle (24saat * 60dk * 60sn)
