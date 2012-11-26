#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2012 Eran Sandler (eran@sandler.co.il),  http://eran.sandler.co.il,  http://forecastcloudy.net
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#

import argparse
try:
	import simplejson as json
except ImportError:
	import json
		
import locale

##import prov_all_pricedb, prov_all_historical
#import prov_aws_pricedb
from prov_aws_pricedb import EC2_INSTANCE_TYPES, EC2_OS_TYPES, EC2_REGIONS
##import prov_aws_historical
from prov_all_historical import *

##DATASETS = prov_all_pricedb.DATASETS[:]
#DATASETS+= prov_aws_pricedb.DATASETS[:]
##DATASETS+= prov_aws_historical.DATASETS[:]

#REGIONS = [
#	"us-east1-a","us-central1-a","us-central2-a",
#	"London","Paris","Frankfurt","Madrid",
#	"ms-preview","ms-ga",
#	"Interxion-Madrid",
#	"Joyent",
#	"acens"
#]
#REGIONS+= EC2_REGIONS[:]

#PROVIDERS = [
#	"Amazon",
#	"IBM",
#	"Google",
#	"COLT",
#	"Gigas",
#	"Microsoft",
#	"Joyent",
#	"Acens"
#]

RESERVATION = [
	"ondemand",
	"reserved"
	]

CURRENCIES = [
	"USD",
	"EUR"
	]
	
ONEUSDINEUR =  0.7758
	
