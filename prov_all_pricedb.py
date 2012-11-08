DATASETS = [
	"azure",
	"google_ce",
	"ibm_eur",
        "ibm_usd",
	"gigas",
	]

def get_pricing(dataset, filter_provider):
    for ds in DATASETS:
        if filter_provider is None or filter_provider == dobj[ds].provider:
            dataset[ds] = dobj[ds].getdata()
	    
class pricingData:
    def __init__(self, provider, product, currency, date):
        self.data = {
            "config": {
                "currency":currency,
                "provider":provider,
                "product":product,
                "date":date
            },
            "regions" : []
        }
	self.provider = provider
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


dobj = {}
       
dobj["google_ce"] = pricingData("Google", "GCE", "USD", "20120831")
dobj["google_ce"].entry("google-us", "n1-standard-1d", "linux", "", {"ondemand":{"hourly":0.145, "upfront":None}})
dobj["google_ce"].entry("google-us", "n1-standard-2d", "linux", "", {"ondemand":{"hourly":0.29, "upfront":None}})
dobj["google_ce"].entry("google-us", "n1-standard-4d", "linux", "", {"ondemand":{"hourly":0.58, "upfront":None}})
dobj["google_ce"].entry("google-us", "n1-standard-8d", "linux", "", {"ondemand":{"hourly":1.16, "upfront":None}})

dobj["azure"] = pricingData("Microsoft", "Azure", "USD", "20120831")

dobj["azure"].entry("ms-preview", "Extra Small", "mswin", "", {"ondemand":{"hourly":0.0133, "upfront":None}} ) 
dobj["azure"].entry("ms-preview", "Small",       "mswin", "", {"ondemand":{"hourly":0.08, "upfront":None}} ) 
dobj["azure"].entry("ms-preview", "Medium",      "mswin", "", {"ondemand":{"hourly":0.16, "upfront":None}} ) 
dobj["azure"].entry("ms-preview", "Large",       "mswin", "", {"ondemand":{"hourly":0.32, "upfront":None}} ) 
dobj["azure"].entry("ms-preview", "Extra Large", "mswin", "", {"ondemand":{"hourly":0.64, "upfront":None}} )

dobj["azure"].entry("ms-ga", "Extra Small",      "mswin", "", {"ondemand":{"hourly":0.02, "upfront":None}} ) 
dobj["azure"].entry("ms-ga", "Small",            "mswin", "", {"ondemand":{"hourly":0.115, "upfront":None}} ) 
dobj["azure"].entry("ms-ga", "Medium",           "mswin", "", {"ondemand":{"hourly":0.23, "upfront":None}} ) 
dobj["azure"].entry("ms-ga", "Large",            "mswin", "", {"ondemand":{"hourly":0.46, "upfront":None}} ) 
dobj["azure"].entry("ms-ga", "Extra Large",      "mswin", "", {"ondemand":{"hourly":0.92, "upfront":None}} )

dobj["azure"].entry("ms-preview", "Extra Small", "linux", "", {"ondemand":{"hourly":0.0133, "upfront":None}} ) 
dobj["azure"].entry("ms-preview", "Small",       "linux", "", {"ondemand":{"hourly":0.08, "upfront":None}} ) 
dobj["azure"].entry("ms-preview", "Medium",      "linux", "", {"ondemand":{"hourly":0.16, "upfront":None}} ) 
dobj["azure"].entry("ms-preview", "Large",       "linux", "", {"ondemand":{"hourly":0.32, "upfront":None}} ) 
dobj["azure"].entry("ms-preview", "Extra Large", "linux", "", {"ondemand":{"hourly":0.64, "upfront":None}} )

dobj["azure"].entry("ms-ga", "Extra Small",      "linux", "", {"ondemand":{"hourly":0.02, "upfront":None}} ) 
dobj["azure"].entry("ms-ga", "Small",            "linux", "", {"ondemand":{"hourly":0.085, "upfront":None}} ) 
dobj["azure"].entry("ms-ga", "Medium",           "linux", "", {"ondemand":{"hourly":0.17, "upfront":None}} ) 
dobj["azure"].entry("ms-ga", "Large",            "linux", "", {"ondemand":{"hourly":0.34, "upfront":None}} ) 
dobj["azure"].entry("ms-ga", "Extra Large",      "linux", "", {"ondemand":{"hourly":0.68, "upfront":None}} ) 

