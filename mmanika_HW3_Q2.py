
import json
from tld import get_fld
from matplotlib_venn import venn2
from matplotlib import pyplot as plt
from prettytable import PrettyTable

def main(harfile_path, domain):
    """Reads a har file from the filesystem, converts to CSV, then dumps to
    stdout.
    """
    harfile = open(harfile_path, "r")
    harfile_json = json.loads(harfile.read())
    harfile.close()
    third_party = {
        "url_data": {},
        "stats": {}
    }
    for entry in harfile_json['log']['entries']:
        url = entry['request']['url']
        try:
            fld = get_fld(url)
            if fld != domain:
                if fld in third_party["url_data"].keys():
                    third_party["url_data"][fld] += 1
                else:
                    third_party["url_data"][fld] = 1
        except:
            continue
    return third_party

if __name__ == '__main__':
    file1 = "www.cnn.com.har"
    file2 = "www.macys.com.har"
    result1 = main(file1, "cnn.com")
    result2 = main(file2, "macys.com")
    print("The total number of third party domains for file {} is {}".format(file1, len(result1["url_data"].keys())))
    result1_table = PrettyTable()
    result1_table.field_names = ["Domains"]
    for i in result1["url_data"].keys():
        result1_table.add_row([i])
    print(result1_table)
    print("The total number of third party domains for file {} is {}".format(file2, len(result2["url_data"].keys())))
    result2_table = PrettyTable()
    result2_table.field_names = ["Domains"]
    for i in result2["url_data"].keys():
        result2_table.add_row([i])
    print(result2_table)
    count = 0
    print("The third party domains that are common among the two sites are listed below.")
    common_domains_table = PrettyTable()
    common_domains_table.field_names = ["Serial", "Domain"]
    for key in result1["url_data"].keys():
        if key in result2["url_data"].keys():
            count += 1
            common_domains_table.add_row([count, key])
    print(common_domains_table)

    venn2(subsets=(len(result1["url_data"].keys())-count, len(result2["url_data"].keys())-count, count), set_labels=("cnn.com", "macys.com"), set_colors=('purple', 'skyblue'), alpha=0.7)
    plt.title("Venn Diagram for Third-Party Domains")
    plt.show()
