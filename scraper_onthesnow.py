#!/usr/bin/env python3
"""
OnTheSnow scraper - Gets snow data from OnTheSnow.com
This is more reliable than scraping individual resort websites.
"""

import requests
from bs4 import BeautifulSoup
import time
import re
from typing import Dict, Optional
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class OnTheSnowScraper:
    """Scrape snow data from OnTheSnow.com"""

    BASE_URL = "https://www.onthesnow.com"

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        })

    def get_resort_slug(self, resort_name: str, country: str) -> Optional[str]:
        """Convert resort name to OnTheSnow URL slug"""
        # Common mappings
        slug_map = {
            # USA
            'Vail': 'colorado/vail',
            'Aspen Snowmass': 'colorado/aspen-snowmass',
            'Breckenridge': 'colorado/breckenridge',
            'Keystone': 'colorado/keystone',
            'Steamboat': 'colorado/steamboat',
            'Park City': 'utah/park-city-mountain-resort',
            'Alta': 'utah/alta',
            'Snowbird': 'utah/snowbird',
            'Deer Valley': 'utah/deer-valley-resort',
            'Mammoth Mountain': 'california/mammoth-mountain',
            'Palisades Tahoe': 'california/palisades-tahoe',
            'Heavenly': 'california/heavenly',
            'Jackson Hole': 'wyoming/jackson-hole',
            'Stowe': 'vermont/stowe',
            'Killington': 'vermont/killington',

            # Canada
            'Whistler Blackcomb': 'british-columbia/whistler-blackcomb',
            'Revelstoke': 'british-columbia/revelstoke-mountain-resort',
            'Big White': 'british-columbia/big-white',
            'Lake Louise': 'alberta/lake-louise',
            'Sunshine Village': 'alberta/sunshine-village',
            'Tremblant': 'quebec/tremblant',

            # Europe
            'Chamonix': 'france/chamonix-mont-blanc',
            "Val d'Isère": 'france/val-d-isere-tignes',
            'Courchevel': 'france/courchevel',
            'Les Trois Vallées': 'france/les-3-vallees',
            'Zermatt': 'switzerland/zermatt',
            'Verbier': 'switzerland/verbier',
            'St. Moritz': 'switzerland/st-moritz',
            'St. Anton': 'austria/st-anton',
            'Ischgl': 'austria/ischgl',
            'Kitzbühel': 'austria/kitzbuehel',
            'Cortina d\'Ampezzo': 'italy/cortina-d-ampezzo',

            # Japan
            'Niseko': 'japan/niseko',
            'Hakuba Valley': 'japan/hakuba-valley',
            'Rusutsu': 'japan/rusutsu',

            # South Korea
            'Yongpyong': 'south-korea/yongpyong',
        }

        return slug_map.get(resort_name)

    def scrape_resort(self, resort_data: Dict) -> Optional[Dict]:
        """Scrape snow data from OnTheSnow for a specific resort"""
        resort_name = resort_data['name']
        country = resort_data['country']

        slug = self.get_resort_slug(resort_name, country)
        if not slug:
            logger.warning(f"No OnTheSnow slug mapping for {resort_name}")
            return None

        url = f"{self.BASE_URL}/{slug}/skireport"

        try:
            logger.info(f"Fetching {url}")
            response = self.session.get(url, timeout=10)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, 'html.parser')

            data = {}

            # Extract snow depths
            snow_data_divs = soup.find_all('div', class_='snow-report__stat')

            for div in snow_data_divs:
                label = div.find('div', class_='snow-report__stat-label')
                value = div.find('div', class_='snow-report__stat-value')

                if label and value:
                    label_text = label.get_text(strip=True).lower()
                    value_text = value.get_text(strip=True)

                    # Parse snow depth values
                    inches_match = re.search(r'(\d+)"', value_text)
                    if inches_match:
                        inches = int(inches_match.group(1))
                        cm = int(inches * 2.54)

                        if 'base' in label_text and 'depth' in label_text:
                            data['snow_depth_base_cm'] = cm
                        elif 'summit' in label_text or 'top' in label_text:
                            data['snow_depth_summit_cm'] = cm
                        elif '24' in label_text or 'overnight' in label_text:
                            data['new_snow_24h_cm'] = cm
                        elif '48' in label_text:
                            data['new_snow_48h_cm'] = cm
                        elif '7' in label_text or 'week' in label_text:
                            data['new_snow_7d_cm'] = cm

            # Extract terrain status
            terrain_divs = soup.find_all('div', class_='terrain-stats__stat')
            for div in terrain_divs:
                label = div.find('div', class_='terrain-stats__label')
                value = div.find('div', class_='terrain-stats__value')

                if label and value:
                    label_text = label.get_text(strip=True).lower()
                    value_text = value.get_text(strip=True)

                    # Parse lift/run data
                    match = re.search(r'(\d+)\s*/\s*(\d+)', value_text)
                    if match:
                        open_count = int(match.group(1))
                        total_count = int(match.group(2))

                        if 'lift' in label_text:
                            data['lifts_open'] = open_count
                            data['lifts_total'] = total_count
                        elif 'trail' in label_text or 'run' in label_text:
                            data['runs_open'] = open_count
                            data['runs_total'] = total_count

            if data:
                logger.info(f"✓ Successfully scraped {resort_name} from OnTheSnow - {len(data)} data points")
                return data
            else:
                logger.warning(f"Could not extract data for {resort_name} from OnTheSnow")
                return None

        except requests.RequestException as e:
            logger.error(f"Error fetching OnTheSnow for {resort_name}: {e}")
            return None
        except Exception as e:
            logger.error(f"Error parsing OnTheSnow data for {resort_name}: {e}")
            return None


def test_scraper():
    """Test the OnTheSnow scraper"""
    scraper = OnTheSnowScraper()

    test_resorts = [
        {'name': 'Vail', 'country': 'USA'},
        {'name': 'Jackson Hole', 'country': 'USA'},
        {'name': 'Whistler Blackcomb', 'country': 'Canada'},
    ]

    for resort in test_resorts:
        print(f"\n{'='*60}")
        print(f"Testing: {resort['name']}")
        print('='*60)
        data = scraper.scrape_resort(resort)
        if data:
            for key, value in data.items():
                print(f"  {key}: {value}")
        else:
            print("  No data extracted")
        time.sleep(2)


if __name__ == '__main__':
    test_scraper()
