'''(C) Copyright 2021 Konstantine Huffman. 
This code was written and compiled solely using my own resources and relavent documentation.
Not for redistribution.

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
'''

import pandas as pd
import json
import openpyxl

class OrderBook():

    def __init__(self, Orderbook_time):
        self.Orderbook_time = Orderbook_time
        ######################################
        #               Configure            #
        ######################################

        self.read_csv()
        #self.read_excel()
        
        ######################################
        self.construct_orderbook()
        self.save_csv()
        self.save_json()

    def read_csv(self):
        #excel save as csv plain. hh:mm:ss.000 format only
        self.Quotes = pd.read_csv("Quotes.csv", index_col='RemoteTime')
        self.Quotes.index = pd.to_datetime(self.Quotes.index, format='%H:%M:%S.%f')
        self.Quotes = self.Quotes.between_time('2:00:00', self.Orderbook_time)
        del self.Quotes['Unnamed: 5']
        del self.Quotes['Unnamed: 6']

    def read_excel(self):
        self.Quotes = pd.read_excel("CAC.xlsx", sheet_name="Quote Data", index_col='RemoteTime',engine="openpyxl")
        self.Quotes = self.Quotes.between_time('2:00:00', self.Orderbook_time)
        del self.Quotes['Unnamed: 5']
        del self.Quotes['Unnamed: 6']

    def construct_orderbook(self):
        self.orderbook = {}
        Price = self.Quotes['Price']
        self.PriceMax = Price.max()
        self.PriceMin = Price.min()

        for i in range(0, int((self.PriceMax - self.PriceMin)/0.5)+1):
            self.orderbook[self.PriceMin+(i/2)] = {'bid':0,'ask':0}

        #for each new trade, update the orderbook
        for index, row in self.Quotes.iterrows():
            if (row['BidOffer'] == 'B') :
                BidOffer = 'bid'
            else:
                BidOffer = 'ask'
            self.orderbook[row['Price']][BidOffer] += row['Quantity']
            self.process_trades()
        
        #Formatting & Printing
        self.OrderVis = pd.DataFrame.from_dict(self.orderbook).transpose()
        print(self.orderbook)
        print(self.OrderVis)


    def process_trades(self):
        for i in range(0, int((self.PriceMax - self.PriceMin)/0.5)+1):
            if (self.orderbook[self.PriceMin+(i/2)]['ask'] != 0):
                level1_ask = self.PriceMin+(i/2)
            else:
                 level1_ask = 100000

            for i in range(0, int((self.PriceMax - self.PriceMin)/0.5)+1):
                if (self.orderbook[self.PriceMax-(i/2)]['bid'] != 0):
                    level1_bid = self.PriceMax-(i/2)
                else:
                    level1_bid = 0

                if (level1_bid >= level1_ask) :
                    while(( self.orderbook[level1_ask]['ask'] > 0) and (self.orderbook[level1_bid]['bid'] > 0)) :

                        if self.orderbook[level1_ask]['ask'] > self.orderbook[level1_bid]['bid']:
                            trades = self.orderbook[level1_bid]['bid']
                        else:
                             trades = self.orderbook[level1_ask]['ask']

                        self.orderbook[level1_ask]['ask'] -= trades
                        self.orderbook[level1_bid]['bid'] -= trades
                        if (self.orderbook[level1_ask]['ask'] == 0):
                            break

    def save_json(self):
        with open('orderbook.json', 'w') as outfile:
            json.dump(self.orderbook, outfile)
    
    def save_csv(self):
         self.OrderVis.to_csv('orderbook.csv', encoding='utf-8')
        
    def plot(self):
        pass


if __name__ == "__main__":
    #OPERATING VARIABLES
    Orderbook_time = '3:00:00' # e.g. '2:01:05' '3:00:00'
    orderbook = OrderBook(Orderbook_time)





