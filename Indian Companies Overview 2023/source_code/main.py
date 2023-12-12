from scrape_ambitionbox import AmbitionBoxScrape
import pandas as pd
from datetime import datetime

month_year = datetime.now().strftime("%B %Y")


"""
we have two csv files company data and company core data
in company data we have pages from 1 to 500 as of my knowledge on dec 2023
and from company data Over-View column we use this variable to find core data of the company

step-1 : run CompanyData2CSV from desired pages
step-2 : run ComapanyCoreData2Csv from desired `Over-View` index within Companydata

"""
pages = 2

if __name__ == '__main__':
    scrape = AmbitionBoxScrape() 
    scrape.CompanyData2CSV(1,pages) # creates companies Data
    # to check the size of companies data to pass in company core data
    rows = pd.read_csv(f'Companies Data {month_year}.csv')['Over-View'].unique().shape[0]
    #creates companies core data from companies data
    scrape.CompanyCoreData2CSV(0,rows)
    # make combined csv file 
    companydata = pd.read_csv(f'Companies Data {month_year}.csv')
    companyCoredata = pd.read_csv(f'Companies Core Data {month_year}.csv')
    merge = pd.merge(companydata,companyCoredata,on='Company-Name',how='inner')
    merge.to_csv(f'Indian Companies Data {month_year}.csv')



