#!/usr/bin/env python3
"""
GribStream API scraper for ski resort snow forecasts.
Uses HRRR and GFS models for snow depth and precipitation data.
"""

import requests
import logging
from datetime import datetime, timedelta
from typing import Dict, Optional, List
import time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class GribStreamScraper:
    """Scrape snow forecast data from GribStream API"""

    API_BASE = "https://gribstream.com/api/v2"
    API_KEY = "58ba41a8c25b193416720508b0ad0c1c1670a8fb"  # Your API key

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'Authorization': f'Bearer {self.API_KEY}',
            'Content-Type': 'application/json'
        })

    def get_snow_forecast(self, resort_data: Dict) -> Optional[Dict]:
        """
        Get snow forecast for a resort using GribStream API

        Uses HRRR model for short-term (0-18h) and GFS for extended forecasts
        """
        resort_name = resort_data['name']
        lat = resort_data.get('latitude')
        lon = resort_data.get('longitude')

        if not lat or not lon:
            logger.warning(f"No coordinates for {resort_name}")
            return None

        try:
            # Get current time and forecast windows
            now = datetime.utcnow()
            forecast_start = now.replace(minute=0, second=0, microsecond=0)
            forecast_end = forecast_start + timedelta(hours=48)

            # Request payload for HRRR model (high resolution, US only)
            payload = {
                "forecastedFrom": forecast_start.isoformat() + "Z",
                "forecastedUntil": forecast_end.isoformat() + "Z",
                "coordinates": [{
                    "lat": lat,
                    "lon": lon,
                    "name": resort_name
                }],
                "variables": [
                    {"name": "ASNOW", "level": "surface", "alias": "snow_accum"},  # Accumulated snow
                    {"name": "SNOD", "level": "surface", "alias": "snow_depth"},    # Snow depth
                    {"name": "APCP", "level": "surface", "alias": "precip"},        # Precipitation
                    {"name": "TMP", "level": "2 m above ground", "alias": "temp"},  # Temperature
                    {"name": "CSNOW", "level": "surface", "alias": "is_snow"}       # Categorical snow
                ]
            }

            # Try HRRR first (US only, high resolution)
            url = f"{self.API_BASE}/hrrr/forecasts"
            logger.info(f"Fetching GribStream forecast for {resort_name} at ({lat}, {lon})")

            response = self.session.post(url, json=payload, timeout=30)

            # If HRRR fails (likely outside US), try GFS global model
            if response.status_code != 200:
                logger.info(f"HRRR unavailable for {resort_name}, trying GFS...")
                url = f"{self.API_BASE}/gfs/forecasts"
                response = self.session.post(url, json=payload, timeout=30)

            response.raise_for_status()
            data = response.json()

            # Parse the response
            return self._parse_gribstream_response(data, resort_name)

        except requests.RequestException as e:
            logger.error(f"API error for {resort_name}: {e}")
            return None
        except Exception as e:
            logger.error(f"Error processing {resort_name}: {e}")
            return None

    def _parse_gribstream_response(self, api_data: dict, resort_name: str) -> Optional[Dict]:
        """Parse GribStream API response into snow data"""

        try:
            if not api_data or 'data' not in api_data:
                logger.warning(f"No data in response for {resort_name}")
                return None

            # GribStream returns time series data
            data_points = api_data['data']

            if not data_points:
                return None

            # Extract snow metrics
            result = {}

            # Get latest values from the time series
            latest = data_points[-1] if isinstance(data_points, list) else data_points

            # Parse snow accumulation (convert kg/m^2 to cm)
            # 1 kg/m^2 of water = 1mm, snow is ~10:1 ratio
            if 'snow_accum' in latest:
                snow_kg = latest['snow_accum']
                result['new_snow_24h_cm'] = int(snow_kg * 10)  # Approximate conversion

            # Parse snow depth (convert m to cm)
            if 'snow_depth' in latest:
                snow_m = latest['snow_depth']
                result['snow_depth_base_cm'] = int(snow_m * 100)

            # Parse precipitation
            if 'precip' in latest:
                precip_kg = latest['precip']
                # Check if it's snow based on temperature or categorical snow
                is_snow = latest.get('is_snow', 0) > 0 or latest.get('temp', 273) < 273.15
                if is_snow:
                    result['new_snow_24h_cm'] = int(precip_kg * 10)

            # Temperature (convert K to C)
            if 'temp' in latest:
                temp_k = latest['temp']
                result['temperature_base_c'] = round(temp_k - 273.15, 1)

            # Calculate 48h and 7d snowfall from time series
            if isinstance(data_points, list) and len(data_points) > 1:
                # Sum snowfall over different time periods
                snow_48h = sum(p.get('snow_accum', 0) for p in data_points[:48])
                result['new_snow_48h_cm'] = int(snow_48h * 10)

            if result:
                logger.info(f"✓ Successfully fetched {resort_name} from GribStream - {len(result)} data points")
                return result
            else:
                return None

        except Exception as e:
            logger.error(f"Error parsing GribStream data for {resort_name}: {e}")
            return None


def test_gribstream():
    """Test the GribStream scraper"""
    scraper = GribStreamScraper()

    # Test with a few US resorts (HRRR coverage)
    test_resorts = [
        {'name': 'Vail', 'latitude': 39.6403, 'longitude': -106.3742},
        {'name': 'Jackson Hole', 'latitude': 43.5875, 'longitude': -110.8281},
        {'name': 'Park City', 'latitude': 40.6514, 'longitude': -111.5079},
    ]

    for resort in test_resorts:
        print(f"\n{'='*60}")
        print(f"Testing: {resort['name']}")
        print('='*60)
        data = scraper.get_snow_forecast(resort)
        if data:
            for key, value in data.items():
                print(f"  {key}: {value}")
        else:
            print("  No data extracted")
        time.sleep(2)


if __name__ == '__main__':
    test_gribstream()
