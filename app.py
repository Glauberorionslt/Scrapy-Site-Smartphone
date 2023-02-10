import scrapy
import logging
from selenium.webdriver.remote.remote_connection import LOGGER
from selenium.common.exceptions import *
from selenium.webdriver.support import expected_conditions as CondicaoExperada
from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from scrapy.selector import Selector
from time import sleep
import sys



def iniciar_driver():
    chrome_options = Options()
    LOGGER.setLevel(logging.WARNING)
    arguments = ['--lang=pt-BR', '--window-size=1920,1080', '--headless']
    for argument in arguments:
        chrome_options.add_argument(argument)

    chrome_options.add_experimental_option('prefs', {
        'download.prompt_for_download': False,
        'profile.default_content_setting_values.notifications': 2,
        'profile.default_content_setting_values.automatic_downloads': 1,

    })
    driver = webdriver.Chrome(service=ChromeService(
        ChromeDriverManager().install()), options=chrome_options)

    wait = WebDriverWait(
        driver,
        10,
        poll_frequency=1,
        ignored_exceptions=[
            NoSuchElementException,
            ElementNotVisibleException,
            ElementNotSelectableException,
        ]
    )
    return driver, wait

class Raspador_dados_spider(scrapy.Spider):   

    #identity
    name = "price_bot"

    def iniciar_requisicao(self):
     urls=['https://telefonesimportados.netlify.app/shop2.html']
     for url in urls:
        yield scrapy.Request(url=url,callback=self.parse, meta={'proximo_url':url})

#Response

    def parse(self,response):
        driver, wait = iniciar_driver()
        driver.get(response.meta['proximo_url'])
        response_webdriver = Selector(text=driver.page_source)

        for produto in response_webdriver.xpath('//div[@class="col-md-3 col-sm-6"]'):
            yield{
                'descricao': produto.xpath('.//div[1]//h2[1]/a/text()').get(),
                'preco_por': produto.xpath('.//div[1]//div[2]//ins/text()').get(),
                'preco_de': produto.xpath('.//div[1]//div[2]//del/text()').get()

            }

        #Link p Proxima pagina

        # try:
            
        #      link_px_pagina = response.xpath("a[@aria-label='Next']/@href")
        #      if link_px_pagina is not None:
        #         link_px_pagina_clp = "https://telefonesimportados.netlify.app/" + link_px_pagina
        #         yield scrapy.Request(url=link_px_pagina_clp,callback=self.parse)

        # except:
        #     print ("Chegamos a ultima pagina")




     