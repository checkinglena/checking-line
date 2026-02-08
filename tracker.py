from matplotlib import dates
from datetime import datetime
from matplotlib import pyplot as plt
import csv
import std
from sys import argv

ref_date = datetime(1970,1,1)

# obsolete function but useful
# def format_date(date):
#     return date.strftime("%d-%m-%y")

def get_data(file):
    #assumes file name format "gurken_STORE.csv"
    _, store = file.split("_")
    store, _ = store.split(".")
    store = store.capitalize()

    with open(file) as file:
        f = csv.DictReader(file, delimiter=";")
        dates = []
        prices = []
        # assumes header row "date;price"
        for row in f:
            dates.append(row["date"])
            prices.append(row["price"].strip())
    prices = list(map(float,prices))

    # date parsing (version w/o dicts)
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
        instance_date = datetime(int(year),int(month),int(day))
        #convert date to number of days passed since reference date
        diff = instance_date - ref_date
        diff_dates.append(diff)

    return diff_dates, prices, store

def plot_data(file, subplot):
    diff_dates, prices, store = get_data(file)
    diff_days = ([x.days for x in diff_dates]) # list of timedelta objects, DO NOT attempt to work w diff_dates
    formatter = dates.DateFormatter('%d-%m-%Y')


    std.default.plt_pretty("date","unit price")
    plt.subplot(1, 1, subplot)
    plt.scatter(diff_days,prices, label=rf"{store}")
    plt.gca().xaxis.set_major_formatter(formatter)
    plt.legend()

def subfigs(file1,file2):

    plot_data(file1,1)


    if len(argv) > 3:
        plt.savefig(argv[3])
    else:
        plt.show()
    return

def main():
    subfigs(argv[1],argv[2])
    return


if __name__ == "__main__":
    main()
