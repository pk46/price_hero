# coding=<utf-8>

import requests, csv, sys, random
from bs4 import BeautifulSoup
from time import sleep

zdrojs = "soubory/abra.csv"
heurekas = "soubory/heureka.csv"
vysledkys = "soubory/vysledky.csv"

with open(vysledkys, 'w'):  # přepíše/vymaže soubor s výsledky
	pass

produkt = []
cena = []
kodh = []
odkazh = []

try:
	with open(zdrojs, encoding="utf-8") as zdroj:  # otevře a automaticky zavře soubor
		reader = csv.reader(zdroj, delimiter=";", skipinitialspace=True)
		for line in reader:  # Pro každý řádek v souboru
			sloupec0 = line[0]  # Načtení sloupce 1
			sloupec1 = line[1]  # Načtení sloupce 2
			produkt.append(sloupec0.replace(" ", ""))  # odebrání mezer a přidání hodnot do seznamu
			cena.append(sloupec1.replace(" ", ""))  # odebrání mezer a přidání hodnot do seznamu
except FileNotFoundError:
	print("V adresáři \"soubory\" chybí soubor \"abra.csv\"", "\n" + "Pro ukončení stiskni Enter")
	input()
	sys.exit(1)

try:
	with open(heurekas, encoding="utf-8") as heureka:  # otevře a automaticky zavře soubor
		reader = csv.reader(heureka, delimiter=",", skipinitialspace=True)
		header = next(reader)  # Přeskočení prvního řádku (hlavičky)
		for line in reader:  # Pro každý řádek v souboru
			sloupec7 = line[6]  # Načtení sloupce 7 - kód produktu
			kodh.append(sloupec7)  # přidání do seznamu
			sloupec9 = line[8]  # Načtení sloupce 9 - všeobecného odkazu na Heruéku
			odkazh.append(sloupec9)  # přidání do seznamu
except FileNotFoundError:
	print("V adresáři \"soubory\" chybí soubor \"heureka.csv\"", "\n" + "Pro ukončení stiskni Enter")
	input()
	sys.exit(1)

if len(produkt) > 100:
	print("Z technických důvodů nelze porovnávat více než 100 položek najednou", "\n" + "Pro ukončení stiskni Enter")
	input()
	sys.exit(1)
else:
	pass

if len(produkt) < 20:
	print("Počet srovnávaných položek je nižší než 20, a proto pracuji plnou rychlostí.")
elif len(produkt) > 19 and len(produkt) < 41:
	print("Počet srovnávaných položek je mezi 20 a 40, a proto snižuji rychlost zpracování.")
else:
	print("Počet srovnávaných položek je nad 40, a proto výrazně snižuji rychlost zpracování.")

nekody = []
popisy = []
obchody = []
ceny = []
odkazy = []
popisyf = []
obchodyf = []
cenyf = []
odkazyf = []
procentaf = []
useragent = [
	"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36",
	"Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML like Gecko) Chrome/44.0.2403.155 Safari/537.36",
	"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML like Gecko) Chrome/51.0.2704.79 Safari/537.36 Edge/14.14931",
	"Mozilla/5.0 (X11; Linux i686; rv:64.0) Gecko/20100101 Firefox/64.0",
	"Mozilla/5.0 (Windows NT 6.1; WOW64; rv:64.0) Gecko/20100101 Firefox/64.0",
	"Opera/9.80 (X11; Linux i686; Ubuntu/14.10) Presto/2.12.388 Version/12.16",
	"Opera/9.80 (Macintosh; Intel Mac OS X 10.14.1) Presto/2.12.388 Version/12.16",
	"Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36",
	"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.4 (KHTML, like Gecko) Chrome/22.0.1250.0 Iron/22.0.2150.0 Safari/537.4",
	"Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.4 (KHTML, like Gecko) Chrome/22.0.1250.0 Iron/22.0.2150.0 Safari/537.4",
	"Mozilla/5.0 (X11; U; Linux amd64) Iron/21.0.1200.0 Chrome/21.0.1200.0 Safari/537.1",
	"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1200.0 Iron/21.0.1200.0 Safari/537.1"
]