if __name__ == "__main__":
	def none_as_string(v, currency="EUR"):
		if not v:
			return locale.str(0.0)
		else:
			return locale.str(v)

	try:
		import argparse 
	except ImportError:
		print "ERROR: You are running Python < 2.7. Please use pip to install argparse:   pip install argparse"


	parser = argparse.ArgumentParser(add_help=True, description="Print out the current prices of EC2 instances")
	parser.add_argument("--filter-currency", "-fc", help="Filter results to a specific currency", choices=CURRENCIES, default="EUR")
	parser.add_argument("--filter-region", "-fr", nargs="+", help="Filter results to a specific region", choices=REGIONS, default=None)
	parser.add_argument("--filter-type", "-ft", help="Filter results to a specific instance type", choices=EC2_INSTANCE_TYPES, default=None)
	parser.add_argument("--filter-os-type", "-fo", help="Filter results to a specific os type", choices=EC2_OS_TYPES, default=None)
	parser.add_argument("--filter-reserve", "-fv", help="Filter results to a specific reservation", choices=RESERVATION, default=None)
	parser.add_argument("--filter-provider", "-fp", nargs="+", help="Filter results to a specific provider", choices=PROVIDERS, default=None)
	parser.add_argument("--filter-product", "-fd", nargs="+", help="Filter results to a specific product", choices=PRODUCTS, default=None)
	parser.add_argument("--format", "-f", choices=["json", "table", "csv", "awsgraph", "scatter3d"], help="Output format", default="table")

	args = parser.parse_args()

	if args.format == "table":
		try:
			from prettytable import PrettyTable
		except ImportError:
			print "ERROR: Please install 'prettytable' using pip:    pip install prettytable"

	dataset = []
	get_pricing(dataset, args.filter_region, args.filter_type, args.filter_os_type, args.filter_provider, args.filter_product)
	#print dataset

	if args.format == "json":
		for data in dataset:
			print json.dumps(data, sort_keys=True, indent=4)

	elif args.format == "table":
		x = PrettyTable()
 		try:
			x.set_field_names(["date", "provider", "product", "region", "type", "os", "utilization", "term", "price", "upfront", "currency"])
		except AttributeError:
			x.field_names = ["date", "provider", "product", "region", "type", "os", "utilization", "term", "price", "upfront", "currency"]

		try:
			x.aligns[-1] = "l"
			x.aligns[-2] = "l"
		except AttributeError:
			x.align["price"] = "l"
			x.align["upfront"] = "l"
		
		for data in dataset:
			provider = data["config"]["provider"]
			product = data["config"]["product"]
			currency = data["config"]["currency"]
			date = data["config"]["date"]
			for r in data["regions"]:
				region_name = r["region"]
				for it in r["instanceTypes"]:
					for term in it["prices"]:
						hourly = it["prices"][term]["hourly"]
						upfront = it["prices"][term]["upfront"]
						if hourly is not None or upfront is not None:
							x.add_row([
								date,
								provider,
								product,
								region_name,
								it["type"],
								it["os"],
								it["utilization"],
								term,
								none_as_string(hourly),
								none_as_string(upfront),
								currency
							   ])
		print x
	elif args.format == "csv":
		locale.setlocale(locale.LC_ALL,"es_ES")
		print "date;provider;product;region;type;os;utilization;term;price;upfront;currency"
		for data in dataset:
		    provider = data["config"]["provider"]
		    product = data["config"]["product"]
		    currency = data["config"]["currency"]
		    date = data["config"]["date"]
		    for r in data["regions"]:
			region_name = r["region"]
			for it in r["instanceTypes"]:
				for term in it["prices"]:
					hourly = it["prices"][term]["hourly"]
					upfront = it["prices"][term]["upfront"]
					if hourly is not None or upfront is not None:							
						print "%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s" % (
									date,
									provider,
									product,
									region_name,
									it["type"],
									it["os"],
									it["utilization"],
									term,
									none_as_string(hourly),
									none_as_string(upfront),
									currency
									)
	elif args.format == "awsgraph":
		locale.setlocale(locale.LC_ALL,"C")
		print """<!--
You are free to copy and use this sample in accordance with the terms of the
Apache license (http://www.apache.org/licenses/LICENSE-2.0.html)
-->

<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<meta http-equiv="content-type" content="text/html; charset=utf-8" />
<title>Google Visualization API Sample</title>

<!-- Google graph motion chart -->
<script type="text/javascript" src="http://www.google.com/jsapi"></script>
<script type="text/javascript">
google.load('visualization', '1', {packages: ['motionchart']});

		function drawVisualization() {
var data = new google.visualization.DataTable();
"""
		for h,t in [
			("string","Type"),
			("date", "Date"),
			("number","Price"),
			("number",mem_key),
			("number",cpu_key),
			("number",sto_key),
			("string",iop_key),
			("string","Family"),
			]:
			print "data.addColumn('%s', '%s');" % (h, t)
		print "data.addRows(["
		for data in dataset:
			provider = data["config"]["provider"]
			product = data["config"]["product"]
			currency = data["config"]["currency"]
			date = data["config"]["date"]	
			for r in data["regions"]:
				region_name = r["region"]
				for it in r["instanceTypes"]:
					for term in it["prices"]:
						hourly = it["prices"][term]["hourly"]
						upfront = it["prices"][term]["upfront"]
						if hourly is not None or upfront is not None:							
							print "['%s', new Date(%s,%s,%s), %s, %s, %s, %s, '%s', '%s']," % (
										it["type"],
										date[:4], date[4:6], date[6:], 
										none_as_string(hourly),
										none_as_string(features[it["type"]][mem_key]),
										none_as_string(features[it["type"]][cpu_key]),
										none_as_string(features[it["type"]][sto_key]),
										features[it["type"]][iop_key],
										it["type"].split('.')[0]
										)
		print "]);"
		print """
var motionchart = new google.visualization.MotionChart(
document.getElementById('visualization'));
motionchart.draw(data, {'width': 800,
'height': 600,
'state':'{"yZoomedDataMax":68.4,"iconType":"BUBBLE","dimensions":{"iconDimensions":["dim0"]},"showTrails":true,"yLambda":0,"orderedByX":false,"iconKeySettings":[],"playDuration":15000,"xZoomedDataMin":1.2,"colorOption":"7","yZoomedIn":false,"sizeOption":"2","orderedByY":false,"xLambda":0,"xZoomedIn":false,"duration":{"timeUnit":"D","multiplier":1},"xZoomedDataMax":105.6,"xAxisOption":"4","time":"2012-12-01","yAxisOption":"3","uniColorForNonSelected":false,"yZoomedDataMin":0.613,"nonSelectedAlpha":0.4}'
});
}
google.setOnLoadCallback(drawVisualization);
</script>
</head>

<body onload="showDemo();" style="cursor: default;">
<body style="font-family: Arial;border: 0 none;">

<div id="visualization" style="width: 800px; height: 600px;">
</div>
</body>
</html>
"""
	elif args.format == "scatter3d":
		locale.setlocale(locale.LC_ALL,"C")
		print """<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
<!-- saved from url=(0042)http://www.canvasxpress.org/scatter3d.html -->
<html><head><meta http-equiv="Content-Type" content="text/html; charset=UTF-8">

    <title>Scatter3d</title>

    <meta http-equiv="X-UA-Compatible" content="chrome=1">
    <meta http-equiv="CACHE-CONTROL" content="NO-CACHE">
    
    <meta name="keywords" content="canvasxpress, canvas, html5, graph, chart, plot, javascript, javascript library, genomic, scientific, android, animation, bar graph, line graph, dotplot, boxplot, heatmap, newick, scatter, 3d, pie, correlation, venn, network, market, candlestick, genome browser, isaac neuhaus">
    <meta name="description" content="">
    <meta http-equiv="Content-Language" content="en-us">
    <meta name="Rating" content="general">
    <meta name="googlebot" content="index,follow">
    <meta name="robots" content="index,follow">
    <meta name="author" content="Fortunato Navarro">
    
<!-- http://www.canvasxpress.org 3D scatter plot -->
 <!--[if IE]><script type="text/javascript" src="./js/excanvas.js"></script><![endif]-->
 <!--[if IE]><script type="text/javascript" src="./js/extext.js"></script><![endif]-->
 <script type="text/javascript" async="" src="http://canvasxpress.org/js/ga.js">
 </script><script type="text/javascript" src="http://canvasxpress.org/js/canvasXpress.min.js"></script>
  <script>
      var showDemo = function () {
        new CanvasXpress("canvas", 
""",
	# Generation of canvasxpress scatter3d plot data and config, see:
	# http://www.canvasxpress.org/documentation.html
	# http://www.canvasxpress.org/scatter3d.html
	# Config samples taken from:
	# http://mauryacravings.com/labs/java%20controls/graphs&charts/graph_5/canvasxpress/scatter3d.html
		cx = {
			"y":{
				"vars":[],
				"smps":["Mem (GB)", "CPU (GHz)", "Storage (100xGB)", "Price (USD/h)"],
				"desc":["intensity",],
				"data":[]
			},
			"z":{
				"Provider":[],
				"Product":[]	
				},
		}
		for data in dataset:
			date = data["config"]["date"]	
			if data["config"]["latest"]:
				provider = data["config"]["provider"]
				product = data["config"]["product"]
				currency = data["config"]["currency"]
				for r in data["regions"]:
					region_name = r["region"]
					for it in r["instanceTypes"]:
						if region_name in args.filter_region and it["os"] == args.filter_os_type:
							for term in it["prices"]:
								hourly = it["prices"][term]["hourly"]
								upfront = it["prices"][term]["upfront"]
								price = hourly
								if args.filter_currency == "EUR":
									if currency == "USD":
										price = hourly * ONEUSDINEUR
								else:
									if currency == "EUR":
										price = hourly / ONEUSDINEUR
								if hourly is not None or upfront is not None:							
									datal = [
										features[it["type"]][mem_key],
										features[it["type"]][cpu_key],
										1000+100*features[it["type"]][sto_key],
										price
										]
									cx["y"]["data"].append(datal)
									cx["y"]["vars"].append(it["type"])
									cx["z"]["Product"].append(product)
									cx["z"]["Provider"].append(provider)
		print json.dumps(cx, sort_keys=True, indent=4),
	print """,
        {
        "graphType": "Scatter3D",
        "zAxis": ["Mem (GB)"],
	"yAxis": ["Price (USD/h)"],
	"xAxis": ["CPU (GHz)"],
	"sizeBy": "Storage (100xGB)",
	"colorBy" : "Provider",
	"shapeBy" : "Product",
        "transformType": "log2",
        "scatterType": false
	}
        )
    }
</script>
</head>

<body onload="showDemo();" style="cursor: default;">
<div>
<canvas id="canvas" width="1000" height="700"></canvas>
</div>
</body>

</html>
"""
