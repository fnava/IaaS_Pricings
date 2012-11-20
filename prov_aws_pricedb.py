import urllib2
try:
	import simplejson as json
except ImportError:
	import json
DATASETS = [
        "amazon_ec2_ondemand",
        "amazon_ec2_reserved"
	]

EC2_REGIONS = [
	"us-east-1", 
	"us-west-1", 
	"us-west-2", 
	"eu-west-1", 
	"ap-southeast-1", 
	"ap-northeast-1", 
	"sa-east-1"
]

EC2_INSTANCE_TYPES = [
	"m1.small",
	"m1.medium",
	"m1.large",
	"m1.xlarge",
	"m3.xlarge",
	"m3.2xlarge",
	"t1.micro",
	"m2.xlarge",
	"m2.2xlarge",
	"m2.4xlarge",
	"c1.medium",
	"c1.xlarge",
	"cc1.4xlarge",
	"cc1.8xlarge", # the official api-name is cc2.8xlarge even if it belongs to clusterComputeI family
        "cg1.4xlarge",
        "hi1.4xlarge"
]

EC2_OS_TYPES = [
	"linux",
	"mswin"
]

JSON_NAME_TO_EC2_REGIONS_API = {
	"us-east" : "us-east-1",
	"us-east-1" : "us-east-1", 
	"us-west" : "us-west-1", 
	"us-west-1" : "us-west-1", 
	"us-west-2" : "us-west-2", 
	"eu-ireland" : "eu-west-1", 
	"eu-west-1" : "eu-west-1",
	"apac-sin" : "ap-southeast-1", 
	"ap-southeast-1" : "ap-southeast-1",
	"apac-tokyo" : "ap-northeast-1", 
	"ap-northeast-1" : "ap-northeast-1",
	"sa-east-1" : "sa-east-1",
	"ap-southeast-2" : "ap-southeast-2",        
	"apac-syd" : "ap-southeast-2",        
}

EC2_REGIONS_API_TO_JSON_NAME = {
	"us-east-1" : "us-east", 
	"us-west-1" : "us-west", 
	"us-west-2" : "us-west-2", 
	"eu-west-1" : "eu-ireland", 
	"ap-southeast-1" : "apac-sin", 
	"ap-northeast-1" : "apac-tokyo",
        "ap-southeast-2" : "apac-syd",
	"sa-east-1" : "sa-east-1"	
}

INSTANCES_ON_DEMAND_URL = "http://aws.amazon.com/ec2/pricing/pricing-on-demand-instances.json"
INSTANCES_RESERVED_LIGHT_UTILIZATION_LINUX_URL = "http://aws.amazon.com/ec2/pricing/ri-light-linux.json"
INSTANCES_RESERVED_LIGHT_UTILIZATION_WINDOWS_URL = "http://aws.amazon.com/ec2/pricing/ri-light-mswin.json"
INSTNACES_RESERVED_MEDIUM_UTILIZATION_LINUX_URL = "http://aws.amazon.com/ec2/pricing/ri-medium-linux.json"
INSTANCES_RESERVED_MEDIUM_UTILIZATION_WINDOWS_URL = "http://aws.amazon.com/ec2/pricing/ri-medium-mswin.json"
INSTANCES_RESERVED_HEAVY_UTILIZATION_LINUX_URL = "http://aws.amazon.com/ec2/pricing/ri-heavy-linux.json"
INSTANCES_RESERVED_HEAVY_UTILIZATION_WINDOWS_URL = "http://aws.amazon.com/ec2/pricing/ri-heavy-mswin.json"

INSTANCES_RESERVED_OS_TYPE_BY_URL = {
	INSTANCES_RESERVED_LIGHT_UTILIZATION_LINUX_URL : "linux",
	INSTANCES_RESERVED_LIGHT_UTILIZATION_WINDOWS_URL : "mswin", 
	INSTNACES_RESERVED_MEDIUM_UTILIZATION_LINUX_URL : "linux",
	INSTANCES_RESERVED_MEDIUM_UTILIZATION_WINDOWS_URL : "mswin",
	INSTANCES_RESERVED_HEAVY_UTILIZATION_LINUX_URL : "linux",
	INSTANCES_RESERVED_HEAVY_UTILIZATION_WINDOWS_URL  : "mswin"
}

INSTANCES_RESERVED_UTILIZATION_TYPE_BY_URL = {
	INSTANCES_RESERVED_LIGHT_UTILIZATION_LINUX_URL : "light",
	INSTANCES_RESERVED_LIGHT_UTILIZATION_WINDOWS_URL : "light", 
	INSTNACES_RESERVED_MEDIUM_UTILIZATION_LINUX_URL : "medium",
	INSTANCES_RESERVED_MEDIUM_UTILIZATION_WINDOWS_URL : "medium",
	INSTANCES_RESERVED_HEAVY_UTILIZATION_LINUX_URL : "heavy",
	INSTANCES_RESERVED_HEAVY_UTILIZATION_WINDOWS_URL  : "heavy"	
}

