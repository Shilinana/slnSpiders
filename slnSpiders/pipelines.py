# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


from scrapy.exporters import JsonLinesItemExporter
from tempfile import mkstemp
from shutil import move
from os import fdopen, remove

class ConvertItem2JsonPipeline(object):
    def open_spider(self, spider):
        self.category_to_exporters = {}
    def close_spider(self, spider):
        for exporter in self.category_to_exporters.values():
            exporter.finish_exporting()
            exporter.file.close()
            file_path_collection = ['music.json', 'machine-learning.json', 'open-journalism.json', 'trending.json']
            for filePath in file_path_collection:
                self.format_json_file(filePath)
    def _exporter_for_item(self, item):
        category = item['category']
        if category not in self.category_to_exporters:
            f = open('{}.json'.format(category), 'wb')
            exporter = JsonLinesItemExporter(f)
            exporter.start_exporting()
            self.category_to_exporters[category] = exporter
        return self.category_to_exporters[category]
    def process_item(self, item, spider):
        exporter = self._exporter_for_item(item)
        exporter.export_item(item)
        return item
    def format_json_file(self, filePath):
        # fileNames = ['music.json', 'machine-learning.json', 'open-journalism.json', 'trending.json']
        fh, abs_path = mkstemp()
        with fdopen(fh, 'w') as new_file:
            with open(filePath) as old_file:
                lines = old_file.readlines()
                for idx, line in enumerate(old_file, 1):
                    line_after_format = line + ','
                    if idx == 0:
                        line_after_format = '[' + line_after_format
                    if idx == len(lines) - 1:
                        line_after_format += ']'
                    new_file.writeline(line_after_format)
        remove(filePath)
        move(abs_path, filePath)