import click
from utilities import conf, get_top_exports, save_top_exports


@click.command(
    "top_exports",
    help="Get the top X exports for a given country. X set in config.json",
)
@click.pass_context
def top_exports(ctx):
    for config in conf(ctx.obj["base"]):
        save_top_exports(
            ctx.obj["base"], config, get_top_exports(ctx.obj["base"], config)
        )

