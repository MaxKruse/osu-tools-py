from copy import deepcopy
import json
import click
import requests
import slider

import calculators
from helpers.Score import Score
from helpers.download_map import download_map

RIPPLE_BASE_URL = "https://ripple.moe/api"
BANCHO_BASE_URL = "https://osu.ppy.sh/api"

@click.group()
@click.pass_context
@click.option("--calculator", default="xexxar_v1", help="Calculator to use, default is xexxar_v1")
def cli(ctx, calculator):
    ctx.ensure_object(dict)
    ctx.obj['calculator'] = calculator
    click.echo(f"Using calculator: {calculator}")

@cli.command()
@click.pass_context
@click.argument("gamemode", type=str, nargs=1)
@click.argument("profile_id", type=int, nargs=1)
@click.option("--api-key", default="NONE", help="API key for bancho. https://osu.ppy.sh/p/api")
def bancho(ctx, profile_id, gamemode, api_key):
    click.echo("Bancho Profile Recalculator")
    click.echo(f"Passed PROFILE_ID = {profile_id}")

    if gamemode != "osu":
        click.echo("Only osu gamemode is supported")
        return
    

    params = {
        "u": profile_id,
        "k": api_key,
        "m": 0,
        "type": "id",
        "limit": 100
    }

    # get user
    resp = requests.get(BANCHO_BASE_URL + "/get_user", params=params)
    if  not resp.ok:
        click.echo("Failed to get user")
        return

    originalUser = resp.json()[0]


    resp = requests.get(BANCHO_BASE_URL + "/get_user_best", params=params)
    if not resp.ok:
        click.echo("Failed to get user best")
        return
    
    user_best = resp.json()
    if len(user_best) == 0:
        click.echo("No scores found")
        return

    scoresOriginal = []
    for score in user_best:
        temp = Score()
        temp.score = score["score"]
        temp.beatmap_id = score["beatmap_id"]
        temp.playerUserID = profile_id
        temp.playerName = originalUser["username"]
        temp.completed = True
        temp.c300 = score["count300"]
        temp.c100 = score["count100"]
        temp.c50 = score["count50"]
        temp.maxCombo = score["maxcombo"]
        temp.cMiss = score["countmiss"]
        temp.mods = score["enabled_mods"]
        temp.pp = score["pp"]

        scoresOriginal.append(temp)

    scoresRecalculated = []
    for score in scoresOriginal:
        # make sure the beatmap_id is reasonable (e.g. above 0)
        if int(score.beatmap_id) < 1:
            click.echo(f"Error: Beatmap ID is below 1 ({score.beatmap_id}), skipping")
            continue

        # Download the beatmap for caching purposes
        download_map(score.beatmap_id)
        print("Calculating score for beatmap " + str(score.beatmap_id))
        beatmap_ = slider.Beatmap.from_path(f"./osu_files/{score.beatmap_id}.osu")
        calculator = calculators.PP_CALCULATORS[ctx.obj["calculator"]](beatmap_, score)
        score.pp = calculator.pp
        scoresRecalculated.append(score)

    # Aggregate the pp of the recalculated scores, where
    # total pp = pp[1] * 0.95^0 + pp[2] * 0.95^1 + pp[3] * 0.95^2 + ... + pp[m] * 0.95^(m-1)
    copyProfile = deepcopy(originalUser)
    copyProfile["pp_raw"] = 0
    i = 0
    for score in scoresRecalculated:
        copyProfile["pp_raw"] += score.pp * (0.95 ** i)
        i += 1

    # print both the old and new profiles
    click.echo(f"Before: {json.dumps(originalUser['pp_raw'], indent=4)}")
    click.echo(f"After: {json.dumps(copyProfile['pp_raw'], indent=4)}")

    pass

@cli.command()
@click.pass_context
@click.argument("gamemode", type=str, nargs=1)
@click.argument("profile_id", type=int, nargs=1)
def ripple(ctx, gamemode, profile_id):
    click.echo("Ripple Profile Recalculator")
    click.echo("Currently not implemented")

    click.echo(f"Passed PROFILE_ID = {profile_id}")

    # only allow gamemode == "osu" for now
    if gamemode != "osu":
        click.echo("Only osu gamemode is supported")
        return

    # get the current player's full profile from /v1/users/full
    params = {
        "id": profile_id
    }
    resp = requests.get(RIPPLE_BASE_URL + "/v1/users/full", params=params)
    if not resp.ok:
        click.echo("Error: " + str(resp.status_code))
        click.echo("Make sure the user isnt restricted.")
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
        click.echo("Error: " + str(resp.status_code))
        click.echo("Make sure the user isnt restricted.")
        return
    respJson = resp.json()
    scoresOriginal = []
    for score in respJson:
        temp = Score()
        temp.score = score["score"]
        temp.beatmap_id = score["beatmap_id"]
        temp.playerUserID = profile_id
        temp.playerName = originalUser["username"]
        temp.completed = True
        temp.c300 = score["count300"]
        temp.c100 = score["count100"]
        temp.c50 = score["count50"]
        temp.maxCombo = score["maxcombo"]
        temp.cMiss = score["countmiss"]
        temp.mods = score["enabled_mods"]
        temp.pp = score["pp"]

        scoresOriginal.append(temp)

    scoresRecalculated = []
    for score in scoresOriginal:
        # make sure the beatmap_id is reasonable (e.g. above 0)
        if int(score.beatmap_id) < 1:
            click.echo(f"Error: Beatmap ID is below 1 ({score.beatmap_id}), skipping")
            continue

        # Download the beatmap for caching purposes
        download_map(score.beatmap_id)
        print("Calculating score for beatmap " + str(score.beatmap_id))
        beatmap_ = slider.Beatmap.from_path(f"./osu_files/{score.beatmap_id}.osu")
        calculator = calculators.PP_CALCULATORS[ctx.obj["calculator"]](beatmap_, score)
        score.pp = calculator.pp
        scoresRecalculated.append(score)
        
    # Aggregate the pp of the recalculated scores, where
    # total pp = pp[1] * 0.95^0 + pp[2] * 0.95^1 + pp[3] * 0.95^2 + ... + pp[m] * 0.95^(m-1)
    copyProfile = deepcopy(originalUser)
    copyProfile["std"]["pp"] = 0
    i = 0
    for score in scoresRecalculated:
        copyProfile["std"]["pp"] += score.pp * (0.95 ** i)
        i += 1

    # print both the old and new profiles
    click.echo(f"Before: {json.dumps(originalUser['std'], indent=4)}")
    click.echo(f"After: {json.dumps(copyProfile['std'], indent=4)}")
    pass

@cli.command()
@click.pass_context
@click.argument("beatmap_id", nargs=1)
def web(ctx, beatmap_id):
    click.echo("Web (beatmap_id) Recalculator")
    click.echo("Currently not implemented")

    click.echo(f"Passed ID = {beatmap_id}")
    pass


@cli.command()
@click.pass_context
@click.argument("beatmap")
def file(ctx, beatmap):
    click.echo("Osu! File Recalculator")

    # generate a beatmap object from the file
    beatmap_ = slider.Beatmap.from_path(beatmap)

    # Make a score here
    score_ = Score()
    score_.c300 = 500
    score_.mods = 64 | 4 | 8
    # etc etc

    calculator = calculators.PP_CALCULATORS[ctx.obj["calculator"]](beatmap_=beatmap_, score_=score_)
    click.echo(f"PP Should already be set, its: {calculator.pp}")

if __name__ == "__main__":
    try:
        cli(obj={})
    except Exception as e:
        import traceback
        traceback.print_exc()