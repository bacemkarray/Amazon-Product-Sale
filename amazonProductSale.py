import requests
import smtplib, ssl



#Before running the script, enter your app password here (see https://stackoverflow.com/a/27515833 for information)
password = "Enter app password here"

#Enter the ASIN number of the product you want to keep track of
asin = "Enter ASIN number here"

def send_email(product_url, password):
    port = 465
    context = ssl.create_default_context()

    #Create secure connection with Gmail SMTP server and send email
    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
        server.login("productsaleproject@gmail.com", password)
        sent_from = "productsaleproject@gmail.com"
        sent_to = sent_from  
        email_text = '''Hello,
              
        You are receiving this email to let you know that the product you have expressed interest in has gone on sale. 
        It can be found at this url: %s ''' % product_url
        server.sendmail(sent_from, sent_to, email_text)
    


#Sends request to API to retrieve the product ifnormation
url = "https://real-time-amazon-data.p.rapidapi.com/product-details"

querystring = {"asin":asin, "country":"US"}

headers = {
	"x-rapidapi-key": "Enter your API key (visit https://rapidapi.com/ajmorenodelarosa/api/amazon-price1 to get one free of charge)",
	"x-rapidapi-host": "real-time-amazon-data.p.rapidapi.com"
}

response = requests.get(url, headers=headers, params=querystring)



#Formats data from the response into necessary format
jsonFormat = response.json()
productPriceCurrent = str(jsonFormat['data']['product_price']).replace("$","")
productPriceOriginal = str(jsonFormat['data']['product_original_price']).replace("$","")

#Checks to see if there's a sale, if so will call email function
if productPriceOriginal != "None": 
    if float(productPriceCurrent) <= float(productPriceOriginal):
        send_email(jsonFormat['data']['product_url'], password)