dobj["ibm_eur"] = pricingData("IBM", "SmartCloud", "EUR", "20120831")

dobj["ibm_eur"].entry("ibm", "Copper 32", "rhel",  "", {"6month":{"hourly":0.069, "upfront":1440}, "12month":{"hourly":0.069, "upfront":1010}} )
dobj["ibm_eur"].entry("ibm", "Copper 32", "sles",  "", {"6month":{"hourly":0.046, "upfront":1440}, "12month":{"hourly":0.046, "upfront":1010}} )
dobj["ibm_eur"].entry("ibm", "Copper 32", "mswin", "", {"6month":{"hourly":0.050, "upfront":1440}, "12month":{"hourly":0.050, "upfront":1010}} )
dobj["ibm_eur"].entry("ibm", "Copper 32", "linux", "", {"6month":{"hourly":0.030, "upfront":1440}, "12month":{"hourly":0.030, "upfront":1010}} )

dobj["ibm_eur"].entry("ibm", "Bronze 32", "rhel",  "", {"6month":{"hourly":0.078, "upfront":1440}, "12month":{"hourly":0.078, "upfront":1010}} )
dobj["ibm_eur"].entry("ibm", "Bronze 32", "sles",  "", {"6month":{"hourly":0.055, "upfront":1440}, "12month":{"hourly":0.055, "upfront":1010}} )
dobj["ibm_eur"].entry("ibm", "Bronze 32", "mswin", "", {"6month":{"hourly":0.058, "upfront":1440}, "12month":{"hourly":0.058, "upfront":1010}} )
dobj["ibm_eur"].entry("ibm", "Bronze 32", "linux", "", {"6month":{"hourly":0.039, "upfront":1440}, "12month":{"hourly":0.039, "upfront":1010}} )

dobj["ibm_eur"].entry("ibm", "Silver 32", "rhel",  "", {"6month":{"hourly":0.105, "upfront":1440}, "12month":{"hourly":0.105, "upfront":1010}} )
dobj["ibm_eur"].entry("ibm", "Silver 32", "sles",  "", {"6month":{"hourly":0.082, "upfront":1440}, "12month":{"hourly":0.082, "upfront":1010}} )
dobj["ibm_eur"].entry("ibm", "Silver 32", "mswin", "", {"6month":{"hourly":0.117, "upfront":1440}, "12month":{"hourly":0.117, "upfront":1010}} )
dobj["ibm_eur"].entry("ibm", "Silver 32", "linux", "", {"6month":{"hourly":0.066, "upfront":1440}, "12month":{"hourly":0.066, "upfront":1010}} )

dobj["ibm_eur"].entry("ibm", "Gold 32", "rhel",    "", {"6month":{"hourly":0.152, "upfront":1440}, "12month":{"hourly":0.152, "upfront":1010}} )
dobj["ibm_eur"].entry("ibm", "Gold 32", "sles",    "", {"6month":{"hourly":0.129, "upfront":1440}, "12month":{"hourly":0.129, "upfront":1010}} )
dobj["ibm_eur"].entry("ibm", "Gold 32", "mswin",   "", {"6month":{"hourly":0.164, "upfront":1440}, "12month":{"hourly":0.164, "upfront":1010}} )
dobj["ibm_eur"].entry("ibm", "Gold 32", "linux",   "", {"6month":{"hourly":0.113, "upfront":1440}, "12month":{"hourly":0.113, "upfront":1010}} )

