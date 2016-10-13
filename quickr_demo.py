# -*- coding: utf-8 -*-
"""
Created on Sun Dec 27 18:14:20 2015

@author: Vijay Anand
"""
from bs4 import BeautifulSoup
import pandas as pd
import urllib2
import numpy as np
import os
import time
import getpass
import lxml
import sys
from selenium import webdriver
import time
from random import randint

###############################################################################

def get_urls(pageno):

    try:

        urllist=[]
        u='http://www.quikr.com/Cars/y71?page='

        url=u+str(pageno)
        resp=driver.get(url)
        resp1=driver.page_source.encode('utf-8')

        soup=BeautifulSoup(resp1,'lxml')

    ## check for captcha page

        try:

            title=soup.find_all('title')

            if title[0].string=='Pardon Our Interruption':
                time.sleep(30)

                resp=driver.get(url)
                resp1=driver.page_source.encode('utf-8')
                soup=BeautifulSoup(resp1,'lxml')

        except Exception as e:
            pass

        x=soup.find_all("div" , { "class" : "col-xs-6 col-lg-4 col-md-3 col-sm-4  product-image" })

        for tgs in x:
            a= tgs.find_all("a")

            for tgs1 in a:
                try:
                    urllist.append(str(tgs1['href']))
                except Exception as e:
                    pass

        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    except Exception as e:

        pass

    return urllist


###############################################################################

def scrap_data(url):

    global df,rows,driver

    try:
        df['Product Url'][rows]=url
    except:
        pass


    try:

        tmpurl=url[7:]
        tmpurl=tmpurl.split('.')
        df['City'][rows]=tmpurl[0]

    except:
        pass

    try:
        resp=driver.get(url)
        time.sleep(randint(2,5))

        resp1=driver.page_source.encode('utf-8')

        soup=BeautifulSoup(resp1,'lxml')

        # check for captcha page

        try:

            title=soup.find_all('title')

            if title[0].string=='Pardon Our Interruption':
                time.sleep(30)

                resp=driver.get(url)
                resp1=driver.page_source.encode('utf-8')
                soup=BeautifulSoup(resp1,'lxml')


        except Exception as e:
            pass

    ## Title

        try:
            title=soup.find_all('title')
            df['Title'][rows]=title[0].string

        except:
            pass

    ## brand, year and url

        try:
            name=soup.find_all("h2" , { "class" : "car-name-attr mob-name-text" })
            n=(name[0].string).encode('utf-8')

            df['Name'][rows]=n[:-9]
            df['Year'][rows]=n[-4:]
            print 'Name: ',n[:-9]
            print 'Year: ',n[-4:]

        except Exception as e:
            pass


    ## price

        try:
            name1=soup.find_all("h2" , { "class" : "car-price-h1" })
            n=(name1[0].text)
            df['Price'][rows]=n
            print 'price: Rs.',n

        except:
            pass

    ## Location

        try:
            name2=soup.find_all("li" , { "class" : "ad-desc" })
            tmploc=[]

            for n in name2:
                tmploc.append(n.text)

            df['Location'][rows]=tmploc[1]

            print 'Location: ',tmploc[1]

        except Exception as e:
            pass

    ## Mobile no

        try:
            mob=soup.find_all("div" , { "class" : "mob-number" })
            mno=mob[0].contents
            df['Contact no'][rows]=mno[1]
            print 'Contact number: ',mno[1]

        except:
            pass

    ## Fuel trype, kms driven, colour

        try:
            props=soup.find_all("div" , { "class" : "vap-tail-desc" })

            ## fuel type and kms driven

            for tags in props:

                cont=tags.contents

                if cont[1].text=='Fuel Type':
                    df['Fuel Type'][rows]=cont[3].text
                    print 'Fuel: ',cont[3].text

                if cont[1].text=='Kms Driven':
                    df['Kms driven'][rows]=cont[3].text[:-5]
                    print 'Kms driven: ',cont[3].text

                if cont[1].text=='Owner':
                    df['Owner'][rows]=cont[3].text
                    print 'Owner: ',cont[3].text

                if cont[1].text=='Color':
                    df['Colour'][rows]=cont[3].text
                    print 'Colour: ',cont[3].text

        except Exception as e:
            pass

        ## Transmission, city mileaga and highway mileage

        try:
            tch=soup.find_all("ul" , { "class" : "car-details-list" })

            print tch[1].contents[1].contents[1].text,' : ',tch[1].contents[1].contents[3].text
            df['Transmission'][rows]= tch[1].contents[1].contents[3].text
            print tch[1].contents[5].contents[1].text,' : ',tch[1].contents[5].contents[3].text
            df['City mileage'][rows]= tch[1].contents[5].contents[3].text
            print tch[1].contents[7].contents[1].text,' : ',tch[1].contents[7].contents[3].text
            df['Highway mileage'][rows]= tch[1].contents[7].contents[3].text

        except:
            pass

        ## comments

        try:
            cmt=soup.find_all("p" , { "class" : "minimize" })
            df['Description'][rows]=cmt[0].text.lstrip()
            #print cmt[0].text.lstrip()

        except:
            pass

        ## Ad-ID
        try:
            adid=soup.find_all("ul" , { "class" : "usr-details" })
            #print 'Ad-ID: ',adid[0].contents[1].contents[1]
            df['Ad Id'][rows]=adid[0].contents[1].contents[1]

        except:
            pass


        ## Save csv

        df.to_csv('dump/quickr.csv',encoding='utf-8')
        rows+=1


    except Exception as e:
        print 'Error in product page !'



###############################################################################

def main():

    global driver,df,rows
    rows=0


    ##############  Initialize dataframe

    #### Define dataframe

    clms=['Title','Name','Car type','Year','Owner','Product Url','Price','City','Location',
          'Contact no','Fuel Type','Kms driven','Colour','Transmission','City mileage',
          'Highway mileage','Description','Ad Id']



    total_rows=15

     ##   DF


    index=np.arange(total_rows)
    df = pd.DataFrame(columns=clms,index=index)

#    if not os.path.exists('images'):
 #       os.makedirs('images')

    if not os.path.exists('dump'):
        os.makedirs('dump')

    #####################

    ## configure firefox for tor connection

    profile=webdriver.FirefoxProfile()
    profile.set_preference( "permissions.default.image", 1 )


    driver = webdriver.Firefox(profile)

    ## Start scraping

    for pageno in range (2,20):

        time.sleep(randint(10,20))
        urllist=get_urls(pageno)


        ## scrap data from urllist

        for url in urllist:
            print ''
            print '###############################################################################'

            try:
                scrap_data(url.encode('utf-8'))

            except Exception as e:
                pass

    print 'Success!'


###############################################################################

if __name__=='__main__':
    main()

