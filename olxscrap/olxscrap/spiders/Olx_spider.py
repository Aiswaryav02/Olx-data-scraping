import scrapy
from scrapy.crawler import CrawlerProcess
import json

class Olx(scrapy.Spider):
    name = 'olx'
    url = 'https://www.olx.in/api/relevance/v4/search?category=1723&facet_limit=100&lang=en-IN&location=4058877&location_facet_limit=20&page=4&platform=web-desktop&relaxedFilters=true&size=40&user=186fcf4ee0bx46c927d3'
    headers={
        "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.108 Safari/537.36"
    }
    def _int_(self):
        with open('properties.json', 'w') as csv_file:
            csv_file.write('title,discription,location,area,beds,bathrooms,total_sqft,price\n')
    def start_requests(self):
        for page in range(0, 100):
            yield scrapy.Request(url=self.url + "&page=" + str(page), headers=self.headers, callback=self.parse)
       


    def parse(self, res):
        data = res.text

        data = json.loads(data)

        for offer in data['data']:
            items = {
                'property_name': offer['title'] ,
                'property_id':offer['ad_id'],
                'price': offer['price']['value']['display'],
        
                'image_url':offer['images'][0]['small']['url'] ,
                'description': offer['description'].replace('\n', ' '),
                'location': offer['locations_resolved']['SUBLOCALITY_LEVEL_1_name'] +','+
                            offer['locations_resolved']['ADMIN_LEVEL_3_name'] +','+
                            offer['locations_resolved']['ADMIN_LEVEL_1_name'],
                'country'  :  offer['locations_resolved']['COUNTRY_name'],
                'property type':offer['parameters'][0]['value_name'],
                'bathrooms': offer['main_info'].split("-")[1],
                'bedrooms': offer['main_info'].split("-")[0],
                # 
                'furnishing':offer['parameters'][3]['value_name'],
                'listed by':offer['parameters'][4]['value_name'],
                'super buildup area':offer['parameters'][5]['value_name'],
                'carpet area':offer['parameters'][6]['value_name'],
                
            
                'date':offer['display_date'],
                
                'total_sqft': offer['main_info'].split("-")[2],
                

            }
            print(json.dumps(items, indent=2))
            # with open('result.csv', 'a') as csv_file:
                # writer = json.DictWriter(csv_file, fieldnames=items.keys())
                # writer.writerow(items)
        
        
        # write data to JSONL file
            with open("datas.json", 'a') as f:
                f.write(json.dumps(items)  + '\n')
        
       
process = CrawlerProcess()
process.crawl(Olx)
process.start()

