from itemloaders.processors import TakeFirst, MapCompose
from scrapy.loader import ItemLoader

# Create and configure Item Loader to:
# 1.) Remove the "pound" sign from the data, and
# 2.) Convert the scraped relative urls to full absolute urls

class ChocolateProductLoader(ItemLoader):

    default_output_processor = TakeFirst()

    #declare input processor for price field (hence the "_in" suffix)
    price_in = MapCompose(lambda x: x.split("£")[-1])
    
    #declare input processor for url field (hence the "_in" suffix). Will append teh passed relative url to base url
    url_in = MapCompose(lambda x: 'https://www.chocolate.co.uk' + x )