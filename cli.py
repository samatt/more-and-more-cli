import click
from commands.all_exports import all_exports
from commands.top_exports import top_exports
from commands.generate_postcard import generate_postcard
from commands.generate_store_menu import generate_store_menu
from commands.generate_bilateral_exports import generate_bilateral_exports


@click.group()
@click.option("--base", default="data", help="Path to the data directory")
@click.pass_context
def cli(ctx, base):
    """
    classify: more-and-more  command line tasks
    """
    ctx.obj["base"] = click.format_filename(base)


cli.add_command(all_exports)
cli.add_command(top_exports)
cli.add_command(generate_store_menu)
cli.add_command(generate_postcard)
cli.add_command(generate_bilateral_exports)
