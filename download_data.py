#
# import urllib.request
# path = r"data/"
# myProxy = urllib.request.ProxyHandler({'http': '127.0.0.2'})
# openProxy = urllib.request.build_opener(myProxy)
# for data in ['confirmed','deaths','recovered']:
#     # link = "https://data.humdata.org/hxlproxy/data/download/time_series_covid19_"+data+"_global_narrow.csv"
#     link = r"https://data.humdata.org/hxlproxy/data/download/time_series_covid19_data_global_narrow.csv"
#     urllib.request.urlretrieve(link, data+".csv")

#
#
# from bs4 import BeautifulSoup
# Python 3.x
# from urllib.request import urlopen, urlretrieve, quote
# from urllib.parse import urljoin
#
# # Remove the trailing / you had, as that gives a 404 page
# url = 'https://data.humdata.org/dataset/novel-coronavirus-2019-ncov-cases'
# u = urlopen(url)
# try:
#     html = u.read().decode('utf-8')
# finally:
#     u.close()
#
# soup = BeautifulSoup(html, "html.parser")
#
# # Select all A elements with href attributes containing URLs starting with http://
# for link in soup.select('a[href^="http://"]'):
#     href = link.get('href')
#
#     # Make sure it has one of the correct extensions
#     if not any(href.endswith(x) for x in ['.global_narrow.csv']):
#         continue
#
#     filename = href.rsplit('/', 1)[-1]
#     print("Downloading %s to %s..." % (href, filename) )
#     urlretrieve(href, filename)
#     print("Done.")

# import csv
# import requests
#
# CSV_URL = "https://data.humdata.org/hxlproxy/data/download/time_series_covid19_confirmed_global_narrow.csv"
#
#
# with requests.Session() as s:
#     download = s.get(CSV_URL)
#
#     decoded_content = download.content.decode('utf-8')
#
#     cr = csv.reader(decoded_content.splitlines(), delimiter=',')
#     my_list = list(cr)
#     for row in my_list:
#         print(row)

import socket
import requests

URL = "https://data.humdata.org/hxlproxy/data/download/time_series_covid19_confirmed_global_narrow.csv"

if socket.gethostbyname(socket.gethostname()).startswith(('8', '9', '7')):
    r = requests.get(URL, stream=True, proxies={'http': 'http://10.10.1.10:3128', 'https': 'http://10.10.1.10:1080'})
else:
    r = requests.get(URL, stream=True)

with open(r'data/confirmed.csv', 'wb') as f:
    for chunk in r:
        f.write(chunk)
