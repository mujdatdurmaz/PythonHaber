import schedule
import time
from datetime import datetime
import fonksiyonlar as ft

def saatbasi():
    ulkeler=["TR"]
    for ulke in ulkeler:
        ft.trendHaberEkle(ulke)

    zaman=datetime.now()
    print("Çalıştırıldı...",zaman)

schedule.every().hour.do(saatbasi)

schedule.every().friday.at("13:30").do(saatbasi)

schedule.every(20).seconds.do(saatbasi)


while True:
    schedule.run_pending()
    time.sleep(1)