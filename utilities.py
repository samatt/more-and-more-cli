import os
import json
import requests
import random
import csv
from PIL import Image, ImageDraw

requests.packages.urllib3.disable_warnings()
BASE_URL = "http://atlas.media.mit.edu"


def conf(base):
    with open(os.path.join(base, "config.json")) as config:
        yield json.load(config)


def hs07_data(base):
    with open(
        os.path.join(base, "inputs", "products_hs_07.tsv")
    ) as classification_file:
        reader = csv.DictReader(
            classification_file, ["id", "hs07", "name"], delimiter="\t"
        )
        return [r for r in reader]


def hs07_description(hs_code, classifications):
    for row in classifications:
        if row["hs07"] == hs_code:
            return (hs_code, '"%s"' % row["name"])
    return ()


def get_all_exports(config):
    country = config["exports"]["country_code"]
    req = "https://atlas.media.mit.edu/%s/export/%s/%s/all/show" % (
        config["classification_system"],
        config["year"],
        country,
    )
    country_res = requests.get(req, verify=False)
    data = json.loads(country_res.text)["data"]
    stuff = [d for d in data if "export_rca" in d and d["hs07_id_len"] == 6]
    rca_dict = {s["hs07_id"]: s["export_rca"] for s in stuff}
    return rca_dict


def save_all_exports(base, config, data):
    folder = os.path.join(base, "exports")
    if not os.path.exists(folder):
        os.makedirs(folder)
    with open(
        os.path.join(
            folder,
            "%s-%s-%s-rca.json"
            % (
                config["exports"]["country_code"],
                config["year"],
                config["classification_system"],
            ),
        ),
        "w",
    ) as out:
        json.dump(data, out)


def icon_path(base, hs_code):
    return os.path.join(base, "icons", "%s-01.png" % hs_code)


def icon_exists(base, hs_code):
    return os.path.exists(icon_path(base, hs_code))


def get_top_exports(base, config, num_exports=0, has_icon=False):
    num_exports = config["exports"]["num_exports"] if num_exports < 1 else num_exports
    country_rca_path = "%s-%s-%s-rca.json" % (
        config["exports"]["country_code"],
        config["year"],
        config["classification_system"],
    )
    if not os.path.exists(os.path.join(base, "exports", country_rca_path)):
        save_all_exports(base, config, get_all_exports(config))
    with open(os.path.join(base, "exports", country_rca_path)) as rca_file:
        country_rca = json.load(rca_file)
        # converting to 4 digit codes
        if has_icon:
            products_rca = [
                (k[-4:], v) for k, v in country_rca.items() if icon_exists(base, k[-4:])
            ]
            products_rca.sort(key=lambda x: x[1], reverse=True)
            return [p[0] for p in products_rca[:num_exports]]
        else:
            products_rca = [(k[-4:], v) for k, v in country_rca.items()]
            products_rca.sort(key=lambda x: x[1], reverse=True)
            return [p[0] for p in products_rca[:num_exports]]


def save_top_exports(base, config, data):
    folder = os.path.join(base, "exports")
    if not os.path.exists(folder):
        os.makedirs(folder)
    with open(
        os.path.join(
            folder,
            "%s-%s-%s-top-%d.txt"
            % (
                config["exports"]["country_code"],
                config["year"],
                config["classification_system"],
                config["exports"]["num_exports"],
            ),
        ),
        "w",
    ) as out:
        classifications = hs07_data(base)
        rows = ["code, description"]
        rows += [
            ",".join(hs07_description(d, classifications))
            for d in data
            if hs07_description(d, classifications)
        ]
        out.write("\n".join(rows))


def parse_country_id(id):
    return id[2:]


def get_source_countries(config, country, hs_code):
    num_src_countries = config["more_and_more_store"]["num_src_countries"]
    # where does country import hs_code from?
    country_req = "http://atlas.media.mit.edu/{}/import/{}/{}/show/{}/".format(
        config["classification_system"], config["year"], country, hs_code
    )
    country_res = requests.get(country_req, verify=False)
    data = json.loads(country_res.text)["data"]
    import_data = [d for d in data if "import_val" in d.keys()]
    import_data.sort(key=lambda x: x["import_val"], reverse=True)
    dest_countries = [parse_country_id(d["dest_id"]) for d in import_data]
    return dest_countries[:num_src_countries]


def save_store_menu(base, config, products_srcs):
    folder = os.path.join(base, "store-menu")
    if not os.path.exists(folder):
        os.makedirs(folder)
    with open(os.path.join(folder, "product_sources.json"), "w") as datafile:
        json.dump(products_srcs, datafile)

    with open(os.path.join(folder, "product_sources_input.json"), "w") as datafile:
        json.dump(config["more_and_more_store"], datafile)


def get_icon_dim(base, hs_code):
    icon = Image.open(icon_path(base, hs_code))
    return icon.size


def generate_grid(base, **kwargs):
    # print(grid_params)
    country_code, width, height, x_padding, y_padding, hs_codes = kwargs.values()
    grid = Image.new("RGB", (width, height), "white")
    icon_width, icon_height = get_icon_dim(base, hs_codes[0])
    used_icons = set()
    for i in range(0, width, (icon_width + x_padding)):
        for j in range(0, height, (icon_height + y_padding)):
            cur_code = random.choice(hs_codes)
            used_icons.add(cur_code)
            icon = Image.open(icon_path(base, cur_code))
            grid.paste(icon, (i, j))
    grid_folder = os.path.join(base, "grids", country_code)
    if not os.path.exists(grid_folder):
        os.makedirs(grid_folder)
    grid.save(
        os.path.join(grid_folder, "%s-%d-products.png" % (country_code, len(hs_codes))),
        "PNG",
    )

    with open(
        os.path.join(
            grid_folder,
            "%s-%d-product-descriptions.csv" % (country_code, len(hs_codes)),
        ),
        "w",
    ) as out:
        classifications = hs07_data(base)
        rows = ["code, description"]
        rows += [
            ",".join(hs07_description(d, classifications))
            for d in used_icons
            if hs07_description(d, classifications)
        ]
        out.write("\n".join(rows))

