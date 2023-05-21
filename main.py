import csv
from bs4 import BeautifulSoup
import spacy
import urllib3
import requests.exceptions
import json

nlp = spacy.load('en_core_web_md')

keywords = ['sofa', 'armchair', 'recliner', 'ottoman', 'table', 'desk', 'bookshelf', 'cabinet', 'bed', 'dresser', 'mirror', 'lamp', 'chair', 'stool', 'bench', 'chaise', 'rug', 'couch', 'futon', 'loveseat', 'sectional', 'rocker', 'glider', 'cradle', 'crib', 'bassinet', 'wardrobe', 'armoire', 'shelf', 'drawer', 'pillow', 'mattress', 'blanket', 'comforter', 'quilt', 'duvet', 'sheet', 'nightstand', 'sideboard', 'hutch', 'buffet', 'tray', 'planters', 'vase', 'bookcase', 'fan', 'clock', 'divider', 'screen', 'lounger', 'stacking', 'ottoman', 'cart', 'trolley', 'tray', 'serving', 'dining', 'arm', 'accent', 'side', 'coffee', 'end', 'console', 'tv', 'stand', 'media', 'cabinet', 'fireplace', 'mantel', 'heater', 'safe', 'shelving', 'display', 'cupboard', 'showcase', 'buffet', 'vanity', 'sink', 'faucet', 'showerhead', 'towel', 'robe', 'hamper', 'basket', 'waste', 'bin', 'container', 'bar', 'counter', 'pub', 'bistro', 'dining', 'tabletop', 'folding', 'nesting', 'serving', 'tray', 'trolley', 'kitchen', 'island']

data = []
def is_furniture_product(text,id,url):
    doc = nlp(text)
    #print(doc)
    for ent in doc:
        # print (ent.label_)
        # print(ent.text.lower())
        if ent.text.lower() in keywords:
            data.append({"url":url,"id":id,"text":doc,"valoare":ent.text.lower()})
            return 1
    return 0

with open('paginiweb.csv') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        id=0
        if row[0].startswith('http'):
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
            http = urllib3.PoolManager(cert_reqs='CERT_NONE')
            try:
                response = http.request('GET', row[0])
                print(response.status)
                if response.status == 200:
                    html = response.data.decode('utf-8')
                    soup = BeautifulSoup(html, "html.parser")
                    p_tags = soup.find_all("p", string=True)+soup.find_all("h1", string=True)+soup.find_all("h2", string=True)+soup.find_all("h3", string=True)+soup.find_all("h4", string=True)+soup.find_all("h5", string=True)+soup.find_all("h6", string=True)+soup.find_all("title", string=True)
                    for tag in p_tags:
                        #print((tag.text.split()))
                        if is_furniture_product((tag.text),id,row[0]):
                            id=id+1
            except (UnicodeDecodeError) as err:
                print(f"Error: {err}")
                pass
            except (urllib3.exceptions.NewConnectionError,requests.exceptions.SSLError, urllib3.exceptions.EmptyPoolError, urllib3.exceptions.ProtocolError, urllib3.exceptions.MaxRetryError, urllib3.exceptions.TimeoutError, requests.exceptions.ConnectionError, requests.exceptions.ReadTimeout) as e:
                print(f"Error: {e}")
                pass

print(data)
data_dict = []
for d in data:
    d_dict = {}
    for k, v in d.items():
        if isinstance(v, spacy.tokens.doc.Doc):
            d_dict[k] = v.text
        else:
            d_dict[k] = v
    data_dict.append(d_dict)

with open('data.json', 'w') as save_file:
    json.dump(data_dict, save_file, indent=6)