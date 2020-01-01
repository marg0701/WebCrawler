
import pandas as pd
import requests
from bs4 import BeautifulSoup
from newspaper import Article
import pandas as pd
import logging
from datetime import datetime,date,time

#Los headers es para que el sitio nos considere un navegador:

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36'}

Elpais_url = "https://elpais.com/internacional/"
Excelsior_url = "https://www.excelsior.com.mx/global#view-1"
CNN_url = "https://cnnespanol.cnn.com/seccion/mundo/"

def GetURLsFromElpais(url):
    #Esta función obtiene los url de las noticias internacionales de Elpais.com
    logging.info('Getting URLs from El Pais')
    
    #Hacer la petición al sitio:
    r = requests.get(url, headers = headers)

    #Crear el obtjeto BeautifulSoup:
    soup = BeautifulSoup(r.content, "html.parser")
    
    #Lista vacia para guardar los URLs

    data = []

    #Buscar los elementos noticia y obtener su url:
    for links in soup.find_all('div', class_='articulo__interior'):

        #el atributo href es el que contiene el URL
        urls = links.a['href']

        data.append(urls)

    return data

#Obtener los ulr de las noticias de Excelsior:
def GetURLsFromExcelsior(url):
    #Esta función obtiene los url de las noticias internacionales del Excelsior:
    logging.info('Getting URLs from Excelsior')

    #Hacer la petición al sitio:
    r = requests.get(url, headers = headers)

    #Crear el obtjeto BeautifulSoup:
    soup = BeautifulSoup(r.content, "html.parser")
    
    #Lista vacia para guardar los URLs

    data = []

    #Buscar los elementos noticia y obtener su url:
    for links in soup.find_all('div', class_= "item-notas-canal prelative left"):

        #el atributo href es el que contiene el URL
        urls = links.a['href']
        urls = "http://" + urls

        data.append(urls)
    
    return data

#Obtener los ulr de las noticias de Excelsior:
def GetURLsFromCNN(url):
    #Esta función obtiene los url de las noticias internacionales del Excelsior:
    logging.info("Getting URLs from CNN news")

    #Hacer la petición al sitio:
    r = requests.get(url, headers = headers)

    #Crear el obtjeto BeautifulSoup:
    soup = BeautifulSoup(r.content, "html.parser")
    
    #Lista vacia para guardar los URLs

    data = []

    #Buscar los elementos noticia y obtener su url:
    
    for article_ in soup.find_all('article', class_="news news--summary news--summary-big post-type--video"):
              
        for divs in article_.find_all('div', class_ = "news__data"):

            for h2s in divs.find_all('h2', class_ = "news__title"):

                #el atributo href es el que contiene el URL
                urls = h2s.a['href']
                data.append(urls)
        

    return data


def CreateDfFromURLs(urls,name_df):
    #Esta funcion recibe una lista de URLS y obtiene el contenido de esas paginas
    
    logging.info("Creating a data frame with the news")
    #Listas para guardar los datos que se van obteniendo:
    Titles = []
    Dates = []
    Authors = []
    Contents = []
    Links = []
    #Para cada url :
    for url in urls:
        try:
            #Crear el objeto y descarlo:
            #article = Article(url)

            article = Article(url, language='es') # Español
            article.download()
            article.html
            article.parse()

            #Obtener sus atributos y agregarlos a las listas correspondientes:
            Links.append(url)

            if article.title != []:
                Titles.append(article.title)
            else:
                Titles.append([None])

            if article.publish_date != []:
                #Fecha = str(article.publish_date).split(" ")
                #Fecha = Fecha[0]
                Dates.append(article.publish_date)
            
            else:
                Dates.append([None])

            if article.authors != []:
                Authors.append(article.authors)
            else:
                Authors.append([None])

            if article.text != []:
                Contents.append(article.text)
            else:
                Contents.append([None])
        except:
            logging.warning("It does not seem a new, next")
            #continue
    #Crear un data frame con todos los datos obtenidos:
    DF = {"Title":Titles,"Date":Dates,"Authors":Authors,"Content":Contents,"URL":Links}
    #Devolver el dataframe:
    DF = pd.DataFrame(DF)

    #DF.to_csv(name_df, encoding="utf-8")

    return DF

