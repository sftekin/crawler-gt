# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
# Extracted data -> Temporary containers (items) -> json/csv files
# Extracted data -> Temporary containers (items) --> Pipeline -> SQL/Mango database


from itemadapter import ItemAdapter


class QuotetutorialPipeline:
    def process_item(self, item, spider):
        return item
