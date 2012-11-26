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
    "colt1":{"pricings":"provs/colt/pricings1.csv",
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
	    "product":"vCloud Essentials"
	    },
    "colt2":{"pricings":"provs/colt/pricings2.csv",
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
	    "product":"vCloud Enterprise"
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
	    },
    "acens":{"pricings":"provs/acens/pricings.csv",
	    "keyword_key":"apiname",
	    "date_key":"Date",
	    "latest_date":"20121125",
	    "location_keys":[
		"acens",
		],
	    "provider":"Acens",
	    "product":"Instant Servers"
    },
    "acens2":{"pricings":"provs/acens/pricings2.csv",
	    "keyword_key":"apiname",
	    "date_key":"Date",
	    "latest_date":"20121125",
	    "location_keys":[
		"acens",
		],
	    "provider":"Acens",
	    "product":"Cloud Servers"
    }
}

PRODUCTS = []
PROVIDERS = []
REGIONS =[]
for providerKey, providerParam in providersDataSources.items():
    if providerParam["product"] not in PRODUCTS:
	PRODUCTS.append(providerParam["product"].replace(' ','_'))
    if providerParam["provider"] not in PROVIDERS:
	PROVIDERS.append(providerParam["provider"].replace(' ','_'))
    for loc in providerParam["location_keys"]:
        if loc not in REGIONS:
	    REGIONS.append(loc.replace(' ','_'))
#print PRODUCTS
#print PROVIDERS
#print REGIONS
	    
# Extract products features:
features = {}
for provider in ["amazon","google","microsoft","colt","gigas","acens","joyent"]:
    reader = csv.DictReader(open('provs/%s/features.csv' % provider), delimiter=';')
    keyword_key="apiname"
    mem_key = "Mem (GB)"
    cpu_key = "CPU (GHz)"
    sto_key = "Storage (GB)"
    iop_key = "I/O Perf"
    for row in reader:
        #print row
        features[row[keyword_key]] = {}
        for k in mem_key, cpu_key, sto_key:
            features[row[keyword_key]][k] = locale.atof(row[k])
        for k in [iop_key, ]:
            features[row[keyword_key]][k] = row[k].strip()
#print features

# Extract pricing information:
def get_pricing(dataset, filter_region=None, filter_instance_type=None, filter_os_type=None, filter_provider=None, filter_product=None):
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
				providerDataset[datasetKey].entry(loc,
								  keyword.strip(),
								  row["OS"].strip(),
								  "",
								  {"ondemand":
								    {"hourly":locale.atof(row[loc]),
								     "upfront":None}
								    }
								  )
				#print providerDataset[datasetKey].getdata()
	#print providerDataset.items()
	for date,providerParam in providerDataset.items():
	    if filter_provider is None or providerParam.data["config"]["provider"].replace(' ','_') in filter_provider:
		if filter_product is None or providerParam.data["config"]["product"].replace(' ','_') in filter_product:
			dataset.append(providerParam.getdata())
    #print dataset