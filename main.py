import gspread
from se_support_functions import *

"""
To get this part working, you'll need to:

(A) Activate the Google Sheets API in the Google API Console
(B) Generate a service key in the console

Details on how to do both are here: https://gsheets.readthedocs.io/en/stable/

"""
gc = gc = gspread.service_account(filename='gsheet_credentials.json')

#google sheet file name goes here
sh = gc.open("spreadsheet name")

search_url='https://streeteasy.com/for-rent/upper-west-side/status:open%7Cprice:-4500%7Cbeds:2-3%7Cbaths%3E=2'

#create session to keep cookies from initial request 
with requests.Session() as s:

    ### 1. Get initial lists 
    print('pull listings')
    i_results=pull_listings(s,search_url)
    results=i_results

    ## get initial apartments
    for x in results:
        #randomness to evade bot detection
        value = randint(30, 150)
        time.sleep(value)
        try:
            apt_info=get_apt_details(s,x)
        except:
            print ('error with:'+x)
        sh.sheet1.append_row(apt_info)

    ## insert data 
    counter=0

    ### 2. While loops until we've gone through all the links
    print('begin phase 2')

    for x in range(2,100):
        try:
            i_results=pull_listings(s,search_url+'?page='+str(x))
            results=i_results

        except:
            break

        next_pull=pull_listings(s,search_url)
        next_listings=next_pull
        print(next_listings)
        for apartment in next_listings:
            time.sleep(20)
            print(x)
            try:
                apt_info=get_apt_details(apartment)
                sh.sheet1.append_row(s,apt_info)
            except:
                print('error with:'+apartment)
                print(listings)
        counter+=1
        print(counter)

