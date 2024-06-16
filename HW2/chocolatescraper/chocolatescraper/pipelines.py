# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem

##### Default pipeline code, kept here for future reference #####
# class ChocolatescraperPipeline:
#     def process_item(self, item, spider):
#         return item


#Create pipeline to convert prices from pounds to USD
class PriceToUSDPipeline:

    #British pound to USD exchange rate
    gbpToUsdRate = 1.3

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        # check is price present
        if adapter.get('price'):

            #converting the price to a float
            floatPrice = float(adapter['price'])

            #converting the price from gbp to usd using our hard coded exchange rate
            adapter['price'] = floatPrice * self.gbpToUsdRate

            return item

        # drop item if no price
        else:
            raise DropItem(f"Missing price in {item}")
        
#Create pipeline to remove product duplicates
class DuplicatesPipeline:

    def __init__(self):
        self.names_seen = set()

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        if adapter['name'] in self.names_seen:
            raise DropItem(f"Duplicate item found: {item!r}")
        else:
            self.names_seen.add(adapter['name'])
            return item