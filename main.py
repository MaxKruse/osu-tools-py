from copy import deepcopy
import json
from re import M
import click
import requests
import slider

import calculators
from helpers.Score import Score
from helpers.download_map import download_map
from helpers.table_print import print_scores

RIPPLE_BASE_URL = "https://ripple.moe/api"

import logging

LOG_LEVELS = {
    "debug": logging.DEBUG,
    "info": logging.INFO,
}

@click.group()
@click.pass_context
@click.option("--calculator", default="xexxar_v1", help="Calculator to use, default is xexxar_v1")
@click.option("--log", default="info", help="Log level, default is debug. Allowed is debug, info")
@click.option("--output", default="", help="Output file, if not specified, output is printed to stdout")
def cli(ctx, calculator, log, output):
    ctx.ensure_object(dict)
    ctx.obj['calculator'] = calculator
    ctx.obj['log'] = log
    ctx.obj['output'] = output
    logging.basicConfig(level=LOG_LEVELS[log], format="[%(levelname)s] %(message)s")
    logging.debug(f"Using calculator: {calculator}")

@cli.command()
@click.pass_context
@click.argument("profile_id", type=int, nargs=1)
def bancho(ctx, profile_id):
    logging.info("Bancho Profile Recalculator")
    logging.debug("Currently not implemented")

    logging.debug(f"Passed PROFILE_ID = {profile_id}")
    pass

@cli.command()
@click.pass_context
@click.argument("gamemode", type=str, nargs=1)
@click.argument("profile_id", type=int, nargs=1)
def ripple(ctx, gamemode, profile_id):
    logging.info("Ripple Profile Recalculator")

    logging.debug(f"Passed PROFILE_ID = {profile_id}")

    # only allow gamemode == "std" for now
    if gamemode != "std":
        logging.error("Only std gamemode is supported")
        return

    # get the current player's full profile from /v1/users/full
    params = {
        "id": profile_id
    }
    resp = requests.get(RIPPLE_BASE_URL + "/v1/users/full", params=params)
    if not resp.ok:
        logging.error("Error: " + str(resp.status_code))
        logging.error("Make sure the user isnt restricted.")
        return
    originalUser = resp.json()

    # Make a request to the ripple api for /get_user_best
    # This will return a list of scores for the user
    # We will then use the calculator to calculate the new score
    params = {
        "u": profile_id,
        "limit": 100,
        "relax": 0
    }
    resp = requests.get(RIPPLE_BASE_URL + "/get_user_best", params=params)
    if not resp.ok:
        logging.error("Error: " + str(resp.status_code))
        logging.error("Make sure the user isnt restricted.")
        return
    respJson = resp.json()
    scoresOriginal = {}
    for score in respJson:
        temp = Score()
        temp.score = int(score["score"])
        temp.beatmap_id = int(score["beatmap_id"])
        temp.playerUserID = int(profile_id)
        temp.playerName = originalUser["username"]
        temp.completed = True
        temp.c300 = int(score["count300"])
        temp.c100 = int(score["count100"])
        temp.c50 = int(score["count50"])
        temp.maxCombo = int(score["maxcombo"])
        temp.cMiss = int(score["countmiss"])
        temp.mods = int(score["enabled_mods"])
        temp.pp = score["pp"]

        scoresOriginal[temp.beatmap_id] = temp

    maps = {}

    scoresRecalculated = {}

    for map_id in scoresOriginal:
        try:
            score = deepcopy(scoresOriginal[map_id])
            # make sure the beatmap_id is reasonable (e.g. above 0)
            if int(score.beatmap_id) < 1:
                logging.debug(f"Error: Beatmap ID is below 1 ({score.beatmap_id}), skipping")
                continue

            # Download the beatmap for caching purposes
            download_map(score.beatmap_id)
            logging.debug("Calculating score for beatmap " + str(score.beatmap_id))
            beatmap_ = slider.Beatmap.from_path(f"./osu_files/{score.beatmap_id}.osu")
            beatmap_.display_name
            calculator = calculators.PP_CALCULATORS[ctx.obj["calculator"]](beatmap_, score)
            logging.debug(f"Before: {score.pp}pp | After: {calculator.pp}pp")
            score.pp = calculator.pp
            scoresRecalculated[map_id] = score
            maps[score.beatmap_id] = beatmap_
        except:
            None

    # sort the recalculated scores by their pp, highest first
    scoresRecalculatedArr = sorted(scoresRecalculated.values(), key=lambda x: x.pp, reverse=True)

    # Aggregate the pp of the recalculated scores, where
    # total pp = pp[1] * 0.95^0 + pp[2] * 0.95^1 + pp[3] * 0.95^2 + ... + pp[m] * 0.95^(m-1)
    copyProfile = deepcopy(originalUser)
    copyProfile[gamemode]["pp"] = 0
    i = 0
    for score in scoresRecalculatedArr:
        copyProfile[gamemode]["pp"] += score.pp * (0.95 ** i)
        i += 1

    print_scores(scoresOriginal, scoresRecalculatedArr, maps, ctx.obj['output'])

    # print both the old and new profiles
    logging.info(f"Profile Before: {originalUser[gamemode]['pp']}pp")
    logging.info(f"Profile After: {copyProfile[gamemode]['pp']}pp")
    pass

@cli.command()
@click.pass_context
@click.argument("beatmap_id", nargs=1)
def web(ctx, beatmap_id):
    logging.info("Web (beatmap_id) Recalculator")
    logging.info("Currently not implemented")

    logging.debug(f"Passed ID = {beatmap_id}")
    pass


@cli.command()
@click.pass_context
@click.argument("beatmap")
def file(ctx, beatmap):
    logging.info("Osu! File Recalculator")

    # generate a beatmap object from the file
    beatmap_ = slider.Beatmap.from_path(beatmap)

    # Make a score here
    score_ = Score()
    score_.c300 = 500
    score_.mods = 64 | 4 | 8
    # etc etc

    calculator = calculators.PP_CALCULATORS[ctx.obj["calculator"]](beatmap_=beatmap_, score_=score_)
    logging.debug(f"PP Should already be set, its: {calculator.pp}")

if __name__ == "__main__":
    try:
        cli(obj={})
    except Exception as e:
        import traceback
        traceback.print_exc()