dobj["ibm_eur"].entry("ibm", "Copper 64", "rhel",  "", {"6month":{"hourly":0.129, "upfront":1440}, "12month":{"hourly":0.129, "upfront":1010}} )
dobj["ibm_eur"].entry("ibm", "Copper 64", "sles",  "", {"6month":{"hourly":0.105, "upfront":1440}, "12month":{"hourly":0.105, "upfront":1010}} )
dobj["ibm_eur"].entry("ibm", "Copper 64", "mswin", "", {"6month":{"hourly":0.160, "upfront":1440}, "12month":{"hourly":0.160, "upfront":1010}} )
dobj["ibm_eur"].entry("ibm", "Copper 64", "linux", "", {"6month":{"hourly":0.090, "upfront":1440}, "12month":{"hourly":0.090, "upfront":1010}} )

dobj["ibm_eur"].entry("ibm", "Bronze 64", "rhel",  "", {"6month":{"hourly":0.164, "upfront":1440}, "12month":{"hourly":0.164, "upfront":1010}} )
dobj["ibm_eur"].entry("ibm", "Bronze 64", "sles",  "", {"6month":{"hourly":0.140, "upfront":1440}, "12month":{"hourly":0.140, "upfront":1010}} )
dobj["ibm_eur"].entry("ibm", "Bronze 64", "mswin", "", {"6month":{"hourly":0.171, "upfront":1440}, "12month":{"hourly":0.171, "upfront":1010}} )
dobj["ibm_eur"].entry("ibm", "Bronze 64", "linux", "", {"6month":{"hourly":0.125, "upfront":1440}, "12month":{"hourly":0.125, "upfront":1010}} )

dobj["ibm_eur"].entry("ibm", "Silver 64", "rhel",  "", {"6month":{"hourly":0.195, "upfront":1440}, "12month":{"hourly":0.195, "upfront":1010}} )
dobj["ibm_eur"].entry("ibm", "Silver 64", "sles",  "", {"6month":{"hourly":0.171, "upfront":1440}, "12month":{"hourly":0.171, "upfront":1010}} )
dobj["ibm_eur"].entry("ibm", "Silver 64", "mswin", "", {"6month":{"hourly":0.210, "upfront":1440}, "12month":{"hourly":0.210, "upfront":1010}} )
dobj["ibm_eur"].entry("ibm", "Silver 64", "linux", "", {"6month":{"hourly":0.156, "upfront":1440}, "12month":{"hourly":0.156, "upfront":1010}} )

dobj["ibm_eur"].entry("ibm", "Gold 64", "rhel",    "", {"6month":{"hourly":0.288, "upfront":1440}, "12month":{"hourly":0.288, "upfront":1010}} )
dobj["ibm_eur"].entry("ibm", "Gold 64", "sles",    "", {"6month":{"hourly":0.265, "upfront":1440}, "12month":{"hourly":0.265, "upfront":1010}} )
dobj["ibm_eur"].entry("ibm", "Gold 64", "mswin",   "", {"6month":{"hourly":0.428, "upfront":1440}, "12month":{"hourly":0.428, "upfront":1010}} )
dobj["ibm_eur"].entry("ibm", "Gold 64", "linux",   "", {"6month":{"hourly":0.249, "upfront":1440}, "12month":{"hourly":0.249, "upfront":1010}} )

dobj["ibm_eur"].entry("ibm", "Platinum 64", "rhel",    "", {"6month":{"hourly":0.561, "upfront":1440}, "12month":{"hourly":0.561, "upfront":1010}} )
dobj["ibm_eur"].entry("ibm", "Platinum 64", "sles",    "", {"6month":{"hourly":0.506, "upfront":1440}, "12month":{"hourly":0.506, "upfront":1010}} )
dobj["ibm_eur"].entry("ibm", "Platinum 64", "mswin",   "", {"6month":{"hourly":0.974, "upfront":1440}, "12month":{"hourly":1.974, "upfront":1010}} )
dobj["ibm_eur"].entry("ibm", "Platinum 64", "linux",   "", {"6month":{"hourly":0.491, "upfront":1440}, "12month":{"hourly":0.491, "upfront":1010}} )

