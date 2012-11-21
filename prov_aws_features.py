import csv
import locale
locale.setlocale(locale.LC_ALL,"es_ES")

features = {}

for provider in ["amazon","google"]:
    reader = csv.DictReader(open('provs/%s/features.csv' % provider), delimiter=';')
    keyword_key="Keyword"
    mem_key = "Mem (GB)"
    cpu_key = "CPU (GHz)"
    sto_key = "Storage (GB)"
    iop_key = "I/O Perf"
    for row in reader:
        features[row[keyword_key]] = {}
        for k in mem_key, cpu_key, sto_key:
            features[row[keyword_key]][k] = locale.atof(row[k])
        for k in [iop_key, ]:
            features[row[keyword_key]][k] = row[k].strip()

#print features