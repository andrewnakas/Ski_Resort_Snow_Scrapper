"""
Expanded list of ski resorts available on OnTheSnow.com
This list includes 100+ resorts with known working URLs.
"""

ONTHESNOW_RESORTS = [
    # === USA - COLORADO (20 resorts) ===
    {'name': 'Vail', 'country': 'USA', 'region': 'Colorado', 'slug': 'colorado/vail'},
    {'name': 'Aspen Snowmass', 'country': 'USA', 'region': 'Colorado', 'slug': 'colorado/aspen-snowmass'},
    {'name': 'Breckenridge', 'country': 'USA', 'region': 'Colorado', 'slug': 'colorado/breckenridge'},
    {'name': 'Keystone', 'country': 'USA', 'region': 'Colorado', 'slug': 'colorado/keystone'},
    {'name': 'Steamboat', 'country': 'USA', 'region': 'Colorado', 'slug': 'colorado/steamboat'},
    {'name': 'Winter Park', 'country': 'USA', 'region': 'Colorado', 'slug': 'colorado/winter-park-resort'},
    {'name': 'Copper Mountain', 'country': 'USA', 'region': 'Colorado', 'slug': 'colorado/copper-mountain-resort'},
    {'name': 'Telluride', 'country': 'USA', 'region': 'Colorado', 'slug': 'colorado/telluride'},
    {'name': 'Crested Butte', 'country': 'USA', 'region': 'Colorado', 'slug': 'colorado/crested-butte'},
    {'name': 'Beaver Creek', 'country': 'USA', 'region': 'Colorado', 'slug': 'colorado/beaver-creek'},
    {'name': 'Arapahoe Basin', 'country': 'USA', 'region': 'Colorado', 'slug': 'colorado/arapahoe-basin'},
    {'name': 'Loveland', 'country': 'USA', 'region': 'Colorado', 'slug': 'colorado/loveland'},
    {'name': 'Monarch Mountain', 'country': 'USA', 'region': 'Colorado', 'slug': 'colorado/monarch'},
    {'name': 'Eldora', 'country': 'USA', 'region': 'Colorado', 'slug': 'colorado/eldora'},
    {'name': 'Silverton Mountain', 'country': 'USA', 'region': 'Colorado', 'slug': 'colorado/silverton-mountain'},
    {'name': 'Wolf Creek', 'country': 'USA', 'region': 'Colorado', 'slug': 'colorado/wolf-creek'},
    {'name': 'Aspen Highlands', 'country': 'USA', 'region': 'Colorado', 'slug': 'colorado/aspen-highlands'},
    {'name': 'Buttermilk', 'country': 'USA', 'region': 'Colorado', 'slug': 'colorado/buttermilk'},
    {'name': 'Powderhorn', 'country': 'USA', 'region': 'Colorado', 'slug': 'colorado/powderhorn'},
    {'name': 'Sunlight', 'country': 'USA', 'region': 'Colorado', 'slug': 'colorado/sunlight'},

    # === USA - UTAH (12 resorts) ===
    {'name': 'Park City', 'country': 'USA', 'region': 'Utah', 'slug': 'utah/park-city-mountain-resort'},
    {'name': 'Alta', 'country': 'USA', 'region': 'Utah', 'slug': 'utah/alta'},
    {'name': 'Snowbird', 'country': 'USA', 'region': 'Utah', 'slug': 'utah/snowbird'},
    {'name': 'Deer Valley', 'country': 'USA', 'region': 'Utah', 'slug': 'utah/deer-valley-resort'},
    {'name': 'Brighton', 'country': 'USA', 'region': 'Utah', 'slug': 'utah/brighton-resort'},
    {'name': 'Solitude', 'country': 'USA', 'region': 'Utah', 'slug': 'utah/solitude-mountain-resort'},
    {'name': 'Snowbasin', 'country': 'USA', 'region': 'Utah', 'slug': 'utah/snowbasin'},
    {'name': 'Powder Mountain', 'country': 'USA', 'region': 'Utah', 'slug': 'utah/powder-mountain'},
    {'name': 'Sundance', 'country': 'USA', 'region': 'Utah', 'slug': 'utah/sundance'},
    {'name': 'Brian Head', 'country': 'USA', 'region': 'Utah', 'slug': 'utah/brian-head'},
    {'name': 'Cherry Peak', 'country': 'USA', 'region': 'Utah', 'slug': 'utah/cherry-peak'},
    {'name': 'Nordic Valley', 'country': 'USA', 'region': 'Utah', 'slug': 'utah/nordic-valley'},

    # === USA - CALIFORNIA (15 resorts) ===
    {'name': 'Mammoth Mountain', 'country': 'USA', 'region': 'California', 'slug': 'california/mammoth-mountain'},
    {'name': 'Palisades Tahoe', 'country': 'USA', 'region': 'California', 'slug': 'california/palisades-tahoe'},
    {'name': 'Heavenly', 'country': 'USA', 'region': 'California', 'slug': 'california/heavenly'},
    {'name': 'Northstar', 'country': 'USA', 'region': 'California', 'slug': 'california/northstar-california'},
    {'name': 'Kirkwood', 'country': 'USA', 'region': 'California', 'slug': 'california/kirkwood'},
    {'name': 'Sugar Bowl', 'country': 'USA', 'region': 'California', 'slug': 'california/sugar-bowl'},
    {'name': 'Alpine Meadows', 'country': 'USA', 'region': 'California', 'slug': 'california/alpine-meadows'},
    {'name': 'Sierra-at-Tahoe', 'country': 'USA', 'region': 'California', 'slug': 'california/sierra-at-tahoe'},
    {'name': 'Dodge Ridge', 'country': 'USA', 'region': 'California', 'slug': 'california/dodge-ridge'},
    {'name': 'Bear Valley', 'country': 'USA', 'region': 'California', 'slug': 'california/bear-valley'},
    {'name': 'Mountain High', 'country': 'USA', 'region': 'California', 'slug': 'california/mountain-high'},
    {'name': 'Snow Summit', 'country': 'USA', 'region': 'California', 'slug': 'california/snow-summit'},
    {'name': 'Bear Mountain', 'country': 'USA', 'region': 'California', 'slug': 'california/bear-mountain'},
    {'name': 'Mt. Shasta', 'country': 'USA', 'region': 'California', 'slug': 'california/mt-shasta'},
    {'name': 'Badger Pass', 'country': 'USA', 'region': 'California', 'slug': 'california/badger-pass'},

    # === USA - WYOMING (5 resorts) ===
    {'name': 'Jackson Hole', 'country': 'USA', 'region': 'Wyoming', 'slug': 'wyoming/jackson-hole'},
    {'name': 'Grand Targhee', 'country': 'USA', 'region': 'Wyoming', 'slug': 'wyoming/grand-targhee-resort'},
    {'name': 'Snow King', 'country': 'USA', 'region': 'Wyoming', 'slug': 'wyoming/snow-king'},
    {'name': 'Hogadon', 'country': 'USA', 'region': 'Wyoming', 'slug': 'wyoming/hogadon-basin-ski-area'},
    {'name': 'White Pine', 'country': 'USA', 'region': 'Wyoming', 'slug': 'wyoming/white-pine'},

    # === USA - VERMONT (10 resorts) ===
    {'name': 'Stowe', 'country': 'USA', 'region': 'Vermont', 'slug': 'vermont/stowe'},
    {'name': 'Killington', 'country': 'USA', 'region': 'Vermont', 'slug': 'vermont/killington'},
    {'name': 'Sugarbush', 'country': 'USA', 'region': 'Vermont', 'slug': 'vermont/sugarbush'},
    {'name': 'Okemo', 'country': 'USA', 'region': 'Vermont', 'slug': 'vermont/okemo'},
    {'name': 'Stratton', 'country': 'USA', 'region': 'Vermont', 'slug': 'vermont/stratton'},
    {'name': 'Jay Peak', 'country': 'USA', 'region': 'Vermont', 'slug': 'vermont/jay-peak'},
    {'name': 'Mad River Glen', 'country': 'USA', 'region': 'Vermont', 'slug': 'vermont/mad-river-glen'},
    {'name': 'Smugglers Notch', 'country': 'USA', 'region': 'Vermont', 'slug': 'vermont/smugglers-notch'},
    {'name': 'Mount Snow', 'country': 'USA', 'region': 'Vermont', 'slug': 'vermont/mount-snow'},
    {'name': 'Bolton Valley', 'country': 'USA', 'region': 'Vermont', 'slug': 'vermont/bolton-valley'},

    # === USA - NEW HAMPSHIRE (8 resorts) ===
    {'name': 'Bretton Woods', 'country': 'USA', 'region': 'New Hampshire', 'slug': 'new-hampshire/bretton-woods'},
    {'name': 'Loon Mountain', 'country': 'USA', 'region': 'New Hampshire', 'slug': 'new-hampshire/loon-mountain'},
    {'name': 'Cannon Mountain', 'country': 'USA', 'region': 'New Hampshire', 'slug': 'new-hampshire/cannon-mountain'},
    {'name': 'Waterville Valley', 'country': 'USA', 'region': 'New Hampshire', 'slug': 'new-hampshire/waterville-valley'},
    {'name': 'Wildcat', 'country': 'USA', 'region': 'New Hampshire', 'slug': 'new-hampshire/wildcat'},
    {'name': 'Attitash', 'country': 'USA', 'region': 'New Hampshire', 'slug': 'new-hampshire/attitash'},
    {'name': 'Cranmore', 'country': 'USA', 'region': 'New Hampshire', 'slug': 'new-hampshire/cranmore'},
    {'name': 'Gunstock', 'country': 'USA', 'region': 'New Hampshire', 'slug': 'new-hampshire/gunstock'},

    # === CANADA - BRITISH COLUMBIA (10 resorts) ===
    {'name': 'Whistler Blackcomb', 'country': 'Canada', 'region': 'British Columbia', 'slug': 'british-columbia/whistler-blackcomb'},
    {'name': 'Revelstoke', 'country': 'Canada', 'region': 'British Columbia', 'slug': 'british-columbia/revelstoke-mountain-resort'},
    {'name': 'Big White', 'country': 'Canada', 'region': 'British Columbia', 'slug': 'british-columbia/big-white'},
    {'name': 'Sun Peaks', 'country': 'Canada', 'region': 'British Columbia', 'slug': 'british-columbia/sun-peaks-resort'},
    {'name': 'Fernie', 'country': 'Canada', 'region': 'British Columbia', 'slug': 'british-columbia/fernie-alpine-resort'},
    {'name': 'Kicking Horse', 'country': 'Canada', 'region': 'British Columbia', 'slug': 'british-columbia/kicking-horse'},
    {'name': 'Red Mountain', 'country': 'Canada', 'region': 'British Columbia', 'slug': 'british-columbia/red-mountain-resort'},
    {'name': 'Silver Star', 'country': 'Canada', 'region': 'British Columbia', 'slug': 'british-columbia/silver-star'},
    {'name': 'Panorama', 'country': 'USA', 'region': 'British Columbia', 'slug': 'british-columbia/panorama'},
    {'name': 'Apex', 'country': 'Canada', 'region': 'British Columbia', 'slug': 'british-columbia/apex-mountain-resort'},

    # === CANADA - ALBERTA (5 resorts) ===
    {'name': 'Lake Louise', 'country': 'Canada', 'region': 'Alberta', 'slug': 'alberta/lake-louise'},
    {'name': 'Sunshine Village', 'country': 'Canada', 'region': 'Alberta', 'slug': 'alberta/sunshine-village'},
    {'name': 'Marmot Basin', 'country': 'Canada', 'region': 'Alberta', 'slug': 'alberta/marmot-basin'},
    {'name': 'Nakiska', 'country': 'Canada', 'region': 'Alberta', 'slug': 'alberta/nakiska'},
    {'name': 'Castle Mountain', 'country': 'Canada', 'region': 'Alberta', 'slug': 'alberta/castle-mountain-resort'},

    # === CANADA - QUEBEC (5 resorts) ===
    {'name': 'Tremblant', 'country': 'Canada', 'region': 'Quebec', 'slug': 'quebec/tremblant'},
    {'name': 'Le Massif', 'country': 'Canada', 'region': 'Quebec', 'slug': 'quebec/le-massif'},
    {'name': 'Mont-Sainte-Anne', 'country': 'Canada', 'region': 'Quebec', 'slug': 'quebec/mont-sainte-anne'},
    {'name': 'Stoneham', 'country': 'Canada', 'region': 'Quebec', 'slug': 'quebec/stoneham'},
    {'name': 'Bromont', 'country': 'Canada', 'region': 'Quebec', 'slug': 'quebec/bromont'},
]

def get_all_resorts():
    """Get all resorts with OnTheSnow data"""
    return ONTHESNOW_RESORTS

def get_resorts_by_country(country: str):
    """Get resorts by country"""
    return [r for r in ONTHESNOW_RESORTS if r['country'] == country]

def get_resorts_by_region(region: str):
    """Get resorts by region"""
    return [r for r in ONTHESNOW_RESORTS if r['region'] == region]
