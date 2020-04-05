from pyzillow.pyzillow import ZillowWrapper, GetDeepSearchResults
from pyzillow.pyzillowerrors import ZillowError
from pyonboard.pyonboard import get_community_info
import csv
import json
import time
zillow_data = ZillowWrapper('X1-ZWz18uvucryqdn_1r7kw')
APIKEY = 'c250b6c418ec047aaa5b286765cb7edf'

def parse_addresses(fpath):
    with open(fpath) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            try:
                address = row['Address']
                zipcode = row["Zipcode"].split()[1] if " " in row["Zipcode"] else row["Zipcode"]
                deep_search_response = zillow_data.get_deep_search_results(address, zipcode, True)
                result = GetDeepSearchResults(deep_search_response)
                result.zillow_id # zillow id, needed for the GetUpdatedPropertyDetails
                rent = float(result.rentzestimate_amount)
                price = float(result.zestimate_amount)
                community_info = get_community_info(APIKEY, 'application/json', 'ZI'+zipcode)
                onboard_keys = ["one_bed_county", "two_bed_county", "three_bed_county", "four_bed_county", "crmcytotc"] 
                onboard_values = [community_info["package"]["item"][0][k] for k in onboard_keys]
                print(", ".join([address, zipcode, str(price), str(rent), str(rent/price)]+onboard_values))
                time.sleep(6)
            except ZillowError:
                print("ZillowError")
                continue
            except (TypeError, ValueError) as e:
                print(e)
                continue

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='Process addresses from csv.')
    parser.add_argument('fpath',
                        help='csv file path')

    args = parser.parse_args()
    print(parse_addresses(args.fpath))
