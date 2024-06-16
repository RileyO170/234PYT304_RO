##### REMEMBER: TO RUN THE SCRAPER YOU MUST DO THIS IN THE POWERSHELL (TERMINAL) #####
#   Directory: C:\Users\rjoro\OneDrive\Documents\Python\Python_Data_Mining_Structures - 234PYT304\HW2\chocolatescraper
#   then type => scrapy crawl chocolatespider

### Saved data to a CSV file via Feed Exporter ###
#   In powershell, type => scrapy crawl chocolatespider -o my_scraped_chocolate_data.csv
#   See output under chocolatescraper > my_scraped_chocolate_data.csv

import scrapy
from chocolatescraper.itemloaders import ChocolateProductLoader
from chocolatescraper.items import ChocolateProduct



class ChocolateSpider(scrapy.Spider):
    
    #the name of the spider
    name = 'chocolatespider'

    #the url of the first page that we will start scraping
    start_urls = ['https://www.chocolate.co.uk/collections/all']

    def parse(self, response):
        products = response.css('product-item')

        for product in products:
            chocolate = ChocolateProductLoader(item=ChocolateProduct(), selector=product)
            chocolate.add_css('name', "a.product-item-meta__title::text")
            chocolate.add_css('price', 'span.price', re='<span class="price">\n              <span class="visually-hidden">Sale price</span>(.*)</span>')
            chocolate.add_css('url', 'div.product-item-meta a::attr(href)')
            yield chocolate.load_item()

        next_page = response.css('[rel="next"] ::attr(href)').get()

        if next_page is not None:
           next_page_url = 'https://www.chocolate.co.uk' + next_page
           yield response.follow(next_page_url, callback=self.parse)



####### Code state for Import Schema creation #######  
# import scrapy
# from chocolatescraper.items import ChocolateProduct  

# class ChocolateSpider(scrapy.Spider):

#   #the name of the spider
#   name = 'chocolatespider'

#   #these are the urls that we will start scraping
#   start_urls = ['https://www.chocolate.co.uk/collections/all']

#   def parse(self, response):

#       products = response.css('product-item')

#       product_item = ChocolateProduct()
#       for product in products:
#           product_item['name'] = product.css('a.product-item-meta__title::text').get()
#           product_item['price'] = product.css('span.price').get().replace('<span class="price">\n              <span class="visually-hidden">Sale price</span>','').replace('</span>','')
#           product_item['url'] = product.css('div.product-item-meta a').attrib['href']
#           yield product_item

#       next_page = response.css('[rel="next"] ::attr(href)').get()

#       if next_page is not None:
#           next_page_url = 'https://www.chocolate.co.uk' + next_page
#           yield response.follow(next_page_url, callback=self.parse)



##### Code from Part I, commented out here: #####

    # def parse(self, response):
        
    #     products = response.css('product-item')
    #     product_item = ChocolateProduct()

    #     #here we are looping through the products and extracting the name, price & url
    #     for product in products:
    #         #here we put the data returned into the format we want to output for our csv (used in this project) or json file
    #         yield{
    #             'name' : product.css('a.product-item-meta__title::text').get(),
    #             'price' : product.css('span.price').get().replace('<span class="price">\n              <span class="visually-hidden">Sale price</span>','').replace('</span>',''),
    #             'url' : product.css('div.product-item-meta a').attrib['href'],
    #         }
        
    #     #transition to the next page to continue scraping data
    #     next_page = response.css('[rel="next"] ::attr(href)').get()

    #     if next_page is not None:
    #        next_page_url = 'https://www.chocolate.co.uk' + next_page
    #        yield response.follow(next_page_url, callback=self.parse)