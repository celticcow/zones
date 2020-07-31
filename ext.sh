#!/usr/bin/bash

export http_proxy=""
export https_proxy=""

/home/gdunlap/zone_ext/extract.py -m 192.168.159.150 -c 192.168.159.151 -f adm1grp.csv > zonedata.csv
/home/gdunlap/zone_ext/extract.py -m 192.168.159.150 -c 192.168.159.155 -f adm5grp.csv >> zonedata.csv
/home/gdunlap/zone_ext/extract.py -m 192.168.159.150 -c 192.168.159.161 -f adm11grp.csv >> zonedata.csv
/home/gdunlap/zone_ext/extract.py -m 192.168.159.150 -c 192.168.159.167 -f adm17grp.csv >> zonedata.csv
/home/gdunlap/zone_ext/extract.py -m 204.135.121.150 -c 204.135.121.158 -f adm8grp.csv >> zonedata.csv

##