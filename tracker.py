from matplotlib import dates
from datetime import datetime
from matplotlib import pyplot as plt
import csv
import std
from sys import argv

ref_date = datetime(1970,1,1)

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
    #ref_date = datetime(2025,12,1)
    diff_dates = []
    instance_dates = []
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
        instance_dates.append(instance_date)
        diff_dates.append(diff)

    #diff_days = ([x.days for x in diff_dates])

    # year = all_dates[x]["day"]


    return diff_dates, prices

def format_date(date):
    return date.strftime("%d-%m-%y")



def plot_data(file):
    diff_dates, prices = get_data(file)
    diff_days = ([x.days for x in diff_dates]) # list of timedelta objects

    #formatted_inst_dates = list(map(format_date,inst_dates))
    #xvals = lambda x: [map(format_date,inst_dates[day]) for day in range(len(x))]

    formatter = dates.DateFormatter('%d-%m-%Y')

    std.default.plt_pretty("date","unit price")
    plt.scatter(diff_days,prices)
    plt.gca().xaxis.set_major_formatter(formatter)
    plt.show()



def main():
    plot_data(argv[1])
    return


if __name__ == "__main__":
    main()
