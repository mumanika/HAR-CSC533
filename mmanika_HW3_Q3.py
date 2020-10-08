
import json
from tld import get_fld
from adblockparser import AdblockRules
from prettytable import PrettyTable
from urllib.parse import urlparse


def main(harfile_path, domain, blockfile):
    harfile = open(harfile_path, "r")
    harfile_json = json.loads(harfile.read())
    harfile.close()
    bfile = open(blockfile, "r")
    block_list = bfile.readlines()
    bfile.close()
    rules = AdblockRules(block_list)
    adblock_db = {
        "url_data": {},
        "stats": {
            "domain": domain,
            "req": 0,
            "succ": 0,
            "block": 0
        }
    }
    options = ('image', 'xmlhttprequest', 'document', 'font', 'script', 'stylesheet', 'other')
    for entry in harfile_json['log']['entries']:
        url = entry['request']['url']
        urlparts = urlparse(url)
        print("Processing {} ...".format(url))
        try:
            fld = get_fld(url, fail_silently=True)
            adblock_db["stats"]["req"] += 1
            if fld != domain:
                d = {}
                if entry["_resourceType"] == "xhr":
                    entry["_resourceType"] = "xmlhttprequest"
                if entry["_resourceType"] not in options:
                    d = {"third-party": True, "domain": urlparts.hostname}
                else:
                    d = {entry["_resourceType"]: True, "third-party": True, "domain": urlparts.hostname}

                if rules.should_block(url, d):
                    adblock_db["stats"]["block"] += 1
                else:
                    adblock_db["stats"]["succ"] += 1
            else:
                if entry["_resourceType"] == "xhr":
                    entry["_resourceType"] = "xmlhttprequest"
                if entry["_resourceType"] not in options:
                    d = {"third-party": False, "domain": urlparts.hostname}
                else:
                    d = {entry["_resourceType"]: True, "third-party": False, "domain": urlparts.hostname}

                if rules.should_block(url, d):
                    adblock_db["stats"]["block"] += 1
                else:
                    adblock_db["stats"]["succ"] += 1
        except:
            continue
    return adblock_db

if __name__ == '__main__':
    file1 = "www.cnn.com.har"
    file2 = "www.macys.com.har"
    adblock_rules_file = "easylist.txt"
    result1 = main(file1, "cnn.com", adblock_rules_file)
    result2 = main(file2, "macys.com", adblock_rules_file)
    result_table = PrettyTable()
    result_table.field_names = ["Site", "# of total HTTP Requests", "# of HTTP Requests Blocked"]
    result_table.add_row(["www.cnn.com", result1["stats"]["req"], result1["stats"]["block"]])
    result_table.add_row(["www.macys.com", result2["stats"]["req"], result2["stats"]["block"]])
    print(result_table)
