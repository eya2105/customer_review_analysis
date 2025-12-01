"""
Configuration settings for the California Gym scraper
"""

# CSV Configuration
CSV_FILENAME = "data/raw/all_california_gym_reviews.csv"
CSV_ENCODING = "utf-8-sig"

# Browser Configuration
HEADLESS = False
IMPLICIT_WAIT = 15
PAGE_LOAD_TIMEOUT = 30
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

# Scraping Configuration
SCROLL_ATTEMPTS_CONTAINER = 8
SCROLL_ATTEMPTS_WINDOW = 6
SCROLL_DELAY = 1.5
DELAY_BETWEEN_LOCATIONS = 2
PROCESSING_DELAY = 0.05

# Google Maps locations to scrape
GOOGLE_LOCATIONS = {
    "California Gym Centre Urbain Nord": "https://www.google.com/maps/place/California+Gym+Centre+Urbain+Nord/@36.8497481,10.1924261,17z/data=!4m8!3m7!1s0x12fd34c8cbbccc13:0xd457adab6be8aee4!8m2!3d36.8497439!4d10.197297!9m1!1b1!16s%2Fg%2F11dxs18wb_?entry=ttu&g_ep=EgoyMDI1MTEyMy4xIKXMDSoASAFQAw%3D%3D",
    "California Gym Lac 1": "https://www.google.com/maps/place/California+Gym+Lac+1/@36.8339787,10.2356224,17z/data=!4m8!3m7!1s0x12fd35007fe0806d:0xa71c1796442e6a29!8m2!3d36.8339745!4d10.2404933!9m1!1b1!16s%2Fg%2F11m67p1dlp?entry=ttu&g_ep=EgoyMDI1MTEyMy4xIKXMDSoASAFQAw%3D%3D",
    "California Gym Platinum": "https://www.google.com/maps/place/California+Gym+Platinum/@36.8449138,10.2778055,17z/data=!4m8!3m7!1s0x12fd4ab66ea16a55:0x7dd7ff7dbfc204cd!8m2!3d36.8449095!4d10.2803804!9m1!1b1!16s%2Fg%2F11c57ysqw8?entry=ttu&g_ep=EgoyMDI1MTEyMy4xIKXMDSoASAFQAw%3D%3D",
    "California Gym Mall": "https://www.google.com/maps/place/California+Gym+Mall/@36.847071,10.2780987,17z/data=!4m8!3m7!1s0x12fd4ab5f2afe9c1:0x7b36723ba1299a4a!8m2!3d36.8470667!4d10.2806736!9m1!1b1!16s%2Fg%2F11f_bzsb5c?entry=ttu&g_ep=EgoyMDI1MTEyMy4xIKXMDSoASAFQAw%3D%3D",
    "California Gym Soukra": "https://www.google.com/maps/place/California+Gym+Soukra/@36.8746327,10.2695407,17z/data=!4m8!3m7!1s0x12e2b51d9e5168f3:0x37eac499d8e07d27!8m2!3d36.8746285!4d10.2744116!9m1!1b1!16s%2Fg%2F11h71nfxq3?entry=ttu&g_ep=EgoyMDI1MTEyMy4xIKXMDSoASAFQAw%3D%3D",
    "California Gym Strength La Marsa": "https://www.google.com/maps/place/California+Gym+Strength+La+Marsa/@36.8851636,10.3188024,17z/data=!4m8!3m7!1s0x12e2b4f4711bf04b:0xb4605a34aaec41b!8m2!3d36.8851594!4d10.3236733!9m1!1b1!16s%2Fg%2F1232g62cq?entry=ttu&g_ep=EgoyMDI1MTEyMy4xIKXMDSoASAFQAw%3D%3D",
    "California Gym Zephyr": "https://www.google.com/maps/place/California+Gym+Zephyr/@36.8835414,10.328392,17z/data=!4m8!3m7!1s0x12e2b593b7a31291:0xfca503c99d4c51ff!8m2!3d36.8835372!4d10.3332629!9m1!1b1!16s%2Fg%2F11snczdqs2?entry=ttu&g_ep=EgoyMDI1MTEyMy4xIKXMDSoASAFQAw%3D%3D",
    "California Gym Boumhel": "https://www.google.com/maps/place/California+Gym+Boumhel/@36.7316581,10.3073693,17z/data=!4m8!3m7!1s0x12fd4994237d011b:0x2b984884a19cbaae!8m2!3d36.7316539!4d10.3122402!9m1!1b1!16s%2Fg%2F11j0v6mszq?entry=ttu&g_ep=EgoyMDI1MTEyMy4xIKXMDSoASAFQAw%3D%3D",
    "California Gym Bardo": "https://www.google.com/maps/place/California+GYM+BARDO/@36.8151127,10.1229798,17z/data=!4m8!3m7!1s0x12fd3390e951c1df:0x9f85266b728bada!8m2!3d36.8151085!4d10.1278507!9m1!1b1!16s%2Fg%2F11h32yshz1?entry=ttu&g_ep=EgoyMDI1MTEyMy4xIKXMDSoASAFQAw%3D%3D",
    "California Gym Jardins d'El Menzah": "https://www.google.com/maps/place/California+Gym+Jardins+d'El+Menzah/@36.8541437,10.1267301,17z/data=!4m8!3m7!1s0x12fd33e9f3d4781f:0x4a1b896957f5b0e2!8m2!3d36.8541395!4d10.131601!9m1!1b1!16s%2Fg%2F11lnlqyqlj?entry=ttu&g_ep=EgoyMDI1MTEyMy4xIKXMDSoASAFQAw%3D%3D",
    "California Gym Ennasr": "https://www.google.com/maps/place/California+gym+ennasr/@36.8604516,10.1424522,17z/data=!4m8!3m7!1s0x12fd3300455d3a11:0x490eb1336e440539!8m2!3d36.8604474!4d10.1473231!9m1!1b1!16s%2Fg%2F11wh3h3zvp?entry=ttu&g_ep=EgoyMDI1MTEyMy4xIKXMDSoASAFQAw%3D%3D",
    "California Gym Sousse": "https://www.google.com/maps/place/California+Gym+Sousse/@35.8416028,10.6248022,17z/data=!4m8!3m7!1s0x130275b8469424b5:0x685a7499cac68ad1!8m2!3d35.8415985!4d10.6273771!9m1!1b1!16s%2Fg%2F11gjs77nc_?entry=ttu&g_ep=EgoyMDI1MTEyMy4xIKXMDSoASAFQAw%3D%3D"
}

# Other websites to scrape (URLs and locations)
OTHER_SOURCES = [
    ("top-rated.online", "https://www.top-rated.online/cities/Tunis/place/p/4803828/California+Gym+Platinum", "California Gym Platinum"),
    ("expat.com", "https://www.expat.com/fr/forum/afrique/tunisie/tunis/162222-que-pensez-vous-du-california-gym-aux-berges-du-lac-1-.html", "California Gym Lac 1"),
    ("trustburn.com", "https://trustburn.com/reviews/california-gym-tunisia", "California Gym Lac 1")
]