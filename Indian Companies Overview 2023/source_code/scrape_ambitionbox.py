from collections import defaultdict
import pandas as pd
from datetime import datetime
from scrape import Scrape

month_year = datetime.now().strftime("%B %Y")

class AmbitionBoxScrape(Scrape):
    def __init__(self, url='https://www.ambitionbox.com'):
        super().__init__(url)
        
    def CompanyData(self,page:int=1):
        cookie = defaultdict(list)
        scrape =Scrape(f'https://www.ambitionbox.com/list-of-companies?campaign=desktop_nav&page={page}')
        cards = scrape.soup.find_all('div',class_='companyCardWrapper')
        for card in cards:
            """ 
            all the companies are stored like cards where it have meta data
            source link of company to other page to extact info about the company
            """
            meta = card.find('div',class_='companyCardWrapper__metaInformation')
            teritory = card.find('div',class_='companyCardWrapper__tertiaryInformation')
            overview_div = card.find('div',class_='companyCardWrapper__companyPrimaryDetailsTopSection')
            # list of data that will be pulled from the website
            company_name = meta.find('h2').text.strip()
            company_rating = meta.find('span',class_='companyCardWrapper__companyRatingValue').text.strip()
            company_details = meta.find('span',class_='companyCardWrapper__interLinking').text.strip()
            company_reviews = teritory.find_all('span',class_='companyCardWrapper__ActionCount')[0].text.strip()
            company_salaries = teritory.find_all('span',class_='companyCardWrapper__ActionCount')[1].text.strip()
            company_interviews = teritory.find_all('span',class_='companyCardWrapper__ActionCount')[2].text.strip()
            company_jobs = teritory.find_all('span',class_='companyCardWrapper__ActionCount')[3].text.strip()
            company_benifits = teritory.find_all('span',class_='companyCardWrapper__ActionCount')[4].text.strip()
            company_overview_page = overview_div.find('a').get('href')
            # feel free to add more data if you like 

            # store these data into the dict called cookie
            cookie['Company-Name'].append(company_name)
            cookie['Ratings'].append(company_rating)
            cookie['Details'].append(company_details)
            cookie['Reviews'].append(company_reviews)
            cookie['Salaries'].append(company_salaries)
            cookie['Interviews'].append(company_interviews)
            cookie['Jobs'].append(company_jobs)
            cookie['Benefits'].append(company_benifits)
            cookie['Over-View'].append(company_overview_page)
        
        return cookie
           
    def __get_company_info(self,page_index:int=0,file_path:str=f'Companies Data {month_year}.csv'):
        """
        0. page index pulls overview data as per its index
        1. first gather companies data in which overview is important to fetch companies info page
        2. make sure to provide file path of companies data which is in csv format
        3. overview column acts as varibale index of companies page info
        """
        df = pd.read_csv(file_path)
        overview = df['Over-View'].unique()
        Page = overview[page_index]
        url = f"https://www.ambitionbox.com/"+Page
        scrape = Scrape(url)
        company_table = scrape.soup.find('ul',class_='aboutTable')
        item_name = company_table.find_all('p',class_='aboutItem__name')
        names = [name.text.strip() for name in item_name]
        table_list = company_table.find_all('li')

        textval_itmval = 'textItem__val aboutItem__value'
        itmval_felxflow = 'aboutItem__value flex-row'
        media = 'socialMedia aboutItem__value aboutItem__socialMedia'
        suggest = 'suggest aboutItem__value'
        website = 'textItem__val aboutItem__value aboutItem__website'

        table = defaultdict(list)

        table['Company-Name'].append(scrape.soup.find('h1',class_='newHInfo__cNtxt').text.strip())

        def get(html,tag,class_):
            return html.find(tag,class_=class_) 

        for (name,li) in zip(names,table_list):
            """
            In the company information table, diverse HTML tag elements are employed,
            ranging from div and anchor tags to p tags. 
            These tags exhibit varying structural patterns in the website source code. 
            The following code detects and handles these diverse patterns to extract relevant information. 
            """
            tree_1 = get(li,'p',textval_itmval)
            tree_2 = get(li,'div',textval_itmval)
            tree_3 = get(li,'div',itmval_felxflow)
            tree_4 = get(li,'div',media)
            tree_5 = get(li,'div',suggest)
            tree_6 = get(li,'div',website)
            #1
            if tree_1:table[name].append(tree_1.text.strip())
            #2
            elif tree_2:
                html = tree_2
                if html.find('a'):
                    table[name].append(html.find('a').text.strip())
                    #print(i,name ,html.find('a').text.strip())
                elif html.find('p'):
                    table[name].append(html.find('p').text.strip())
            #3        
            elif tree_3:
                html = tree_3
                for a in html.find_all('a'):
                    text = a.text.strip()
                    table[name].append(text)
                n = '|'.join(table[name])
            #4    
            elif tree_4:
                html = tree_4
                for media_link in html.find_all('a'):
                    table[name].append(media_link.get('href'))    
            #5    
            elif tree_5:
            
                html = tree_5
                if name not in table.keys():
                    if html.find('p').text.strip()=='Suggest':
                        table[name].append(str(None))
            #6    
            elif tree_6:
                webSite =tree_6 
                link = webSite.find('a').get('href')
                table[name].append(link)
            
        return table

    def CompanyCoreData(self,page_index:int=0,file_path:str =f'Companies Data {month_year}.csv'):
        """

        0. page index pulls overview data as per its index
        1. first gather companies data in which overview is important to fetch companies info page
        2. make sure to provide file path of companies data which is in csv format
        3. overview column acts as varibale index of companies page info
        4.main call this function ensures that in tables we have sub list of variable size so that we must join them into one string
        
        I'm joining them with `|` 
        
        """
        new = defaultdict(list)
        for key,val in zip(self.__get_company_info(page_index,file_path).keys(),
                        self.__get_company_info(page_index).values()):
            values = '|'.join(val)
            new[key].append(values)
        return new

    def CompanyData2CSV(self,
                    start: int = 1, end: int = 2,
                    save_file_loc: str = f'Companies Data {month_year}.csv'):
        """
        save company data to CSV
        """
        for i in range(start, end):
            data = self.CompanyData(i)
            if i!=start:
                pd.DataFrame(data).to_csv(save_file_loc, index=False, mode='a', header=False)
            else:
                pd.DataFrame(data).to_csv(save_file_loc, index=False, mode='w', header=True)
            
    def CompanyCoreData2CSV(self,
                     start:int=0,end:int=2, # page range start and end 
                     file_path:str=f'Companies Data {month_year}.csv', #file path
                     save_file_loc:str=f'Companies Core Data {month_year}.csv' # file destination
                     ):
        """
        save company core data to csv
        """
        for i in range(start,end):
            data = self.CompanyCoreData(i,file_path)
            if i!=start:
                pd.DataFrame(data).to_csv(save_file_loc, index=False, mode='a', header=False)
            else:
                pd.DataFrame(data).to_csv(save_file_loc, index=False, mode='w', header=True)



                