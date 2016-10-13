# -*- coding: utf-8 -*-
"""
Created on Sun Sep 06 18:37:22 2015

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

def extract_urls(mainurl,df):

    url=mainurl
    
    try:
        response=urllib2.urlopen(url).read()
        
    
    except urllib2.URLError, e:
        
        pass

    
    try:
    
        soup=BeautifulSoup(response,'lxml')
        x=soup.find_all("h2" , { "class" : "listingTitle font18" })

    #### Extract product urls from mainpage

        tmplist=[]
        for tgs in x:
            
            try:
                a= tgs.find_all("a")
                
                tmplist.append('http://www.carwale.com'+a[0]['href'])
                         

            except:
                pass

    except Exception as e:
        pass

    return tmplist

###############################################################################

def scraper(url):


    try:
        response=urllib2.urlopen(url).read()

    except urllib2.URLError, e:
        pass
    
    try:      
        
        soup=BeautifulSoup(response,'lxml')

        z=soup.findAll("div" , { "id" : "overview" })

        for tgs in z:

            a=tgs.findAll("div" , { "class" : "equal-width dark-text" })

        x=soup.findAll("div" , { "class" : "content-box-shadow content-inner-block-10 font14" })

        for tgs1 in x:
            b=tgs1.findAll("p" )

        y=soup.findAll("strong", { "class" : "leftfloat" } )

        ii=soup.findAll("div", { "class" : "uc-pg-contact-name-box font14" } )

        img=soup.findAll("div", {"class":"uc-thumbnail"} )
        
        ## image url

        pic=[]
        for image in img:
            pic=image.findAll("img" )
            
            
        ## owner comments
        oc=''
        owncom=soup.findAll("div" , { "class" : "content-box-shadow content-inner-block-10 font14" })
        
        for ts in owncom:
            
            oc=oc+(ts.text).strip()+'. '
             
        ## About Dealer
        
        ad=''
        
        try:
            
            abtdlr=soup.findAll("div" , { "class" : "about-dealer-details" })
            
                        
            for tags in abtdlr:
                
                ad=ad+(tags.text).strip()+'. '
            
            ad=ad.strip()
            
        except:
            pass
        
        ## Features
        
        features=''
        
        try:
        
            f=soup.findAll("div" , { "id" : "features" })
            
            for tags1 in f:

                aa=tags1.findAll("div" , { "class" : "equal-width" }) ## all the data
            
                for tags2 in aa:
                
                    features=features+(tags2.text).strip()+'. '
            
                    
        except:
            pass
        
        ## Car name 
        nam=''
        name=soup.findAll("h1")
        nam=name[0]['title']
        

        ret=[a,b[0],y,ii,pic,oc,ad,features,nam]
        return ret

    except Exception as e:
        return []

    

###############################################################################

def cleaner(ret,url):

    global rows,df
    lst=ret[0]
    contactno=ret[2]
    contactname=ret[3]
    img=ret[4]
    owner_com=ret[5]
    about_dealer=ret[6]
    feat=ret[7]
    name=ret[8]
    
    try:
        print ''
        print 'Product: ',name.encode('utf-8')
        print 'Price: ',(lst[0].text).encode('utf-8')
        print 'Year: ',(lst[1].text).encode('utf-8')
        print 'Kilometer: ',(lst[2].text).encode('utf-8')
        print 'Car Available at: ',(lst[5].text).encode('utf-8')
        print 'Color: ',(lst[6].text).encode('utf-8')
        print 'Registered at: ',(lst[10].text).encode('utf-8')
        print 'Last Updated: ',(lst[14].text).encode('utf-8')
        
    except exception as e:
        
        pass
    
    try:
        df['Name'][rows]= (name).encode('utf-8')
    except:
        pass
    try:
        df['Price'][rows]= (lst[0].text).encode('utf-8')
    except:
        pass
    try:
        df['Year'][rows]= (lst[1].text).encode('utf-8')
    except:
        pass
    try:
        df['Kilometer'][rows]= (lst[2].text).encode('utf-8')
    except:
        pass
    try:
        df['Fuel Type'][rows]= (lst[3].text).encode('utf-8')
    except:
        pass
    try:
        df['Transmission'][rows]= (lst[4].text).encode('utf-8')
    except:
        pass
    try:
        df['Car Available at'][rows]= (lst[5].text).encode('utf-8')
    except:
        pass
    try:
        df['Color'][rows]= (lst[6].text).encode('utf-8')
    except:
        pass
    try:
        df['Fuel Economy'][rows]= (lst[7].text).encode('utf-8')
    except:
        pass
    try:
        df['Sold by'][rows]= (lst[8].text).encode('utf-8')
    except:
        pass
    try:
        df['No. of Owner(s)'][rows]= (lst[9].text).encode('utf-8')
    except:
        pass
    try:
        df['Registered at'][rows]= (lst[10].text).encode('utf-8')
    except:
        pass
    try:
        df['Insurance'][rows]= (lst[11].text.strip()).encode('utf-8')
    except:
        pass
    try:
        df['LifeTime Tax'][rows]= (lst[12].text).encode('utf-8')
    except:
        pass
    try:
        df['Profile Id'][rows]= (lst[13].text).encode('utf-8')
    except:
        pass
    try:
        df['Last Updated'][rows]= (lst[14].text).encode('utf-8')
    except:
        pass
    try:
        df['Product Url'][rows]= (url).encode('utf-8')
    except:
        pass
    try:
        df['Comments'][rows]= (ret[1].text).encode('utf-8')
    except:
        pass

    try:
        if contactno==[]:
            df['Contact no'][rows]= 'Not Available'
        else:
            df['Contact no'][rows]= (contactno[0].text).encode('utf-8')
    except:
        pass
            
    try:

        if contactname==[]:
            df['Owner Name'][rows]= 'Not Available'
        else:
            df['Owner Name'][rows]= (contactname[0].text).encode('utf-8')
            
    except:
        pass
            
    try:

        if img==[]:
            df['Image URL'][rows]= 'Not Available'
        else:
            df['Image URL'][rows]= (img[0]['src']).encode('utf-8')
    except:
        pass

    try:
        df['Owner comments'][rows]= (owner_com).encode('utf-8')   
    except:
        pass
    try:
        df['Features'][rows]= (feat).encode('utf-8')
    except:
        pass
    try:
        df['About dealer'][rows]= (about_dealer).encode('utf-8')
    except:
        pass
        
        
    try:

        if rows%2==0:
            df.to_csv('dump/carwale_1.csv')
        else:
            df.to_csv('dump/carwale.csv')

        rows+=1

    except Exception as e:

        print "Error processing data fields!"
        
##############################################################################
       

def main():
    
    intro()

    
    global df, rows
    rows=0

#    #### Authentication
    print ''
    print 'Enter the user name and password. Please note that the password is hidden.'
    print 'After entering username/password, press enter.'
    print ''
    print 'After 3 incorrect attempts, the application will terminate' 
    print 'automatically!'
    print ''
    print '#############################################################################'

    cnt=0
    while True:
        cnt+=1
        print ''
        username = raw_input("Please enter your name : ")
        password= getpass.getpass(prompt='Password: ')

        if username=='demo' and password=='demo':

            print ''
            print '################'
            print '##  Success!  ##'
            print '################'
            break

        else:

            if cnt==3:
                print ''
                print 'Maximum number of incorrect attempts reached. The application will terminate'
                print 'automatically in 10 seconds!'
                time.sleep(2)
                sys.exit()
            else:
                print ''
                print 'Incorrect username/password. Try again!'




    #### Define dataframe

    clms=['Name','Product Url','Owner Name','Owner comments','Contact no','About dealer','Price','Year','Kilometer','Fuel Type','Transmission','Car Available at',
          'Color','Fuel Economy','Sold by','No. of Owner(s)','Registered at','Insurance',
          'LifeTime Tax','Profile Id','Last Updated','Comments','Image URL','Features']


    ## get maximum number of rows

    while True:
        
        print ''

        total_rows=10
        print ''

        try:
            total_rows=int(total_rows)
            if isinstance(total_rows, int):

                total_rows=total_rows-(total_rows%10)
                break
        except:
            print ''
            print 'Please check the value entered!'
            print ''
            pass

     ##   DF

    index=np.arange(total_rows)
    df = pd.DataFrame(columns=clms,index=index)


    if not os.path.exists('dump'):
        os.makedirs('dump')
    
    start=time.time()

    for x in range (int(total_rows/15),1,-1):
        
        u='http://www.carwale.com/used/cars-for-sale/#pn='+str(x)
        try:
            links=extract_urls(u,df)
            time.sleep(2)

            for url in links:
                
                time.sleep(2)
                print ''
                print '#############################################################################'
                print ''
                print url
                print ''
                print '#############################################################################'
                    
                ret=scraper(url)
                    
                if len(ret)!=0:
                    cleaner(ret,url)
                    
                print ''
                print 'Time elapsed: ',int(time.time()-start),' seconds'
                print 'Percentage completed: ',(rows/float(total_rows))*100,' %'
                
                if rows==total_rows:
                    break
                    
                        

        except Exception as e:
            print "Error extracting data!"

    

    print ''
    print '##############################################################'
    print '##  Successfully completed! You may close the window now !  ##'
    print '##############################################################'

if __name__ == "__main__":
    main()
