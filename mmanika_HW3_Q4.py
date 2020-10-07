import csv

def main(csv_file):

    f = open(csv_file, "r")
    csv_reader = csv.DictReader(f)

    countries = {}
    bw_dict = {}
    for row in csv_reader:
        if row["Country Code"] in countries.keys():
            countries[row["Country Code"]] += 1
        else:
            countries[row["Country Code"]] = 1

        bw_dict[row["Router Name"]] = float(row["Bandwidth (KB/s)"])


    print("The top 5 countries that host the most number of Tor relays are:")
    print(sorted(countries.keys(), key= lambda x: countries[x], reverse=True)[:5])
    print("The top 5 relay names that contribute bandwidth are:")
    print(sorted(bw_dict.keys(), key=lambda x: bw_dict[x], reverse=True)[:5])
    f.close()

if __name__ == '__main__':
    file_name = "Tor_query_EXPORT-1.csv"
    main(file_name)