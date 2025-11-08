#!/usr/bin/env python3
"""
Generate HTML dashboard for GitHub Pages from ski resort database.
"""

import sqlite3
from datetime import datetime
from typing import List, Dict, Optional
import os


class HTMLGenerator:
    def __init__(self, db_path: str = 'ski_resorts.db'):
        self.db_path = db_path
        if not os.path.exists(db_path):
            raise FileNotFoundError(f"Database file not found: {db_path}")
        self.conn = sqlite3.connect(db_path)
        self.conn.row_factory = sqlite3.Row

    def get_latest_data(self) -> List[Dict]:
        """Get latest snow data for all resorts."""
        cursor = self.conn.cursor()
        query = """
        SELECT
            r.name,
            r.country,
            r.region,
            r.website_url,
            s.date,
            s.snow_depth_base_cm,
            s.snow_depth_summit_cm,
            s.new_snow_24h_cm,
            s.new_snow_48h_cm,
            s.new_snow_7d_cm,
            s.season_total_cm,
            s.lifts_open,
            s.lifts_total,
            s.runs_open,
            s.runs_total,
            s.temperature_base_c,
            s.weather_condition,
            s.last_snowfall_date
        FROM snow_data s
        JOIN resorts r ON s.resort_id = r.id
        WHERE s.date = (
            SELECT MAX(date) FROM snow_data WHERE resort_id = s.resort_id
        )
        ORDER BY s.new_snow_24h_cm DESC NULLS LAST, r.name
        """

        cursor.execute(query)
        results = []
        for row in cursor.fetchall():
            results.append(dict(row))
        return results

    def get_statistics(self) -> Dict:
        """Get database statistics."""
        cursor = self.conn.cursor()

        stats = {}

        # Total resorts
        cursor.execute("SELECT COUNT(*) FROM resorts")
        stats['total_resorts'] = cursor.fetchone()[0]

        # Total records
        cursor.execute("SELECT COUNT(*) FROM snow_data")
        stats['total_records'] = cursor.fetchone()[0]

        # Latest update date
        cursor.execute("SELECT MAX(date) FROM snow_data")
        stats['last_update'] = cursor.fetchone()[0]

        # Countries
        cursor.execute("SELECT COUNT(DISTINCT country) FROM resorts")
        stats['total_countries'] = cursor.fetchone()[0]

        # Top powder resort today
        cursor.execute("""
            SELECT r.name, s.new_snow_24h_cm
            FROM snow_data s
            JOIN resorts r ON s.resort_id = r.id
            WHERE s.date = (SELECT MAX(date) FROM snow_data)
            AND s.new_snow_24h_cm IS NOT NULL
            ORDER BY s.new_snow_24h_cm DESC
            LIMIT 1
        """)
        top = cursor.fetchone()
        if top:
            stats['top_powder_resort'] = top[0]
            stats['top_powder_amount'] = top[1]
        else:
            stats['top_powder_resort'] = None
            stats['top_powder_amount'] = None

        return stats

    def generate_html(self, output_path: str = 'index.html'):
        """Generate complete HTML page."""
        data = self.get_latest_data()
        stats = self.get_statistics()

        html = self._get_html_template(data, stats)

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html)

        print(f"✓ Generated {output_path}")
        print(f"  - {len(data)} resorts with data")
        print(f"  - Last update: {stats.get('last_update', 'N/A')}")

    def _format_value(self, value, unit: str = '') -> str:
        """Format a value for display."""
        if value is None:
            return '<span class="na">N/A</span>'
        return f'{value}{unit}'

    def _get_snow_badge(self, cm: Optional[float]) -> str:
        """Get colored badge for snowfall amount."""
        if cm is None:
            return ''
        elif cm >= 30:
            return f'<span class="badge badge-epic">{cm} cm</span>'
        elif cm >= 15:
            return f'<span class="badge badge-great">{cm} cm</span>'
        elif cm >= 5:
            return f'<span class="badge badge-good">{cm} cm</span>'
        else:
            return f'<span class="badge badge-light">{cm} cm</span>'

    def _get_html_template(self, data: List[Dict], stats: Dict) -> str:
        """Generate the complete HTML template."""

        # Generate table rows
        rows = []
        for resort in data:
            website = resort.get('website_url', '#')
            name_link = f'<a href="{website}" target="_blank">{resort["name"]}</a>' if website and website != '#' else resort['name']

            row = f"""
            <tr>
                <td class="resort-name">{name_link}</td>
                <td>{resort.get('country', 'N/A')}</td>
                <td>{resort.get('region', 'N/A')}</td>
                <td class="snow-data">{self._get_snow_badge(resort.get('new_snow_24h_cm'))}</td>
                <td class="snow-data">{self._format_value(resort.get('new_snow_48h_cm'), ' cm')}</td>
                <td class="snow-data">{self._format_value(resort.get('new_snow_7d_cm'), ' cm')}</td>
                <td>{self._format_value(resort.get('snow_depth_base_cm'), ' cm')}</td>
                <td>{self._format_value(resort.get('snow_depth_summit_cm'), ' cm')}</td>
                <td>{self._format_lifts(resort.get('lifts_open'), resort.get('lifts_total'))}</td>
                <td class="conditions">{resort.get('weather_condition', 'N/A')}</td>
            </tr>
            """
            rows.append(row)

        table_content = '\n'.join(rows) if rows else '<tr><td colspan="10" class="no-data">No data available yet. Run the scraper to collect data!</td></tr>'

        # Generate stats cards
        last_update = stats.get('last_update', 'Never')
        if last_update and last_update != 'Never':
            try:
                last_update_dt = datetime.strptime(last_update, '%Y-%m-%d')
                last_update = last_update_dt.strftime('%B %d, %Y')
            except:
                pass

        top_resort_html = ''
        if stats.get('top_powder_resort'):
            top_resort_html = f"""
            <div class="stat-card powder-alert">
                <div class="stat-value">{stats['top_powder_amount']} cm</div>
                <div class="stat-label">Best 24h Snow</div>
                <div class="stat-detail">{stats['top_powder_resort']}</div>
            </div>
            """

        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Ski Resort Snow Report Dashboard</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: #333;
            padding: 20px;
            min-height: 100vh;
        }}

        .container {{
            max-width: 1400px;
            margin: 0 auto;
            background: white;
            border-radius: 16px;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
            overflow: hidden;
        }}

        header {{
            background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
            color: white;
            padding: 40px;
            text-align: center;
        }}

        h1 {{
            font-size: 2.5em;
            margin-bottom: 10px;
            font-weight: 700;
        }}

        .subtitle {{
            font-size: 1.1em;
            opacity: 0.9;
        }}

        .stats {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            padding: 30px 40px;
            background: #f8f9fa;
            border-bottom: 2px solid #e9ecef;
        }}

        .stat-card {{
            background: white;
            padding: 20px;
            border-radius: 12px;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
            text-align: center;
        }}

        .stat-card.powder-alert {{
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
            color: white;
        }}

        .stat-value {{
            font-size: 2em;
            font-weight: 700;
            color: #2a5298;
            margin-bottom: 5px;
        }}

        .powder-alert .stat-value {{
            color: white;
        }}

        .stat-label {{
            font-size: 0.9em;
            color: #6c757d;
            text-transform: uppercase;
            letter-spacing: 1px;
        }}

        .powder-alert .stat-label {{
            color: rgba(255, 255, 255, 0.9);
        }}

        .stat-detail {{
            font-size: 0.85em;
            margin-top: 5px;
            font-weight: 600;
        }}

        .content {{
            padding: 40px;
        }}

        .table-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 20px;
        }}

        h2 {{
            color: #2a5298;
            font-size: 1.8em;
        }}

        .last-update {{
            color: #6c757d;
            font-size: 0.9em;
        }}

        .table-container {{
            overflow-x: auto;
            border-radius: 12px;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
        }}

        table {{
            width: 100%;
            border-collapse: collapse;
            background: white;
        }}

        thead {{
            background: linear-gradient(135deg, #2a5298 0%, #1e3c72 100%);
            color: white;
        }}

        th {{
            padding: 15px 12px;
            text-align: left;
            font-weight: 600;
            font-size: 0.9em;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}

        td {{
            padding: 12px;
            border-bottom: 1px solid #e9ecef;
        }}

        tr:hover {{
            background: #f8f9fa;
        }}

        .resort-name {{
            font-weight: 600;
            color: #2a5298;
        }}

        .resort-name a {{
            color: #2a5298;
            text-decoration: none;
        }}

        .resort-name a:hover {{
            text-decoration: underline;
        }}

        .snow-data {{
            font-weight: 600;
        }}

        .badge {{
            display: inline-block;
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 0.9em;
            font-weight: 600;
        }}

        .badge-epic {{
            background: #d63031;
            color: white;
        }}

        .badge-great {{
            background: #0984e3;
            color: white;
        }}

        .badge-good {{
            background: #00b894;
            color: white;
        }}

        .badge-light {{
            background: #dfe6e9;
            color: #2d3436;
        }}

        .na {{
            color: #adb5bd;
            font-style: italic;
        }}

        .no-data {{
            text-align: center;
            padding: 40px !important;
            color: #6c757d;
        }}

        .conditions {{
            font-size: 0.9em;
        }}

        footer {{
            background: #2c3e50;
            color: white;
            padding: 30px 40px;
            text-align: center;
        }}

        footer a {{
            color: #3498db;
            text-decoration: none;
        }}

        footer a:hover {{
            text-decoration: underline;
        }}

        .legend {{
            margin-top: 20px;
            padding: 15px;
            background: #f8f9fa;
            border-radius: 8px;
            font-size: 0.85em;
        }}

        .legend-title {{
            font-weight: 600;
            margin-bottom: 8px;
            color: #2a5298;
        }}

        .legend-items {{
            display: flex;
            gap: 15px;
            flex-wrap: wrap;
        }}

        @media (max-width: 768px) {{
            body {{
                padding: 10px;
            }}

            h1 {{
                font-size: 1.8em;
            }}

            .content {{
                padding: 20px;
            }}

            .stats {{
                padding: 20px;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>❄️ Ski Resort Snow Report</h1>
            <p class="subtitle">Live snow conditions from major ski resorts worldwide</p>
        </header>

        <div class="stats">
            <div class="stat-card">
                <div class="stat-value">{stats.get('total_resorts', 0)}</div>
                <div class="stat-label">Tracked Resorts</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">{stats.get('total_countries', 0)}</div>
                <div class="stat-label">Countries</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">{stats.get('total_records', 0)}</div>
                <div class="stat-label">Total Records</div>
            </div>
            {top_resort_html}
        </div>

        <div class="content">
            <div class="table-header">
                <h2>Current Conditions</h2>
                <div class="last-update">Last updated: {last_update}</div>
            </div>

            <div class="table-container">
                <table>
                    <thead>
                        <tr>
                            <th>Resort</th>
                            <th>Country</th>
                            <th>Region</th>
                            <th>24h Snow</th>
                            <th>48h Snow</th>
                            <th>7d Snow</th>
                            <th>Base Depth</th>
                            <th>Summit Depth</th>
                            <th>Lifts</th>
                            <th>Conditions</th>
                        </tr>
                    </thead>
                    <tbody>
                        {table_content}
                    </tbody>
                </table>
            </div>

            <div class="legend">
                <div class="legend-title">24h Snowfall Legend:</div>
                <div class="legend-items">
                    <span class="badge badge-epic">30+ cm Epic</span>
                    <span class="badge badge-great">15-29 cm Great</span>
                    <span class="badge badge-good">5-14 cm Good</span>
                    <span class="badge badge-light">&lt;5 cm Light</span>
                </div>
            </div>
        </div>

        <footer>
            <p>Data collected using automated web scraping • Updated daily via GitHub Actions</p>
            <p style="margin-top: 10px;">
                <a href="https://github.com/andrewnakas/Ski_Resort_Snow_Scrapper" target="_blank">View on GitHub</a>
            </p>
        </footer>
    </div>
</body>
</html>
"""
        return html

    def _format_lifts(self, open_lifts: Optional[int], total_lifts: Optional[int]) -> str:
        """Format lift status."""
        if open_lifts is None or total_lifts is None:
            return '<span class="na">N/A</span>'

        percentage = (open_lifts / total_lifts * 100) if total_lifts > 0 else 0
        return f'{open_lifts}/{total_lifts} ({percentage:.0f}%)'

    def close(self):
        """Close database connection."""
        self.conn.close()


def create_placeholder_page():
    """Create a placeholder page when no data is available."""
    html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Ski Resort Snow Report - Coming Soon</title>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            margin: 0;
            padding: 20px;
            text-align: center;
        }
        .container {
            max-width: 600px;
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            padding: 60px 40px;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
        }
        h1 {
            font-size: 3em;
            margin-bottom: 20px;
        }
        p {
            font-size: 1.2em;
            line-height: 1.6;
            opacity: 0.9;
        }
        .emoji {
            font-size: 4em;
            margin-bottom: 20px;
        }
        a {
            color: #fff;
            text-decoration: underline;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="emoji">❄️ 🎿</div>
        <h1>Snow Dashboard Coming Soon!</h1>
        <p>The ski resort snow scraper is being set up.</p>
        <p>To populate this dashboard, run the workflow manually from the Actions tab and select some resorts to scrape.</p>
        <p style="margin-top: 30px;">
            <a href="https://github.com/andrewnakas/Ski_Resort_Snow_Scrapper" target="_blank">View Project on GitHub</a>
        </p>
    </div>
</body>
</html>
"""
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print("✓ Created placeholder page")


def main():
    """Main function."""
    print("Generating HTML dashboard...")

    try:
        generator = HTMLGenerator()
        generator.generate_html()
        generator.close()

        print("✓ HTML dashboard generated successfully!")
        print("  Open index.html in your browser to view locally")
    except FileNotFoundError as e:
        print(f"⚠ Warning: {e}")
        print("  Database not found. Creating placeholder page...")
        create_placeholder_page()
        return 0
    except Exception as e:
        print(f"⚠ Warning: {e}")
        print("  No data available yet. Creating placeholder page...")
        create_placeholder_page()
        return 0


if __name__ == '__main__':
    import sys
    sys.exit(main() or 0)
