# MoreAndMore utilities

This package contains all the command line tools needed for MoreAndMore. The utility can be used to generate the MoreAndMore store menu options, top export postcards for different countries and a couple of other utility steps.

## About the data

All the data for this project comes from [The Observatory of Economic Complexity API](https://atlas.media.mit.edu/api/).

The default configuration for this project uses the following API parameters:

- `hs07` - 2007 Harmonized System trade classification. 
  - **DO NOT CHANGE THIS**! All our icons are labeled based on this classification
  - The HS Codes the API returns are 6 digits long but we cut this down to 4 digits because all our icons are made for the 4 digit codes. 
  - I will say it again in bold because it is important - **We only use 4 digit HS Codes**. All 6 digit code usage is for intermediate steps
- `2010 - 2012` - the time period

- The API uses three digit country codes that can be found in `data/inputs/country_names.tsv` taken from [here](https://atlas.media.mit.edu/en/resources/data/)
- There is also a description of all HS07 codes at `data/inputs/products_hs_07.tsv` also taken from [here](https://atlas.media.mit.edu/en/resources/data/)



## Icons

If you want to use the utilities to generate the postcards you will need to add all the icon pngs that Marina made into `data/inputs/icons` . If you arent sure where these are ask Surya, Sarah or Marina

## config.json

All the commands in the module are configured in the config file at `data/config.json`. Before you do anything else have a look at that file to get a sense of what is possible.



## Setup

### Prerequisites

This package runs on python `3.6.8` and uses [pipenv](https://docs.pipenv.org/en/latest/) for installing dependencies.

To install pipenv you will need to use pip:

`pip install pipenv`.

### Installation

`pipenv install` to install dependencies

Before running any of the commands of this package run `pipenv shell` to create a virtual environment

## Commands



### `all_exports`

#### Usage

` python run.py all_exports`

#### Description

This command downloads all the exports for the country listed in  the `"exports"` object in  `data/config.json` . It uses the `"classification_system"` and "`year"` from `data/config.json` as well

It saves the data in the  `data/exports` folder. The data is saved as a JSON file where the keys are the 4 digit HS code and he value is the RCA value for that HS code for that country

#### Example



{"nor":
	{
		"104812": 0.066,
		"104813": 0.003,
		"104810": 0.145,
		"104811": 0.061,
		"104816": 0.114,
		"104817": 0.576,
		"104814": 0.04
	}
}



### `top_exports`

#### Usage 

`python run.py top_exports`

#### Description

This command generates a list of the top exports of a country, sorted by their RCA value. You can set the country and max number of exports to include in the `"exports"` object in `data/config.json`

#### Verify the data

You can look at the top exports of a country by using the following URL

```
https://atlas.media.mit.edu/en/visualize/tree_map/CLASSIFICATION_SYSTEM/export/COUNTRY_CODE/all/show/YEAR/
```

To test the output of the command:

\- Replace CLASSIFICATION_SYSTEM and YEAR by the value in the JSON file at `data/config.json`

\- Replace the country code with what you have in the `country_codes` value in the `exports` object in the `data/config.json`.

**NOTE** The visualization is mapped to the export value **NOT** RCA (worlds fair share) value. But going if you hover over a block it will show you the RCA value.



### `generate_postcard`

### Usage

`python run.py generate_postcard`

#### Description

This command can be used to generate a countries top export postcard grid.  To configure this command look at the `"postcard"` object in `data/config.json` the dimenion parameters are what we used when we made the postcards at Gov Island. You can change them as needed

The generated grid and description text file are stored at `data/grids/<country-name>`

### `generate_store_menu`

#### Usage

`python run.py generate_store_menu`

#### Description

Get source countries for a given product and destination country. This command generates a list of potential sources for a given destination and product. This is used in the MoreAndMore store website .

The generated data is stored at `data/store-menu`. Two files are generated:

- `product_sources_input.json` - This is the file that contains the list of destination countries and list of products. This is copied over from the `data/config.json` file's "more_and_more_store" object
- `product_sources.json` - This file contains the list of possible sources for a destination country and a given product. The format is a little weird, here is an example of what it looks like for one product

```
{
   "9302":[
      {
         "possible_srcs":[
            "aut",
            "cze",
            "arg",
            "gbr",
            "ita",
            "svk",
            "deu",
            "usa",
            "esp",
            "che"
         ],
         "dst":"bra"
      },
      {
         "possible_srcs":[
            "aut",
            "bra",
            "deu",
            "hrv",
            "ita",
            "phl",
            "arg",
            "cze",
            "isr",
            "tur"
         ],
         "dst":"usa"
      },
      {
         "possible_srcs":[
            "che",
            "deu",
            "cze",
            "ita",
            "est",
            "usa",
            "svk",
            "esp",
            "tha"
         ],
         "dst":"rus"
      },
      {
         "possible_srcs":[
            "aut",
            "ita",
            "usa",
            "cze",
            "isr",
            "bra",
            "blx",
            "deu"
         ],
         "dst":"mex"
      },
      {
         "possible_srcs":[
            "usa",
            "deu",
            "ita",
            "che",
            "chn",
            "isr",
            "dnk",
            "tur",
            "zaf",
            "jpn"
         ],
         "dst":"ind"
      },
      {
         "possible_srcs":[
            "ita",
            "che",
            "deu",
            "aus",
            "nzl"
         ],
         "dst":"chn"
      },
      {
         "possible_srcs":[
            "deu",
            "usa",
            "ita",
            "tha"
         ],
         "dst":"jpn"
      },
      {
         "possible_srcs":[
            "aut",
            "deu",
            "hrv",
            "usa",
            "che",
            "cze",
            "gbr"
         ],
         "dst":"tur"
      },
      {
         "possible_srcs":[
            "gbr"
         ],
         "dst":"som"
      },
      {
         "possible_srcs":[
            "che"
         ],
         "dst":"prk"
      },
      {
         "possible_srcs":[

         ],
         "dst":"nga"
      }
   ]
}
```



#### Verify the data

This got a little confusing the last time we tried this so here is a way to verify it.

- You can get a list of possible import countries("_Where should the product come from?_" page on More and More store website) for a given product and destination country ("_Where Are You?_" page on More and More store website) on the OEC website by using the following URL:
  - `https://atlas.media.mit.edu/en/visualize/tree_map/CLASSIFICATION_SYSTEM/import/DESTINATION_COUNTRY/show/PRODUCT_CODE/YEAR/`
  - Replace CLASSIFICATION_SYSTEM and YEAR by the value in the JSON file at `data/config.json`
  - Pick a DESTINATION_COUNTRY and PRODUCT_CODE from the `country_codes` and `product_codes` array in the JSON file.
  - An [example](https://atlas.media.mit.edu/en/visualize/tree_map/hs07/import/rus/show/0804/2012/):
    - CLASSIFICATION_SYSTEM: hs07
    - DESTINATION_COUNTRY: rus
    - PRODUCT_CODE: 0804
    - YEAR: 2012

### `generate_bilateral_exports`

#### Usage

`python run.py generate_bilateral_exports`

#### Description

This generates JSON files for trade between to countries saved in `data/bilateral-exports/{src_country}-{dst_country}.json`
This is used to generate all the other items that came on the container with the product of your choice on the MoreAndMore website


#### Verify the data

    Get exports from src country to dst country.
    The data is sorted based on the largest exports from src country
    To verify https://oec.world/en/visualize/tree_map/{config["classification_system"]}/export/{src}/{dst}/show/{config["year"]}/
    The number of exports is limited using ["more_and_more_store"]["max_export_products"]