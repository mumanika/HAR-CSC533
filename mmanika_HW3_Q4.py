import csv
from matplotlib_venn import venn3
from matplotlib import pyplot as plt
import hashlib
from prettytable import PrettyTable

def main(csv_file):

    f = open(csv_file, "r")
    csv_reader = csv.DictReader(f)
    countries = {}
    tor_relays = {}
    relay = []
    guard = []
    exit = []
    for row in csv_reader:
        if row["Country Code"] in countries.keys():
            countries[row["Country Code"]] += 1
        else:
            countries[row["Country Code"]] = 1
        tor_relays[hashlib.md5(str.encode(row["Router Name"]+row["Bandwidth (KB/s)"]+row["IP Address"]+row["Hostname"])).hexdigest()] = {
            "country": row["Country Code"],
            "bw": row["Bandwidth (KB/s)"],
            "ip": row["IP Address"],
            "hostname": row["Hostname"],
            "exit_relay": row["Flag - Exit"],
            "guard_relay": row["Flag - Guard"],
            "name": row["Router Name"]
        }
    f.close()
    stats = {
        "mid_bw": 0,
        "ex_only_bw": 0,
        "ex_guard_bw": 0,
        "guard_only_bw": 0
    }
    for key, value in tor_relays.items():
        if value["guard_relay"] == "0" and value["exit_relay"] == "0":
            relay.append(key)
            stats["mid_bw"] += float(value["bw"])
        elif value["exit_relay"] == "1" and value["guard_relay"] == "0":
            exit.append(key)
            stats["ex_only_bw"] += float(value["bw"])
        elif value["guard_relay"] == "1" and value["exit_relay"] == "1":
            exit.append(key)
            guard.append(key)
            stats["ex_guard_bw"] += float(value["bw"])
        else:
            guard.append(key)
            stats["guard_only_bw"] += float(value["bw"])
    print("The top 5 countries that host the most number of Tor relays are:")
    print(sorted(countries.keys(), key= lambda x: countries[x], reverse=True)[:5])
    print("The top 5 relays that contribute bandwidth are:")
    relay_list = sorted(tor_relays.values(), key= lambda x: float(x["bw"]), reverse=True)[:5]
    bw_table = PrettyTable()
    bw_table.field_names = ["Router Name", "Hostname", "IP Address", "Bandwidth"]
    for i in relay_list:
        bw_table.add_row([i["name"], i["hostname"], i["ip"], i["bw"]])
    print(bw_table)
    print("The bandwidth distribution in the venn groups of relays are as follows:")
    cum_bw_table = PrettyTable()
    cum_bw_table.title = "Cumulative Bandwidths Per group"
    cum_bw_table.field_names = ["Guard Relay Only BW (kbps)", "Middle Relay Only BW (kbps)",
                                "Exit Relay Only BW (kbps)", "Exit + Guard Relay BW (kbps)"]
    cum_bw_table.add_row([stats["guard_only_bw"], stats["mid_bw"], stats["ex_only_bw"], stats["ex_guard_bw"]])
    print(cum_bw_table)
    venn3([set(relay), set(guard), set(exit)], set_labels=("Middle Relays", "Guard Relays", "Exit Relays"))
    plt.title("Venn Diagram for Relay types")
    plt.show()

if __name__ == '__main__':
    file_name = "Tor_query_EXPORT-1.csv"
    main(file_name)