dobj["ibm_eur"].entry("ibm", "Copper 32", "rhel",  "", {"ondemand":{"hourly":0.097, "upfront":None}} )
dobj["ibm_eur"].entry("ibm", "Copper 32", "sles",  "", {"ondemand":{"hourly":0.074, "upfront":None}} )
dobj["ibm_eur"].entry("ibm", "Copper 32", "mswin", "", {"ondemand":{"hourly":0.078, "upfront":None}} )
dobj["ibm_eur"].entry("ibm", "Copper 32", "linux", "", {"ondemand":{"hourly":0.058, "upfront":None}} )

dobj["ibm_eur"].entry("ibm", "Bronze 32", "rhel",  "", {"ondemand":{"hourly":0.113, "upfront":None}} )
dobj["ibm_eur"].entry("ibm", "Bronze 32", "sles",  "", {"ondemand":{"hourly":0.090, "upfront":None}} )
dobj["ibm_eur"].entry("ibm", "Bronze 32", "mswin", "", {"ondemand":{"hourly":0.093, "upfront":None}} )
dobj["ibm_eur"].entry("ibm", "Bronze 32", "linux", "", {"ondemand":{"hourly":0.074, "upfront":None}} )

dobj["ibm_eur"].entry("ibm", "Silver 32", "rhel",  "", {"ondemand":{"hourly":0.179, "upfront":None}} )
dobj["ibm_eur"].entry("ibm", "Silver 32", "sles",  "", {"ondemand":{"hourly":0.156, "upfront":None}} )
dobj["ibm_eur"].entry("ibm", "Silver 32", "mswin", "", {"ondemand":{"hourly":0.187, "upfront":None}} )
dobj["ibm_eur"].entry("ibm", "Silver 32", "linux", "", {"ondemand":{"hourly":0.140, "upfront":None}} )

dobj["ibm_eur"].entry("ibm", "Gold 32", "rhel",    "", {"ondemand":{"hourly":0.280, "upfront":None}} )
dobj["ibm_eur"].entry("ibm", "Gold 32", "sles",    "", {"ondemand":{"hourly":0.257, "upfront":None}} )
dobj["ibm_eur"].entry("ibm", "Gold 32", "mswin",   "", {"ondemand":{"hourly":0.288, "upfront":None}} )
dobj["ibm_eur"].entry("ibm", "Gold 32", "linux",   "", {"ondemand":{"hourly":0.241, "upfront":None}} )

dobj["ibm_eur"].entry("ibm", "Copper 64", "rhel",  "", {"ondemand":{"hourly":0.234, "upfront":None}} )
dobj["ibm_eur"].entry("ibm", "Copper 64", "sles",  "", {"ondemand":{"hourly":0.210, "upfront":None}} )
dobj["ibm_eur"].entry("ibm", "Copper 64", "mswin", "", {"ondemand":{"hourly":0.265, "upfront":None}} )
dobj["ibm_eur"].entry("ibm", "Copper 64", "linux", "", {"ondemand":{"hourly":0.195, "upfront":None}} )

dobj["ibm_eur"].entry("ibm", "Bronze 64", "rhel",  "", {"ondemand":{"hourly":0.312, "upfront":None}} )
dobj["ibm_eur"].entry("ibm", "Bronze 64", "sles",  "", {"ondemand":{"hourly":0.288, "upfront":None}} )
dobj["ibm_eur"].entry("ibm", "Bronze 64", "mswin", "", {"ondemand":{"hourly":0.312, "upfront":None}} )
dobj["ibm_eur"].entry("ibm", "Bronze 64", "linux", "", {"ondemand":{"hourly":0.273, "upfront":None}} )

dobj["ibm_eur"].entry("ibm", "Silver 64", "rhel",  "", {"ondemand":{"hourly":0.374, "upfront":None}} )
dobj["ibm_eur"].entry("ibm", "Silver 64", "sles",  "", {"ondemand":{"hourly":0.351, "upfront":None}} )
dobj["ibm_eur"].entry("ibm", "Silver 64", "mswin", "", {"ondemand":{"hourly":0.389, "upfront":None}} )
dobj["ibm_eur"].entry("ibm", "Silver 64", "linux", "", {"ondemand":{"hourly":0.335, "upfront":None}} )

