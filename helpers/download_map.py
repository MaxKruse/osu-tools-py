
import os
import time

import requests


def download_map(beatmap_id):
    try:
        # Download the beatmap
        beatmap_url = f"https://osu.ppy.sh/osu/{beatmap_id}"

        # Check if ./osu_files folder exist
        if not os.path.exists("./osu_files"):
            os.mkdir("./osu_files")
            
        # Check if the beatmap exists in the local ./osu_files folder
        if not os.path.exists(f"./osu_files/{beatmap_id}.osu"):
            print(f"Downloading map {beatmap_id}...")
            # Download the beatmap
            resp = requests.get(beatmap_url)
            if not resp.ok:
                print("Error " + str(resp.status_code) + ": " + resp.reason)
                return
            with open(f"./osu_files/{beatmap_id}.osu", "wb") as f:
                f.write(resp.content)
            # sleep a bit (like 500ms), we dont want to literally ddos peppy
            time.sleep(0.5)
            
        # Check if the beatmap exists in the local ./osu_files folder
        if not os.path.exists(f"./osu_files/{beatmap_id}.osu"):
            print("Error: Something went wrong while downloading the beatmap")
            return
        # Check if the filesize is reasonable. Anything over 1kb is fine
        if os.path.getsize(f"./osu_files/{beatmap_id}.osu") < 1024:
            # delete the file
            os.remove(f"./osu_files/{beatmap_id}.osu")
            return

    except Exception as e:
        print(f"Exception occured in download_map: {e}")
        return