def CreateDfForElPais(urls,name_df):
    #Esta funcion recibe una lista de URLS y obtiene el contenido de esas paginas
    logging.info("Creating a data frame for El pais with the news")
    
    #Listas para guardar los datos que se van obteniendo:
    Titles = []
    Dates = []
    Hours = []
    Authors = []
    Contents = []
    Links = []
    #Para cada url :
    for url in urls:
        try:
            #Crear el objeto y descarlo:
            #article = Article(url)

            article = Article(url, language='es') # Español
            article.download()
            article.html
            article.parse()

            #Obtener sus atributos y agregarlos a las listas correspondientes:
            
            Links.append(url)
            
            try:
                
                Date, Hour = GetDatesFromElpais(url)
                if Date == "":
                    Date = None
                if Hour == "":
                    Hour = None
                
            except:
                
                Date = None
                Hour = None

            Dates.append(Date)
            Hours.append(Hour)

            if article.title != []:
                Titles.append(article.title)
            else:
                Titles.append([None])
            
            if article.authors != []:
                Authors.append(article.authors)
            else:
                Authors.append([None])
            if article.text != []:
                Contents.append(article.text)
            else:
                Contents.append([None])
            

            

        except:
            logging.warning("It does not seem a new of El pais, next")
            #continue

    #Crear un data frame con todos los datos obtenidos:
    DF = {"Title":Titles,"Date":Dates,"Hour":Hours,"Authors":Authors,"Content":Contents,"URL":Links}
    DF = pd.DataFrame(DF)
    #DF.to_csv(name_df, encoding="utf-8")
    return DF

def CreateDfForCNN(urls,name_df):
    #Esta funcion recibe una lista de URLS y obtiene el contenido de esas paginas
    
    logging.info("Creating a data frame with the news")
    #Listas para guardar los datos que se van obteniendo:
    Titles = []
    Dates = []
    Hours = []
    Authors = []
    Contents = []
    Links = []
    #Para cada url :
    for url in urls:
        try:
            #Crear el objeto y descarlo:
            #article = Article(url)

            article = Article(url, language='es') # Español
            article.download()
            article.html
            article.parse()

            #Obtener sus atributos y agregarlos a las listas correspondientes:
            Links.append(url)

            if article.title != []:
                Titles.append(article.title)
            else:
                Titles.append([None])

            if article.publish_date != []:
                #Fecha = str(article.publish_date).split(" ")
                #Fecha = Fecha[0]
                Publish= str(article.publish_date)

                Fecha = Publish[:-15]
                Hora = Publish[11:-6]
                Dates.append(Fecha)
                Hours.append(Hora)
            
            else:
                Dates.append([None])

            if article.authors != []:
                Authors.append(article.authors)
            else:
                Authors.append([None])

            if article.text != []:
                Contents.append(article.text)
            else:
                Contents.append([None])
        except:
            logging.warning("It does not seem a new, next")
            #continue
    #Crear un data frame con todos los datos obtenidos:
    DF = {"Title":Titles,"Date":Dates,"Hour":Hours,"Authors":Authors,"Content":Contents,"URL":Links}
    #Devolver el dataframe:
    DF = pd.DataFrame(DF)
    
    #DF.to_csv(name_df, encoding="utf-8")
    return DF