dobj["ibm_eur"].entry("ibm", "Gold 64", "rhel",    "", {"ondemand":{"hourly":0.576, "upfront":None}} )
dobj["ibm_eur"].entry("ibm", "Gold 64", "sles",    "", {"ondemand":{"hourly":0.553, "upfront":None}} )
dobj["ibm_eur"].entry("ibm", "Gold 64", "mswin",   "", {"ondemand":{"hourly":0.748, "upfront":None}} )
dobj["ibm_eur"].entry("ibm", "Gold 64", "linux",   "", {"ondemand":{"hourly":0.537, "upfront":None}} )

dobj["ibm_eur"].entry("ibm", "Platinum 64", "rhel",    "", {"ondemand":{"hourly":1.137, "upfront":None}} )
dobj["ibm_eur"].entry("ibm", "Platinum 64", "sles",    "", {"ondemand":{"hourly":1.083, "upfront":None}} )
dobj["ibm_eur"].entry("ibm", "Platinum 64", "mswin",   "", {"ondemand":{"hourly":1.550, "upfront":None}} )
dobj["ibm_eur"].entry("ibm", "Platinum 64", "linux",   "", {"ondemand":{"hourly":1.067, "upfront":None}} )

dobj["ibm_usd"] = pricingData("IBM", "SmartCloud", "USD", "20120831")

dobj["ibm_usd"].entry("ibm", "Copper 32", "rhel",  "", {"6month":{"hourly":0.089, "upfront":1850}, "12month":{"hourly":0.089, "upfront":1300}} )
dobj["ibm_usd"].entry("ibm", "Copper 32", "sles",  "", {"6month":{"hourly":0.059, "upfront":1850}, "12month":{"hourly":0.059, "upfront":1300}} )
dobj["ibm_usd"].entry("ibm", "Copper 32", "mswin", "", {"6month":{"hourly":0.064, "upfront":1850}, "12month":{"hourly":0.064, "upfront":1300}} )
dobj["ibm_usd"].entry("ibm", "Copper 32", "linux", "", {"6month":{"hourly":0.039, "upfront":1850}, "12month":{"hourly":0.039, "upfront":1300}} )

dobj["ibm_usd"].entry("ibm", "Bronze 32", "rhel",  "", {"6month":{"hourly":0.100, "upfront":1850}, "12month":{"hourly":0.100, "upfront":1300}} )
dobj["ibm_usd"].entry("ibm", "Bronze 32", "sles",  "", {"6month":{"hourly":0.070, "upfront":1850}, "12month":{"hourly":0.070, "upfront":1300}} )
dobj["ibm_usd"].entry("ibm", "Bronze 32", "mswin", "", {"6month":{"hourly":0.075, "upfront":1850}, "12month":{"hourly":0.075, "upfront":1300}} )
dobj["ibm_usd"].entry("ibm", "Bronze 32", "linux", "", {"6month":{"hourly":0.050, "upfront":1850}, "12month":{"hourly":0.050, "upfront":1300}} )

dobj["ibm_usd"].entry("ibm", "Silver 32", "rhel",  "", {"6month":{"hourly":0.135, "upfront":1850}, "12month":{"hourly":0.135, "upfront":1300}} )
dobj["ibm_usd"].entry("ibm", "Silver 32", "sles",  "", {"6month":{"hourly":0.105, "upfront":1850}, "12month":{"hourly":0.105, "upfront":1300}} )
dobj["ibm_usd"].entry("ibm", "Silver 32", "mswin", "", {"6month":{"hourly":0.150, "upfront":1850}, "12month":{"hourly":0.150, "upfront":1300}} )
dobj["ibm_usd"].entry("ibm", "Silver 32", "linux", "", {"6month":{"hourly":0.085, "upfront":1850}, "12month":{"hourly":0.085, "upfront":1300}} )

