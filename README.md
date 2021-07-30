# Market_Limit_Orderbook

The limit order book refers to a system that matches orders on a price, then time, priority basis. Bids and offers are entered at desired price levels and matched off when an opposing order comes into the market at an equal or improved price. Normally, orders can be entered, cancelled or filled (matched off/traded).

This script reconstructs raw order data to reflect the state of an instruments' order book at any given specified point in time. As a trial attempt, the raw market operations have been implemented, although better data structures could improve the performance time of the script.


################################################################################################
INTRUCTIONS:
################################################################################################

(OPTION 1. Running using provided source excel sheet)

1. Install the 'Open Python Excel (openpyxl)' Package using PIP INSTALL
    In cmd command line: 'py -m pip install openpyxl'

2. Comment out line 45
3. Uncomment line 46
4 (Optional: Changing time of orderbook): On line 130, Input the desired end time you wish to 
    view the orderbook at (e.g. '3:00:00').
5. Save orderbook.py
6. Run orderbook.py, and a csv and json file of the open interest will be saved.

(OPTION 2. Running using formatted Quotes.csv)

1. Place 'Quotes.CSV in the same folder/path as orderbook.py
2. (Optional: Changing time of orderbook): On line 130, Input the desired end time you wish to 
    view the orderbook at (e.g. '3:00:00').
3. Save orderbook.py
4. Run orderbook.py, and a csv and json file of the open interest will be saved.


################################################################################################
