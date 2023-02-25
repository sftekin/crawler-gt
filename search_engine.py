import json
import time
from elasticsearch import Elasticsearch, exceptions
from cleantext import clean


def main():
    K = 800
    crawled_file = "crawled_data.json"
    with open(crawled_file, "r") as f:
        crawled_data = json.load(f)

    es = Elasticsearch("http://localhost:9200")
    print(es.info().body)

    mappings = {
        "properties": {
            "name": {"type": "text", "analyzer": "standard"},
            "title": {"type": "text", "analyzer": "english"},
            "research_area": {"type": "text", "analyzer": "standard"},
            "email": {"type": "text", "analyzer": "standard"},
            "bio_url": {"type": "keyword"},
            "bio": {"type": "text", "analyzer": "whitespace"}
        }
    }

    try:
        es.indices.create(index="faculty", mappings=mappings)
    except exceptions.RequestError as ex:
        if ex.error == 'resource_already_exists_exception':
            pass # Index already exists. Ignore.
        else: # Other exception - raise it
            raise ex

    print("Adding data to the index")
    start_time = time.time()
    success_idx = 0
    for i, sample in enumerate(crawled_data):
        if sample["name"] is None:
            continue
        content = None
        if "content" in sample.keys():
            content = sample["content"]["paragraph"] + " " + sample["content"]["span"]
        doc = {
            "name": clean(sample["name"].split(",")[0]),
            "title": sample["title"],
            "research_area": sample["research_area"],
            "email": get_contact(sample["contacts"], mode="email"),
            "bio_url": get_contact(sample["contacts"], mode="webpage"),
            "bio": content,
        }
        es.index(index="faculty", id=i, document=doc)
        success_idx += 1

        if success_idx > K:
            break
    creation_time = time.time() - start_time

    es.indices.refresh(index="faculty")
    print(es.cat.count(index="faculty", format="json"))

    print("Faculty has Machine Learning area but not a Ph.D. Student")
    start_time = time.time()
    resp = es.search(
        index="faculty",
        body={
            "query": {
                "bool": {
                    "must": {
                        "match_phrase": {
                            "research_area": "Machine Learning",
                        }
                    },
                    "filter": {"bool": {"must_not": {"match_phrase": {"title": "Ph.D. Student"}}}},
                },
            },
        }
    )
    resp_time = time.time() - start_time
    for hit in resp.body["hits"]["hits"]:
        print(hit["_source"]["name"])

    print(f"Creation took {creation_time:.4f}, Response took {resp_time:.4f}")

    es.indices.delete(index='faculty')


def get_contact(in_list, mode="email"):
    ret_val = None
    if len(in_list) == 0:
        return ret_val

    for c in in_list:
        if mode == "email" and "@" in c:
            ret_val = c
        elif mode == "webpage":
            ret_val = c
        else:
            pass
    return ret_val


if __name__ == '__main__':
    main()