DEFAULT_CURRENCY = "USD"

INSTANCE_TYPE_MAPPING = {
	"stdODI" : "m1",
	"uODI" : "t1",
	"hiMemODI" : "m2",
	"secgenstdODI" : "m3",
	"hiCPUODI" : "c1",
	"clusterComputeI" : "cc1",
	"clusterGPUI" : "cg1",
	"hiIoODI" : "hi1",

	# Reserved Instance Types
	"stdResI" : "m1",
	"uResI" : "t1",
	"hiMemResI" : "m2",
	"hiCPUResI" : "c1",
	"clusterCompResI" : "cc1",
	"clusterGPUResI" : "cg1",
	"hiIoResI" : "hi1"
}

INSTANCE_SIZE_MAPPING = {
	"u" : "micro",
	"sm" : "small",
	"med" : "medium",
	"lg" : "large",
	"xl" : "xlarge",
	"xxl" : "2xlarge",
	"xxxxl" : "4xlarge",
	"xxxxxxxxl" : "8xlarge"
}

# while published JSON refers to clusterComputeI xxxxxxxxl instance the api-name is cc2.8xlarge
INSTANCE_REMAPPING = {
	"cc1.8xlarge":"cc2.8xlarge"
}

def _load_data(url):
	f = urllib2.urlopen(url)
	return json.loads(f.read())

def get_ec2_reserved_instances_prices(filter_region=None, filter_instance_type=None, filter_os_type=None):
	""" Get EC2 reserved instances prices. Results can be filtered by region """

	get_specific_region = (filter_region is not None)
	if get_specific_region:
		filter_region = EC2_REGIONS_API_TO_JSON_NAME[filter_region]
	get_specific_instance_type = (filter_instance_type is not None)
	get_specific_os_type = (filter_os_type is not None)

	currency = DEFAULT_CURRENCY

	urls = [
		INSTANCES_RESERVED_LIGHT_UTILIZATION_LINUX_URL,
		INSTANCES_RESERVED_LIGHT_UTILIZATION_WINDOWS_URL,
		INSTNACES_RESERVED_MEDIUM_UTILIZATION_LINUX_URL,
		INSTANCES_RESERVED_MEDIUM_UTILIZATION_WINDOWS_URL,
		INSTANCES_RESERVED_HEAVY_UTILIZATION_LINUX_URL,
		INSTANCES_RESERVED_HEAVY_UTILIZATION_WINDOWS_URL 
	]

	result_regions = []
	result_regions_index = {}
	result = {
		"config" : {
			"currency" : currency,
		},
		"regions" : result_regions
	}

	for u in urls:
		os_type = INSTANCES_RESERVED_OS_TYPE_BY_URL[u]
		utilization_type = INSTANCES_RESERVED_UTILIZATION_TYPE_BY_URL[u]
		data = _load_data(u)
		if "config" in data and data["config"] and "regions" in data["config"] and data["config"]["regions"]:
			for r in data["config"]["regions"]:
				if "region" in r and r["region"]:
					if get_specific_region and filter_region != r["region"]:
						continue

				region_name = JSON_NAME_TO_EC2_REGIONS_API[r["region"]]
				if region_name in result_regions_index:
					instance_types = result_regions_index[region_name]["instanceTypes"]
				else:
					instance_types = []
					result_regions.append({
						"region" : region_name,
						"instanceTypes" : instance_types
					})
					result_regions_index[region_name] = result_regions[-1]
					
				if "instanceTypes" in r:
					for it in r["instanceTypes"]:
						instance_type = INSTANCE_TYPE_MAPPING[it["type"]]
						if "sizes" in it:
							for s in it["sizes"]:
								instance_size = INSTANCE_SIZE_MAPPING[s["size"]]

								prices = {
									"1year" : {
										"hourly" : None,
										"upfront" : None
									},
									"3year" : {
										"hourly" : None,
										"upfront" : None
									}
								}

								_type = "%s.%s" % (instance_type, instance_size)

								if get_specific_instance_type and _type != filter_instance_type:
									continue

								if get_specific_os_type and os_type != filter_os_type:
									continue

								instance_types.append({
									"type" : _type,
									"os" : os_type,
									"utilization" : utilization_type,
									"prices" : prices
								})

								for price_data in s["valueColumns"]:
									price = None
									try:
										price = float(price_data["prices"][currency])
									except ValueError:
										price = None
									
									if price_data["name"] == "yrTerm1":
										prices["1year"]["upfront"] = price
									elif price_data["name"] == "yrTerm1Hourly":
										prices["1year"]["hourly"] = price
									elif price_data["name"] == "yrTerm3":
										prices["3year"]["upfront"] = price
									elif price_data["name"] == "yrTerm3Hourly":
										prices["3year"]["hourly"] = price			

	return result

