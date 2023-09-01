import json
import logging
import os

import scrapy

logging.basicConfig(level=logging.INFO)


class FinancialtimesscraperSpider(scrapy.Spider):
    """
    Scrapy spider for scraping data from the Financial Times website.
    """

    name = "FinancialTimesScraper"
    allowed_domains = ["www.ft.com"]
    start_urls = ["https://www.ft.com/green-bonds"]

    def parse(self, response, **kwargs):
        """
        Parse the response from the initial URL and extract data from the web page.

        Args:
            response (scrapy.http.Response): The response object containing the web page content.

        Yields:
            scrapy.Request: A request to scrape the next page if available.
        """
        all_li_tags = response.xpath("//div[contains(@class,'stream-card__date')]/../..")
        for tag in all_li_tags:
            special_report = tag.css("span.o-teaser__tag-prefix").get()
            is_special_report = "Special Report" in special_report if special_report else False
            image_element = tag.css("img.o-teaser__image.o-lazy-load::attr(data-src)").get()
            date_posted = tag.css('time.o-date::text').get()
            posted_by = tag.css('a.o-teaser__tag::text').get()
            title = tag.css('div.o-teaser__heading a::text').get()
            description = tag.css('p.o-teaser__standfirst a.js-teaser-standfirst-link::text').get()
            scraped_data = {'is_special_report': is_special_report, 'image_element': image_element,
                            'date_posted': date_posted, 'posted_by': posted_by, 'title': title,
                            'description': description}
            logging.info(f"Successfully scraped data of: {title}")
            self.fill_scraper_data_in_json(scraped_data, 'output.json')
        if next_page_link := response.css('a.o-buttons-icon--arrow-right::attr(href)').get():
            yield scrapy.Request(url=f'https://www.ft.com/green-bonds{next_page_link}', callback=self.parse)

    @staticmethod
    def fill_scraper_data_in_json(new_row, output_file_name):
        """
        Append scraped data to a JSON file or create a new JSON file if it doesn't exist.

        Args:
            new_row (dict): The scraped data to be added to the JSON file.
            output_file_name (str): The name of the JSON output file.

        Raises:
            Exception: If there is an error while reading or writing the JSON file.
        """
        if not os.path.exists(output_file_name):
            data = {new_row['image_element']: new_row}
            with open(output_file_name, 'w', encoding='utf-8') as json_file:
                json.dump(data, json_file, ensure_ascii=False, indent=4)
        else:
            try:
                with open(output_file_name, 'r', encoding='utf-8') as json_file:
                    data = json.load(json_file)
                data[new_row['image_element']] = new_row
                with open(output_file_name, 'w', encoding='utf-8') as json_file:
                    json.dump(data, json_file, ensure_ascii=False, indent=4)
            except Exception as e:
                logging.info(f"Error: {e}")
