import scrapy
import re
import json
import os

# TODO: add parse exception handling

START_FILE = "eo1.json"

class CharitySpider(scrapy.Spider):
    name = 'charity'  
    allowed_domains = ['charitynavigator.org']  # Restrict crawling to this domain
    
    start_urls = []  # Initialize as empty list
    
    def _prepare_start_urls(self):
        with open(START_FILE, 'r') as file:
            ein_list = json.load(file)['ein_numbers']
        return [f'https://www.charitynavigator.org/ein/{ein}' for ein in ein_list]
    
    def start_requests(self):
        for url in self._prepare_start_urls():
            yield scrapy.Request(
                url=url,
                callback=self.parse,
                dont_filter=True,
                meta={'handle_httpstatus_list': [403, 404, 500, 406]}
                
            )

    
    def _get_rating_information_text(self, response):
        texts = response.css('div#overall-rating-section-2 ::text').getall()
        return ' '.join(text.strip() for text in texts if text.strip())
    
    def _get_alert_details_text(self, response):
        texts = response.css('div#alert-details-section ::text').getall()
        return ' '.join(text.strip() for text in texts if text.strip())
    
    def _get_rating_section_text(self, response):
        texts = response.css(".tw-bg-white.tw-border.tw-rounded-2xl ::text").getall()
        return ' '.join(text.strip() for text in texts if text.strip())
    
    def _get_contact_section_text(self, response):
        texts = response.css('div.tw-grid.tw-grid-cols-1.md\\:tw-grid-cols-2 ::text').getall()
        return ' '.join(text.strip() for text in texts if text.strip())
    
    def _parse_name(self, response):
        return " ".join(response.css('#cn-header h1::text').getall()).strip()
    
    def _parse_ein(self, response):
        container = response.css('div.tw-flex.tw-flex-row.tw-px-4.tw-items-center::text').getall()
        text = ''.join(container)
        
        ein_match = re.search(r'EIN:\s*(\d+)\s*-\s*(\d+)', text)
        if ein_match:
            return ein_match.group(1) + ein_match.group(2)


    def _parse_score(self, response):
        rating_information_texts = self._get_rating_information_text(response)

        score_match = re.search(r"score is\s*(\d+)\s*%", rating_information_texts)
        if score_match:
            return f"{int(score_match.group(1))}%"
        else:
            return None
    

    def _parse_star_rating(self, response):
        rating_information_texts = self._get_rating_information_text(response)
        
        star_match = re.search(r"earning it a\s*(One|Two|Three|Four)-Star\s*rating", rating_information_texts)
        if star_match:
            star_map = {
                'Four': 4,
                'Three': 3,
                'Two': 2,
                'One': 1
            }
            return star_map.get(star_match.group(1))
        return None
    

    def _parse_keywords(self, response):
        KEYWORDS = [
            "This organization is not rated",
            "Not currently rated",
            "Not rated",
            "Review Before Proceeding",
            "Proceed with Caution",
            "Proceed with Increased Caution",
            "Giving Not Recommended",
            "Confirmed Revocation",
            "Giving Basket is Disabled"
        ]
        
        seen_keywords = set()
        
        

        rating_information_texts = self._get_rating_information_text(response)
        alert_details_section = self._get_alert_details_text(response)
        rating_section_text = self._get_rating_section_text(response)
        contact_section_text = self._get_contact_section_text(response)
        
        target_text = f"{rating_information_texts} {alert_details_section} {rating_section_text} {contact_section_text}"
        
        for keyword in KEYWORDS:
            if keyword.lower() in target_text.lower():
                seen_keywords.add(keyword)
        
        return ', '.join(seen_keywords)
        
            
    def _parse_website(self, response):
        website_path = 'M11 3a1 1 0 100 2h2.586l-6.293 6.293a1 1 0 101.414 1.414L15 6.414V9a1 1 0 102 0V4a1 1 0 00-1-1h-5z'        
        website = response.xpath(f'//path[@d="{website_path}"]/ancestor::div[contains(@class, "tw-flex-row")][1]//div[@class="tw-flex-1"]//a[contains(@href, "http")]/@href').get()
        return website
                
        
    def _parse_address(self, response):
        location_path = 'M5.05 4.05a7 7 0 119.9 9.9L10 18.9l-4.95-4.95a7 7 0 010-9.9zM10 11a2 2 0 100-4 2 2 0 000 4z'
        address_texts = response.xpath(f'//path[@d="{location_path}"]/ancestor::div[contains(@class, "tw-flex-row")][1]//div[contains(@class, "tw-text-gray-600")]//text()').getall()
        address = ', '.join(text.strip() for text in address_texts if text.strip())
        return address
    
    def _parse_phone(self, response):
        phone_path = 'M2 3a1 1 0 011-1h2.153a1 1 0 01.986.836l.74 4.435a1 1 0 01-.54 1.06l-1.548.773a11.037 11.037 0 006.105 6.105l.774-1.548a1 1 0 011.059-.54l4.435.74a1 1 0 01.836.986V17a1 1 0 01-1 1h-2C7.82 18 2 12.18 2 5V3z'
        phone = response.xpath(f'//path[@d="{phone_path}"]/ancestor::div[contains(@class, "tw-flex-row")][1]//div[@class="tw-flex-1"]//a/text()').get()
        return phone
    
    def _parse_organization_mission(self, response):
        mission_texts = response.xpath('//div[text()="Organization Mission"]/ancestor::div[@class="tw-px-4"][1]//text()').getall()
        mission = ' '.join(text.strip() for text in mission_texts if text.strip())
        
        if mission.startswith('Organization Mission '):
            mission = mission[len('Organization Mission '):]
        
        return mission
    
    def _parse_IRS_ruling_year(self, response):
        container = response.css('div.tw-flex.tw-flex-row.tw-px-4.tw-items-center::text').getall()
        text = ''.join(container)
        
        year_match = re.search(r'IRS ruling year:\s*(\d{4})', text)
        if year_match:
            return year_match.group(1)
        return None
    
    def _parse_contain_keywords(self, response):
        keywords = self._parse_keywords(response)
        if keywords:
            return 'Yes'
        return 'No'
    
    def parse(self, response):
        """
        Main parsing method that processes the response from start_urls
        """
        
        if response.status == 406:
            self.logger.error(f"Error parsing {response.url}: {response.status}")
            with open('error_log.txt', 'a') as f:
                f.write(f"{response.url} - {response.status}\n")
            return
        
        
        try:
            item = {
                    'url': response.url,
                    'name': ''.join(response.css("h1.tw-text-3xl::text").getall()).strip(),
                    'ein': response.url.split('/')[-1],
                    'score': self._parse_score(response),
                    'star_rating': self._parse_star_rating(response),
                    'keywords': self._parse_keywords(response),
                    'website': self._parse_website(response),
                    'address': self._parse_address(response),
                    'phone': self._parse_phone(response),
                    'organization_mission': self._parse_organization_mission(response),
                    'IRS_ruling_year': self._parse_IRS_ruling_year(response),
                    'contain_keywords': self._parse_contain_keywords(response),
            }
            yield item
        except Exception as e:
            self.logger.error(f"Error parsing {response.url}: {str(e)}")
            with open('error_log.txt', 'a') as f:
                f.write(f"{response.url} - {str(e)}\n")
            