def get_ec2_ondemand_instances_prices(filter_region=None, filter_instance_type=None, filter_os_type=None):
	""" Get EC2 on-demand instances prices. Results can be filtered by region """

	get_specific_region = (filter_region is not None)
	if get_specific_region:
		filter_region = EC2_REGIONS_API_TO_JSON_NAME[filter_region]

	get_specific_instance_type = (filter_instance_type is not None)
	get_specific_os_type = (filter_os_type is not None)

	currency = DEFAULT_CURRENCY

	result_regions = []
	result = {
		"config" : {
			"currency" : currency,
			"unit" : "perhr"
		},
		"regions" : result_regions
	}

	data = _load_data(INSTANCES_ON_DEMAND_URL)
	if "config" in data and data["config"] and "regions" in data["config"] and data["config"]["regions"]:
		for r in data["config"]["regions"]:
			if "region" in r and r["region"]:
				if get_specific_region and filter_region != r["region"]:
					continue

				region_name = JSON_NAME_TO_EC2_REGIONS_API[r["region"]]
				instance_types = []
				if "instanceTypes" in r:
					for it in r["instanceTypes"]:
						instance_type = INSTANCE_TYPE_MAPPING[it["type"]]
						# nasty remapping:
						if instance_type in INSTANCE_REMAPPING:
							instance_type = INSTANCE_REMAPPING[instance_type]
						if "sizes" in it:
							for s in it["sizes"]:
								instance_size = INSTANCE_SIZE_MAPPING[s["size"]]


								for price_data in s["valueColumns"]:
									price = None
									try:
										price = float(price_data["prices"][currency])
									except ValueError:
										price = None

									_type = "%s.%s" % (instance_type, instance_size)

									if get_specific_instance_type and _type != filter_instance_type:
										continue

									if get_specific_os_type and price_data["name"] != filter_os_type:
										continue
								
                                                                        prices = {
                                                                                "ondemand" : {
                                                                                        "hourly" : None,
                                                                                        "upfront" : None
                                                                                }
                                                                        }
                                                                        
                                                                        prices["ondemand"]["hourly"] = price
                                                                
									instance_types.append({
										"type" : _type,
										"os" : price_data["name"],
                                                                                "utilization" : "",
										"prices" : prices
									})

					result_regions.append({
						"region" : region_name,
						"instanceTypes" : instance_types
					})

		return result

	return None
    
def get_pricing(dataset, filter_region=None, filter_instance_type=None, filter_os_type=None, filter_provider=None, filter_reserve=None):
    if filter_provider is None or filter_provider == "Amazon":
	if filter_reserve is None or filter_reserve == "ondemand": 
		dataset["amazon_ec2_ondemand"] = None
		dataset["amazon_ec2_ondemand"] = get_ec2_ondemand_instances_prices(filter_region, filter_instance_type, filter_os_type)
		dataset["amazon_ec2_ondemand"]["config"]["provider"]="Amazon"
		dataset["amazon_ec2_ondemand"]["config"]["product"]="AWS"
		dataset["amazon_ec2_ondemand"]["config"]["date"]="20120831"
	if filter_reserve is None or filter_reserve == "reserved": 
		dataset["amazon_ec2_reserved"] = None
		dataset["amazon_ec2_reserved"] = get_ec2_reserved_instances_prices(filter_region, filter_instance_type, filter_os_type)
		dataset["amazon_ec2_reserved"]["config"]["provider"]="Amazon"
		dataset["amazon_ec2_reserved"]["config"]["product"]="AWS"
		dataset["amazon_ec2_reserved"]["config"]["date"]="20120831"
                
                
if __name__ == '__main__':
    ds = {}
    get_pricing(ds, filter_reserve="ondemand")
    
    tbl = {"linux":{}, "mswin":{}}
    for t in EC2_INSTANCE_TYPES:
        tbl["linux"][t] = {}
        tbl["mswin"][t] = {}

    for k, data in ds.items():
        for r in data["regions"]:
            region_name = r["region"]
            for it in r["instanceTypes"]:
                for term in it["prices"]:
                    hourly = it["prices"][term]["hourly"]
                    os = it["os"]
                    vmtype = it["type"]
                    tbl[os][vmtype][region_name]=hourly    

    import locale
    #locale.setlocale(locale.LC_ALL,"es_ES")

    print "Date;OS;Type;keyword",
    for r in EC2_REGIONS:
        print ";%s" % r,
    print

    for os,ostbl in tbl.items():
        for vmtype in EC2_INSTANCE_TYPES:
            if vmtype in ostbl:
                vmtbl = ostbl[vmtype]
                print "%s;%s;%s" % ("20121101", os, vmtype),
                for r in EC2_REGIONS:
                    if r in vmtbl and vmtbl[r] is not None:
                        print ";%s" % locale.str(vmtbl[r]),
                    else:
                        print ";",
                print