for i, kod in enumerate(produkt):  # procházení seznamu "produkt"
	print("Nyní zpracovávám", kod, "{0}{1}".format(i + 1, "."), "z", len(produkt))
	if kod in kodh:
		x = kodh.index(kod)  # vrací index "kod" v seznamu "kodh"
		URL = odkazh[x]+"/#o=2"  # definice odkazu + řazení od nejnižší ceny
		headers = {'User-Agent': random.choice(useragent)}  # náhodný výběr useragenta ze seznamu "useragent"
		page = requests.get(URL, headers=headers)
		soup = BeautifulSoup(page.content, "html.parser")
		for title in soup.find_all(class_="desc__exit-link js-paragraph-to-shorten"):  # vyhledávání záchytného klíče v HTML
			title = title.text.strip()  # vypsání textu a odstranění netiskutelných znaků
			popisy.append(title)  # přidání hodnot do seznamu

		shop = soup.find_all(class_="shop-name")  # vyhledávání záchytného klíče v HTML
		for shop in shop:
			shop = shop.get_text().strip()  # získání potřebného textu a odstranění netisknutelných znaků
			obchody.append(shop)  # přidání hodnot do seznamu

		product = soup.find_all(class_="pr")  # vyhledávání záchytného klíče v HTML
		for product in product:
			product = product.get_text().split("Kč")[0].strip()  # výpis textu, rozdělení do tabulky, vypsání první
			# hodnoty a odstranění netisknutelných znaků
			product = product.replace(" ", "")
			ceny.append(float(product))  # odstranění mezer a přidání ceny do seznamu

		odkaz = soup.find_all(class_="link shop-name__link")  # vyhledávání záchytného klíče v HTML
		for odkaz in odkaz:
			odkaz = odkaz.get("href")  # výpis textu
			odkazy.append(odkaz)  # přidání do seznamu

		"""Mazání duplicitních eshopů ze seznamu """
		try:
			for n, m in enumerate(obchody):
				if obchody.count(m) > 1:
					obchody.pop(n)
					popisy.pop(n)
					ceny.pop(n)
					odkazy.pop(n)
		except IndexError:
			pass

		with open(vysledkys, mode="a") as finalnisoubor:
			writer = csv.writer(finalnisoubor, delimiter=";")
			writer.writerow([""])  # zapsání přázdného řádku
			writer.writerow([kod, odkazh[x]+"/#o=2", cena[i], "rozdíl v %"])  # zapsání hlaviček

		for g, h in enumerate(ceny):  # procházení seznamu "ceny"
			if h < float(cena[i]):  # podmínka
				cenyf.append(h)  # přidání hodnot splněných podmínek do seznamu
				popisyf.append(popisy[g])  # přidání hodnot splněných podmínek do seznamu
				obchodyf.append(obchody[g])  # přidání hodnot splněných podmínek do seznamu
				odkazyf.append(odkazy[g])  # přidání hodnot splněných podmínek do seznamu
				procentaf.append(format((h/float(cena[i])-1)*100, ".2f").replace(".", ","))

		"""Mazání duplicitních eshopů ze seznamu """
		for n, m in enumerate(obchodyf):
			if obchodyf.count(m) > 1:
				obchodyf.pop(n)
				popisyf.pop(n)
				cenyf.pop(n)
				odkazyf.pop(n)
				procentaf.pop(n)

		try:
			cenyf, popisyf, obchodyf, odkazyf, procentaf = (list(t) for t in zip(*sorted(zip(cenyf, popisyf, obchodyf, odkazyf, procentaf))))
		# seřadí všechny seznamy podle ceny vzestupně
		except ValueError:
			pass

		for c in range(len(cenyf)):
			try:
				cenyf.append(str(cenyf[c]).replace(".", ","))  # převod na string a přidání na konec seznamu
			except ValueError:
				cenyf.append(0)  # pokud je na daném indexu prázdná hodnota, přidá se nula
		del cenyf[:int(len(cenyf)/2)]  # mazání daného záznamu ze začátku seznamu

		if len(cenyf) < 1:
			with open(vysledkys, mode="a") as finalnisoubor:
				writer = csv.writer(finalnisoubor, delimiter=";")
				for row in zip([""], ["Nebylo nalezeno žádné porušení cen"]):
					writer.writerow(row)  # zapsání řádku
		else:
			with open(vysledkys, mode="a") as finalnisoubor:
				writer = csv.writer(finalnisoubor, delimiter=";")
				for row in zip(popisyf, obchodyf, cenyf, procentaf, odkazyf):  # procházení všemi seznamy najednou
					writer.writerow(row)  # zapsání hodnot do souboru

		del popisyf[:], cenyf[:], obchodyf[:], odkazyf[:], procentaf[:]  # mazání seznamu
		del popisy[:], ceny[:], obchody[:], odkazy[:]  # mazání seznamu

		if len(produkt) < 20:
			pass
		elif len(produkt) >= 20 and len(produkt) < 41:
			sleep(1)
		else:
			sleep(3)

	else:
		with open(vysledkys, mode="a") as finalnisoubor:
			writer = csv.writer(finalnisoubor, delimiter=";")
			writer.writerow([""])  # zapsání prázdného řádku
			for row in zip([kod], ["Nenalezeno v csv z Heuréky, zkusím to vyhledat...Vyhledávání však nemusí být "
								"přesné"]):  # definice textu, pokud nebyl produkt nalezen
				writer.writerow(row)  # zapsání řádku

		nekody.append(kod)
		filtr = []  # tento seznam slouží pro výsledky vyhledávání, kde je v ceně pomlčka (Heuréka vrací 3 typy
		# výsledků vyhledávání)

		vnazev = []  # seznam pro vyhledané položky
		vobchod = []  # seznam pro vyhledané položky
		vceny = []  # seznam pro vyhledané položky
		vodkaz = []  # seznam pro vyhledané položky

		vnazevf = []  # seznam pro vyfiltrované položky
		vobchodf = []  # seznam pro vyfiltrované položky
		vcenyf = []  # seznam pro vyfiltrované položky
		vodkazf = []  # seznam pro vyfiltrované položky
		vrozdilf = []

		"""Konflitky je seznam kódů Solight, které mají stejná počáteční písmena jako Skross"""
		konflikty = ["DC23", "DC33", "DC38", "DC38A", "DC39", "DC43", "DC44", "DC45", "DC46", "DC47", "DC48", "DC49",
					"DC50", "DC51", "DC60", "DC61", "DC62", "DN22", "DN25", "PA01-UK", "PA01-USA", "PA20", "PA21"]

		vkod = ""
		for j in nekody:
			ident = j.partition("-")[0]
			if len(ident) < 3 and "-" in j:
				if j[2] == "-" and j[0:2] == "FU":
					vkod = j.replace("FU-", "Fujitsu ")
				elif j[2] == "-" and j[0:2] == "CL":
					vkod = j.replace("CL-", "Case Logic ")
				elif j[2] == "-" and j[0:2] == "DS":
					vkod = j.replace("DS-", "Dyson ")
				elif j[2] == "-" and j[0:2] == "BN":
					vkod = j.replace("BN-", "Bandridge ")
				elif j[2] == "-" and j[0:2] == "TL":
					vkod = j.replace("TL-", "Thule ")
				elif j[2] == "-" and j[0:2] == "MR":
					vkod = j.replace("MR-", "Morphy Richards ")
				elif j[2] == "-" and j[0:2] == "AP":
					vkod = j.replace("AP-", "Agfaphoto ")
				elif j[2] == "-" and j[0:2] == "ND":
					vkod = j.replace("ND-", "Nedis ")
			elif len(j) == 3:  # toto slouží pro nejkratší kódy zn. Solight, např. V15
				vkod = "Solight " + j
			elif j[0:2] == "DC" and j not in konflikty:
				vkod = "Skross " + j
			elif j[0:2] == "DN" and j not in konflikty:
				vkod = "Skross " + j
			elif j[0:2] == "PA" and j not in konflikty:
				vkod = "Skross " + j
			elif j[3] == "-" and j[0:3] == "JCB":
				vkod = j.replace("JCB-", "JCB ")
			elif j[0:3] == "PRO":
				vkod = "Profigold " + j
			else:
				vkod = "Solight " + j

		URL2 = "https://www.heureka.cz/?h%5Bfraze%5D=" + vkod.replace(" ", "+") + "&min=&max=&o=3"
		headers = {'User-Agent': random.choice(useragent)}  # náhodný výběr useragenta ze seznamu "useragent"
		page = requests.get(URL2, headers=headers)
		soup = BeautifulSoup(page.content, "html.parser")

		chyba_nenalezeno = soup.select("p", string="Bohužel se nám nepodařilo najít produkt ")  # scrapování začne až od třídy class="pag", viz níže
		if "Bohužel se nám nepodařilo najít produkt " in chyba_nenalezeno[2]:
			with open(vysledkys, mode="a") as finalnisoubor:
				writer = csv.writer(finalnisoubor, delimiter=";")
				# writer.writerow([""])  # zapsání přázdného řádku
				writer.writerow([kod+" (Vyhledáno)", "Produkt nenalezen na Heurece"])  # zapsání hlaviček
		else:
			try:
				start = soup.select_one(".srovnani-result")  # scrapování začne až od třídy class="srovnani-result", viz níže

				for title in start.find_all_next(class_="desc"):
					title = title.h2.text
					vnazev.append(title)

				for shop in start.find_all_next(class_="shop-name"):
					shop = shop.get_text().strip()
					vobchod.append(shop)

				for product in start.find_all_next(class_="wherebuy js-serpSpamScore"):
					product = product.get_text().split("\n")[1]
					# price = product.split(" ")[0:2]
					price = product.replace("Kč", "").replace(" ", "")
					vceny.append(float(price))

				for odkaz in start.find_all_next(class_="pricen"):
					odkaz = odkaz.get("href")  # získání odkazu
					vodkaz.append(odkaz)  # přidání do seznamu
			except AttributeError:
				start = soup.select_one(".pag")  # scrapování začne až od třídy class="pag", viz níže

				try:
					for title in start.find_all_next(class_="desc"):
						title = title.h2.text
						vnazev.append(title)

					for shop in start.find_all_next(class_="shop-name"):
						shop = shop.get_text().strip()
						vobchod.append(shop)

					for product in start.find_all_next(class_="wherebuy js-serpSpamScore"):
						product = product.get_text().split("\n")[1]
						# price = product.split(" ")[0:2]
						price = product.replace("Kč", "").replace(" ", "")
						vceny.append(float(price))

					for odkaz in start.find_all_next(class_="pricen"):
						odkaz = odkaz.get("href")  # získání odkazu
						vodkaz.append(odkaz)  # přidání do seznamu
				except AttributeError:
					pass

		try:
			vceny, vnazev, vobchod, vodkaz = (list(t) for t in zip(
				*sorted(zip(vceny, vnazev, vobchod, vodkaz))))  # seřadí všechny seznamy podle ceny vzestupně
		except ValueError:
			pass

		if "Bohužel se nám nepodařilo najít produkt " in chyba_nenalezeno[2]:
			pass
		else:
			with open(vysledkys, mode="a") as finalnisoubor:
				writer = csv.writer(finalnisoubor, delimiter=";")
				writer.writerow([""])  # zapsání přázdného řádku
				writer.writerow([kod+" (Vyhledáno)", URL2, cena[i], "rozdíl v %"])  # zapsání hlaviček

		for k, l in enumerate(vceny):
			if l < float(cena[i]):
				vobchodf.append(vobchod[k])
				vnazevf.append(vnazev[k])
				vodkazf.append(vodkaz[k])
				vcenyf.append(l)
				vrozdilf.append(format((l/float(cena[i])-1)*100, ".2f").replace(".", ","))

		for i in range(len(vnazevf)):
			vnazevf.append(vnazevf[i].replace(u"\xb2", "2"))  # přidání na konec seznamu
		del vnazevf[:int(len(vnazevf)/2)]  # mazání daného záznamu ze začátku seznamu

		for c in range(len(vcenyf)):
			try:
				vcenyf.append(str(vcenyf[c]).replace(".", ","))  # převod na string a přidání na konec seznamu
			except ValueError:
				vcenyf.append(0)  # pokud je na daném indexu prázdná hodnota, přidá se nula
		del vcenyf[:int(len(vcenyf)/2)]  # mazání daného záznamu ze začátku seznamu

		if "Bohužel se nám nepodařilo najít produkt " in chyba_nenalezeno[2]:
			pass
		else:
			if len(vcenyf) < 1:
				with open(vysledkys, mode="a") as finalnisoubor:
					writer = csv.writer(finalnisoubor, delimiter=";")
					for row in zip([""], ["Nebylo nalezeno žádné porušení cen"]):
						writer.writerow(row)  # zapsání řádku
			else:
				with open(vysledkys, mode="a") as finalnisoubor:
					writer = csv.writer(finalnisoubor, delimiter=";")
					for row in zip(vnazevf, vobchodf, vcenyf, vrozdilf, vodkazf):  # procházení všemi seznamy najednou
						writer.writerow(row)  # zapsání hodnot do souboru

		# print("Vobchod", vobchod)
		# print("Vnazev", vnazev)
		# print("Vceny", vceny)
		# print("vodkaz", vodkaz)
		# print("--------------")
		# print("Vobchodf", vobchodf)
		# print("Vnazevf", vnazevf)
		# print("Vcenyf", vcenyf)
		# print("vodkazf", vodkazf)
		# print("filtr", filtr)
		del vobchod[:], vnazev[:], vceny[:], vodkaz[:]
		del vobchodf[:], vnazevf[:], vcenyf[:], vodkazf[:], vrozdilf[:]
		del filtr[:]

		if len(produkt) < 20:
			pass
		elif len(produkt) >= 20 and len(produkt) < 41:
			sleep(1)
		else:
			sleep(3)

print("hotovo", "\n"+"Výsledky najdeš v souboru \"soubory/vysledky.csv\""+"\n"+"Stiskni ENTER pro ukončení")
input()
