
import logging
import os
import time

import requests


def download_map(beatmap_id):

    # if the map is already downloaded, skip it
    if os.path.isfile(f"./osu_files/{beatmap_id}.osu"):
        logging.debug(f"Map {beatmap_id} already downloaded, skipping")
        return

    try:
        # Download the beatmap
        beatmap_url = f"https://osu.ppy.sh/osu/{beatmap_id}"

        # Check if ./osu_files folder exist
        if not os.path.exists("./osu_files"):
            os.mkdir("./osu_files")
            
        # Check if the beatmap exists in the local ./osu_files folder
        if not os.path.exists(f"./osu_files/{beatmap_id}.osu"):
            logging.debug(f"Downloading map {beatmap_id}...")
            # Download the beatmap
            resp = requests.get(beatmap_url)
            if not resp.ok:
                logging.error("Error " + str(resp.status_code) + ": " + resp.reason)
                return
            with open(f"./osu_files/{beatmap_id}.osu", "wb") as f:
                f.write(resp.content)
            # sleep a bit (like 500ms), we dont want to literally ddos peppy
            time.sleep(0.5)
            
        # Check if the beatmap exists in the local ./osu_files folder
        if not os.path.exists(f"./osu_files/{beatmap_id}.osu"):
            logging.error("Error: Something went wrong while downloading the beatmap")
            return
        # Check if the filesize is reasonable. Anything over 1kb is fine
        if os.path.getsize(f"./osu_files/{beatmap_id}.osu") < 1024:
            # delete the file
            os.remove(f"./osu_files/{beatmap_id}.osu")
            return

    except Exception as e:
        logging.error(f"Exception occured in download_map: {e}")
        return