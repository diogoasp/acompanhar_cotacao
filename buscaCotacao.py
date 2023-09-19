# %%
import requests
from bs4 import BeautifulSoup
import configparser
import time
from win10toast import ToastNotifier

config = configparser.ConfigParser()
config.read('config.ini')
acoes = config['DEFAULT']['acoes'].split(',')

print("Executando...")
print("Página referência: {}\nAções observadas:".format(config['DEFAULT']['url_base']))

for acao in acoes:
    nome, meta = acao.split(':')
    min, max = meta.split('x')
    print("Metas: R${} > {} > R${}".format(min,nome,max))

time.sleep(10)

while True:
    data = {}
    txt = ""
    for acao in acoes:
        nome = acao.split(':')[0]
        html = requests.get(config['DEFAULT']['url_base'].format(nome)).content
        soup = BeautifulSoup(html, 'html.parser')
        valor = soup.find("div", class_="value").text.split('\n')[1].replace(',','.')
        try:
            valor = float(valor)
        except:
            valor = None
        data[nome] = valor
        txt += "{};{}\n".format(nome,valor)
    
    with open(config['DEFAULT']['out_file'], 'w') as f:
        f.write(txt)
    
    print("\nNo momento: {}".format(data))
    for acao in acoes:
        nome, meta = acao.split(':')
        min, max = meta.split('x')
        if (data[nome] != None) and ((data[nome] <= float(min)) or (data[nome] >= float(max))):
            print("!!! Alerta para {} com valor R${} !!!".format(nome, data[nome]))
            n = ToastNotifier()
            n.show_toast("Alerta para {}".format(nome), "{} com valor R${}!".format(nome, data[nome]), duration = int(config['DEFAULT']['notification_duration']), icon_path ="warning.ico")

    time.sleep(int(config['DEFAULT']['delay']))


