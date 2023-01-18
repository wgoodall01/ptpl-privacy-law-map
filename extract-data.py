#!/usr/bin/env python3
import csv
import sys
import pandas as pd

def main():
    # Load the region codes, and create mappings.
    region_data = pd.read_csv("./data/region-codes.csv", na_filter=False)
    region_codes = region_data[['alpha-2', 'name']]
    country_code_to_name = {code: name for [_, [code, name]] in region_codes.iterrows()}
    name_to_country_code = {name: code for [_, [code, name]] in region_codes.iterrows()}

    # Load the laws data.
    laws = pd.read_excel("./data/DP.xlsx", na_filter=False)

    # Load the countries data.
    countries = pd.read_json("./data/country-data.json").filter(["countries"])

    # Write CSV output to stdout.
    csv_fields = ["Country Code", "Country Name", "Legislation Status", "Law Names", "Law URLs"]
    csv_writer = csv.DictWriter(sys.stdout, fieldnames=csv_fields)
    csv_writer.writeheader()


    # Construct the output for each country.
    for (country_code, [flags]) in countries.iterrows():
        country_name = country_code_to_name[country_code]

        # Get the status of that country's privacy legislation.
        privacy_law_status = decode_status(flags[2])

        # Get data from the laws list.
        relevant_laws = laws[laws['Country'] == country_name]
        if len(relevant_laws) > 0:
            law_names = ", ".join(relevant_laws["Title of Legislation/Draft Legislation"])
            law_urls = ", ".join(relevant_laws["Links to laws"])
        else:
            law_names = None
            law_urls = None

        csv_writer.writerow({
            "Country Code": country_code,
            "Country Name": country_name,
            "Legislation Status": privacy_law_status,
            "Law Names": law_names,
            "Law URLs": law_urls
        })

def decode_status(code):
    """Convert an integer status for a law type to a string description."""
    return [
        "No Data",
        "Legislation",
        "Draft Legislation",
        "No Legislation",
    ][code]


if __name__ == "__main__": main()

