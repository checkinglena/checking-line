import numpy as np
from matplotlib import dates
from datetime import datetime
from matplotlib import pyplot as plt
import matplotlib.colors
import std
import sys
import csv

ref_date = datetime(1970,1,1)

# obsolete function but useful
# def format_date(date):
#     return date.strftime("%d-%m-%y")
#
#

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
    name = rf"(normalized to {ref})"
    return diff_dates, index_prices, name

def fit_polynomial(x,y, order):
    return np.polynomial.Polynomial.fit(x,y,deg=order,full=True)

def plot_index(file,ref="1.19",colorcoded=False):
    diff_dates, prices, store = get_data(file)
    diff_days, prices_indexed, name = calc_index(diff_dates, prices,ref)
    diff_days = ([x.days for x in diff_dates]) # list of timedelta objects


    #sorting data
    sorting_indices = np.argsort(diff_days)
    diff_days_sorted = [diff_days[x] for x in sorting_indices]
    diff_dates_sorted = [diff_dates[x] for x in sorting_indices]
    prices_indexed_sorted = [prices_indexed[x] for x in sorting_indices]
    prices_sorted = [prices[x] for x in sorting_indices]
    dates_sorted = [x+ref_date for x in diff_dates_sorted]

    #assigning seasonality
    seasonality = []
    if colorcoded is True:
        spring_date = datetime(year=2026,month=3,day=20)
        summer_date = datetime(2026,6,21)
        fall_date = datetime(2026,9,23)
        winter_date_25 = datetime(2025,12,21)
        winter_date_26 = datetime(2026,12,21)
        in_season = []
        for x in range(len(dates_sorted)):
            a = True if (winter_date_25 - dates_sorted[x]).days <= 0 else False
            b = True if (spring_date - dates_sorted[x]).days <= 0 else False
            c = True if (summer_date - dates_sorted[x]).days <= 0 else False
            d = True if (fall_date - dates_sorted[x]).days <= 0 else False
            e = True if (winter_date_26 - dates_sorted[x]).days <= 0 else False
            if c and not d: #summer
                in_season.append(1)
            else:
                in_season.append(0)
        seasonality = [prices_sorted[x] if in_season[x] == 0 else 1 for x in range(len(prices_indexed_sorted))]


    # fit polynomial
    order = len(diff_days_sorted) - 1
    polynomial, res = fit_polynomial(diff_days_sorted, prices_sorted, order)
    fit = polynomial.convert().coef
    fitted_poly = np.polynomial.polynomial.Polynomial(fit)
    #xrange = np.linspace(min(diff_days_sorted),max(diff_days_sorted),1000)
    xrange = np.linspace(min(diff_days_sorted),max(diff_days_sorted),1000)
    #plotting
    formatter = dates.DateFormatter('%d-%m-%Y')

    if colorcoded is True:
        plt.ylim(0.1)
        plt.scatter(diff_days,seasonality,color="red",marker=".",label=rf"in season")

    plt.plot(diff_days_sorted,prices_indexed_sorted, label=rf"index {name}",linestyle="dotted",color="tab:green")
    plt.plot(xrange,fitted_poly(xrange),color="tab:green",label=f"polynomial fit (order={order})")
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
    std.default.plt_pretty("sample date","unit price")
    plt.subplot(1, totalplots, subplot) # (1,1,1) for only one data file given
    plt.scatter(diff_days_sorted,prices_sorted, label=rf"{store}",marker="x",color="tab:green")

    plt.gca().xaxis.set_major_formatter(formatter)
    plt.gca().set_xticklabels("sample date",fontsize="small") #TO DO: needs a better solution w/o warning
    return


# TO DO: display for multiple files in subfigures
#
# def subfigs(file1,file2):
#     plot_data(file1,2,1)
#     plot_data(file2,2,2)
#     return

def main():
    plot_data(sys.argv[1], 1, 1)
    plot_index(sys.argv[1],colorcoded=True)
    plt.legend(loc="best",fontsize='small')
    if len(sys.argv) > 3:
        plt.savefig(sys.argv[2])
    else:
        plt.show()
    return


if __name__ == "__main__":
    main()
