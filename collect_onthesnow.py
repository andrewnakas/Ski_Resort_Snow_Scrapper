#!/usr/bin/env python3
"""
Collect snow data using OnTheSnow as the data source.
This is more reliable than scraping individual resort websites.
"""

import argparse
import logging
from datetime import date
from database import SkiResortDatabase
from resorts_onthesnow import ONTHESNOW_RESORTS
from scraper_onthesnow import OnTheSnowScraper
import time

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def init_database():
    """Initialize database with OnTheSnow resorts"""
    logger.info("Initializing database with OnTheSnow resorts...")
    db = SkiResortDatabase()

    added = 0
    for resort in ONTHESNOW_RESORTS:
        try:
            # Add resort with OnTheSnow URL
            resort_data = {
                'name': resort['name'],
                'country': resort['country'],
                'region': resort['region'],
                'website_url': f"https://www.onthesnow.com/{resort['slug']}",
                'snow_report_url': f"https://www.onthesnow.com/{resort['slug']}/skireport"
            }
            db.add_resort(resort_data)
            added += 1
        except Exception as e:
            # Resort might already exist
            pass

    logger.info(f"Database initialized with {len(ONTHESNOW_RESORTS)} resorts ({added} new)")


def collect_data(countries=None, resorts=None, limit=None):
    """Collect snow data from OnTheSnow"""
    db = SkiResortDatabase()
    scraper = OnTheSnowScraper()

    # Filter resorts
    resorts_to_scrape = ONTHESNOW_RESORTS

    if countries:
        resorts_to_scrape = [r for r in resorts_to_scrape if r['country'] in countries]

    if resorts:
        resorts_to_scrape = [r for r in resorts_to_scrape if r['name'] in resorts]

    if limit:
        resorts_to_scrape = resorts_to_scrape[:limit]

    logger.info(f"Starting scrape of {len(resorts_to_scrape)} resorts from OnTheSnow...")

    success_count = 0
    fail_count = 0
    start_time = time.time()

    for i, resort in enumerate(resorts_to_scrape, 1):
        logger.info(f"Processing resort {i}/{len(resorts_to_scrape)}: {resort['name']}")

        try:
            # Scrape data
            snow_data = scraper.scrape_resort(resort)

            if snow_data and len(snow_data) > 0:
                # Get resort ID from database
                resort_id = db.get_resort_id(resort['name'])

                if resort_id:
                    # Add snow data
                    snow_data['resort_id'] = resort_id
                    snow_data['date'] = date.today()

                    db.add_snow_data(snow_data)
                    logger.info(f"✓ Saved data for {resort['name']}")
                    success_count += 1
                else:
                    logger.warning(f"Resort {resort['name']} not found in database")
                    fail_count += 1
            else:
                logger.warning(f"✗ No data extracted for {resort['name']}")
                fail_count += 1

        except Exception as e:
            logger.error(f"Error processing {resort['name']}: {e}")
            fail_count += 1

        # Polite delay between requests
        time.sleep(2)

    elapsed = time.time() - start_time
    logger.info("=" * 60)
    logger.info(f"Scraping completed in {elapsed:.1f} seconds")
    logger.info(f"Success: {success_count}/{len(resorts_to_scrape)}")
    logger.info(f"Failed: {fail_count}/{len(resorts_to_scrape)}")
    logger.info("=" * 60)


def show_latest_data(resort_name=None):
    """Display latest snow data"""
    db = SkiResortDatabase()

    if resort_name:
        data = db.get_latest_snow_data(resort_name)
        if data:
            print(f"\n{resort_name} - Latest Snow Report")
            print("=" * 60)
            for key, value in data.items():
                if value is not None:
                    print(f"  {key}: {value}")
        else:
            print(f"No data found for {resort_name}")
    else:
        # Show all resorts
        print("\nLatest Snow Reports (OnTheSnow)")
        print("=" * 60)

        for resort in ONTHESNOW_RESORTS:
            data = db.get_latest_snow_data(resort['name'])
            if data:
                print(f"\n{resort['name']} ({resort['country']})")
                if data.get('new_snow_24h_cm'):
                    print(f"  24h Snow: {data['new_snow_24h_cm']} cm")
                if data.get('snow_depth_base_cm'):
                    print(f"  Base Depth: {data['snow_depth_base_cm']} cm")


def main():
    parser = argparse.ArgumentParser(description='Collect ski resort snow data from OnTheSnow')
    parser.add_argument('--init', action='store_true', help='Initialize database')
    parser.add_argument('--collect', action='store_true', help='Collect snow data')
    parser.add_argument('--show', action='store_true', help='Show latest data')
    parser.add_argument('--countries', nargs='+', help='Filter by countries')
    parser.add_argument('--resorts', nargs='+', help='Filter by resort names')
    parser.add_argument('--limit', type=int, help='Limit number of resorts to scrape')
    parser.add_argument('--resort', type=str, help='Show data for specific resort')

    args = parser.parse_args()

    if args.init:
        init_database()
    elif args.collect:
        collect_data(args.countries, args.resorts, args.limit)
    elif args.show:
        show_latest_data(args.resort)
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
