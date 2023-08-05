from datetime import datetime
from dateutil.parser import parse

date_a_convertir = "27 mars 2023"
test = ""
mois_traduction_fr_to_anglais = {
    "janvier": "january",
    "février": "february",
    "mars": "march",
    "avril": "april",
    "mai": "may",
    "juin": "june",
    "juillet": "july",
    "août": "august",
    "septembre": "september",
    "octobre": "october",
    "novembre": "november",
    "décembre": "december"
}
for mois in list(mois_traduction):
    if mois in date_a_convertir:
        date_a_convertir = date_a_convertir.replace(mois,mois_traduction[mois])


try:
    date_obj = date_obj = parse(date_a_convertir)
except:
    formats = ['%d %B %Y', '%d %B %Y', '%d/%m/%Y', '%Y-%m-%d','%d %B %Y']
    for fmt in formats:
        try:
            date_obj = datetime.strptime(date_a_convertir, fmt)
            break
        except ValueError:
            continue
print(date_obj)
