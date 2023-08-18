from bs4 import BeautifulSoup
import requests,openpyxl

excel=openpyxl.Workbook()
print(excel.sheetnames)
sheet=excel.active
sheet.title="Top rated movies"
sheet.append(["Movie Rank","Movie name"," Release Year"," Rating "])

url=requests.get("https://www.imdb.com/chart/top/")
url.raise_for_status()
soup=BeautifulSoup(url.text,"html.parser")
# print(soup)
b=soup.find('tbody',class_="lister-list").find_all("tr")
for i in b:
    name=i.find("td",class_="titleColumn").a.text
    rank=int(i.find("td",class_="titleColumn").get_text(strip=True).split('.')[0])
    year=i.find("td",class_="titleColumn").span.text.strip("()")
    rating=i.find("td",class_="ratingColumn imdbRating").strong.text
    print(rank,name,year,rating)
    sheet.append([rank,name,year,rating])

excel.save('IMDB Movies Rating.xlsx')


