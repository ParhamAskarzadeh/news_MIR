from scrapy import Selector
from requests import ReadTimeout, TooManyRedirects, Timeout
from requests.exceptions import ChunkedEncodingError, ConnectionError
import time
import requests
import re


class Crawler:

    def crawl_news(self, news_id):
        def get_data(content):
            doc = {
                'title': Selector(text=content).xpath("//span[@class='title-news']//text()").get(),
                'id': int(Selector(text=content).xpath("//span[@class='number-news']//text()").get().replace(' ', '')),
                'lead': Selector(text=content).xpath("//h2[@class='Htags_news_subtitle']//strong[@class='news_strong']//text()").get(),
                'main_image': Selector(text=content).xpath("//div[@class='parent-lead-img']//img/@src").get(),
                'published_date': Selector(text=content).xpath(
                    "//meta[@property='article:published_time']/@content").get(),
                'tags': Selector(text=content).xpath("//div[@class='path_bottom_body']//a//text()").getall(),
                'category': Selector(text=content).xpath("//a[@class='cat-news-details']//text()").get()
            }
            temp_content = Selector(text=content).xpath("//div[@class='row baznashr-body']//p//text()").getall()
            content = ''
            for s in temp_content:
                content += s
            doc['content'] = content
            return doc

        url = 'https://www.yjc.news/fa/news/' + str(news_id)
        while True:
            try:
                response = requests.get(url, timeout=30)
                if response.status_code == 429:
                    time.sleep(1)
                    continue
            except (Timeout, ReadTimeout, ConnectionError, TooManyRedirects, ChunkedEncodingError) as e:
                time.sleep(30)
                continue

            result = {}

            result['news_information'] = get_data(response.text)
            result['other_news_ids'] = self.__get_links_of_news(response.text)
            return result

    def __get_links_of_news(self, content):
        all_links = Selector(text=content).xpath("//a/@href").getall()
        news_links = []
        for link in all_links:
            short_link = re.findall("/fa/news/(?:\d+)/.[^\.]*$", link)
            if len(short_link) > 0:
                news_links.append(re.findall("news/(\d+)/", short_link[0])[0])
        return news_links


