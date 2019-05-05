import click
from utilities import conf, get_source_countries, save_store_menu


@click.command(
    "generate_store_menu",
    help="Generate possible src countries for a dest country and HS code. This information is used in the MoreAndMore store website",
)
@click.option("--verbose", is_flag=True)
@click.pass_context
def generate_store_menu(ctx, verbose):
    for config in conf(ctx.obj["base"]):
        country_codes, product_codes, num_src_countries = config[
            "more_and_more_store"
        ].values()
        product_srcs = {}
        for product in product_codes:
            country_combos = []
            for country in country_codes:
                # {"possible_srcs": ["cxr", "jpn", "zaf", "swe", "mys", "mda", "hun", "prk", "ita", "ant"], "dst": "bra"}
                src_countries = get_source_countries(config, country, product)
                if verbose:
                    print(country, product, src_countries)
                cur_combo = {"possible_srcs": src_countries, "dst": country}
                country_combos.append(cur_combo)
            product_srcs[product] = country_combos
        save_store_menu(ctx.obj["base"], config, product_srcs)
