import click
from utilities import conf, get_top_exports, save_all_exports, generate_grid


@click.command("generate_postcard", help="Generate a countrys top export postcard")
@click.pass_context
def generate_postcard(ctx):
    for config in conf(ctx.obj["base"]):
        # country_code, width, height, x_padding, y_padding = config["postcard"]
        config["postcard"]["hs_codes"] = get_top_exports(
            ctx.obj["base"], config, 1000, True
        )
        generate_grid(ctx.obj["base"], **config["postcard"])
