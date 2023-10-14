#!/usr/bin/env python3
import abc
import argparse
import datetime
from jinja2 import Environment, FileSystemLoader
import logging
from os.path import dirname
from pathlib import Path
from parsel import Selector
import re
import requests
from typing import Dict, List
import uuid
from urllib.parse import urljoin

class Renderer:
    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'render')
                and callable(subclass.render))

class JinjaTemplateRender:
    def __init__(self, searchpath=f"{dirname(__file__)}", template='ssdf_catalog.json.j2'):
        self.loader = FileSystemLoader(searchpath)
        self.environment = Environment(loader=self.loader, autoescape=True)
        try:
            self.template = self.environment.get_template(template)
            self.template.globals.update({
                'strftime': datetime.datetime.strftime,
                'uuid4': uuid.uuid4
            })
        except Exception as err:
            logging.exception(f"Template at '{template}' failed to load, must reinit!")
            logging.exception(err)
            self.template = None
    def render(self, *args, **kwargs):
        return self.template.render(*args, **kwargs)

class Transformer(metaclass=abc.ABCMeta):
    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'load')
                and callable(subclass.load)
                and hasattr(subclass, 'transform')
                and callable(subclass.transform)
                and hasattr(subclass, 'save')
                and callable(subclass.save))

class AWSSecurityHubControlTransformer:
    def __init__(self, raw_data: List[Selector]):
        self.raw_data = raw_data if raw_data else []
        self.controls: Dict[str, Dict] = {}

    def transform(self):
        current_control_id: str = ''
        for d in self.raw_data:
            try:
                tag = d.root.tag
                if tag == 'p':
                    self.process_p(d, current_control_id)
                if tag == 'div':
                    self.process_div(d, current_control_id)
                if tag == 'h3':
                    self.process_h3(d, current_control_id)                    
                if tag == 'h2':
                    control_id, control_label, control_title = self.process_h2(d)
                    self.controls[control_id] = {}
                    self.controls[control_id] = {
                        'label': control_label,
                        'title': control_title
                    }
                    current_control_id = control_id

            except Exception as err:
                logging.exception(err)
        return self.controls

    def process_p(self, data: Selector, control_id: str):
        tag = 'p'
        print(f"{tag}: {data.extract()}")
        return

    def process_div(self, data: Selector, control_id: str):
        tag = 'div'
        print(f"{tag}: {data.extract()}")
        div_class = data.xpath("./@class").extract()[0]
        print(f"{tag}: {div_class}")
        if div_class == 'itemizedList':
            pass
        if div_class == 'other':
            pass
        return

    def process_h3(self, data: Selector, control_id: str):
        tag = 'h3'
        return

    def process_h2(self, data: Selector) -> (str, str, str):
        tag = 'h2'
        control_id = data.xpath("./@id").extract()[0]
        rest = data.xpath("./text()").extract()[0]
        matches = re.match(r"^\[([.A-Z0-9]{3,})\] (.*)$", rest)
        control_label, control_title = matches.groups()
        return control_id, control_label, control_title

class ControlIndexSpider:
    def __init__(self, url=[]):
        self.url = url
        self.raw_html = ''
        self.target_urls = []

    def crawl(self):
        try:
            response = requests.get(self.url)
            self.raw_html = response.content.decode('utf-8')
            selector = Selector(text=self.raw_html)
            data = selector.xpath("//div[@class='highlights']/ul/li/a/@href")                
            self.target_urls = [urljoin(response.url, url.extract()) for url in data]
            return self.target_urls
        except Exception as err:
            logging.exception(err)        

class ControlDetailSpider:
    def __init__(self, urls: List[str]):
        self.urls = urls if urls else []
        self.raw_data: List[Selector] = []
        self.raw_html = ''
    
    def crawl(self):
        for url in self.urls:
            try:
                #response = requests.get(url)
                #self.raw_html = response.content.decode('utf-8')
                with open('example.html') as fd:
                    self.raw_html = fd.read()
                selector = Selector(text=self.raw_html)
                self.raw_data = selector.xpath(
                    """
                    //div[@id='main-col-body']/*
                        [
                            self::div[@class != 'awsdocs-page-header-container'] or 
                            self::h2 or self::h3 or 
                            self::p/preceding-sibling::div[not(@class ='awsdocs-page-header-container')]
                        ]
                    """
                )                
                return self.raw_data
            
            except Exception as err:
                logging.exception(err)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Convert the AWS Security Hub controls website to an OSCAL JSON catalog')
    parser.add_argument(
        '-o',
        '--output-file',
        help='Path intended to save OSCAL JSON catalog file. If not provided print to standard out.',
        type=argparse.FileType('w'),
        dest='output_file',
        required=False
    )
    # index_spider = ControlIndexSpider(url='https://docs.aws.amazon.com/securityhub/latest/userguide/securityhub-controls-reference.html')
    # index_spider.crawl()
    control_spider = ControlDetailSpider(urls=['https://docs.aws.amazon.com/securityhub/latest/userguide/s3-controls.html'])
    raw_data = control_spider.crawl()
    transformer = AWSSecurityHubControlTransformer(raw_data)
    transformer.transform()