def CreateDfForExcelsior(urls,name_df):
    #Esta funcion recibe una lista de URLS y obtiene el contenido de esas paginas
    
    logging.info("Creating a data frame with the news")
    #Listas para guardar los datos que se van obteniendo:
    Titles = []
    Dates = []
    Hours = []
    Authors = []
    Contents = []
    Links = []
    #Para cada url :
    for url in urls:
        try:
            #Crear el objeto y descarlo:
            #article = Article(url)

            article = Article(url, language='es') # Español
            article.download()
            article.html
            article.parse()

            #Obtener sus atributos y agregarlos a las listas correspondientes:
            Links.append(url)

            if article.title != []:
                Titles.append(article.title)
            else:
                Titles.append([None])

            if article.publish_date != []:

                Date, Hour = SplitDatesOfExcelsior(article.publish_date)
                Dates.append(Date)
                Hours.append(Hour)
            
            else:
                Dates.append([None])

            if article.authors != []:
                Authors.append(article.authors)
            else:
                Authors.append([None])

            if article.text != []:
                Contents.append(article.text)
            else:
                Contents.append([None])
        except:
            logging.warning("It does not seem a new, next")
            #continue
    #Crear un data frame con todos los datos obtenidos:
    DF = {"Title":Titles,"Date":Dates,"Hour":Hours,"Authors":Authors,"Content":Contents,"URL":Links}
    #Devolver el dataframe:
    DF = pd.DataFrame(DF)
    
    #DF.to_csv(name_df, encoding="utf-8")
    return DF
def GetDatesFromElpais(url):
    #Esta función obtiene la fecha de cada noticia del Elpais.com
    logging.info('Getting Date from every new of El Pais')
    
    #Hacer la petición al sitio:
    r_ = requests.get(url, headers = headers)

    #Crear el obtjeto BeautifulSoup:
    soup_ = BeautifulSoup(r_.content, "html.parser")
    
    #Lista vacia para guardar los URLs

    time_ = soup_.find('time')
    date = time_["datetime"]
    Fecha = str(date)[:-15]
    Hora = str(date)[11:-6]
    if Fecha == "":
        Fecha = None
    if Hora == "":
        Hora = None
    #Buscar los elementos noticia y obtener su url:
    return Fecha, Hora

def SplitDatesOfExcelsior(FechaDePublicacion):

    Date = str(FechaDePublicacion).split(" ")
 
    #A la fecha no le hacemos nada más
    Fecha = Date[0]

    #Separamos la hora de la diferencia horaria:
    Hora = str(Date[1]).split("-")

    #La hora es el primer elemento de la lista obtenida:
    Hora_  = Hora[0].split(":")
    

    #La diferencia el segundo elemento:
    diferencia = Hora[1].split(":")
    
    #Ajustar la diferencia de horarios:
    aaa = int(Hora_[0])-int(diferencia[0])
    if aaa < 0:
        aaa = 0

    #Rearmar la hora:
    #Hora = str(aaa) +":" + str(Hora_[1]) + ":" + str(Hora_[2])
    Hora = time(aaa,int(Hora_[1]),int(Hora_[2]))
    Hora = str(Hora)
    

    return Fecha, Hora

def UpdateNews(Elpais_url=Elpais_url,Excelsior_url=Excelsior_url,CNN_url=CNN_url):

    try:

        #Obtener los links de las noticias del día de hoy:
        
        URLs_ElPAIS = GetURLsFromElpais(Elpais_url)
        
        URLs_Excels = GetURLsFromExcelsior(Excelsior_url)
        URLs_CNN    = GetURLsFromCNN(CNN_url)

        #De los links obtenidos, traer la información de cada noticia:
        
        df_ELPAIS = CreateDfForElPais(URLs_ElPAIS,"NoticiasDelPais.csv")
        
        df_Excels = CreateDfForExcelsior(URLs_Excels,"NoticiasDelExcelsior.csv")
        df_CNN    = CreateDfForCNN(URLs_CNN,"NoticiasDeCNN.csv")

    except:
        logging.warning("Aviso: Something fail building the data frames")

    #Devolver los tres dataframe:
    return df_ELPAIS,df_Excels,df_CNN

# url de los resultados que se desea obtener:


