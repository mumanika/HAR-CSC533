import csv
from matplotlib_venn import venn3
from matplotlib import pyplot as plt

def main(csv_file):

    f = open(csv_file, "r")
    csv_reader = csv.DictReader(f)

    countries = {}
    bw_dict = {}
    relay = []
    guard = []
    exit = []
    for row in csv_reader:
        if row["Country Code"] in countries.keys():
            countries[row["Country Code"]] += 1
        else:
            countries[row["Country Code"]] = 1

        bw_dict[row["IP Address"]] = [row["Router Name"], float(row["Bandwidth (KB/s)"])]


        if row["Flag - Guard"] == "1":
            guard.append(row["IP Address"])
        if row["Flag - Exit"] == "1":
            exit.append(row["IP Address"])
        if row["Flag - Guard"] == "0" and row["Flag - Exit"] == "1":
            relay.append(row["IP Address"])

    print("The top 5 countries that host the most number of Tor relays are:")
    print(sorted(countries.keys(), key= lambda x: countries[x], reverse=True)[:5])
    print("The top 5 relays that contribute bandwidth are:")
    relay_list = sorted(bw_dict.items(), key=lambda x: x[1][1], reverse=True)[:5]
    for i in relay_list:
        print("Name: {}\tIP Address: {}\tBandwidth: {}".format(i[1][0], i[0], i[1][1]))
    venn3([set(relay), set(guard), set(exit)], set_labels=("Middle Relays", "Guard Relays", "Exit Relays"))
    plt.title("Venn Diagram for Relay types")
    plt.show()
    f.close()

if __name__ == '__main__':
    file_name = "Tor_query_EXPORT-1.csv"
    main(file_name)