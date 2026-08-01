"""
Main entry point - shows progress bars and results
"""
import os
import time

import pandas as pd

from scraper.config import GOOGLE_LOCATIONS, OTHER_SOURCES
from scraper.scraper import UnifiedReviewScraper


def main():
    """Main function to scrape from all sources."""
    scraper = UnifiedReviewScraper()
    scraper.setup_driver()

    try:
        initial_total = scraper.get_total_reviews()
        print("=" * 80)
        print("CALIFORNIA GYM REVIEWS SCRAPER - ALL SOURCES")
        print("=" * 80)
        print(f"Initial reviews in CSV: {initial_total}")
        print()

        total_stats = {"found": 0, "successful": 0, "failed": 0, "new": 0}
        start_time = time.time()

        print("📱 SOURCE 1: GOOGLE MAPS")
        print("-" * 60)
        google_list = list(GOOGLE_LOCATIONS.items())
        from tqdm import tqdm

        with tqdm(total=len(google_list), desc="Google Maps locations", bar_format="{desc}: {percentage:3.0f}%|{bar}| {n_fmt}/{total_fmt}") as google_pbar:
            for idx, (location_name, url) in enumerate(google_list, 1):
                print(f"\n[{idx}/{len(google_list)}] {location_name}")
                loc_found, loc_success, loc_failed, loc_new = scraper.scrape_google_location(url, location_name)
                total_stats["found"] += loc_found
                total_stats["successful"] += loc_success
                total_stats["failed"] += loc_failed
                total_stats["new"] += loc_new
                print(f"   📈 Results: Found: {loc_found}, Successful: {loc_success}, Failed: {loc_failed}, New: {loc_new}")
                if idx < len(google_list):
                    time.sleep(2)
                google_pbar.update(1)

        print("\n" + "=" * 60)
        print("GOOGLE MAPS COMPLETE")
        print("=" * 60)

        print("\n📱 SOURCE 2: OTHER WEBSITES")
        print("-" * 60)
        other_sources = [
            ("top-rated.online", scraper.scrape_top_rated),
            ("expat.com", scraper.scrape_expat),
            ("trustburn.com", scraper.scrape_trustburn),
        ]

        with tqdm(total=len(other_sources), desc="Other websites", bar_format="{desc}: {percentage:3.0f}%|{bar}| {n_fmt}/{total_fmt}") as other_pbar:
            for source_name, scrape_func in other_sources:
                print(f"\n{source_name.upper()}")
                source_found, source_success, source_failed, source_new = scrape_func()
                total_stats["found"] += source_found
                total_stats["successful"] += source_success
                total_stats["failed"] += source_failed
                total_stats["new"] += source_new
                print(f"   Results: Found: {source_found}, Successful: {source_success}, Failed: {source_failed}, New: {source_new}")
                time.sleep(2)
                other_pbar.update(1)

        end_time = time.time()
        final_total = scraper.get_total_reviews()

        print("\n" + "=" * 80)
        print("SCRAPING COMPLETE - ALL SOURCES")
        print("=" * 80)
        print(f"Total time: {end_time - start_time:.1f} seconds")
        print(f"Sources processed: {len(google_list) + len(other_sources)}")
        print(f"Total reviews in CSV: {final_total}")
        print(f"New reviews added: {total_stats['new']}")
        print(f"Reviews failed to scrape: {total_stats['failed']}")
        print("=" * 80)

        if final_total > 0 and os.path.exists(scraper.csv_filename):
            print(f"\nFile saved: {scraper.csv_filename}")
            print(f"File size: {os.path.getsize(scraper.csv_filename) / 1024:.1f} KB")
    except Exception as exc:  # pragma: no cover - runtime path
        print(f"\nError: {exc}")
    finally:
        scraper.close()
        print("\nScraping finished")


if __name__ == "__main__":
    main()
