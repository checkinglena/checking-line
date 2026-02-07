import numpy as np
from matplotlib import dates
from datetime import datetime
import csv
from matplotlib import pyplot as plt
import std


def get_data(file):
    #converters = {0: lambda x: dates.datestr2num(str(x))}
    #day = datetime.strptime("01-01-2003", "%d-%m-%Y").strftime("%m-%d-%Y")

    with open(file) as file:
        f = csv.DictReader(file, delimiter=";")
        dates = []
        prices = []
        for row in f:
            dates.append(row["date"])
            prices.append(row[" price"].strip())

    # date parser
    #all_dates = {}
    ref_date = datetime(2025,12,1)
    diff_dates = []
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
        diff = instance_date - ref_date
        diff_dates.append(diff)

    diff_days = ([x.days for x in diff_dates])
    #print(diff_days)
    #
    #
    #convert date to number of days passed
    #reference date: 01-12-2025
    # year = all_dates[x]["day"]

    # datetime.datetime(year,month,day)

    # print(type(day))
    # dates, prices = np.transpose(
    #     np.loadtxt(
    #         file,
    #         delimiter=";",
    #         skiprows=1,
    #         converters=converters,
    #     )
    # )
    # print(dates, prices)
    return diff_days, prices, dates

def plot_data(file):
    diff_days, prices, raw_dates = get_data(file)
    std.default.plt_pretty("Tage seit 01.01.2025","Gurkenpreis")
    plt.scatter(diff_days,prices)
    plt.show()



def main():
    plot_data("./gurken.csv")
    return


if __name__ == "__main__":
    main()
