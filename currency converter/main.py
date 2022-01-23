import tkinter
import tkinter.ttk
import datetime
import forex_python.converter
# forexData contains all the offline forex data in order to stop the use of the
# forex API until an update is requested. This significantly improves the performance.
import forexData


def updateConversion(one=None, two=None, three=None):
    # The trace has to be removed so that it is not triggered again
    # when using amount.set(). The trace is again set at the end.
    global amountTrace
    amount.trace_remove("write", amountTrace)

    prevBaseCurr = previousBaseCurrency.get()
    baseCurr = baseCurrency.get()
    destCurr = destCurrency.get()

    prevBaseCurrSymbol = currencyDetails[prevBaseCurr][0]

    baseCurrSymbol = currencyDetails[baseCurr][0]
    baseCurrName = currencyDetails[baseCurr][1]
    baseCurrCode = currencyDetails[baseCurr][2]

    destCurrSymbol = currencyDetails[destCurr][0]
    destCurrName = currencyDetails[destCurr][1]
    destCurrCode = currencyDetails[destCurr][2]

    # If base currency has been changed then the currency symbol
    # needs changing to avoid errors later
    if baseCurr != prevBaseCurr:
        previousBaseCurrency.set(baseCurr)
        amount.set(amount.get().replace(prevBaseCurrSymbol, baseCurrSymbol))

    maxNumberAllowed = 1e16
    currAmount = amount.get().replace(",", "").replace(" ", "").replace(baseCurrSymbol, "")

    # The below try block can simplified as:
    #   If amount is int, then display as int if below maxNumberAllowed
    #   If amount is float, then display as with 2 decimal points if below maxNumberAllowed
    #   If amount is a number (int or float) then convert to float
    #   If amount is not a number or above maxNumberAllowed then leave amount unchanged
    #    and make conversion calculation as if amount was equal to one
    try:
        if (int(currAmount) < maxNumberAllowed):
            amount.set(f"{baseCurrSymbol} {int(currAmount):,}")
            currAmount = float(currAmount)
        else:
            currAmount = 1
    except ValueError:
        try:
            if (float(currAmount) < maxNumberAllowed):
                amount.set(f"{baseCurrSymbol} {float(currAmount):,.2f}")
                currAmount = float(currAmount)
            else:
                currAmount = 1
        except ValueError:
            currAmount = 1

    amountTrace = amount.trace_add("write", updateConversion)

    # This block is to cover to unusual situation where ILS has conversion rates for
    # all required currencies but all required currencies do not have a conversion
    # rate for ILS. Thus just take the inverse.
    try:
        conversionRate = currencyRates[baseCurr][destCurrCode]
    except KeyError:
        try:
            conversionRate = 1 / currencyRates[destCurr][baseCurrCode]
        except KeyError:
            conversionRate = 0

    resultOne.set(f"{currAmount:,.2f} {baseCurrName} = ")
    resultTwo.set(f"{currAmount*conversionRate:,.5f} {destCurrName}")
    resultThree.set(f"1 {baseCurrCode} = {conversionRate:,.5f} {destCurrCode}")
    resultFour.set(f"(Last updated on {updateDate})")


def focusOnEntry(event=None):
    amountEntry.focus()
    amountEntry.icursor(len(baseCurrency.get()))


# amount.set() triggers it's trace write and
# so updateConversion() is automatically called
def swapCurrencies(event=None):
    newBase = destCurrency.get()
    newDest = baseCurrency.get()
    baseCurrency.set(newBase)
    destCurrency.set(newDest)
    amount.set(amount.get().replace(currencyDetails[newDest][0], currencyDetails[newBase][0]))


def updateForexData(event=None):
    root.withdraw()
    updateWindow = tkinter.Toplevel(root)
    updateWindow.title("Update Progress")
    updateWindow.geometry(f"341x88+{int(root.winfo_x()+root.winfo_width()/2-341/2)}+{int(root.winfo_y()+root.winfo_height()/2-88/2)}")
    updateWindow.resizable(width=False, height=False)
    # The next to lines disable the ability to close updateWindow to avoid any errors
    updateWindow.overrideredirect(True)
    updateWindow.protocol("WM_DELETE_WINDOW", nothing)

    aFrame = tkinter.ttk.Frame(updateWindow, padding=widgetPadding)
    aFrame.grid(column=0, row=0)

    tkinter.ttk.Label(aFrame,
                      text="Fetching updated rates from https://ratesapi.io",
                      font=updateWindowFont).grid(column=0, row=0, pady=widgetPadding)

    progress = tkinter.ttk.Progressbar(aFrame,
                                       orient=tkinter.HORIZONTAL,
                                       length=200,
                                       mode="determinate",
                                       value=0)
    progress.grid(column=0, row=1, pady=widgetPadding)

    forexRates = forex_python.converter.CurrencyRates()
    forexCodes = forex_python.converter.CurrencyCodes()

    for currency in currencyNames:
        # The progress bar is only updated here as all other code in the
        # updateForexData() function takes essentially no time and
        # root.update() is called to update the progress bar
        progress.step(3)
        root.update()
        currencyRates[currency] = forexRates.get_rates(currencyDetails[currency][2])
        currencyRates[currency][currencyDetails[currency][2]] = 1

    global updateDate
    updateDate = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open("./currency converter/forexData.py", "w", encoding="utf-8") as file:
        file.write(f"updateDate = '{updateDate}'\n\n")
        file.write(f"currencyNames = {str(currencyNames)}\n\n")
        file.write(f"currencyDetails = {str(currencyDetails)}\n\n")
        file.write(f"currencyRates = {str(currencyRates)}\n")

    updateConversion()
    updateWindow.destroy()
    root.deiconify()


