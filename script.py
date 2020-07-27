from bs4 import BeautifulSoup as soup  # HTML data structure
import requests
import csv
import sys
import os
import json
import re


# if(restaurant_url == None):
#     print("Enter restaurant url.........................")
#     return
# print("Wait while fecthing Details.......................")
print("Give restaurant URL!")
restaurant_url=input()
print("restaurant_url:"+restaurant_url)
request = requests.get(restaurant_url)
html = request.text

# parses html into a soup data structure to traverse html
# as if it were a json data type.

page_soup = soup(html, "html.parser")
containers = page_soup.findAll(
    "li", {"class": ["dish-card", "h-product hrecipe", "menu__item"]})
Address = page_soup.find("p", {"class": "vendor-location"}).text
Name = page_soup.find("h1", {"class": "fn"}).text
Delivery_hours = page_soup.find(
    "ul", {"class": "vendor-delivery-times"}).li.text.strip().replace(" ", "")

# print(Name)
# print("Address = "+Address)
# print(str(Delivery_hours).replace(" ", ""))
# print(len(containers))

# if not os.path.exists("Restaurants_CSV"):
#     os.makedirs("Restaurants_CSV")
out_file = open("output.csv", "w", newline='', encoding="utf-8")
out_file_fields = ['sr_no', 'category', 'subcategory',
                    'dish_name', 'price', 'description', 'chef_special', 'preparation_time', 'veg', 'non-veg',
                    'image_url'
                    ]
writer = csv.DictWriter(out_file, out_file_fields)
writer.writeheader()
sr_no = 1
description = ""
image_url = ""
price = ""
subcategory = ""
dish_name = ""

for i in containers:
    description = ""
    image_url = ""
    veg = "Y"
    non_veg = "N"
    try:
        price = str(
            i.find("span", {"class": ["price", "p-price"]}).text).strip().replace(" ", "")
        price = (''.join(i for i in price if (
            i.isdigit() or i == '.' or i == '0')))
        price = price.split('.')
        price = price[0]+"."+price[1][:2]
        subcategory = category = str(i["data-menu-category"])
        dish_name = str(i.span.text)

    except:
        pass
    try:
        description = str(
            i.find("p", {"class": "dish-description"}).text).strip()
    except:
        pass
    try:
        image_url = str(
            i.find("div", {"class": ["photo", "u-photo", "b-lazy"]})["data-src"])
        # image_url = str(json.loads(i['data-object'])['file_path'])
    except:
        pass
    non_veg_content = str(dish_name+description).lower()
    if "chicken" in non_veg_content or "pork" in non_veg_content or "beef" in non_veg_content or "mutton" in non_veg_content or "murgh" in non_veg_content or "gosht" in non_veg_content or "lamb" in non_veg_content or "fish" in non_veg_content:
        non_veg = "Y"
        veg = "N"
    writer.writerow({"price": price,
                        "dish_name": re.sub(r'[^\x00-\x7F]+', '', dish_name),
                        "category": re.sub(r'[^\x00-\x7F]+', '', category),
                        "subcategory": re.sub(r'[^\x00-\x7F]+', '', subcategory),
                        "image_url": image_url,
                        "sr_no": sr_no,
                        "preparation_time": 20,
                        "veg": veg,
                        "non-veg": non_veg,
                        "image_url": image_url,
                        "description": re.sub(r'[^\x00-\x7F]+', '', description)
                        })
    sr_no += 1
out_file.close()
# return {"address": Address,
#         "restaurant_name": Name.replace("'", "_"),
#         "delivery_hours": Delivery_hours}