dobj["ibm_usd"].entry("ibm", "Gold 32", "rhel",    "", {"6month":{"hourly":0.195, "upfront":1850}, "12month":{"hourly":0.195, "upfront":1300}} )
dobj["ibm_usd"].entry("ibm", "Gold 32", "sles",    "", {"6month":{"hourly":0.165, "upfront":1850}, "12month":{"hourly":0.165, "upfront":1300}} )
dobj["ibm_usd"].entry("ibm", "Gold 32", "mswin",   "", {"6month":{"hourly":0.210, "upfront":1850}, "12month":{"hourly":0.210, "upfront":1300}} )
dobj["ibm_usd"].entry("ibm", "Gold 32", "linux",   "", {"6month":{"hourly":0.145, "upfront":1850}, "12month":{"hourly":0.145, "upfront":1300}} )

dobj["ibm_usd"].entry("ibm", "Copper 64", "rhel",  "", {"6month":{"hourly":0.165, "upfront":1850}, "12month":{"hourly":0.165, "upfront":1300}} )
dobj["ibm_usd"].entry("ibm", "Copper 64", "sles",  "", {"6month":{"hourly":0.135, "upfront":1850}, "12month":{"hourly":0.135, "upfront":1300}} )
dobj["ibm_usd"].entry("ibm", "Copper 64", "mswin", "", {"6month":{"hourly":0.205, "upfront":1850}, "12month":{"hourly":0.205, "upfront":1300}} )
dobj["ibm_usd"].entry("ibm", "Copper 64", "linux", "", {"6month":{"hourly":0.115, "upfront":1850}, "12month":{"hourly":0.115, "upfront":1300}} )

dobj["ibm_usd"].entry("ibm", "Bronze 64", "rhel",  "", {"6month":{"hourly":0.210, "upfront":1850}, "12month":{"hourly":0.210, "upfront":1300}} )
dobj["ibm_usd"].entry("ibm", "Bronze 64", "sles",  "", {"6month":{"hourly":0.180, "upfront":1850}, "12month":{"hourly":0.180, "upfront":1300}} )
dobj["ibm_usd"].entry("ibm", "Bronze 64", "mswin", "", {"6month":{"hourly":0.220, "upfront":1850}, "12month":{"hourly":0.220, "upfront":1300}} )
dobj["ibm_usd"].entry("ibm", "Bronze 64", "linux", "", {"6month":{"hourly":0.160, "upfront":1850}, "12month":{"hourly":0.160, "upfront":1300}} )

dobj["ibm_usd"].entry("ibm", "Silver 64", "rhel",  "", {"6month":{"hourly":0.250, "upfront":1850}, "12month":{"hourly":0.250, "upfront":1300}} )
dobj["ibm_usd"].entry("ibm", "Silver 64", "sles",  "", {"6month":{"hourly":0.220, "upfront":1850}, "12month":{"hourly":0.220, "upfront":1300}} )
dobj["ibm_usd"].entry("ibm", "Silver 64", "mswin", "", {"6month":{"hourly":0.270, "upfront":1850}, "12month":{"hourly":0.270, "upfront":1300}} )
dobj["ibm_usd"].entry("ibm", "Silver 64", "linux", "", {"6month":{"hourly":0.200, "upfront":1850}, "12month":{"hourly":0.200, "upfront":1300}} )

dobj["ibm_usd"].entry("ibm", "Gold 64", "rhel",    "", {"6month":{"hourly":0.370, "upfront":1850}, "12month":{"hourly":0.370, "upfront":1300}} )
dobj["ibm_usd"].entry("ibm", "Gold 64", "sles",    "", {"6month":{"hourly":0.340, "upfront":1850}, "12month":{"hourly":0.340, "upfront":1300}} )
dobj["ibm_usd"].entry("ibm", "Gold 64", "mswin",   "", {"6month":{"hourly":0.550, "upfront":1850}, "12month":{"hourly":0.550, "upfront":1300}} )
dobj["ibm_usd"].entry("ibm", "Gold 64", "linux",   "", {"6month":{"hourly":0.320, "upfront":1850}, "12month":{"hourly":0.320, "upfront":1300}} )

