import datetime

def datePicker(date):
    if (date=="today"):
        date = thisDay()
    elif (date=="week"):
        date = thisWeek()
    elif (date=="month"):
        date = thisMonth()
    elif (date=="year"):
        date = thisYear()
    elif (date=="lastmonth"):
        date = lastMonth()
    elif (date=="1stquarter"):
        date = firstQuarter()
    elif (date=="2ndquarter"):
        date = secondQuarter()
    elif (date=="3rdquarter"):
        date = thirdQuarter()
    elif (date=="4thquarter"):
        date = fourthQuarter()
    else:
        try:
            customdate = date.split("-")
            date = [datetime.datetime.strptime(customdate[0], "%m/%d/%Y").strftime("%Y-%m-%d"),datetime.datetime.strptime(customdate[1], "%m/%d/%Y").strftime("%Y-%m-%d")]
        except:
            date = [datetime.datetime.strptime(customdate[0], "%m/%d/%Y").strftime("%Y-%m-%d")]
    return date

def summaryPicker(date):
    if(date==""):
        summary = "All Time"
    elif (date=="today"):
        summary = "Today's"
    elif (date=="week"):
        summary = "This Week's"
    elif (date=="month"):
        summary = "This Month's"
    elif (date=="year"):
        summary = "This Year's"
    elif (date=="lastmonth"):
        summary = "Last Month's"
    elif (date=="1stquarter"):
        summary = "1st Quarter's"
    elif (date=="2ndquarter"):
        summary = "2nd Quarter's"
    elif (date=="3rdquarter"):
        summary = "3rd Quarter's"
    elif (date=="4thquarter"):
        summary = "4th Quarter's"
    else:
        custom = date.split("-")
        summary = "["+str(custom[0]) + " - " + str(custom[1]) + "] Custom"
    return summary

def thisDay():
    day = datetime.date.today()
    return([str(day)])

def thisMonth():
    month1 = datetime.date.today()
    month0 = month1.replace(day=1)
    return([str(month0),str(month1 + datetime.timedelta(days=1))])

def thisWeek():
    week1 = datetime.date.today()
    lastMonth = week1 - datetime.timedelta(days=7)
    week0 = lastMonth.strftime("%Y-%m-%d")
    return([str(week0),str(week1 + datetime.timedelta(days=1))])

def thisYear():
    year1 = datetime.date.today() + datetime.timedelta(days=1)
    year0 = year1.replace(day=1,month=1)
    return([str(year0),str(year1)])

def lastMonth():
    today = datetime.date.today()
    first = today.replace(day=1)
    lastMonth = first - datetime.timedelta(days=1)
    dateLastMonth1 = lastMonth.strftime("%Y-%m-%d")
    a = dateLastMonth1.split("-")
    dateLastMonth0 = a[0] + "-" + a[1] + "-" + "1"
    return([str(dateLastMonth0),str(today.replace(day=1))])

def firstQuarter():
    now = datetime.datetime.now()
    return([str(now.year)+"-1-1",str(now.year)+"-4-1"])

def secondQuarter():
    now = datetime.datetime.now()
    return([str(now.year)+"-4-1",str(now.year)+"-7-1"])

def thirdQuarter():
    now = datetime.datetime.now()
    return([str(now.year)+"-7-1",str(now.year)+"-10-1"])

def fourthQuarter():
    now = datetime.datetime.now()
    return([str(now.year)+"-10-1",str(int(now.year)+1)+"-1-1"])
