import glob
import csv
from bs4 import BeautifulSoup

receipts = [f for f in glob.glob("receipts/*.html")]

receipt = receipts[0]
with open("payments.csv", "w") as csv_file:
    показатели = [
        "Горячее водоотведение",
        "Горячее водоснабжение",
        "Холодное водоотведение",
        "Холодное водоснабжение",
        "Отопление",
        "Обслуживание дома",
        "Итого начислено, руб.",
    ]
    csv_file.write(",".join((x.replace(",", "") for x in показатели)) + "\n")
    for receipt in receipts:
        with open(receipt, encoding="utf8") as r:
            soup = BeautifulSoup(r, "html.parser")
            коммунальные = 0
            всего_начислено = {}
            for показатель in показатели:
                элементы = soup.find_all("td", string=показатель)
                начислено = float(
                    элементы[1]
                    .parent.find_all("td")[-1]
                    .text.replace(" ", "")
                    .replace(",", ".")
                    or 0
                    if элементы and len(элементы) > 1
                    else 0
                )
                коммунальные += (
                    начислено if показатель != "Итого начислено, руб." else 0
                )
                всего_начислено[показатель] = начислено

            всего_начислено["Обслуживание дома"] = (
                всего_начислено["Итого начислено, руб."] - коммунальные
            )
            csv_file.write(",".join(map(str, всего_начислено.values())) + "\n")
