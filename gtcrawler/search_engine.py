import json
from elasticsearch import Elasticsearch


def main():
    crawled_file = "crawled_data.json"
    with open(crawled_file, "r") as f:
        crawled_data = json.load(f)

    es = Elasticsearch("http://localhost:9200")
    print(es.info().body)


if __name__ == '__main__':
    main()


