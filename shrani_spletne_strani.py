import requests
import os
import re
import sys
# koda bo najprej shranila vseh 9 spletnih strani, nato pa se bo sprehajala po teh straneh in jemala html-povezave do posameznih knjig
def pripravi_imenik(ime_datoteke):
    imenik = os.path.dirname(ime_datoteke)
    if imenik:
        os.makedirs(imenik, exist_ok=True)

def shrani_spletno_stran(url, ime_datoteke, vsili_prenos=False):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        print(f'Shranjujem {url} ...', end='')
        sys.stdout.flush()
        if os.path.isfile(ime_datoteke) and not vsili_prenos:
            print('shranjeno že od prej!')
            return
        r = requests.get(url, headers=headers)
        r.raise_for_status()  # Preverimo, ali je bila zahteva uspešna
    except:
        pripravi_imenik(ime_datoteke)
        with open(ime_datoteke, 'w', encoding='utf-8') as datoteka:
            datoteka.write(r.text)
            print('shranjeno!')

st_strani = 9
for stran in range(1, st_strani + 1):
    url = f"https://www.goodreads.com/list/show/24320.Books_With_a_Goodreads_Average_Rating_of_4_2_and_Above?page={stran}"
    shrani_spletno_stran(url, f"spletne_stranii/strani-{stran}.html")

def odpri_spletne_strani(st_strani):
    for stran in range(1, st_strani + 1):
        with open(f'spletne_stranii/strani-{stran}.html', 'r', encoding='utf-8') as dat:
            prebrano = dat.read()
        for povezava in re.finditer(r'<a class="bookTitle" itemprop="url" href="(.*?)"', prebrano):
            yield povezava.group(1)

def oblikuj_spletne_strani(st_strani):
    stevec = 1
    for del_url in odpri_spletne_strani(st_strani):
        url = f'https://www.goodreads.com{del_url}'
        shrani_kot = f'html_knjigee/knjigaa_{stevec}.html'
        shrani_spletno_stran(url, shrani_kot)
        stevec += 1

oblikuj_spletne_strani(st_strani)
