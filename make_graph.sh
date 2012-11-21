#!/bin/bash
python iaaspricing.py \
--filter-provider Amazon \
--filter-reserve ondemand \
--filter-os linux \
--filter-region us-east-1 \
-f awsgraph > graph_aws_ondemand.html

python iaaspricing.py \
--filter-provider Google Amazon \
--filter-reserve ondemand \
--filter-os linux \
--filter-region us-east-1 \
-f scatter3d > graph_aws_scatter3d.html
