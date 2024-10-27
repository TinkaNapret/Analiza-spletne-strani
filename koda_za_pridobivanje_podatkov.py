import re
import html
import json
import os
import csv

# Regularni izrazi
vzorec_naslov = re.compile(r'<h1 class=".*?">(.*?)</h1>')
vzorec_avtor = re.compile(r'<span class="ContributorLink__name" data-testid="name">(.*?)</span>')
vzorec_leto = re.compile(r'<p data-testid="publicationInfo">.*?(\d{4})</p>')
vzorec_opis = re.compile(r'<span class="Formatted">(.*?)</span>', re.DOTALL)
vzorec_ocena = re.compile(r'<div class="RatingStatistics__rating" aria-hidden="true">(.*?)</div>')
vzorec_strani = re.compile(r'<p data-testid="pagesFormat">(\d+) pages.*?</p>')
vzorec_glasov = re.compile(r'<span data-testid="ratingsCount" aria-hidden="true">([\d,]+)<!--.*?ratings</span>')
vzorec_zanri = re.compile(r'<a href=".*?" class="Button Button--tag Button--medium"><span class="Button__labelItem">(.*?)</span></a>')

def poberi_podatke(pot_datoteke):
    with open(pot_datoteke, 'r', encoding='utf-8') as dat:
        html_vsebina = dat.read()

    naslov_match = vzorec_naslov.search(html_vsebina)
    avtor_match = vzorec_avtor.search(html_vsebina)
    leto_match = vzorec_leto.search(html_vsebina)
    opis_match = vzorec_opis.search(html_vsebina)
    ocena_match = vzorec_ocena.search(html_vsebina)
    strani_match = vzorec_strani.search(html_vsebina)
    glasov_match = vzorec_glasov.search(html_vsebina)
    zanri_matches = vzorec_zanri.findall(html_vsebina)

    naslov = naslov_match.group(1) if naslov_match else "Ni naslova"
    avtor = avtor_match.group(1) if avtor_match else "Ni avtorja"
    leto = int(leto_match.group(1)) if leto_match else "Ni leta"
    opis = opis_match.group(1) if opis_match else "Ni opisa"
    ocena = float(ocena_match.group(1).replace(',', '.')) if ocena_match else "Ni ocene"
    število_strani = int(strani_match.group(1)) if strani_match else "Ni števila strani"
    število_glasov = int(glasov_match.group(1).replace(',', '')) if glasov_match else "Ni števila glasov"
    zanri = [html.unescape(zanr).lower() for zanr in zanri_matches]

    # Omejitev na prvih 4 žanre
    zanri = zanri[:4]

    naslov = html.unescape(naslov)
    opis = re.sub(r'</?i>', '', re.sub(r'<.*?>', '', html.unescape(opis).replace("<br />", "").strip())).replace('\n', '').strip()

    return {
        "naslov": naslov,
        "avtor": avtor,
        "leto": leto,
        "opis": opis,
        "ocena": ocena,
        "število_strani": število_strani,
        "število_glasov": število_glasov,
        "žanri": zanri
    }

knjige = []

# Uporabi pravilno pot do mape
mapa_knjig = r'html_knjigee'
datoteke = [f for f in os.listdir(mapa_knjig) if f.startswith('knjigaa_') and f.endswith('.html')]

for datoteka in datoteke:
    pot_datoteke = os.path.join(mapa_knjig, datoteka)
    knjiga = poberi_podatke(pot_datoteke)
    knjige.append(knjiga)

# Shranjevanje v JSON datoteko
json_datoteka = os.path.join(os.path.dirname(__file__), "knjige.json")
with open(json_datoteka, "w", encoding='utf-8') as dat:
    json.dump(knjige, dat, indent=4, ensure_ascii=False)

# Shranjevanje v CSV datoteko
csv_datoteka = os.path.join(os.path.dirname(__file__), "knjige.csv")
with open(csv_datoteka, "w", newline='', encoding='utf-8') as csv_dat:
    fieldnames = ["naslov", "avtor", "leto", "število_strani", "opis", "žanri", "ocena", "število_glasov"]
    writer = csv.DictWriter(csv_dat, fieldnames=fieldnames)
    writer.writeheader()
    for knjiga in knjige:
        knjiga["žanri"] = ", ".join(knjiga["žanri"])  # Pretvori seznam žanrov v string
        writer.writerow(knjiga)

# Izpis povezave do JSON in CSV datotek
print(f"Podatki so bili uspešno shranjeni v '{json_datoteka}' in '{csv_datoteka}'.")
