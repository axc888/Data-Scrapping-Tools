# -*- coding: utf-8 -*-
"""
Created on Sun Sep 27 11:01:10 2015

@author: Vijay Anand
"""
from bs4 import BeautifulSoup
import pandas as pd
import urllib2
import numpy as np
import os
import time
import re
###############################################################################
def extract_urls(mainurl,df):

    url=mainurl
    try:
        response=urllib2.urlopen(url).read()
        soup=BeautifulSoup(response)
        x=soup.find_all('a')


    #### Extract product urls from mainpage

        tmplist=[]
        for tgs in x:

            try:
                a= tgs['href']

                if a[:19]=='http://olx.in/item/':
                    tmplist.append(a)


            except:
                pass

    except Exception as e:
        pass
    t=tmplist[0:][::2]
    print len(t)

    return t

###############################################################################
def scrapper(prod_urls):

    global df,rows  

    df['Product Url'][rows]=prod_urls  
        
    try:
        response=urllib2.urlopen(prod_urls).read()
        soup=BeautifulSoup(response)
               
        z=soup.findAll("div" , { "class" : "pding5_10" })
        
        print '+++++++++++'
        #print z
        lst=[]
        for zz in z:
            s=zz.text
            s=re.sub('\t+', '', s)
            s=re.sub('\n+', '', s)
            s=re.sub('\r+', '', s)
            #print s
            lst.append(s)
        
        #print lst
        
        for y in range(0,len(lst)):
            
            if y==0:
                field=lst[0]
                field=field[6:]
                df['Brand'][rows]=field
                
            if y==1:
                field=lst[1]
                field=field[6:]
                df['Model'][rows]=field
                
            if y==2:
                field=lst[2]
                field=field[5:]
                df['Year'][rows]=field
                
            if y==3:
                field=lst[3]
                field=field[5:]
                df['Fuel Type'][rows]=field

            if y==4:
                field=lst[4]
                field=field[12:]
                df['Kilometer'][rows]=field
                
        ## Find owner info
        try:        
            owner=soup.findAll("span" , { "class" : "block color-5 brkword xx-large" })
            df['Owner Name'][rows]=owner[0].text
        except:
            pass
        
        try:
            phone=soup.findAll("strong" , { "class" : "brkword xx-large lheight20 fnormal" })
            df['Contact no'][rows]=phone[0].text
            
        except:
            pass
        
        try:
            loc=soup.findAll("strong" , { "class" : "c2b small" })
            lo=loc[0].text
            lo=re.sub('\t+', '', lo)
            lo=re.sub('\n+', '', lo)
            lo=re.sub('\r+', '', lo)
            df['Location'][rows]=lo
            
        except:
            pass
        
        try:
            loc=soup.findAll("strong" , { "class" : "c000" })
            price=loc[0].text
            price=re.sub('\t+', '', price)
            price=re.sub('\n+', '', price)
            price=re.sub('\r+', '', price)
            df['Price'][rows]=price
            
        except:
            pass

        try:
            loc=soup.findAll("p" , { "class" : "pding10 lheight20 large" })
            com=loc[0].text
            com=re.sub('\t+', '', com)
            com=re.sub('\n+', '', com)
            com=re.sub('\r+', '', com)
            df['Comments'][rows]=com
            
        except:
            pass

        try:
            img=soup.findAll("label" , { "class" : "block br4" })
            
            print img
            print len(img)
            
        except:
            pass

        rows+=1
    except:
        pass



###############################################################################

###############################################################################

def main():

    print "Welcome !"

    global df, rows
    rows=0
    total_rows=10

    #### Define dataframe

    clms=['Product Url','Owner Name','Contact no','Brand','Model','Price','Year','Kilometer','Fuel Type','Location',
          'Comments','Image URL']
    index=np.arange(total_rows)

    df = pd.DataFrame(columns=clms,index=index)

    if not os.path.exists('images'):
        os.makedirs('images')
    if not os.path.exists('csv'):
        os.makedirs('csv')

    ## Extract urls

    for x in range (2,3):

        u='http://olx.in/chennai/cars/?page='
        url=u+str(x)
        links=extract_urls(url,df)

        for prod_urls in links:
            
            scrapper(prod_urls)
            
    df.to_csv('csv/olx.csv')



if __name__ == "__main__":
    main()