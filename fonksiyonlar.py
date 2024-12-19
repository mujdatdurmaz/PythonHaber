import requests
import xml.etree.ElementTree as et
import sqlite3
import uuid
import datetime

conn=sqlite3.connect("trendbase.sqlite3")
c=conn.cursor()

c.execute("""CREATE TABLE IF NOT EXISTS trendler(
  baslik TEXT,
  aciklama TEXT,
  trafik INTEGER,
  tarih TEXT,
  ulke TEXT,
  eklenme TEXT,
  key TEXT
  )""")
conn.commit()

c.execute("""CREATE TABLE IF NOT EXISTS haberler(
  trendkey TEXT,
  trend TEXT,
  baslik TEXT,
  url TEXT,
  kaynak TEXT,
  resim TEXT,
  ulke TEXT)""")
conn.commit()


def trendGetir(dil):
  dil=dil.upper()
  link=f"https://trends.google.com/trending/rss?geo={dil}"

  r=requests.get(link)
  veri=r.content
  rss=et.fromstring(veri)


  trendler=[]
  for etiket in rss[0]:
    if etiket.tag=="item":
      baslik=etiket[0].text
      trafik=etiket[1].text
      trafik=trafik.replace("+","")
      trafik=int(trafik)
      aciklama=etiket[2].text
      tarih=etiket[4].text

      trend={} #trendleri dict e alalım
      haberler=[]

      trend.update({"baslik":baslik,"trafik":trafik,"aciklama":aciklama,"tarih":tarih})


      for altetiket in etiket:
        haber={}
        if "news_item" in altetiket.tag:
          if "title" in altetiket[0].tag:
            haber['baslik']=altetiket[0].text
          if "url" in altetiket[2].tag:
            haber['url']=altetiket[2].text
          if "picture" in altetiket[3].tag:
            haber['resim']=altetiket[3].text
          if "source" in altetiket[4].tag:
            haber['kaynak']=altetiket[4].text

          haberler.append(haber)
          trend.update({"haberler":haberler})

      trendler.append(trend)
  return trendler

def trendEkle(baslik,aciklama,trafik,tarih,ulke,eklenme,key):
  conn=sqlite3.connect("trendbase.sqlite3")
  c=conn.cursor()
  sonuc=trendVarmi(baslik,tarih)
  if sonuc!=True:
    c.execute("INSERT INTO trendler VALUES(?,?,?,?,?,?,?)",(baslik,aciklama,trafik,tarih,ulke,eklenme,key))
    conn.commit()

def haberEkle(trendkey,trend,baslik,url,aciklama,kaynak,resim,ulke):
  conn=sqlite3.connect("trendbase.sqlite3")
  c=conn.cursor()
  sonuc=haberVarmi(url)
  if sonuc!=True:
    c.execute("INSERT INTO haberler VALUES(?,?,?,?,?,?,?,?)",(trendkey,trend,baslik,url,aciklama,kaynak,resim,ulke))
    conn.commit()


def trendHaberEkle(ulke):
  trendler=trendGetir(ulke)
  for trend in trendler:
    baslik=trend.get("baslik")
    trafik=trend.get("trafik")
    aciklama=trend.get("aciklama")
    tarih=trend.get("tarih")
    key=str(uuid.uuid4())
    trendEkle(baslik,aciklama,trafik,tarih,ulke,str(datetime.datetime.today()),key)

    haberler=trend.get("haberler")

    for haber in haberler:
      if haber!=None:
        trendkey=key
        trend=baslik
        haberbaslik=haber.get("baslik")
        haberaciklama=haber.get("aciklama")
        haberurl=haber.get("url")
        haberkaynak=haber.get("kaynak")
        haberresim=haber.get("resim")
        haberEkle(trendkey,trend,haberbaslik,haberurl,haberaciklama,haberkaynak,haberresim,ulke)

def trendler(ulke="0",adet=100):
  conn=sqlite3.connect("trendbase.sqlite3")
  c=conn.cursor()
  komut="SELECT * FROM trendler"
  if ulke!="0":
    komut=komut + " WHERE ulke=?"
  komut=komut + f" LIMIT {adet}"
  if ulke!="0":
    c.execute(komut,(ulke,))
  else:
    c.execute(komut)
  sonuc=c.fetchall()
  return sonuc

def trendVarmi(baslik,tarih):
  conn=sqlite3.connect("trendbase.sqlite3")
  c=conn.cursor()
  c.execute("SELECT * FROM trendler WHERE baslik=? AND tarih=?",(baslik,tarih))
  sonuc=c.fetchall()
  if len(sonuc)>0:
    return True
  else:
    return False

def haberVarmi(url):
  conn=sqlite3.connect("trendbase.sqlite3")
  c=conn.cursor()
  c.execute("SELECT * FROM haberler WHERE url=?",(url,))
  sonuc=c.fetchall()
  if len(sonuc)>0:
    return True
  else:
    return False

def haberler(ulke="*",adet=50):
  conn=sqlite3.connect("trendbase.sqlite3")
  c=conn.cursor()
  if ulke=="*":
    c.execute("SELECT * FROM haberler")
  else:
    c.execute("SELECT * FROM haberler WHERE ulke=?",(ulke,))

  sonuc=c.fetchmany(adet)
  return sonuc

def haberfromkey(key):
  conn=sqlite3.connect("trendbase.sqlite3")
  c=conn.cursor()
  komut="SELECT * FROM haberler WHERE trendkey=?"
  c.execute(komut,(key,))
  sonuc=c.fetchall()
  return sonuc


# SAYAC ekleyelim yani trendlerin ve haberlerin sayısını bulalım
def sayac():
  conn = sqlite3.connect("trendbase.sqlite3")
  c = conn.cursor()
  c.execute("SELECT * FROM trendler")
  trendsayac = len(c.fetchall())
  c.execute("SELECT * FROM haberler")
  habersayac = len(c.fetchall())

  # c.execute("SELECT COUNT(*) FROM trendler")
  # trendsayac=c.fetchone()
  # c.execute("SELECT COUNT(*) FROM haberler")
  # habersayac=c.fetchone()

  return trendsayac, habersayac