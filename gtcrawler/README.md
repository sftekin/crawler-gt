# Requirements
platforms:
- docker
- conda

Packages:
- scrapy
- elasticsearch
- cleantext
- pandas
- matplotlib

# Installation
Install the packages
```
$ pip install -r requirements.txt
```

# Running
## Crawler
make sure you are in at the `./gtcrawler` directory, then run
```
$ scrapy crawl gts -o crawl_output.json
```
this will save the data in `crawl_output.json` and also output `stats.csv` for the statistics.

to perform analysis run
```
$ python analyze_crawler.py
```
this will output `crawler_analysis.png`

## Search Engine
run the following command to initialize local elasticsearch cluster
```
$ docker run --rm -p 9200:9200 -p 9300:9300 -e "xpack.security.enabled=false" -e "discovery.type=single-node" docker.elastic.co/elasticsearch/elasticsearch:8.3.3
```
then run the search engine
```
$ python search_engine.py
```
to perform analysis run
```
$ python analyze_se.py
```