dobj["ibm_usd"].entry("ibm", "Platinum 64", "rhel",    "", {"6month":{"hourly":0.720, "upfront":1850}, "12month":{"hourly":0.720, "upfront":1300}} )
dobj["ibm_usd"].entry("ibm", "Platinum 64", "sles",    "", {"6month":{"hourly":0.650, "upfront":1850}, "12month":{"hourly":0.650, "upfront":1300}} )
dobj["ibm_usd"].entry("ibm", "Platinum 64", "mswin",   "", {"6month":{"hourly":1.250, "upfront":1850}, "12month":{"hourly":1.250, "upfront":1300}} )
dobj["ibm_usd"].entry("ibm", "Platinum 64", "linux",   "", {"6month":{"hourly":0.630, "upfront":1850}, "12month":{"hourly":0.630, "upfront":1300}} )

dobj["ibm_usd"].entry("ibm", "Copper 32", "rhel",  "", {"ondemand":{"hourly":0.125, "upfront":None}} )
dobj["ibm_usd"].entry("ibm", "Copper 32", "sles",  "", {"ondemand":{"hourly":0.095, "upfront":None}} )
dobj["ibm_usd"].entry("ibm", "Copper 32", "mswin", "", {"ondemand":{"hourly":0.100, "upfront":None}} )
dobj["ibm_usd"].entry("ibm", "Copper 32", "linux", "", {"ondemand":{"hourly":0.075, "upfront":None}} )

dobj["ibm_usd"].entry("ibm", "Bronze 32", "rhel",  "", {"ondemand":{"hourly":0.145, "upfront":None}} )
dobj["ibm_usd"].entry("ibm", "Bronze 32", "sles",  "", {"ondemand":{"hourly":0.115, "upfront":None}} )
dobj["ibm_usd"].entry("ibm", "Bronze 32", "mswin", "", {"ondemand":{"hourly":0.120, "upfront":None}} )
dobj["ibm_usd"].entry("ibm", "Bronze 32", "linux", "", {"ondemand":{"hourly":0.095, "upfront":None}} )

dobj["ibm_usd"].entry("ibm", "Silver 32", "rhel",  "", {"ondemand":{"hourly":0.230, "upfront":None}} )
dobj["ibm_usd"].entry("ibm", "Silver 32", "sles",  "", {"ondemand":{"hourly":0.200, "upfront":None}} )
dobj["ibm_usd"].entry("ibm", "Silver 32", "mswin", "", {"ondemand":{"hourly":0.240, "upfront":None}} )
dobj["ibm_usd"].entry("ibm", "Silver 32", "linux", "", {"ondemand":{"hourly":0.180, "upfront":None}} )

dobj["ibm_usd"].entry("ibm", "Gold 32", "rhel",    "", {"ondemand":{"hourly":0.360, "upfront":None}} )
dobj["ibm_usd"].entry("ibm", "Gold 32", "sles",    "", {"ondemand":{"hourly":0.330, "upfront":None}} )
dobj["ibm_usd"].entry("ibm", "Gold 32", "mswin",   "", {"ondemand":{"hourly":0.370, "upfront":None}} )
dobj["ibm_usd"].entry("ibm", "Gold 32", "linux",   "", {"ondemand":{"hourly":0.310, "upfront":None}} )

dobj["ibm_usd"].entry("ibm", "Copper 64", "rhel",  "", {"ondemand":{"hourly":0.300, "upfront":None}} )
dobj["ibm_usd"].entry("ibm", "Copper 64", "sles",  "", {"ondemand":{"hourly":0.270, "upfront":None}} )
dobj["ibm_usd"].entry("ibm", "Copper 64", "mswin", "", {"ondemand":{"hourly":0.340, "upfront":None}} )
dobj["ibm_usd"].entry("ibm", "Copper 64", "linux", "", {"ondemand":{"hourly":0.250, "upfront":None}} )

