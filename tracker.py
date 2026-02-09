import numpy as np
from matplotlib import dates
from datetime import datetime
from matplotlib import pyplot as plt
import csv
import std
import sys

ref_date = datetime(1970,1,1)

# obsolete function but useful
# def format_date(date):
#     return date.strftime("%d-%m-%y")

def get_data(file):
    #assumes file name format "PATH/gurken_STORE.csv" or "PATH/gurken.csv"
    store = file.split("gurken")[-1]
    try:
        _, store  = store.split("_")
        store, _ = store.split(".")
        #store = store.capitalize()
    except ValueError:
        store = "unspecified"

    try:
        with open(file) as file:
            f = csv.DictReader(file, delimiter=";")
            dates = []
            prices = []
            # assumes header row "date;price"
            for row in f:
                dates.append(row["date"])
                prices.append(row["price"].strip())
    except FileNotFoundError:
        sys.exit("cannot open file")

    prices = list(map(float,prices))

    # date parsing (version w/o dicts)
    diff_dates = []
    # assumes YYYY-MM-DD format for date input (possible separators: -, / or .)
    for x in range(len(dates)):
        if "-" in dates[x]:
            year,month,day = dates[x].split("-")
        elif "/" in dates[x]:
            year,month,day = dates[x].split("/")
        elif "." in dates[x]:
            year,month,day = dates[x].split(".")
        else:
            print("not a valid date format")
        instance_date = datetime(int(year),int(month),int(day))
        #convert date to number of days passed since reference date
        diff = instance_date - ref_date
        diff_dates.append(diff)
    return diff_dates, prices, store

def calc_index(diff_dates,prices,ref="1.19"):
    ref_price = float(ref) #arbitrarily set
    index_prices =[]
    for x in range(len(diff_dates)):
        proportion = prices[x] / ref_price
        index_prices.append(proportion)
    name = rf"index (normalized to {ref})"
    return diff_dates, index_prices, name

def plot_index(file,ref="1.19"):
    diff_dates, prices, store = get_data(file)
    diff_days, prices_indexed, name = calc_index(diff_dates, prices,ref)
    diff_days = ([x.days for x in diff_dates]) # list of timedelta objects

    #sorting data
    sorting_indices = np.argsort(diff_days)
    diff_days_sorted = [diff_days[x] for x in sorting_indices]
    prices_indexed_sorted = [prices_indexed[x] for x in sorting_indices]

    formatter = dates.DateFormatter('%d-%m-%Y')
    plt.plot(diff_days_sorted,prices_indexed_sorted, label=rf"{name} for {store}",linestyle="dotted",color="tab:green")
    plt.gca().xaxis.set_major_formatter(formatter)
    return



def plot_data(file, totalplots, subplot):
    diff_dates, prices, store = get_data(file)
    diff_days = ([x.days for x in diff_dates]) # list of timedelta objects, DO NOT attempt to work w diff_dates

    #sorting data
    sorting_indices = np.argsort(diff_days)
    diff_days_sorted = [diff_days[x] for x in sorting_indices]
    diff_dates_sorted = [diff_dates[x] for x in sorting_indices]
    prices_sorted = [prices[x] for x in sorting_indices]

    formatter = dates.DateFormatter('%d-%m-%Y')
    std.default.plt_pretty("date","unit price")
    plt.subplot(1, totalplots, subplot) # (1,1,1) for only one data file given
    plt.scatter(diff_days_sorted,prices_sorted, label=rf"{store}",marker="x",color="tab:green")

    plt.gca().xaxis.set_major_formatter(formatter)
    plt.gca().set_xticklabels("date",fontsize="small")
    return


# TO DO: display for multiple files in subfigures
#
# def subfigs(file1,file2):
#     plot_data(file1,2,1)
#     plot_data(file2,2,2)
#     return

def main():
    plot_data(sys.argv[1], 1, 1)
    plot_index(sys.argv[1])
    plt.legend(loc="best",fontsize='small')
    if len(sys.argv) > 3:
        plt.savefig(sys.argv[2])
    else:
        plt.show()
    return


if __name__ == "__main__":
    main()