# Keyboard shortcuts and general information that may be useful to the user
def displayInfoWindow(event=None):
    root.withdraw()
    global infoWindow
    infoWindow = tkinter.Toplevel(root)
    infoWindow.title("Important Information")
    infoWindow.geometry(f"390x534+{int(root.winfo_x()+root.winfo_width()/2-390/2)}+{int(root.winfo_y()+root.winfo_height()/2-534/2)}")
    infoWindow.resizable(width=False, height=False)
    infoWindow.overrideredirect(True)
    infoWindow.protocol("WM_DELETE_WINDOW", nothing)
    infoWindow.focus_force()

    infoWindow.bind("<Return>", quitInfoWindow)
    infoWindow.bind("<Control-q>", quitInfoWindow)

    mainFrame = tkinter.ttk.Frame(infoWindow, padding=framePadding)
    mainFrame.grid(column=0, row=0)

    tkinter.ttk.Label(mainFrame,
                      text="""Keyboard Shortcuts
CTRL + E    Move cursor focus to amount entry field
CTRL + S    Swap currencies
CTRL + U    Update forex rates
CTRL + I    Show info window
CTRL + C    Copy conversion result to the clipboard
CTRL + Q    Close window

Input amount must be positive and less than 1e16

This program uses the 'forex-python' modules which
itself uses the 'https://ratesapi.io' API, whose rates
are updated at 3PM CET by the ECB.

This program uses offline rates to improve it's
performance, however it's rates can be updated using
the update button or keyboard shortcut.

Updating the rates goes through all 33 supported
currency codes by 'forex-python' and so this
process can take up to a minute or two.""",
                      justify=tkinter.LEFT,
                      font=infoWindowFont).grid(column=0, row=0, pady=widgetPadding)
    # quitInfoWindow function is used as the root window deiconify() function
    # needs to be called after destroying the infoWindow, but calling infoWindow.destroy()
    # does not allow root.deiconify() to be called after infoWindow.mainloop()
    tkinter.ttk.Button(mainFrame,
                       text="OK",
                       width=10,
                       command=quitInfoWindow).grid(column=0, row=1, pady=widgetPadding)

    infoWindow.mainloop()


def quitInfoWindow(event=None):
    infoWindow.destroy()
    root.deiconify()


# Copies the converted result
def copyOutputToClipboard(event=None):
    root.clipboard_clear()
    root.clipboard_append(resultTwo.get())


def nothing():
    pass


def quitMainWindow(event=None):
    root.quit()