dobj["ibm_usd"].entry("ibm", "Bronze 64", "rhel",  "", {"ondemand":{"hourly":0.400, "upfront":None}} )
dobj["ibm_usd"].entry("ibm", "Bronze 64", "sles",  "", {"ondemand":{"hourly":0.370, "upfront":None}} )
dobj["ibm_usd"].entry("ibm", "Bronze 64", "mswin", "", {"ondemand":{"hourly":0.400, "upfront":None}} )
dobj["ibm_usd"].entry("ibm", "Bronze 64", "linux", "", {"ondemand":{"hourly":0.350, "upfront":None}} )

dobj["ibm_usd"].entry("ibm", "Silver 64", "rhel",  "", {"ondemand":{"hourly":0.480, "upfront":None}} )
dobj["ibm_usd"].entry("ibm", "Silver 64", "sles",  "", {"ondemand":{"hourly":0.450, "upfront":None}} )
dobj["ibm_usd"].entry("ibm", "Silver 64", "mswin", "", {"ondemand":{"hourly":0.500, "upfront":None}} )
dobj["ibm_usd"].entry("ibm", "Silver 64", "linux", "", {"ondemand":{"hourly":0.430, "upfront":None}} )

dobj["ibm_usd"].entry("ibm", "Gold 64", "rhel",    "", {"ondemand":{"hourly":0.740, "upfront":None}} )
dobj["ibm_usd"].entry("ibm", "Gold 64", "sles",    "", {"ondemand":{"hourly":0.710, "upfront":None}} )
dobj["ibm_usd"].entry("ibm", "Gold 64", "mswin",   "", {"ondemand":{"hourly":0.960, "upfront":None}} )
dobj["ibm_usd"].entry("ibm", "Gold 64", "linux",   "", {"ondemand":{"hourly":0.690, "upfront":None}} )

dobj["ibm_usd"].entry("ibm", "Platinum 64", "rhel",    "", {"ondemand":{"hourly":1.460, "upfront":None}} )
dobj["ibm_usd"].entry("ibm", "Platinum 64", "sles",    "", {"ondemand":{"hourly":1.390, "upfront":None}} )
dobj["ibm_usd"].entry("ibm", "Platinum 64", "mswin",   "", {"ondemand":{"hourly":1.990, "upfront":None}} )
dobj["ibm_usd"].entry("ibm", "Platinum 64", "linux",   "", {"ondemand":{"hourly":1.370, "upfront":None}} )

dobj["gigas"] = pricingData("Gigas", "Cloud DC", "EUR", "20120831")

dobj["gigas"].entry("mad-interxion", "DC 1 giga",  "", "", {"1month":{"hourly":0.0, "upfront":59}} )
dobj["gigas"].entry("mad-interxion", "DC 2 gigas", "", "", {"1month":{"hourly":0.0, "upfront":99}} )
dobj["gigas"].entry("mad-interxion", "DC 4 gigas", "", "", {"1month":{"hourly":0.0, "upfront":179}} )
dobj["gigas"].entry("mad-interxion", "DC 6 gigas", "", "", {"1month":{"hourly":0.0, "upfront":259}} )
dobj["gigas"].entry("mad-interxion", "DC 8 gigas", "", "", {"1month":{"hourly":0.0, "upfront":349}} )
dobj["gigas"].entry("mad-interxion", "DC 12 gigas", "", "", {"1month":{"hourly":0.0, "upfront":499}} )
dobj["gigas"].entry("mad-interxion", "DC 16 gigas", "", "", {"1month":{"hourly":0.0, "upfront":649}} )
dobj["gigas"].entry("mad-interxion", "DC 32 gigas", "", "", {"1month":{"hourly":0.0, "upfront":1099}} )
dobj["gigas"].entry("mad-interxion", "DC 64 gigas", "", "", {"1month":{"hourly":0.0, "upfront":1899}} )
dobj["gigas"].entry("mad-interxion", "DC 96 gigas", "", "", {"1month":{"hourly":0.0, "upfront":2499}} )

