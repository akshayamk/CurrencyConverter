import requests
import tkinter as tk
from tkinter import messagebox as mbox

API_KEY = 'c0d8c300955ecb24f0f3'
HEIGHT = 300
WIDTH = 700

class MakeGUI:

    def getuserinput (self,variable, variable1, userentry, labelresults):

        if len (userentry) == 0 or not userentry.isdigit():
            #print(int(userentry))
            mbox.showerror("Error", "Please check input again.")
            return
        
        fromcurrency = variable.get()
        tocurrency = variable1.get()

        if fromcurrency == tocurrency:
            mbox.showerror("Error", "Please check input again. Choose a different currency to convert to.")
            return

        fromcurrency_param = fromcurrency[-4:-1]
        tocurrency_param = tocurrency[-4:-1]


        UserResponse(fromcurrency_param, tocurrency_param, userentry, labelresults)

    

    def getlistofcurrencies(self, currencies):
        #/api/v7/currencies?apiKey=[YOUR_API_KEY]
        url = 'https://free.currconv.com/api/v7/currencies'
        params = {'apiKey' : API_KEY}
        #response = requests.get(url, params)
        response = requests.get(url, params).json()

        for currency in response['results']:
            currencyname = response['results'][currency]['currencyName']
            currencyid = response['results'][currency]['id']
            listappend = str(currencyname) + ' (' + str(currencyid) + ')'
            currencies.append(listappend)


            

    def __init__(self, root):
        currencies = []
        root.title("Currency Converter")
        canvas = tk.Canvas(root, height = HEIGHT, width = WIDTH, bg='black')
        canvas.pack()

        label1 = tk.Label(root, text='Amount to convert:', bg='yellow')
        label1.place(relx = 0.1, rely=0.15)

        entry = tk.Entry(root, font=40, bd=5)
        entry.place(relx=0.3, rely=0.15, relheight= 0.1, relwidth=0.5)

        label2 = tk.Label(root, text='From:', bg='yellow')
        label2.place(relx = 0.1, rely=0.35)

        self.getlistofcurrencies(currencies)

        variable = tk.StringVar(root)
        variable.set(currencies[0]) # default value

        variable1 = tk.StringVar(root)
        variable1.set(currencies[0])

        currencydropdown = tk.OptionMenu(root, variable, *currencies)
        currencydropdown.place(relx = 0.2, rely=0.35)

        label3 = tk.Label(root, text='To:', bg='yellow')
        label3.place(relx = 0.5, rely=0.35)

        currencydropdown2 = tk.OptionMenu(root, variable1, *currencies)
        currencydropdown2.place(relx = 0.6, rely=0.35)

        labelresults = tk.Label(root, bg='black', borderwidth=2, relief="groove")
        labelresults.place (relx = 0.1, rely=0.7, relheight = 0.2, relwidth = 0.6)

        buttonconvert = tk.Button(root, text='Convert', bd=3, command=lambda: self.getuserinput(variable,variable1, entry.get(), labelresults))
        buttonconvert.place(relx=0.3, rely=0.5, relheight=0.1, relwidth = 0.3)


class UserResponse:
    
    def getuserresponse(self, fromcurrency_param, tocurrency_param, userentry, labelresults):
        try:
            url = 'https://free.currconv.com/api/v7/convert'
            makeparam = str(fromcurrency_param) + '_' + str(tocurrency_param)
            params = {'q': makeparam, 'compact' : 'ultra', 'apiKey' : API_KEY}
            userresponse = requests.get(url, params).json()

            Display(userresponse[makeparam], labelresults, userentry, fromcurrency_param,tocurrency_param)
        except:
            mbox.showerror("Error", "Could not get exchange rate.")



    def __init__(self, fromcurrency_param, tocurrency_param, userentry, labelresults):
        self.getuserresponse(fromcurrency_param, tocurrency_param, userentry, labelresults)

class Display:

    def displayexchangerate(self, exchangerate, labelresults, userentry,fromcurrency_param,tocurrency_param):
        labelresults['fg'] = 'white'
        totalamount = exchangerate*float(userentry)
        labelresults['text'] = '1 %s = %s %s. %s %s = %s %s' % (fromcurrency_param, exchangerate, tocurrency_param, userentry, fromcurrency_param, totalamount, tocurrency_param)
  

    def __init__(self, exchangerate, labelresults, userentry,fromcurrency_param,tocurrency_param):
        self.displayexchangerate (exchangerate, labelresults, userentry,fromcurrency_param,tocurrency_param)




root = tk.Tk()
b = MakeGUI(root)
root.mainloop()

