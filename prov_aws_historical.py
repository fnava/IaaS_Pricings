import csv
import locale
locale.setlocale(locale.LC_ALL,"C")

class pricingData:
    def __init__(self, provider, product, currency, date, latest=False):
        self.data = {
            "config": {
                "currency":currency,
                "provider":provider,
                "product":product,
                "date":date,
		"latest":latest
            },
            "regions" : []
        }
    def entry(self, region, vmtype, os, utilization, pricedict):
        instanceType = {
                "os": os,
                "prices": pricedict,
                "type": vmtype,
                "utilization": utilization
            }
        for r in self.data["regions"]:
            if region in r:
                r["instanceTypes"].append(instanceType)
                return
        # create instanceType and append data
        newRegion = {
                    "instanceTypes" : [ instanceType, ],
                    "region" : region
        }
        self.data["regions"].append(newRegion)
    def getdata(self):
        return self.data

features = {}
reader = csv.DictReader(open('provs/amazon/pricings.csv'), delimiter=';')
keyword_key="apiname"
date_key="Date"
locations_keys=[
        "us-east-1", 
	"us-west-2", 
	"us-west-1",
        "eu-west-1", 
	"ap-southeast-1", 
	"ap-northeast-1",
        "ap-southeast-2",
	"sa-east-1"
        ]

DATASETS = []
dobj = {}
latest_date = "20121101"

def get_pricing(dataset, filter_region=None, filter_instance_type=None, filter_os_type=None, filter_provider=None):
    for row in reader:
        #print row
        if row[date_key] not in dobj:
	    latest = row[date_key] == latest_date
            dobj[row[date_key]] = pricingData("Amazon", "AWS", "USD", row[date_key], latest)
            DATASETS.append(row[date_key])
        for loc in locations_keys:
            #print row
            if filter_region is None or loc in filter_region:
                if filter_instance_type is None or filter_instance_type == row[keyword_key]:
                    if filter_os_type is None or filter_os_type == row["OS"]:
                        #print row[date_key]
                        if row[loc] is not None and row[loc].strip() != "":
                            dobj[row[date_key]].entry(loc, row[keyword_key].strip(), row["OS"].strip(), "", {"ondemand":{"hourly":locale.atof(row[loc]), "upfront":None}})

    #print DATASETS
    for ds in DATASETS:
        if filter_provider is None or "Amazon" in filter_provider:
            dataset[ds] = dobj[ds].getdata()
            #print dataset[ds]