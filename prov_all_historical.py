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


providersDataSources = {
    "aws":{"pricings":"provs/amazon/pricings.csv",
	   "keyword_key":"apiname",
	   "date_key":"Date",
	   "latest_date":"20121101",
	   "location_keys":[
		"us-east-1", 
		"us-west-1", 
		"us-west-2", 
		"eu-west-1", 
		"ap-southeast-1", 
		"ap-northeast-1", 
		"sa-east-1"
		],
	    "provider":"Amazon",
	    "product":"AWS"
	   },
    "google":{"pricings":"provs/google/pricings.csv",
	   "keyword_key":"apiname",
	   "date_key":"Date",
	   "latest_date":"20120628",
	   "location_keys":[
		"us-east1-a",
		"us-central1-a",
		"us-central2-a"
		],
	    "provider":"Google",
	    "product":"GCE"
	   },
    "microsoft":{"pricings":"provs/microsoft/pricings.csv",
	   "keyword_key":"apiname",
	   "date_key":"Date",
	   "latest_date":"20121122",
	   "location_keys":[
		"ms-preview",
		"ms-ga",
		],
	    "provider":"Microsoft",
	    "product":"Azure VM"
	   },
    "colt":{"pricings":"provs/colt/pricings.csv",
	    "keyword_key":"apiname",
	    "date_key":"Date",
	    "latest_date":"20121115",
	    "location_keys":[
		"London",
		"Paris",
		"Franfurkt",
		"Madrid"
		],
	    "provider":"COLT",
	    "product":"vCloud"
	    },
"gigas":{"pricings":"provs/gigas/pricings.csv",
	    "keyword_key":"apiname",
	    "date_key":"Date",
	    "latest_date":"20121121",
	    "location_keys":[
		"Interxion-Madrid",
		],
	    "provider":"Gigas",
	    "product":"Cloud Datacenter"
	    },
"joyent":{"pricings":"provs/joyent/pricings.csv",
	    "keyword_key":"apiname",
	    "date_key":"Date",
	    "latest_date":"20121123",
	    "location_keys":[
		"Joyent",
		],
	    "provider":"Joyent",
	    "product":"Cloud"
	    }
}

features = {}

def get_pricing(dataset, filter_region=None, filter_instance_type=None, filter_os_type=None, filter_provider=None):
    for providerKey, providerParam in providersDataSources.items():
	providerDataset = {}
	reader = csv.DictReader(open(providerParam["pricings"]), delimiter=';')
	for row in reader:
	    #print row
	    date = row[providerParam["date_key"]] 
	    currency = row["currency"]
	    datasetKey = date + currency
	    if datasetKey not in providerDataset:
		latest = ( date == providerParam["latest_date"] )
		name = providerParam["provider"]
		product = providerParam["product"]
		providerDataset[datasetKey] = pricingData(name, product, currency, date, latest)
	    for loc in providerParam["location_keys"]:
		#print row
		if filter_region is None or loc in filter_region:
		    keyword = row[providerParam["keyword_key"]]
		    if filter_instance_type is None or filter_instance_type == keyword:
			if filter_os_type is None or filter_os_type == row["OS"]:
			    if row[loc] is not None and row[loc].strip() != "":
				providerDataset[datasetKey].entry(loc, keyword.strip(), row["OS"].strip(), "", {"ondemand":{"hourly":locale.atof(row[loc]), "upfront":None}})
                                #print providerDataset[date]

	#print providerDataset
	for date,providerParam in providerDataset.items():
	    if filter_provider is None or providerParam.data["config"]["provider"] in filter_provider:
		    dataset.append(providerParam.getdata())
		    #print dataset