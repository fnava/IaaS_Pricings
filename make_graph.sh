#!/bin/bash

python iaaspricing.py \
    --filter-provider Amazon \
    --filter-reserve ondemand \
    --filter-os linux \
    --filter-region us-east-1 \
    -f awsgraph > graph_aws_ondemand.html


