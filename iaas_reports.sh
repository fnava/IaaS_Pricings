#!/bin/bash
python iaaspricing.py \
--filter-provider Amazon \
--filter-reserve ondemand \
--filter-os linux \
--filter-region us-east-1 \
-f awsgraph > graph_aws_ondemand.html

python iaaspricing.py \
--filter-currency EUR \
--filter-provider Amazon Google Microsoft Acens \
--filter-product AWS GCE Azure_VM Instant_Servers \
--filter-reserve ondemand \
--filter-os linux \
--filter-region us-east-1 us-east1-a ms-preview Madrid Interxion-Madrid acens Joyent \
-f scatter3d > graph_aws_scatter3d_vm.html

python iaaspricing.py \
--filter-currency EUR \
--filter-provider COLT Gigas Acens \
--filter-product vCloud_Essentials vCloud_Enterprise Cloud_Datacenter Cloud_Servers \
--filter-reserve ondemand \
--filter-os linux \
--filter-region us-east-1 us-east1-a ms-preview Madrid Interxion-Madrid acens Joyent \
-f scatter3d > graph_aws_scatter3d_dc.html

python iaaspricing.py \
--filter-currency EUR \
--filter-provider Amazon Gigas Acens  \
--filter-product AWS Cloud_Datacenter Cloud_Servers \
--filter-reserve ondemand \
--filter-os linux \
--filter-region us-east-1 us-east1-a ms-preview Madrid Interxion-Madrid acens Joyent \
-f scatter3d > graph_aws_scatter3d_vv.html
