import click
import slider

import calculators
from helpers.Score import Score

@click.group()
@click.pass_context
@click.option("--calculator", default="xexxar_v1", help="Calculator to use, default is xexxar_v1")
def cli(ctx, calculator):
    ctx.ensure_object(dict)
    ctx.obj['calculator'] = calculator

@cli.command()
@click.pass_context
@click.argument("profile_id", type=int, nargs=1)
def bancho(ctx, profile_id):
    click.echo("Bancho Profile Recalculator")
    click.echo("Currently not implemented")

    click.echo(f"Passed PROFILE_ID = {profile_id}")
    pass

@cli.command()
@click.pass_context
@click.argument("profile_id", type=int, nargs=1)
def ripple(ctx, profile_id):
    click.echo("Ripple Profile Recalculator")
    click.echo("Currently not implemented")

    click.echo(f"Passed PROFILE_ID = {profile_id}")
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
    click.echo("Using calculator: {}".format(calculator.__class__.__name__))
    click.echo(f"PP Should already be set, its: {calculator.pp}")

if __name__ == "__main__":
    try:
        cli(obj={})
    except Exception as e:
        import traceback
        traceback.print_exc()