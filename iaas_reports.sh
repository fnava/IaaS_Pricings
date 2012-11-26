#!/bin/bash
python iaaspricing.py \
--filter-provider Amazon \
--filter-reserve ondemand \
--filter-os linux \
--filter-region us-east-1 \
-f awsgraph > graph_aws_ondemand.html

python iaaspricing.py \
--filter-currency EUR \
--filter-provider Amazon Google Microsoft COLT Gigas Acens \
--filter-reserve ondemand \
--filter-os linux \
--filter-region us-east-1 us-east1-a ms-preview Madrid Interxion-Madrid acens Joyent \
-f scatter3d > graph_aws_scatter3d.html
