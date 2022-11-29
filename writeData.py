"""
Writes data for each ticker to a file
"""

import yahoo_fin.stock_info as si 
import math

# Used to write multiple tickers at a time to make less system calls 
toWrite = ""

startDate = "2021-01-01" 
endDate = "2021-12-31" 

# File that the ticker data will be written to 
writeToFile = open("newData.txt", "a")

"""
Gets the data for a single ticker and adds it to a string to write to a file 
Data features are: 
    - Percent Gain: gain in stock for the year 
        - Formula = (final price - start price) / (start price)
    - Percent Change Volatility: volatility of the daily percent change for the year 
        - Formula: 
             - each xi is the percent change in price for day i: xi = (high-low)/high
             - calculate mean = (x1 + x2 + x3 ... + xN) / N 
             - calculate each deviation from mean: (D1 = x1 - mean, D2 = x2 - mean ...)
             - Calculate the variance: S = (D1^2 + D2^2 + ... + DN^2)/(N-1)
             - Calculate the volatility = sqrt(S)    
"""
def getTickerStartDateData(t):
    data = si.get_data(t, start_date = startDate, end_date = endDate, index_as_date = True, interval="1d")
    highs = data.get("high")
    lows = data.get("low")
    # Find the percent gain for the year (the first feature)
    startDateOpen = data.get("open")[0]
    endDateClose = data.get("close")[-1]    
    percentGain = (endDateClose - startDateOpen) / startDateOpen 
    # Find the volatility of daily percent gain for the year (the second feature)
    percentChangeSum = 0 # Sum of the daily percent change for the year
    meanPercentChange = 0 # Mean daily percent change for the year
    N = 0 
    i = 0 
    deviations = [0] * len(data) # Stores the squared deviations in percent change for each day
    
    global toWrite
    for day in range(0, len(data)): 
        dailyPercentChange = (highs[day] - lows[day]) / highs[day] # The percent change in price for a single day 
        deviations[i] = dailyPercentChange 
        percentChangeSum += dailyPercentChange 
        N += 1 
        i += 1
    # Find the mean percent change for the year 
    meanPercentChange = percentChangeSum / N 
    # Calculate the deviations from the mean for each day 
    # Square each deviation 
    # Then add to sq_deviation_sum to find variance 
    sq_deviation_sum = 0
    variance = 0
    for j in range(0, len(deviations)): 
        deviations[j] = deviations[j] - meanPercentChange 
        sq_deviation_sum += math.pow(deviations[j], 2)
    variance = sq_deviation_sum / (N-1) 
    volatility = math.sqrt(variance)    
     
    toWrite += (str(t) + " " + str(percentGain) + " " + str(volatility) + "\n")
    
# For each ticker, get the data and write to a file
f = open("tickers.txt", 'r')
running = False
while True:
    if len(toWrite) > 10000: # Write once line is > 10000 characters (to make less write calls)
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
    if ticker == "DPCSU":
        running = True
    if ticker == "DWAS":
        #running = True
        break
print("writing")
copy = toWrite
writeToFile.write(copy)

f.close()
writeToFile.close()

