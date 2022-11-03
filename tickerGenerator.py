import yahoo_fin.stock_info as si 
tickers = set()
# tickers_dow
# tickers_ftse100
# tickers_ftse250
# tickers_ibovespa
# tickers_nasdaq
# tickers_nifty50
# tickers_niftybank
# tickers_other
# tickers_sp500


f = open("tickers.txt", "a")
# f.write("dow\n")
for t in si.tickers_dow():
    tickers.add(t)
    f.write(t + "\n")
# f.write("ftse250\n")
for t in si.tickers_ftse250():
    if(t not in tickers):
        f.write(t+"\n")
        tickers.add(t)
# f.write("ftse100\n")
for t in si.tickers_ftse100():
    if(t not in tickers):
        f.write(t+"\n")
        tickers.add(t)

# f.write("ibovespa\n")
for t in si.tickers_ibovespa(): 
    if(t not in tickers):
        f.write(t+"\n")
        tickers.add(t)

# f.write("nasdaq\n")
for t in si.tickers_nasdaq(): 
    if(t not in tickers):
        f.write(t+"\n")
        tickers.add(t)

# f.write("nifty50\n")
for t in si.tickers_nifty50(): 
    if(t not in tickers):
        f.write(t+"\n")
        tickers.add(t)

# f.write("niftybank\n")
for t in si.tickers_niftybank(): 
    if(t not in tickers):
        f.write(t+"\n")
        tickers.add(t)

# f.write("other\n")
for t in si.tickers_other(): 
    if(t not in tickers):
        f.write(t+"\n")
        tickers.add(t)

# f.write("sp500\n")
for t in si.tickers_sp500(): 
    if(t not in tickers):
        f.write(t+"\n")
        tickers.add(t)

f.close()

