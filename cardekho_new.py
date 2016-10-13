# -*- coding: utf-8 -*-
"""
Created on Sun Jan 17 13:18:43 2016
# -*- coding: utf-8 -*-

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

###############################################################################
def extract_urls(u,df):

    url=u

    try:
        response=urllib2.urlopen(url).read()

    except urllib2.URLError, e:
        'Error in page url'


    try:

        soup=BeautifulSoup(response,'lxml')
        x=soup.find_all("div" , { "class" : "cartitle" })

    #### Extract product urls from mainpage

        tmplist=[]
        for tgs in x:

            try:
                a= tgs.find_all("a")

                tmplist.append(a[0]['href'])


            except:
                pass

    except Exception as e:
        pass


    return tmplist


###############################################################################

def scraper(url):

    global df,rows

    df['Product Url'][rows]=url

    try:
        response=urllib2.urlopen(url).read()

    except urllib2.URLError, e:
        'Error in page url'

    soup=BeautifulSoup(response,'lxml')

    ## Title

    try:
        heading=soup.findAll("h1" )
        print 'Car : ',heading[0].text
        df['Title'][rows]=heading[0].text.encode('utf-8')

    except Exception as e:
        pass

    ## Location

    try:
        loc=soup.find_all("div" , { "class" : "carinfo" })
        location=loc[0].contents
        l=location[1].contents[1]
        print 'Location : ',l
        df['Location'][rows]=l.encode('utf-8')

    except Exception as e:
        pass

    ## Price

    try:

        price=soup.find_all("div" , { "class" : "headbg" })
        p=price[0].contents

        print 'price : ',p[1]
        df['Price'][rows]=p[1].encode('utf-8')

    except Exception as e:
        pass

    ## Phone no

    try:
        phone=soup.find_all("div" , { "class" : "callseller" })
        pno = phone[0].contents[3].text.encode('utf-8')
        print 'Contact no: ',pno
        df['Contact no'][rows]=pno


    except Exception as e:
        pass


    ## Many params

    try:

        many=soup.find_all("div" , { "class" : "dttop" })

        try:
            year=many[0].text.encode('utf-8')
            print 'Year: ',year
            df['Model year'][rows]=year

        except:
            pass

        try:

            kms=many[1].text.encode('utf-8')
            print 'Kms Driven: ',kms
            df['Km Driven'][rows]=kms

        except:
            pass

        try:

            fuel=many[2].text.encode('utf-8')
            print 'Fuel type: ',fuel
            df['Fuel Type'][rows]=fuel

        except:
            pass

        try:
            owner=many[3].text.encode('utf-8')
            print 'Owner: ',owner
            df['Owner'][rows]=owner

        except:
            pass

        try:
            seller=many[4].text.encode('utf-8')
            print 'Seller type: ',seller
            df['Seller Type'][rows]=seller
        except:
            pass

        try:

            colour=many[5].text.encode('utf-8')
            print 'Colour: ',colour
            df['Color'][rows]=colour
        except:
            pass


    except Exception as e:
        pass

    ## Dealer address
    try:

        dealer=soup.find_all("ul" , { "id" : "scroll1" })

        dealer=dealer[0].contents
        dealer=dealer[1:]

        for tmp in dealer:

            try:
                tm=tmp.text
                addrs= tm.splitlines()
                if addrs[1]=='Seller Address':
                    print 'Seller Address: ',addrs[2]
                    df['Dealer Address'][rows]=addrs[2].encode('utf-8')

            except:
                pass

    except Exception as e:
        pass

    ## Save csv

    try:

        if rows%2==0:
            df.to_csv('dump/cardekho_1.csv',index=False)
        else:
            df.to_csv('dump/cardekho.csv',index=False)

        rows+=1

    except Exception as e:

        print "Error while saving csv!"

###############################################################################

def main():

    global df, rows
    rows=0

#### Define dataframe

    clms=['Title','Location','Price','Color','Model year','Km Driven','Fuel Type',
          'Owner','Seller Type','Dealer Address','Contact no','Product Url']


    ## get maximum number of rows
    total_rows=20

#    while True:
#
#        print ''
#        total_rows=raw_input('Enter maximum number of data rows: ')
#        print ''
#
#        try:
#            total_rows=int(total_rows)
#            if isinstance(total_rows, int):
#
#                total_rows=total_rows-(total_rows%10)
#                break
#        except:
#            print ''
#            print 'Please check the value entered!'
#            print ''
#            pass


     ##   DF

    index=np.arange(total_rows)
    df = pd.DataFrame(columns=clms,index=index)


    if not os.path.exists('dump'):
        os.makedirs('dump')

    start=time.time()

    ## Loop through pages
    print ''
    print '###############################################################################'
    print ''
    print '                         Starting the demo. please wait !'
    print ''
    print '###############################################################################'
    print ''

    for x in range (int(total_rows/40),1,-1):

        u='http://www.cardekho.com/used-cars+in+india/'+str(x)


        try:
            links=extract_urls(u,df)
            #time.sleep(2)

            for url in links:
                #url='http://www.cardekho.com/used-car-details/used-Skoda-Rapid-1.5-TDI-Ambition-cars-Nashik_933427.htm'
                time.sleep(2)
                print ''
                print '###############################################################################'
                print ''
                scraper(url)

        except Exception as e:
            pass

    print 'Finshed ! You may close this window'

    time.sleep(300)



###############################################################################
if __name__ == "__main__":
    main()