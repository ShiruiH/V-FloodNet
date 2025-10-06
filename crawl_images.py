from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
import requests
import argparse
import os
from datetime import datetime

# Set up Chrome options
options = Options()
# options.add_argument("--headless")  # Run in background
# options.add_argument("--disable-gpu")
options.add_argument("--headless=new")              # modern headless mode
options.add_argument("--no-sandbox")                # required in GCP containers
options.add_argument("--disable-dev-shm-usage")     # use /tmp instead of /dev/shm
options.add_argument("--disable-gpu")               # safe to keep
options.add_argument("--remote-debugging-port=9222")# helps stability


def get_parser():
    parser = argparse.ArgumentParser(description='The date to be process')
    parser.add_argument('--date-str', type=str, required=True,
                        help='Date string YYYY-MM-DD')

    return parser.parse_args()


def main(args):

    out_dir = f'/home/shirui_hao/V-FloodNet-SH/nhd_data/lavenders_bridge/{args.date_str}'
    os.makedirs(out_dir, exist_ok=True)

    # Provide path to chromedriver
    service = Service(f'/usr/local/bin/chromedriver')

    # Start driver
    driver = webdriver.Chrome(service=service, options=options)
    driver.get(f'https://webcam.io/webcams/zAyE5z/12-hours?fps=1&repeat=1&delay_start=0&delay_end=1')

    # Track previously seen URLs to avoid duplicates
    seen_urls = set()

    # How many frames you want to collect
    frame_count = 30

    start_hour, end_hour = 6, 19

    try:
        while len(seen_urls) < frame_count:
            img_element = driver.find_element("id", "timelapse-player-image")
            timecode_element = driver.find_element("class name", "timecode")

            src = img_element.get_attribute("src")
            # timecode_dt = timecode_element.text.strip().split(" ")[0]
            timecode = timecode_element.text.strip()
            timecode_dt = timecode.replace(" ", "-").replace(":", "-")
            timecode_t = timecode.split(' ')[1].split(':')[0]
            formatted_time = f'{timecode_dt}'

            if src in seen_urls:
                print("No new image found, stopping.")
                break

            if start_hour <= int(timecode_t) < end_hour:
                # if start_hour <= int(timecode_t) < end_hour:
                seen_urls.add(src)

                response = requests.get(src)
                if response.status_code == 200:
                    filepath = f"{out_dir}/{formatted_time}.jpg"
                    with open(filepath, "wb") as f:
                        f.write(response.content)
                    print(f"Saved {formatted_time}.jpg")
            time.sleep(1)

    finally:
        driver.quit()

    print(f"Saved {len(seen_urls)} images.")


if __name__ == '__main__':

    _args = get_parser()
    print(_args)

    main(_args)