if __name__ == "__main__":
    labelFont = ("Segoe UI", 10, "bold")
    widgetFont = ("Segoe UI", 14, "normal")
    resultsOneFont = ("Segoe UI", 16, "normal")
    resultsTwoFont = ("Segoe UI", 18, "bold")
    resultsThreeFont = ("Segoe UI", 12, "normal")
    resultsFourFont = ("Segoe UI", 12, "normal")
    updateWindowFont = ("Segoe UI", 12, "normal")
    infoWindowFont = ("Segoe UI", 12, "normal")
    framePadding = 10
    widgetPadding = 10
    buttonsPadding = 20
    comboBoxWidth = 28
    entryWidth = 24

    # Get all forex data now so that updated rates can be used right away and printed back to forexData
    updateDate = forexData.updateDate
    currencyNames = forexData.currencyNames
    currencyDetails = forexData.currencyDetails
    currencyRates = forexData.currencyRates

    root = tkinter.Tk()
    root.title("Currency Converter")
    root.geometry(f"1012x258+{int(root.winfo_screenwidth()/2-1012/2)}+{int(root.winfo_screenheight()/2-258/2)}")
    root.resizable(width=False, height=False)
    root.iconphoto(True, tkinter.PhotoImage(file="currency converter\\resources\\app.png"))
    root.tk.call("source", "themes\\sun-valley.tcl")
    root.tk.call("set_theme", "dark")

    swapButtonImg = tkinter.PhotoImage(file="currency converter\\resources\\swapButton.png")
    updateButtonImg = tkinter.PhotoImage(file="currency converter\\resources\\updateButton.png")
    infoButtonImg = tkinter.PhotoImage(file="currency converter\\resources\\infoButton.png")
    copyButtonImg = tkinter.PhotoImage(file="currency converter\\resources\\copyButton.png")

    amount = tkinter.StringVar(value="£ 1.00")
    # This is required so that the currency symbol can be found so that it can be updated
    previousBaseCurrency = tkinter.StringVar(value="GBP — British Pound")
    baseCurrency = tkinter.StringVar(value="GBP — British Pound")
    destCurrency = tkinter.StringVar(value="USD — United States Dollar")
    resultOne = tkinter.StringVar(value="1.00 British Pound = ")
    resultTwo = tkinter.StringVar(value=f"{currencyRates['GBP — British Pound']['USD']:,.5f} United States Dollar")
    resultThree = tkinter.StringVar(value=f"1 GBP = {currencyRates['GBP — British Pound']['USD']:,.5f} USD")
    resultFour = tkinter.StringVar(value=f"(Last updated on {forexData.updateDate})")

    amountTrace = amount.trace_add("write", updateConversion)
    root.bind("<<ComboboxSelected>>", updateConversion)
    root.bind("<Control-e>", focusOnEntry)
    root.bind("<Control-s>", swapCurrencies)
    root.bind("<Control-u>", updateForexData)
    root.bind("<Control-i>", displayInfoWindow)
    root.bind("<Control-c>", copyOutputToClipboard)
    root.bind("<Control-q>", quitMainWindow)

    InputFrame = tkinter.ttk.Frame(root, padding=framePadding)
    InputFrame.grid(column=0, row=0)

    tkinter.ttk.Label(InputFrame,
                      text="Amount                                                   ",
                      justify=tkinter.LEFT,
                      font=labelFont).grid(column=0, row=0)
    amountEntry = tkinter.ttk.Entry(InputFrame,
                                    textvariable=amount,
                                    font=widgetFont,
                                    justify=tkinter.LEFT,
                                    width=entryWidth)
    amountEntry.grid(column=0, row=1, padx=widgetPadding)
    focusOnEntry()

    tkinter.ttk.Label(InputFrame,
                      text="From                                                                       ",
                      font=labelFont).grid(column=1, row=0)
    tkinter.ttk.Combobox(InputFrame,
                         textvariable=baseCurrency,
                         font=widgetFont,
                         justify=tkinter.LEFT,
                         width=comboBoxWidth,
                         state="readonly",
                         values=currencyNames).grid(column=1, row=1, padx=widgetPadding)

    tkinter.ttk.Button(InputFrame,
                       image=swapButtonImg,
                       command=swapCurrencies).grid(column=2, row=1)

    tkinter.ttk.Label(InputFrame,
                      text="To                                                                           ",
                      font=labelFont).grid(column=3, row=0)
    tkinter.ttk.Combobox(InputFrame,
                         textvariable=destCurrency,
                         font=widgetFont,
                         justify=tkinter.LEFT,
                         width=comboBoxWidth,
                         state="readonly",
                         values=currencyNames).grid(column=3, row=1, padx=widgetPadding)

    outputFrame = tkinter.ttk.Frame(root)
    outputFrame.grid(column=0, row=1)
    tkinter.ttk.Label(outputFrame,
                      textvariable=resultOne,
                      font=resultsOneFont).grid(column=0, row=0)
    tkinter.ttk.Label(outputFrame,
                      textvariable=resultTwo,
                      font=resultsTwoFont).grid(column=0, row=1, pady=5)
    tkinter.ttk.Label(outputFrame,
                      textvariable=resultThree,
                      font=resultsThreeFont).grid(column=0, row=2, pady=5)
    tkinter.ttk.Label(outputFrame,
                      textvariable=resultFour,
                      font=resultsFourFont).grid(column=0, row=3)

    bottomFrame = tkinter.ttk.Frame(root, padding=framePadding)
    bottomFrame.grid(column=0, row=2)
    tkinter.ttk.Button(bottomFrame,
                       image=updateButtonImg,
                       command=updateForexData).grid(column=0, row=0, padx=buttonsPadding)
    tkinter.ttk.Button(bottomFrame,
                       image=infoButtonImg,
                       command=displayInfoWindow).grid(column=1, row=0, padx=buttonsPadding)
    tkinter.ttk.Button(bottomFrame,
                       image=copyButtonImg,
                       command=copyOutputToClipboard).grid(column=2, row=0, padx=buttonsPadding)

    root.mainloop()
