from flask import Flask, render_template, request,jsonify
from flask_cors import CORS,cross_origin
import requests
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen as uReq

app=Flask(__name__)

@app.route('/',methods = ['GET'])
def main_page():
    return render_template('login.html')
@app.route("/search" , methods = ['POST' , 'GET'])
def index():
    if request.method == 'POST':
        search_string=request.form['search'].replace(" ","")
        url="https://www.flipkart.com/search?q="+search_string
        flipkartPage = requests.get(url)
        print(flipkartPage.status_code)
        html_url = bs(flipkartPage.content, "html.parser")
        box1=html_url.findAll("div",{"class":"_1AtVbE col-12-12"})
        del box1[0:3]
        box=box1[0]
        product_link = "https://www.flipkart.com" + box.div.div.div.a["href"]
        print("product_link", product_link)
        f_Page = requests.get(product_link)
        req_cont=f_Page.content
        html_url1=bs(req_cont,"html.parser")
        # print(html_url1)
        c_box = html_url1.findAll("div",{"class":"_16PBlm"})
        print(c_box)
        reviews=[]
        for comments in c_box:
            # try:
            #     # name.encode(encoding='utf-8')
            #     name = comments.div.div.find_all('p', {'class': '_2sc7ZR _2V5EHH'})[0].text
            #
            # except:
            #     name="No Name Specify"
            #     print("name")
            #
            # try:
            #     # rating.encode(encoding='utf-8')
            #     rating = comments.div.div.div.div.text
            # except:
            #     rating = 'No Rating'
            #     print("rating")
            #
            # try:
            #     # commentHead.encode(encoding='utf-8')
            #     commentHead = comments.div.div.div.p.text
            #
            # except:
            #     commentHead = 'No Comment Heading'
            #     print(commentHead)
            # try:
            #     comtag = comments.div.div.find_all('div', {'class': ''})
            #     # custComment.encode(encoding='utf-8')
            #     custComment = comtag[0].div.text
            # except Exception as e:
            #     custComment="No commects"
            #     print(custComment)

            try:
                # name.encode(encoding='utf-8')
                rating = comments.div.div.div.div.text
            except:
                print("rating")
            try:
                # name.encode(encoding='utf-8')
                caption = comments.div.div.div.p.text
            except:
                print("rating")
            try:
                # name.encode(encoding='utf-8')
                comtag = comments.div.div.find_all('div', {'class': ''})
                # custComment.encode(encoding='utf-8')
                custComment = comtag[0].div.text
            except:
                print("rating")
            try:
                # name.encode(encoding='utf-8')
                name = comments.div.div.find_all('p', {'class': '_2sc7ZR _2V5EHH'})[0].text
            except:
                print("rating")


            mydict = {"Product": search_string, "Name": name, "Rating": rating, "Comments": custComment,"commentHead": caption}
            print(mydict)
            reviews.append(mydict)
        print(reviews)
        return render_template('result.html',reviews=reviews[0:(len(reviews)-1)])

if __name__=="__main__":
    app.run(port=9000)