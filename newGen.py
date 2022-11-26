import yahoo_fin.stock_info as si 

toWrite = ""

startDate = "2021-01-01"
endDate = "2021-12-31"

writeToFile = open("data2021.txt", "a")

def getTickerStartDateData(t):
    data = si.get_data(t, start_date = startDate, end_date = endDate, index_as_date = True, interval="1d")
    highs = data.get("high")
    lows = data.get("low")
    startDateOpen = data.get("open")[0]
    endDateClose = data.get("close")[-1]
    percentGain = (endDateClose - startDateOpen) / startDateOpen
    variance = 0
    global toWrite
    for day in range(0, len(data)):
        dayPercentVar = (highs[day] - lows[day]) / highs[day]
        variance += dayPercentVar
    toWrite += (str(t) + " " + str(percentGain) + " " + str(variance) + "\n")
    


f = open("tickers.txt", 'r')
running = False
while True:
    if len(toWrite) > 10000:
        print("writing")
        copy = toWrite
        writeToFile.write(copy)
        toWrite = ""
    ticker = f.readline().strip()
    if running:
        if not ticker:
            break
        try:
            getTickerStartDateData(ticker)
        except:
            continue


    if ticker == "DWAS":
        running = True

    
f.close()
writeToFile.close()