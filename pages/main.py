import streamlit as st
import fonksiyonlar as ft

ulkeler=["TR"]

for ulke in ulkeler:
    ft.trendHaberEkle(ulke)

sayac=ft.sayac()
st.sidebar.write("Toplam Trend Sayısı : ",sayac[0])
st.sidebar.write("Toplam Haber Sayısı : ",sayac[1])


ulkesec=st.sidebar.multiselect("Ülke Seç",ulkeler)


trendler=ft.trendler()
trendler.reverse()
haberler=ft.haberler()
haberler.reverse()

###st.dataframe(trendler)
###st.dataframe(haberler)

st.header("Güncel Trendler ve Haberler")

for t in trendler:
    with st.expander(t[0]):
        st.write(t[1],t[2],t[3])
        thaberler=ft.haberfromkey(t[6])
        for thaber in thaberler:
            st.link_button(thaber[2],thaber[3])
            #st.image(thaber[6])




