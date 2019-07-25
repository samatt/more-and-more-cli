import click
from utilities import (
    get_products,
    conf,
    get_source_countries,
    save_store_menu,
    product_sources,
    exports_exist,
    get_all_exports,
    save_all_exports,
    save_bilateral_exports,
    bilateral_exports_exist,
)


@click.command(
    "generate_bilateral_exports",
    help="Generate a list of HS Codes that a src country exports to dst country. This information is used to display the container products on the MoreAndMore Store website",
)
@click.option("--verbose", is_flag=True)
@click.option("--force", is_flag=False)
@click.pass_context
def generate_bilateral_exports(ctx, verbose, force):
    config = [c for c in conf(ctx.obj["base"])][0]

    menu_destination_countries = config["more_and_more_store"]["country_codes"]

    for country in menu_destination_countries:
        if not exports_exist(ctx.obj["base"], config, country):
            print("RCA exports json doesnt exist for %s, downloading..." % country)
            data = get_all_exports(config, country_code=country)
            save_all_exports(ctx.obj["base"], config, data, country_code=country)
    data = [d for d in product_sources(ctx.obj["base"])][0]

    for hs_code, country_data in data.items():
        for c in country_data:
            possible_srcs, dst = c.values()
            for src in possible_srcs:
                print("Downloading bilateral data for %s-%s" % (src, dst))
                if (
                    bilateral_exports_exist(ctx.obj["base"], config, src, dst)
                    and not force
                ):
                    print("Already exists, skipping")
                    continue

                data = get_products(ctx.obj["base"], config, src, dst)
                if data is not None:
                    save_bilateral_exports(ctx.obj["base"], config, src, dst, data)
