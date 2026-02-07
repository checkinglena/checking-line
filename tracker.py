import numpy as np
from matplotlib import dates
from datetime import datetime
import csv
from matplotlib import pyplot as plt
import std
from sys import argv


def get_data(file):
    with open(file) as file:
        f = csv.DictReader(file, delimiter=";")
        dates = []
        prices = []
        # assumes header row "date;price"
        for row in f:
            dates.append(row["date"])
            prices.append(row["price"].strip())

    prices = list(map(float,prices))
    # date parser
    #all_dates = {}
    ref_date = datetime(2025,12,1)
    diff_dates = []
    # assumes DD-MM-YYYY format for date input (possible separators: -, / or .)
    for x in range(len(dates)):

        if "-" in dates[x]:
            day,month,year = dates[x].split("-")
        elif "/" in dates[x]:
            day,month,year = dates[x].split("/")
        elif "." in dates[x]:
            day,month,year = dates[x].split(".")
        else:
            print("not a valid date format")
        #dict_date = {"day":int(day),"month":int(month),"year":int(year)}
        #all_dates.update({x: dict_date})
        instance_date = datetime(int(year),int(month),int(day))
        #convert date to number of days passed since reference date
        diff = instance_date - ref_date
        diff_dates.append(diff)

    diff_days = ([x.days for x in diff_dates])

    # year = all_dates[x]["day"]

    return diff_days, prices, dates

def plot_data(file):
    diff_days, prices, raw_dates = get_data(file)
    std.default.plt_pretty("days since 01-12-2025","unit price")
    plt.scatter(diff_days,prices)
    plt.show()



def main():
    plot_data(argv[1])
    return


if __name__ == "__main__":
    main()
