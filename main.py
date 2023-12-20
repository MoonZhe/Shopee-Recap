import datetime
import json
import os

import requests


def main():

    __location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))
    file_path = os.path.join(__location__, "cookie.json")
    with open(file_path, "r") as f:
        data = json.load(f)

    cookie = data["cookie"]
    
    currentYearItems = []
    offset = 0
    finalTotal = 0.00
    yearChecker = True
    desiredStatuses = ["label_order_completed", "label_preparing_order", "label_on_the_way"]
    
    while yearChecker == True:
        print("Order count atm: " + str(offset))
        url = 'https://shopee.com.my/api/v4/order/get_all_order_and_checkout_list?limit=20&offset=' + str(offset) 
    
        headers = {
            "Cookie": cookie,
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }
        
        response = requests.request("GET", url, headers=headers)
        
        if response.status_code == 200:
            responseData = response.json()
            
            offset = responseData["data"]["next_offset"]
            currResponse = responseData["data"]["order_data"]["details_list"]
            
            for c in currResponse:
                if c["status"]["status_label"]["text"] in desiredStatuses:
                    ctime = c["shipping"]["tracking_info"]["ctime"]
                    if ctime:
                        dateTimeObj = datetime.datetime.fromtimestamp(ctime)
                        currYear = datetime.datetime.now().year
                        dateTimeYear = dateTimeObj.year
                        
                        if currYear != dateTimeYear:
                            yearChecker = False
                            print(str(currYear - 1) + "'s order found, calculating total spent and writing to file now...")
                            break
                            

                    finalTotal += float(f"{c['info_card']['final_total'] / 100000:.2f}")
                
            currentYearItems.append(currResponse)
        else:
            print("error")
            
    combined_list = [item for sublist in currentYearItems for item in sublist]
    with open('all_purchases.json', 'w') as file:
        json.dump(combined_list, file, indent=4) 
    print("Oh well, you've spent " + str(round(finalTotal, 2)))
    
main()
