import time
import tweepy
import requests
import os

auth = tweepy.OAuthHandler("consumer_key", "consumer_secret") # Bu bölümü kendi twitter developer account'ınız tarafından türetilen keyler ile doldurmanız gerekmekte
auth.set_access_token("access_token", "access_token_secret")

api = tweepy.API(auth)

try:
    api.verify_credentials()
    print("Authentication OK")
except:
    print("Autontatication Error!!!")

api = tweepy.API(auth, wait_on_rate_limit=True,
                wait_on_rate_limit_notify=True)

def sendTweet(image_url, content, url): # Bu kısmı app.py içerisinde kullanıyoruz
    filename = 'temp_image.jpg'
    request = requests.get(image_url, stream=True) # kapak fotosunun bulunduğu url'e istek atılıyor
    
    if request.status_code == 200: # Ve bu fotoğraf bulunulan dizine "temp_image.jpg" olarak kaydediliyor
        with open(filename, 'wb') as image:  # Çünkü tweepy sadece dizinde kayıt olan fotoğraf ile tweet paylaşımı gerçekleştirebiliyor
            for chunk in request:
                image.write(chunk)


        tweet = content + ' ' + url # Blog giriş cümlesini ve blog url'ini bir tweette görünecek şekilde arka arkaya birleştiriyoruz
        api.update_with_media(filename, tweet) # Ve tweetimizi atıyoruz
        print('----------------------')
        os.remove(filename) # Kaydedilen görsel ile işimizi bittiği için görseli dizinden siliyoruz
        print('tweet atildi')






