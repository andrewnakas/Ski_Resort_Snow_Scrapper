#!/usr/bin/env python3
"""
Collect snow forecast data using GribStream API.
Uses weather forecast models (HRRR for US, GFS globally) to get snow data.
"""

import argparse
import logging
from datetime import date
from database import SkiResortDatabase
from resorts_onthesnow import ONTHESNOW_RESORTS
from scraper_gribstream import GribStreamScraper
import time

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def init_database():
    """Initialize database with resort coordinates"""
    logger.info("Initializing database with resort data...")
    db = SkiResortDatabase()

    # Add coordinates to resorts (these are approximate, you can update with exact coordinates)
    resort_coords = {
        # Colorado
        'Vail': (39.6403, -106.3742),
        'Aspen Snowmass': (39.2091, -106.9461),
        'Breckenridge': (39.4817, -106.0384),
        'Keystone': (39.5792, -105.9347),
        'Steamboat': (40.4580, -106.8050),
        'Winter Park': (39.8869, -105.7625),
        'Copper Mountain': (39.5022, -106.1503),
        'Telluride': (37.9375, -107.8123),
        'Crested Butte': (38.8997, -106.9653),
        'Beaver Creek': (39.6042, -106.5165),
        'Arapahoe Basin': (39.6428, -105.8719),
        'Loveland': (39.6800, -105.8978),

        # Utah
        'Park City': (40.6514, -111.5079),
        'Alta': (40.5885, -111.6381),
        'Snowbird': (40.5830, -111.6560),
        'Deer Valley': (40.6374, -111.4783),
        'Brighton': (40.5981, -111.5831),
        'Solitude': (40.6200, -111.5919),

        # California
        'Mammoth Mountain': (37.6308, -119.0326),
        'Palisades Tahoe': (39.1969, -120.2357),
        'Heavenly': (38.9352, -119.9394),
        'Northstar': (39.2730, -120.1217),
        'Kirkwood': (38.6844, -120.0644),

        # Wyoming
        'Jackson Hole': (43.5875, -110.8281),
        'Grand Targhee': (43.7897, -111.1142),

        # Vermont
        'Stowe': (44.5303, -72.7817),
        'Killington': (43.6042, -72.8223),
        'Sugarbush': (44.1342, -72.9031),

        # New Hampshire
        'Bretton Woods': (44.2592, -71.4420),
        'Loon Mountain': (44.0369, -71.6214),

        # Canada - BC
        'Whistler Blackcomb': (50.1163, -122.9574),
        'Revelstoke': (50.9981, -118.1957),
        'Big White': (49.7253, -118.9335),

        # Canada - Alberta
        'Lake Louise': (51.4254, -116.1773),
        'Sunshine Village': (51.1125, -115.7642),
    }

    added = 0
    for resort in ONTHESNOW_RESORTS:
        try:
            coords = resort_coords.get(resort['name'])
            if coords:
                resort_data = {
                    'name': resort['name'],
                    'country': resort['country'],
                    'region': resort['region'],
                    'latitude': coords[0],
                    'longitude': coords[1],
                    'website_url': f"https://www.onthesnow.com/{resort['slug']}",
                    'snow_report_url': f"https://www.onthesnow.com/{resort['slug']}/skireport"
                }
                db.add_resort(resort_data)
                added += 1
        except Exception as e:
            pass  # Resort might already exist

    logger.info(f"Database initialized with {len(ONTHESNOW_RESORTS)} resorts ({added} new with coordinates)")


def collect_data(countries=None, resorts=None, limit=None):
    """Collect snow forecast data from GribStream"""
    db = SkiResortDatabase()
    scraper = GribStreamScraper()

    # Filter resorts
    resorts_to_scrape = ONTHESNOW_RESORTS

    if countries:
        resorts_to_scrape = [r for r in resorts_to_scrape if r['country'] in countries]

    if resorts:
        resorts_to_scrape = [r for r in resorts_to_scrape if r['name'] in resorts]

    if limit:
        resorts_to_scrape = resorts_to_scrape[:limit]

    logger.info(f"Starting GribStream forecast collection for {len(resorts_to_scrape)} resorts...")

    success_count = 0
    fail_count = 0
    start_time = time.time()

    for i, resort in enumerate(resorts_to_scrape, 1):
        logger.info(f"Processing resort {i}/{len(resorts_to_scrape)}: {resort['name']}")

        # Need to get coordinates from database
        resort_id = db.get_resort_id(resort['name'])
        if not resort_id:
            logger.warning(f"Resort {resort['name']} not in database")
            fail_count += 1
            continue

        # Get full resort data with coordinates
        conn = db.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM resorts WHERE id = ?", (resort_id,))
        resort_record = cursor.fetchone()
        conn.close()

        if not resort_record:
            fail_count += 1
            continue

        # Convert to dict with coordinates
        resort_with_coords = {
            'name': resort['name'],
            'latitude': resort_record[4],  # latitude column
            'longitude': resort_record[5],  # longitude column
        }

        try:
            # Scrape forecast data
            snow_data = scraper.get_snow_forecast(resort_with_coords)

            if snow_data and len(snow_data) > 0:
                # Add snow data to database
                snow_data['resort_id'] = resort_id
                snow_data['date'] = date.today()

                db.add_snow_data(snow_data)
                logger.info(f"✓ Saved forecast for {resort['name']}")
                success_count += 1
            else:
                logger.warning(f"✗ No forecast data for {resort['name']}")
                fail_count += 1

        except Exception as e:
            logger.error(f"Error processing {resort['name']}: {e}")
            fail_count += 1

        # Polite API delay
        time.sleep(1)

    elapsed = time.time() - start_time
    logger.info("=" * 60)
    logger.info(f"Collection completed in {elapsed:.1f} seconds")
    logger.info(f"Success: {success_count}/{len(resorts_to_scrape)}")
    logger.info(f"Failed: {fail_count}/{len(resorts_to_scrape)}")
    logger.info("=" * 60)


def show_latest_data(resort_name=None):
    """Display latest forecast data"""
    db = SkiResortDatabase()

    if resort_name:
        data = db.get_latest_snow_data(resort_name)
        if data:
            print(f"\n{resort_name} - Latest Forecast")
            print("=" * 60)
            for key, value in data.items():
                if value is not None:
                    print(f"  {key}: {value}")
        else:
            print(f"No data found for {resort_name}")
    else:
        # Show all resorts
        print("\nLatest Snow Forecasts (GribStream)")
        print("=" * 60)

        for resort in ONTHESNOW_RESORTS[:20]:  # Show first 20
            data = db.get_latest_snow_data(resort['name'])
            if data:
                print(f"\n{resort['name']} ({resort['country']})")
                if data.get('new_snow_24h_cm'):
                    print(f"  24h Forecast: {data['new_snow_24h_cm']} cm")
                if data.get('snow_depth_base_cm'):
                    print(f"  Snow Depth: {data['snow_depth_base_cm']} cm")
                if data.get('temperature_base_c'):
                    print(f"  Temperature: {data['temperature_base_c']}°C")


def main():
    parser = argparse.ArgumentParser(description='Collect snow forecasts from GribStream API')
    parser.add_argument('--init', action='store_true', help='Initialize database')
    parser.add_argument('--collect', action='store_true', help='Collect forecast data')
    parser.add_argument('--show', action='store_true', help='Show latest forecasts')
    parser.add_argument('--countries', nargs='+', help='Filter by countries')
    parser.add_argument('--resorts', nargs='+', help='Filter by resort names')
    parser.add_argument('--limit', type=int, help='Limit number of resorts')
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
