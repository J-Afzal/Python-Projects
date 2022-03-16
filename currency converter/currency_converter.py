import datetime
import json
import os
import sys
import tkinter
import tkinter.ttk

import forex_python.converter


class App:
    def __init__(self):
        self.label_font = ('Segoe UI', 10, 'bold')
        self.widget_font = ('Segoe UI', 14, 'normal')
        self.results_one_font = ('Segoe UI', 16, 'normal')
        self.results_two_font = ('Segoe UI', 18, 'bold')
        self.results_three_font = ('Segoe UI', 12, 'normal')
        self.results_four_font = ('Segoe UI', 12, 'normal')
        self.update_window_font = ('Segoe UI', 12, 'normal')
        self.info_window_font = ('Segoe UI', 12, 'normal')

        self.frame_pad = 10
        self.widget_pad = 10
        self.button_pad = 20
        self.combo_box_width = 32
        self.entry_width = 24

        self.root = tkinter.Tk()
        self.root.title('Currency Converter')
        self.root.geometry(f'1092x278+{int(self.root.winfo_screenwidth() / 2 - 1092 / 2)}+'f'{int(self.root.winfo_screenheight() / 2 - 278 / 2)}')
        self.root.resizable(width=False, height=False)
        self.root.iconphoto(True, tkinter.PhotoImage(file=self.get_path('app.png')))
        self.root.tk.call('source', self.get_path('theme\\sun-valley.tcl'))
        self.root.tk.call('set_theme', 'dark')

        self.info_window = None

        with open(self.get_path('forex_data.json'), 'r', encoding='utf8') as f:
            self.forex_data = json.load(f)

        self.amount = tkinter.StringVar(value='£ 1.00')
        self.previous_base_currency = tkinter.StringVar(value='GBP — British Pound')
        self.base_currency = tkinter.StringVar(value='GBP — British Pound')
        self.destination_currency = tkinter.StringVar(value='USD — United States Dollar')
        self.result_one = tkinter.StringVar(value="")
        self.result_two = tkinter.StringVar(value="")
        self.result_three = tkinter.StringVar(value="")
        self.result_four = tkinter.StringVar(value="")

        self.amount_trace = self.amount.trace_add('write', self.update_conversion)
        self.root.bind('<<ComboboxSelected>>', self.update_conversion)
        self.root.bind('<Control-e>', self.focus_on_entry)
        self.root.bind('<Control-s>', self.swap_currencies)
        self.root.bind('<Control-u>', self.update_conversion)
        self.root.bind('<Control-i>', self.display_info_window)
        self.root.bind('<Control-c>', self.copy_to_clipboard)
        self.root.bind('<Control-q>', self.quit_main_window)

        self.swap_btn_img = tkinter.PhotoImage(file=self.get_path('swapButton.png'))
        self.update_btn_img = tkinter.PhotoImage(file=self.get_path('updateButton.png'))
        self.info_btn_img = tkinter.PhotoImage(file=self.get_path('infoButton.png'))
        self.copy_btn_img = tkinter.PhotoImage(file=self.get_path('copyButton.png'))

        self.input_frame = tkinter.ttk.Frame(self.root, padding=self.frame_pad)
        self.input_frame.grid(column=0, row=0)

        tkinter.ttk.Label(self.input_frame, text='Amount' + 51 * ' ', font=self.label_font).grid(column=0, row=0)
        self.amount_entry = tkinter.ttk.Entry(self.input_frame,
                                              textvariable=self.amount,
                                              font=self.widget_font,
                                              justify=tkinter.LEFT,
                                              width=self.entry_width)
        self.amount_entry.grid(column=0, row=1, padx=self.widget_pad)

        tkinter.ttk.Label(self.input_frame, text='From' + 71 * ' ', font=self.label_font).grid(column=1, row=0)
        tkinter.ttk.Combobox(self.input_frame,
                             textvariable=self.base_currency,
                             font=self.widget_font,
                             justify=tkinter.LEFT,
                             width=self.combo_box_width,
                             state='readonly',
                             values=self.forex_data['currency_names']).grid(column=1, row=1, padx=self.widget_pad)

        tkinter.ttk.Button(self.input_frame, image=self.swap_btn_img, command=self.swap_currencies).grid(column=2, row=1)

        tkinter.ttk.Label(self.input_frame, text='To' + 75 * ' ', font=self.label_font).grid(column=3, row=0)
        tkinter.ttk.Combobox(self.input_frame,
                             textvariable=self.destination_currency,
                             font=self.widget_font,
                             justify=tkinter.LEFT,
                             width=self.combo_box_width,
                             state='readonly',
                             values=self.forex_data['currency_names']).grid(column=3, row=1, padx=self.widget_pad)

        self.output_frame = tkinter.ttk.Frame(self.root, padding=self.frame_pad)
        self.output_frame.grid(column=0, row=1)
        tkinter.ttk.Label(self.output_frame, textvariable=self.result_one, font=self.results_one_font).grid(column=0, row=0)
        tkinter.ttk.Label(self.output_frame, textvariable=self.result_two, font=self.results_two_font).grid(column=0, row=1, pady=5)
        tkinter.ttk.Label(self.output_frame, textvariable=self.result_three, font=self.results_three_font).grid(column=0, row=2, pady=5)
        tkinter.ttk.Label(self.output_frame, textvariable=self.result_four, font=self.results_four_font).grid(column=0, row=3)

        self.bottom_frame = tkinter.ttk.Frame(self.root, padding=self.frame_pad)
        self.bottom_frame.grid(column=0, row=2)
        tkinter.ttk.Button(self.bottom_frame, image=self.update_btn_img, command=self.update_forex_data).grid(column=0, row=0, padx=self.button_pad)
        tkinter.ttk.Button(self.bottom_frame, image=self.info_btn_img, command=self.display_info_window).grid(column=1, row=0, padx=self.button_pad)
        tkinter.ttk.Button(self.bottom_frame, image=self.copy_btn_img, command=self.copy_to_clipboard).grid(column=2, row=0, padx=self.button_pad)

        self.focus_on_entry()

        self.update_conversion()

        self.root.mainloop()

    # noinspection PyMethodMayBeStatic
    def get_path(self, file_name):
        try:
            # noinspection PyProtectedMember
            return os.path.join(sys._MEIPASS, file_name)
        except AttributeError:
            return 'currency converter\\resources\\' + file_name

    def focus_on_entry(self):
        self.amount_entry.focus()
        self.amount_entry.icursor(len(self.base_currency.get()))

    # noinspection PyUnusedLocal
    def update_conversion(self, one=None, two=None, three=None):
        # The trace has to be removed so that it is not triggered again when
        # using amount.set(). The trace is added back at the end of the function.
        self.amount.trace_remove('write', self.amount_trace)

        prev_base_curr = self.previous_base_currency.get()
        base_curr = self.base_currency.get()
        destination_curr = self.destination_currency.get()

        prev_base_curr_symbol = self.forex_data['currency_details'][prev_base_curr][0]

        base_curr_symbol = self.forex_data['currency_details'][base_curr][0]
        base_curr_name = self.forex_data['currency_details'][base_curr][1]
        base_curr_code = self.forex_data['currency_details'][base_curr][2]

        destination_curr_name = self.forex_data['currency_details'][destination_curr][1]
        destination_curr_code = self.forex_data['currency_details'][destination_curr][2]

        # If base currency has been changed then the currency symbol to avoid errors later on
        if base_curr != prev_base_curr:
            self.previous_base_currency.set(base_curr)
            self.amount.set(self.amount.get().replace(prev_base_curr_symbol, base_curr_symbol))

        max_number_allowed = 1e16
        curr_amount = self.amount.get().replace(',', '').replace(' ', '').replace(base_curr_symbol, '')

        # The below try block can read as:
        #   If amount is int
        #       If below maxNumberAllowed -> accept
        #       Else -> set current amount to 1
        #   Else If amount is float
        #       If below maxNumberAllowed -> accept with precision of two
        #       Else -> set current amount to 1
        #   Else
        #       Set current amount to 1
        #
        # Int and float separated to avoid .00 for ints
        try:
            if int(curr_amount) < max_number_allowed:
                self.amount.set(f'{base_curr_symbol} {int(curr_amount):,}')
                curr_amount = float(curr_amount)
            else:
                curr_amount = 1
        except ValueError:
            try:
                if float(curr_amount) < max_number_allowed:
                    self.amount.set(f'{base_curr_symbol} {float(curr_amount):,.2f}')
                    curr_amount = float(curr_amount)
                else:
                    curr_amount = 1
            except ValueError:
                curr_amount = 1

        self.amount_trace = self.amount.trace_add('write', self.update_conversion)

        # This block is to cover to unusual situation where ILS (Israeli Shekel) has conversion rates for
        # all required currencies but all required currencies do not have a conversion rate for ILS.
        # Thus, just take the inverse, or 0 if neither exists.
        try:
            conversion_rate = self.forex_data['currency_rates'][base_curr][destination_curr_code]
        except KeyError:
            try:
                conversion_rate = 1 / self.forex_data['currency_rates'][destination_curr][base_curr_code]
            except KeyError:
                conversion_rate = 0

        self.result_one.set(f'{curr_amount:,.2f} {base_curr_name} = ')
        self.result_two.set(f'{curr_amount * conversion_rate:,.5f} {destination_curr_name}')
        self.result_three.set(f'1 {base_curr_code} = {conversion_rate:,.5f} {destination_curr_code}')
        self.result_four.set(f'(Last updated at {self.forex_data["update_date"]})')

    def swap_currencies(self):
        new_base = self.destination_currency.get()
        new_destination = self.base_currency.get()
        self.base_currency.set(new_base)
        self.destination_currency.set(new_destination)
        # amount.set() triggers its trace write and so updateConversion() is automatically called
        self.amount.set(self.amount.get().replace(self.forex_data['currency_details'][new_destination][0],
                                                  self.forex_data['currency_details'][new_base][0]))

    def update_forex_data(self):
        self.root.withdraw()
        update_window = tkinter.Toplevel(self.root)
        update_window.title('Update Progress')
        update_window.geometry(f'341x88+{int(self.root.winfo_x() + self.root.winfo_width() / 2 - 341 / 2)}+'
                               f'{int(self.root.winfo_y() + self.root.winfo_height() / 2 - 88 / 2)}')
        update_window.resizable(width=False, height=False)
        # The next to lines disable the ability to close updateWindow to avoid any errors
        update_window.overrideredirect(True)
        update_window.protocol('WM_DELETE_WINDOW', self.nothing)

        frame = tkinter.ttk.Frame(update_window, padding=self.widget_pad)
        frame.grid(column=0, row=0)

        tkinter.ttk.Label(frame,
                          text='Fetching updated rates from https://ratesapi.io',
                          font=self.update_window_font).grid(column=0, row=0, pady=self.widget_pad)

        progress = tkinter.ttk.Progressbar(frame, orient=tkinter.HORIZONTAL, length=200, mode='determinate', value=0)
        progress.grid(column=0, row=1, pady=self.widget_pad)

        forex_rates = forex_python.converter.CurrencyRates()

        for currency in self.forex_data['currency_names']:
            # The progress bar is only updated here as all other code in the
            # updateForexData() function takes essentially no time and
            # root.update() is called to update the progress bar
            progress.step(3)
            self.root.update()
            self.forex_data['currency_rates'][currency] = forex_rates.get_rates(self.forex_data['currency_details'][currency][2])
            self.forex_data['currency_rates'][currency][self.forex_data['currency_details'][currency][2]] = 1

        self.forex_data['update_date'] = datetime.datetime.now().strftime('%H:%M:%S %d-%m-%Y')

        with open(self.get_path('forex_data.json'), 'w', encoding="utf8") as f:
            json.dump(self.forex_data, f)

        self.update_conversion()
        update_window.destroy()
        self.root.deiconify()

    def display_info_window(self):
        self.root.withdraw()
        self.info_window = tkinter.Toplevel(self.root)
        self.info_window.title('Important Information')
        self.info_window.geometry(f'390x534+{int(self.root.winfo_x() + self.root.winfo_width() / 2 - 390 / 2)}+'
                                  f'{int(self.root.winfo_y() + self.root.winfo_height() / 2 - 534 / 2)}')
        self.info_window.resizable(width=False, height=False)
        self.info_window.overrideredirect(True)
        self.info_window.protocol('WM_DELETE_WINDOW', self.nothing)
        self.info_window.focus_force()

        self.info_window.bind('<Return>', self.quit_info_window)
        self.info_window.bind('<Control-q>', self.quit_info_window)

        main_frame = tkinter.ttk.Frame(self.info_window, padding=self.frame_pad)
        main_frame.grid(column=0, row=0)

        # Keyboard shortcuts and general information that may be useful to the user
        tkinter.ttk.Label(main_frame,
                          text=''' Keyboard Shortcuts
 CTRL + E    Move cursor focus to amount entry field
 CTRL + S    Swap currencies
 CTRL + U    Update forex rates
 CTRL + I    Show info window
 CTRL + C    Copy conversion result to the clipboard
 CTRL + Q    Close window
 
 Input amount must be positive and less than 1e16
 
 This program uses the 'forex-python' library which
 itself uses the 'https://ratesapi.io' API, whose 
 rates are updated at 3PM CET by the ECB.
 
 This program uses offline rates to improve it's
 performance, however it's rates can be updated 
 using the update button or keyboard shortcut.
 
 Updating the rates goes through all 33 supported
 currency codes by 'forex-python' and so this
 process can take up to a minute or two.''',
                          justify=tkinter.LEFT, font=self.info_window_font).grid(column=0, row=0, pady=self.widget_pad)

        tkinter.ttk.Button(main_frame, text='OK', width=10, command=self.quit_info_window).grid(column=0, row=1, pady=self.widget_pad)

        self.info_window.mainloop()

    def quit_info_window(self):
        self.info_window.destroy()
        self.root.deiconify()

    def copy_to_clipboard(self):
        self.root.clipboard_clear()
        self.root.clipboard_append(self.result_two.get())

    def quit_main_window(self):
        self.root.quit()

    def nothing(self):
        pass
