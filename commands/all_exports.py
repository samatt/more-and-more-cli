import click
from utilities import conf, get_all_exports, save_all_exports, hs07_data


@click.command("all_exports", help="Get all exports for a given country")
@click.pass_context
def all_exports(ctx):
    for config in conf(ctx.obj["base"]):
        exports = get_all_exports(config)
        hs07_data(ctx.obj["base"])
        # save_all_exports(ctx.obj["base"], config, exports)

