import datetime
import json
import os
import sys
import tkinter
import tkinter.ttk

import forex_python.converter


class App:
    def __init__(self):
        # Variables
        with open(self.get_path('forex data.json'), 'r', encoding='utf8') as f:
            self.forex_data = json.load(f)

        self.root = tkinter.Tk()
        self.info_window = None
        self.update_window = None
        self.update_progress_bar = None

        self.amount = None
        self.amount_entry = None
        self.amount_trace = None
        self.prev_base_curr_symbol = None
        self.base_currency = None
        self.dest_currency = None
        self.input_amount_text = None
        self.output_amount_text = None
        self.conversion_rate_text = None
        self.last_updated_text = None

        # Constants
        self.FONT = 'Segoe UI'
        self.LABEL_FONT = (self.FONT, 10, 'bold')
        self.WIDGET_FONT = (self.FONT, 14, 'normal')
        self.RESULTS_ONE_FONT = (self.FONT, 16, 'normal')
        self.RESULTS_TWO_FONT = (self.FONT, 18, 'bold')
        self.RESULTS_THREE_FONT = (self.FONT, 12, 'normal')
        self.RESULTS_FOUR_FONT = (self.FONT, 12, 'normal')
        self.UPDATE_WINDOW_FONT = (self.FONT, 12, 'normal')
        self.INFO_WINDOW_FONT = (self.FONT, 12, 'normal')

        self.FRAME_PAD = 10
        self.WIDGET_PAD = 10
        self.BUTTON_PAD = 20

        self.COMBO_BOX_WIDTH = 32
        self.ENTRY_WIDTH = 24

        self.MAX_NUMBER_ALLOWED = 1e16

        self.SWAP_BUTTON_IMG = tkinter.PhotoImage(file=self.get_path('swap button.png'))
        self.UPDATE_BUTTON_IMG = tkinter.PhotoImage(file=self.get_path('update button.png'))
        self.INFO_BUTTON_IMAGE = tkinter.PhotoImage(file=self.get_path('info button.png'))
        self.COPY_BUTTON_IMG = tkinter.PhotoImage(file=self.get_path('copy button.png'))

        # Setup functions
        self.create_main_window()
        self.focus_on_entry()
        self.update_conversion()

        # Main loop
        self.root.mainloop()

    def get_path(self, file_name):
        try:
            return os.path.join(sys._MEIPASS, file_name)
        except AttributeError:
            return 'currency converter\\resources\\' + file_name

    def create_main_window(self):
        self.root.title('Currency Converter')
        self.root.geometry(f'1092x278+{int(self.root.winfo_screenwidth() / 2 - 1092 / 2)}+'f'{int(self.root.winfo_screenheight() / 2 - 278 / 2)}')
        self.root.resizable(width=False, height=False)
        self.root.iconphoto(True, tkinter.PhotoImage(file=self.get_path('app.png')))
        self.root.tk.call('source', self.get_path('theme\\sun-valley.tcl'))
        self.root.tk.call('set_theme', 'dark')

        self.amount = tkinter.StringVar(value='£ 1.00')
        self.prev_base_curr_symbol = "£"
        self.base_currency = tkinter.StringVar(value='GBP — British Pound')
        self.dest_currency = tkinter.StringVar(value='USD — United States Dollar')
        self.input_amount_text = tkinter.StringVar(value="")
        self.output_amount_text = tkinter.StringVar(value="")
        self.conversion_rate_text = tkinter.StringVar(value="")
        self.last_updated_text = tkinter.StringVar(value="")

        self.amount_trace = self.amount.trace_add('write', self.update_conversion)
        self.root.bind('<<ComboboxSelected>>', self.update_conversion)
        self.root.bind('<Control-e>', self.focus_on_entry)
        self.root.bind('<Control-s>', self.swap_currencies)
        self.root.bind('<Control-u>', self.update_conversion)
        self.root.bind('<Control-i>', self.display_info_window)
        self.root.bind('<Control-c>', self.copy_to_clipboard)
        self.root.bind('<Control-q>', self.quit)

        input_frame = tkinter.ttk.Frame(self.root, padding=self.FRAME_PAD)
        input_frame.grid(column=0, row=0)

        tkinter.ttk.Label(input_frame, text='Amount' + 51 * ' ', font=self.LABEL_FONT).grid(column=0, row=0)
        self.amount_entry = tkinter.ttk.Entry(input_frame, textvariable=self.amount, font=self.WIDGET_FONT, justify=tkinter.LEFT, width=self.ENTRY_WIDTH)
        self.amount_entry.grid(column=0, row=1, padx=self.WIDGET_PAD)

        tkinter.ttk.Label(input_frame, text='From' + 71 * ' ', font=self.LABEL_FONT).grid(column=1, row=0)
        tkinter.ttk.Combobox(input_frame, textvariable=self.base_currency, font=self.WIDGET_FONT, justify=tkinter.LEFT, width=self.COMBO_BOX_WIDTH, state='readonly', values=self.forex_data['currency_names']).grid(column=1, row=1, padx=self.WIDGET_PAD)

        tkinter.ttk.Button(input_frame, image=self.SWAP_BUTTON_IMG, command=self.swap_currencies).grid(column=2, row=1)

        tkinter.ttk.Label(input_frame, text='To' + 75 * ' ', font=self.LABEL_FONT).grid(column=3, row=0)
        tkinter.ttk.Combobox(input_frame, textvariable=self.dest_currency, font=self.WIDGET_FONT, justify=tkinter.LEFT, width=self.COMBO_BOX_WIDTH, state='readonly', values=self.forex_data['currency_names']).grid(column=3, row=1, padx=self.WIDGET_PAD)

        output_frame = tkinter.ttk.Frame(self.root, padding=self.FRAME_PAD)
        output_frame.grid(column=0, row=1)
        tkinter.ttk.Label(output_frame, textvariable=self.input_amount_text, font=self.RESULTS_ONE_FONT).grid(column=0, row=0)
        tkinter.ttk.Label(output_frame, textvariable=self.output_amount_text, font=self.RESULTS_TWO_FONT).grid(column=0, row=1, pady=5)
        tkinter.ttk.Label(output_frame, textvariable=self.conversion_rate_text, font=self.RESULTS_THREE_FONT).grid(column=0, row=2, pady=5)
        tkinter.ttk.Label(output_frame, textvariable=self.last_updated_text, font=self.RESULTS_FOUR_FONT).grid(column=0, row=3)

        bottom_frame = tkinter.ttk.Frame(self.root, padding=self.FRAME_PAD)
        bottom_frame.grid(column=0, row=2)
        tkinter.ttk.Button(bottom_frame, image=self.UPDATE_BUTTON_IMG, command=self.update_forex_data).grid(column=0, row=0, padx=self.BUTTON_PAD)
        tkinter.ttk.Button(bottom_frame, image=self.INFO_BUTTON_IMAGE, command=self.display_info_window).grid(column=1, row=0, padx=self.BUTTON_PAD)
        tkinter.ttk.Button(bottom_frame, image=self.COPY_BUTTON_IMG, command=self.copy_to_clipboard).grid(column=2, row=0, padx=self.BUTTON_PAD)

    def focus_on_entry(self, event=None):
        self.amount_entry.focus()
        self.amount_entry.icursor(len(self.base_currency.get()))

    def copy_to_clipboard(self, event=None):
        self.root.clipboard_clear()
        self.root.clipboard_append(self.output_amount_text.get())

    def swap_currencies(self, event=None):
        new_base = self.dest_currency.get()
        new_destination = self.base_currency.get()
        self.base_currency.set(new_base)
        self.dest_currency.set(new_destination)
        # Replace old currency code with new one - also amount.set() triggers its trace write, thus updateConversion() is automatically called
        self.amount.set(self.amount.get().replace(self.forex_data['currency_details'][new_destination]['symbol'], self.forex_data['currency_details'][new_base]['symbol']))

    def update_conversion(self, one=None, two=None, three=None):
        # The trace has to be removed so that it is not triggered again when using amount.set().
        self.amount.trace_remove('write', self.amount_trace)

        base_curr = self.base_currency.get()
        dest_curr = self.dest_currency.get()

        base_curr_symbol = self.forex_data['currency_details'][base_curr]['symbol']
        base_curr_name = self.forex_data['currency_details'][base_curr]['name']
        base_curr_code = self.forex_data['currency_details'][base_curr]['code']

        dest_curr_name = self.forex_data['currency_details'][dest_curr]['name']
        dest_curr_code = self.forex_data['currency_details'][dest_curr]['code']

        # If base currency has been changed then change the currency symbol to avoid errors later on
        if base_curr_symbol != self.prev_base_curr_symbol:
            self.amount.set(self.amount.get().replace(self.prev_base_curr_symbol, base_curr_symbol))
            self.prev_base_curr_symbol = self.forex_data['currency_details'][base_curr]['symbol']

        curr_amount = self.amount.get().replace(base_curr_symbol, '').replace(',', '').replace(' ', '')

        try:
            if int(curr_amount) < self.MAX_NUMBER_ALLOWED:
                self.amount.set(f'{base_curr_symbol} {int(curr_amount):,}')
                curr_amount = float(curr_amount)
            else:
                curr_amount = 1
        except ValueError:  # if curr_amount has decimal point
            try:
                if float(curr_amount) < self.MAX_NUMBER_ALLOWED:
                    self.amount.set(f'{base_curr_symbol} {float(curr_amount):,.2f}')
                    curr_amount = float(curr_amount)
                else:
                    curr_amount = 1
            except ValueError:
                curr_amount = 1

        # The trace is added back
        self.amount_trace = self.amount.trace_add('write', self.update_conversion)

        # This block is to cover the unusual situation where ILS (Israeli Shekel) has conversion rates for
        # all required currencies but all required currencies do not have a conversion rate for ILS.
        # Thus, for this case just take the inverse, or 0 if neither conversion exists.
        try:
            conversion_rate = self.forex_data['currency_rates'][base_curr][dest_curr_code]
        except KeyError:
            try:
                conversion_rate = 1 / self.forex_data['currency_rates'][dest_curr][base_curr_code]
            except KeyError:
                conversion_rate = 0

        self.input_amount_text.set(f'{curr_amount:,.2f} {base_curr_name} = ')
        self.output_amount_text.set(f'{curr_amount * conversion_rate:,.5f} {dest_curr_name}')
        self.conversion_rate_text.set(f'1 {base_curr_code} = {conversion_rate:,.5f} {dest_curr_code}')
        self.last_updated_text.set(f'(Last updated at {self.forex_data["update_date"]})')

    def update_forex_data(self):
        self.root.withdraw()
        self.create_update_window()

        forex_rates = forex_python.converter.CurrencyRates()

        for currency in self.forex_data['currency_names']:
            self.forex_data['currency_rates'][currency] = forex_rates.get_rates(self.forex_data['currency_details'][currency]['code'])
            self.forex_data['currency_rates'][currency][self.forex_data['currency_details'][currency]['code']] = 1
            self.update_progress_bar.step(3)
            self.root.update()

        self.forex_data['update_date'] = datetime.datetime.now().strftime('%H:%M:%S %d-%m-%Y')

        with open(self.get_path('forex data.json'), 'w', encoding="utf8") as f:
            json.dump(self.forex_data, f, indent=2)

        self.update_conversion()
        self.update_window.destroy()
        self.root.deiconify()

    def create_update_window(self):
        self.update_window = tkinter.Toplevel(self.root)
        self.update_window.title('Update Progress')
        self.update_window.geometry(f'341x88+{int(self.root.winfo_x() + self.root.winfo_width() / 2 - 341 / 2)}+{int(self.root.winfo_y() + self.root.winfo_height() / 2 - 88 / 2)}')
        self.update_window.resizable(width=False, height=False)
        self.update_window.overrideredirect(True)
        self.update_window.protocol('WM_DELETE_WINDOW', self.nothing)
        self.update_window.focus_force()

        frame = tkinter.ttk.Frame(self.update_window, padding=self.WIDGET_PAD)
        frame.grid(column=0, row=0)

        tkinter.ttk.Label(frame, text='Fetching updated rates from https://ratesapi.io', font=self.UPDATE_WINDOW_FONT).grid(column=0, row=0, pady=self.WIDGET_PAD)

        self.update_progress_bar = tkinter.ttk.Progressbar(frame, orient=tkinter.HORIZONTAL, length=200, mode='determinate', value=0)
        self.update_progress_bar.grid(column=0, row=1, pady=self.WIDGET_PAD)

    def display_info_window(self, event=None):
        self.root.withdraw()
        self.create_info_window()
        self.info_window.mainloop()

    def create_info_window(self):
        self.info_window = tkinter.Toplevel(self.root)
        self.info_window.title('Important Information')
        self.info_window.geometry(f'390x534+{int(self.root.winfo_x() + self.root.winfo_width() / 2 - 390 / 2)}+{int(self.root.winfo_y() + self.root.winfo_height() / 2 - 534 / 2)}')
        self.info_window.resizable(width=False, height=False)
        self.info_window.overrideredirect(True)
        self.info_window.protocol('WM_DELETE_WINDOW', self.nothing)
        self.info_window.focus_force()

        self.info_window.bind('<Return>', self.quit_info_window)

        frame = tkinter.ttk.Frame(self.info_window, padding=self.FRAME_PAD)
        frame.grid(column=0, row=0)

        tkinter.ttk.Label(frame,
                          text='''Keyboard Shortcuts
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
 process can take up to a minute or two.''', justify=tkinter.LEFT, font=self.INFO_WINDOW_FONT).grid(column=0, row=0, pady=self.WIDGET_PAD)

        tkinter.ttk.Button(frame, text='OK', width=10, command=self.quit_info_window).grid(column=0, row=1, pady=self.WIDGET_PAD)

    def quit_info_window(self, event=None):
        self.info_window.destroy()
        self.root.deiconify()

    def quit(self, event=None):
        self.root.quit()

    def nothing(self):
        pass
