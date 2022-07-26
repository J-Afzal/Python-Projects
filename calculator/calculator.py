import tkinter
import tkinter.ttk as ttk
import os
import sys
import math


class Calculator:
    def __init__(self):
        # Variables
        self.current_answer = '0'
        self.previous_answer = '0'
        self.previous_inputs = []
        self.previous_input_selection = -1

        self.root = tkinter.Tk()
        self.info_window = None

        self.input_entry = None
        self.input_trace = None
        self.input_text = None
        self.output_text = None

        # Constants
        self.FONT = 'Segoe UI'
        self.INPUT_FONT = (self.FONT, 32, 'normal')
        self.OUTPUT_FONT = (self.FONT, 64, 'normal')
        self.INFO_FONT = (self.FONT, 12, 'normal')

        self.PAD = 5
        self.EXTRA_PAD = 15
        self.FRAME_PAD = 15
        
        self.ANS = tkinter.PhotoImage(file=self.get_path('ans.png'))
        self.RAND_INT = tkinter.PhotoImage(file=self.get_path('rand int.png'))
        self.PREVIOUS = tkinter.PhotoImage(file=self.get_path('previous.png'))
        self.INFO = tkinter.PhotoImage(file=self.get_path('info.png'))
        self.NEXT = tkinter.PhotoImage(file=self.get_path('next.png'))
        self.RAND_FLOAT = tkinter.PhotoImage(file=self.get_path('rand float.png'))
        self.AC = tkinter.PhotoImage(file=self.get_path('ac.png'))

        self.SIN = tkinter.PhotoImage(file=self.get_path('sin.png'))
        self.COS = tkinter.PhotoImage(file=self.get_path('cos.png'))
        self.TAN = tkinter.PhotoImage(file=self.get_path('tan.png'))
        self.LOG = tkinter.PhotoImage(file=self.get_path('log.png'))
        self.LOG10 = tkinter.PhotoImage(file=self.get_path('log10.png'))
        self.LN = tkinter.PhotoImage(file=self.get_path('ln.png'))

        self.SIN_INV = tkinter.PhotoImage(file=self.get_path('sin inv.png'))
        self.COS_INV = tkinter.PhotoImage(file=self.get_path('cos inv.png'))
        self.TAN_INV = tkinter.PhotoImage(file=self.get_path('tan inv.png'))
        self.X_TO_X = tkinter.PhotoImage(file=self.get_path('x^x.png'))
        self.TEN_TO_X = tkinter.PhotoImage(file=self.get_path('10^x.png'))
        self.E_TO_X = tkinter.PhotoImage(file=self.get_path('e^x.png'))

        self.X_TO = tkinter.PhotoImage(file=self.get_path('x^.png'))
        self.X_TO_TWO = tkinter.PhotoImage(file=self.get_path('x^2.png'))
        self.X_TO_THREE = tkinter.PhotoImage(file=self.get_path('x^3.png'))
        self.X_TO_MINUS_ONE = tkinter.PhotoImage(file=self.get_path('x^-1.png'))
        self.X_FACTORIAL = tkinter.PhotoImage(file=self.get_path('x!.png'))
        self.ABS = tkinter.PhotoImage(file=self.get_path('abs.png'))

        self.BLANK_ROOT = tkinter.PhotoImage(file=self.get_path('root.png'))
        self.SQUARE_ROOT = tkinter.PhotoImage(file=self.get_path('sqrt.png'))
        self.CUBE_ROOT = tkinter.PhotoImage(file=self.get_path('cube root.png'))
        self.PI = tkinter.PhotoImage(file=self.get_path('pi.png'))
        self.TAU = tkinter.PhotoImage(file=self.get_path('tau.png'))
        self.GOLDEN_RATIO = tkinter.PhotoImage(file=self.get_path('golden ratio.png'))

        # Setup functions
        self.create_main_window()
        self.focus_on_input()

        # Main loop
        self.root.mainloop()

    def get_path(self, file_name):
        try:
            return os.path.join(sys._MEIPASS, file_name)
        except AttributeError:
            return 'calculator\\resources\\' + file_name

    def create_main_window(self):
        self.root.title('Calculator')
        self.root.geometry(f'856x834+{int(self.root.winfo_screenwidth() / 2 - 834 / 2)}+{int(self.root.winfo_screenheight() / 2 - 830 / 2)}')
        self.root.resizable(width=False, height=False)
        self.root.iconphoto(True, tkinter.PhotoImage(file=self.get_path('app.png')))
        self.root.tk.call('source', self.get_path('theme\\forest-dark.tcl'))
        ttk.Style().theme_use('forest-dark')

        self.input_text = tkinter.StringVar(value="")
        self.output_text = tkinter.StringVar(value='= 0')

        self.input_trace = self.input_text.trace_add('write', self.update_output)
        self.root.bind('<Return>', self.enter_key_pressed)
        self.root.bind('<Control-e>', self.focus_on_input)
        self.root.bind('<Control-i>', self.info_button_pressed)
        self.root.bind('<Control-Up>', self.previous_pressed)
        self.root.bind('<Control-Down>', self.next_pressed)
        self.root.bind('<Control-Delete>', self.ac_pressed)
        self.root.bind('<Control-p>', self.pi_pressed)
        self.root.bind('<Control-t>', self.tau_pressed)
        self.root.bind('<Control-g>', self.golden_ration_pressed)
        self.root.bind('<Control-c>', self.copy_output_to_clipboard)
        self.root.bind('<Control-q>', self.quit)

        entry_frame = tkinter.ttk.Frame(self.root, padding=self.FRAME_PAD)
        entry_frame.grid(column=0, row=0)

        self.input_entry = tkinter.ttk.Entry(entry_frame, width=34, textvariable=self.input_text, font=self.INPUT_FONT)
        self.input_entry.grid(column=0, row=0, pady=(0, 20))

        tkinter.ttk.Entry(entry_frame, width=17, textvariable=self.output_text, justify=tkinter.RIGHT, state='readonly', font=self.OUTPUT_FONT).grid(column=0, row=1)

        top_frame = tkinter.ttk.Frame(self.root, padding=self.FRAME_PAD)
        top_frame.grid(column=0, row=1)

        ttk.Button(top_frame, image=self.ANS, command=self.ans_pressed).grid(column=0, row=0, padx=self.PAD)
        ttk.Button(top_frame, image=self.RAND_INT, command=self.rand_int_pressed).grid(column=1, row=0, padx=self.PAD)
        ttk.Button(top_frame, image=self.PREVIOUS, command=self.previous_pressed).grid(column=2, row=0, padx=(self.EXTRA_PAD + 9, self.PAD))
        ttk.Button(top_frame, image=self.INFO, command=self.info_button_pressed).grid(column=3, row=0, padx=self.PAD)
        ttk.Button(top_frame, image=self.NEXT, command=self.next_pressed).grid(column=4, row=0, padx=(self.PAD, self.EXTRA_PAD + 9))
        ttk.Button(top_frame, image=self.RAND_FLOAT, command=self.rand_float_pressed).grid(column=5, row=0, padx=self.PAD)
        ttk.Button(top_frame, image=self.AC, command=self.ac_pressed).grid(column=6, row=0, padx=self.PAD)

        main_frame = tkinter.ttk.Frame(self.root, padding=self.FRAME_PAD)
        main_frame.grid(column=0, row=2)

        ttk.Button(main_frame, image=self.SIN, command=self.sin_pressed).grid(column=0, row=0, padx=self.PAD, pady=(self.EXTRA_PAD, self.PAD))
        ttk.Button(main_frame, image=self.COS, command=self.cos_pressed).grid(column=1, row=0, padx=self.PAD, pady=(self.EXTRA_PAD, self.PAD))
        ttk.Button(main_frame, image=self.TAN, command=self.tan_pressed).grid(column=2, row=0, padx=(self.PAD, self.EXTRA_PAD), pady=(self.EXTRA_PAD, self.PAD))
        ttk.Button(main_frame, image=self.LOG, command=self.log_pressed).grid(column=3, row=0, padx=(self.EXTRA_PAD, self.PAD), pady=(self.EXTRA_PAD, self.PAD))
        ttk.Button(main_frame, image=self.LOG10, command=self.log_ten_pressed).grid(column=4, row=0, padx=self.PAD, pady=(self.EXTRA_PAD, self.PAD))
        ttk.Button(main_frame, image=self.LN, command=self.ln_pressed).grid(column=5, row=0, padx=self.PAD, pady=(self.EXTRA_PAD, self.PAD))

        ttk.Button(main_frame, image=self.SIN_INV, command=self.sin_inv_pressed).grid(column=0, row=1, padx=self.PAD, pady=(self.PAD, self.EXTRA_PAD))
        ttk.Button(main_frame, image=self.COS_INV, command=self.cos_inv_pressed).grid(column=1, row=1, padx=self.PAD, pady=(self.PAD, self.EXTRA_PAD))
        ttk.Button(main_frame, image=self.TAN_INV, command=self.tan_inv_pressed).grid(column=2, row=1, padx=(self.PAD, self.EXTRA_PAD), pady=(self.PAD, self.EXTRA_PAD))
        ttk.Button(main_frame, image=self.X_TO_X, command=self.x_to_x_pressed).grid(column=3, row=1, padx=(self.EXTRA_PAD, self.PAD), pady=(self.PAD, self.EXTRA_PAD))
        ttk.Button(main_frame, image=self.TEN_TO_X, command=self.ten_to_x_pressed).grid(column=4, row=1, padx=self.PAD, pady=(self.PAD, self.EXTRA_PAD))
        ttk.Button(main_frame, image=self.E_TO_X, command=self.e_to_x_pressed).grid(column=5, row=1, padx=self.PAD, pady=(self.PAD, self.EXTRA_PAD))

        ttk.Button(main_frame, image=self.X_TO, command=self.x_to_pressed).grid(column=0, row=2, padx=self.PAD, pady=self.EXTRA_PAD)
        ttk.Button(main_frame, image=self.X_TO_TWO, command=self.x_to_two_pressed).grid(column=1, row=2, padx=self.PAD, pady=self.EXTRA_PAD)
        ttk.Button(main_frame, image=self.X_TO_THREE, command=self.x_to_three_pressed).grid(column=2, row=2, padx=(self.PAD, self.EXTRA_PAD), pady=self.EXTRA_PAD)
        ttk.Button(main_frame, image=self.X_TO_MINUS_ONE, command=self.x_to_minus_one_pressed).grid(column=3, row=2, padx=(self.EXTRA_PAD, self.PAD), pady=self.EXTRA_PAD)
        ttk.Button(main_frame, image=self.X_FACTORIAL, command=self.x_factorial_pressed).grid(column=4, row=2, padx=self.PAD, pady=self.EXTRA_PAD)
        ttk.Button(main_frame, image=self.ABS, command=self.abs_pressed).grid(column=5, row=2, padx=self.PAD, pady=self.EXTRA_PAD)

        ttk.Button(main_frame, image=self.BLANK_ROOT, command=self.blank_root_pressed).grid(column=0, row=3, padx=self.PAD, pady=(self.EXTRA_PAD, self.PAD))
        ttk.Button(main_frame, image=self.SQUARE_ROOT, command=self.square_root_pressed).grid(column=1, row=3, padx=self.PAD, pady=(self.EXTRA_PAD, self.PAD))
        ttk.Button(main_frame, image=self.CUBE_ROOT, command=self.cube_root_pressed).grid(column=2, row=3, padx=(self.PAD, self.EXTRA_PAD), pady=(self.EXTRA_PAD, self.PAD))
        ttk.Button(main_frame, image=self.PI, command=self.pi_pressed).grid(column=3, row=3, padx=(self.EXTRA_PAD, self.PAD), pady=(self.EXTRA_PAD, self.PAD))
        ttk.Button(main_frame, image=self.TAU, command=self.tau_pressed).grid(column=4, row=3, padx=self.PAD, pady=(self.EXTRA_PAD, self.PAD))
        ttk.Button(main_frame, image=self.GOLDEN_RATIO, command=self.golden_ration_pressed).grid(column=5, row=3, padx=self.PAD, pady=(self.EXTRA_PAD, self.PAD))

    def focus_on_input(self, event=None, cursor_pos=None, scroll_value=None):
        self.input_entry.focus()
        if cursor_pos is None and scroll_value is None:
            self.input_entry.icursor(len(self.input_text.get()))
        else:
            self.input_entry.icursor(cursor_pos)
            self.input_entry.xview_scroll(scroll_value, tkinter.UNITS)

    def copy_output_to_clipboard(self, event=None):
        self.root.clipboard_clear()
        self.root.clipboard_append(self.output_text.get()[2:])

    def update_output(self, one=None, two=None, three=None, called_by_code=False, reset_current_selection=True):
        if not called_by_code:
            if len(self.input_text.get()) > 64:
                self.input_text.set(self.input_text.get()[:64])

        if reset_current_selection:
            self.previous_input_selection = -1

        input_copy = self.input_text.get()
        input_copy = input_copy.replace('RANDi', 'random.randint')
        input_copy = input_copy.replace('RANDf', 'random.uniform')
        input_copy = input_copy.replace('sin(', 'math.sin(')
        input_copy = input_copy.replace('cos(', 'math.cos(')
        input_copy = input_copy.replace('tan(', 'math.tan(')
        input_copy = input_copy.replace('sin⁻¹', 'math.asin')
        input_copy = input_copy.replace('cos⁻¹', 'math.acos')
        input_copy = input_copy.replace('tan⁻¹', 'math.atan')
        input_copy = input_copy.replace('log', 'math.log')
        input_copy = input_copy.replace('ln', 'math.log')
        input_copy = input_copy.replace('^', '**')
        input_copy = input_copy.replace('PI', 'math.pi')
        input_copy = input_copy.replace('TAU', 'math.tau')
        input_copy = input_copy.replace('PHI', '((1 + 5 ** 0.5) / 2)')
        input_copy = input_copy.replace('EXP', 'math.e')
        input_copy = input_copy.replace('factorial', 'math.factorial')
        input_copy = input_copy.replace('ANS', str(self.previous_answer))

        try:
            self.current_answer = float(eval(input_copy))
            self.output_text.set('= ' + str(f'{self.current_answer:.8G}'))
        except (SyntaxError, AttributeError, NameError, TypeError, ValueError, ZeroDivisionError):
            self.output_text.set('= 0')

    def insert_text_to_input(self, txt, pos):
        if not ((len(self.input_text.get()) + len(txt)) > 64):
            curr_pos = self.input_entry.index(tkinter.INSERT)
            self.input_text.set(self.input_text.get()[:curr_pos] + txt + self.input_text.get()[curr_pos:])
            self.focus_on_input(cursor_pos=curr_pos + pos, scroll_value=pos)
        else:
            self.input_entry.focus()

    def enter_key_pressed(self, event=None):
        self.previous_answer = self.current_answer
        self.previous_inputs.insert(0, self.input_text.get())
        self.update_output(called_by_code=True)

    def ans_pressed(self):
        self.insert_text_to_input('ANS', 3)

    def rand_int_pressed(self):
        self.insert_text_to_input('RANDi(,)', 6)

    def previous_pressed(self, event=None):
        if len(self.previous_inputs) != 0:
            if self.previous_input_selection < (len(self.previous_inputs) - 1):
                self.previous_input_selection += 1

            self.input_text.trace_remove('write', self.input_trace)
            self.input_text.set(self.previous_inputs[self.previous_input_selection])
            self.input_trace = self.input_text.trace_add('write', self.update_output)
            self.update_output(called_by_code=True, reset_current_selection=False)

        self.focus_on_input()

    def next_pressed(self, event=None):
        if len(self.previous_inputs) != 0:
            if self.previous_input_selection > 0:
                self.previous_input_selection -= 1

            self.input_text.trace_remove('write', self.input_trace)
            self.input_text.set(self.previous_inputs[self.previous_input_selection])
            self.input_trace = self.input_text.trace_add('write', self.update_output)
            self.update_output(called_by_code=True, reset_current_selection=False)

        self.focus_on_input()

    def rand_float_pressed(self):
        self.insert_text_to_input('RANDf(,)', 6)

    def ac_pressed(self, event=None):
        self.input_text.set("")
        self.focus_on_input()

    def sin_pressed(self):
        self.insert_text_to_input('sin()', 4)

    def cos_pressed(self):
        self.insert_text_to_input('cos()', 4)

    def tan_pressed(self):
        self.insert_text_to_input('tan()', 4)

    def log_pressed(self):
        self.insert_text_to_input('log(,)', 4)

    def log_ten_pressed(self):
        self.insert_text_to_input('log(,10)', 4)

    def ln_pressed(self):
        self.insert_text_to_input('ln()', 3)

    def sin_inv_pressed(self):
        self.insert_text_to_input('sin⁻¹()', 6)

    def cos_inv_pressed(self):
        self.insert_text_to_input('cos⁻¹()', 6)

    def tan_inv_pressed(self):
        self.insert_text_to_input('tan⁻¹()', 6)

    def x_to_x_pressed(self):
        self.insert_text_to_input('()^()', 1)

    def ten_to_x_pressed(self):
        self.insert_text_to_input('10^()', 4)

    def e_to_x_pressed(self):
        self.insert_text_to_input('EXP^()', 5)

    def x_to_pressed(self):
        self.insert_text_to_input('^()', 2)

    def x_to_two_pressed(self):
        self.insert_text_to_input('^(2)', 4)

    def x_to_three_pressed(self):
        self.insert_text_to_input('^(3)', 4)

    def x_to_minus_one_pressed(self):
        self.insert_text_to_input('^(-1)', 5)

    def x_factorial_pressed(self):
        self.insert_text_to_input('factorial()', 10)

    def abs_pressed(self):
        self.insert_text_to_input('abs()', 4)

    def blank_root_pressed(self):
        self.insert_text_to_input('()^(1/)', 1)

    def square_root_pressed(self):
        self.insert_text_to_input('()^(1/2)', 1)

    def cube_root_pressed(self):
        self.insert_text_to_input('()^(1/3)', 1)

    def pi_pressed(self, event=None):
        self.insert_text_to_input('PI', 2)

    def tau_pressed(self, event=None):
        self.insert_text_to_input('TAU', 3)

    def golden_ration_pressed(self, event=None):
        self.insert_text_to_input('PHI', 3)

    def info_button_pressed(self, event=None):
        self.root.withdraw()
        self.create_info_window()
        self.info_window.mainloop()

    def create_info_window(self):
        self.info_window = tkinter.Toplevel(self.root)
        self.info_window.title('Important Information')
        self.info_window.geometry(f'421x775+{int(self.root.winfo_x() + self.root.winfo_width() / 2 - 421 / 2)}+{int(self.root.winfo_y() + self.root.winfo_height() / 2 - 775 / 2)}')
        self.info_window.resizable(width=False, height=False)
        self.info_window.overrideredirect(True)
        self.info_window.protocol('WM_DELETE_WINDOW', self.nothing)
        self.info_window.focus_force()

        self.info_window.bind('<Return>', self.quit_info_window)

        main_frame = tkinter.ttk.Frame(self.info_window, padding=self.FRAME_PAD)
        main_frame.grid(column=0, row=0)

        ttk.Label(main_frame, text='***** WARNING *****', justify=tkinter.CENTER, font=self.INFO_FONT).grid(column=0, row=0, pady=(self.EXTRA_PAD, 0))
        ttk.Label(main_frame, text='This program uses eval() to evaluate the input field\nand thus is vulnerable to being exploited.', justify=tkinter.CENTER, font=self.INFO_FONT).grid(column=0, row=1, pady=(0, self.EXTRA_PAD))

        ttk.Label(main_frame, text='Keyboard Shortcuts', justify=tkinter.CENTER, font=self.INFO_FONT).grid(column=0, row=2, pady=(self.EXTRA_PAD, 0))
        ttk.Label(main_frame, text="""Enter Key       Add input field/output field to memory
CTRL + E        Move cursor focus to input field
CTRL + I        Show info window
CTRL + Up       Retrieve older input from memory
CTRL + Down     Retrieve newer input from memory
CTRL + Delete   Clear input field (AC)
CTRL + P        Add Pi to input field (PI)
CTRL + T        Add Tau to input field (TAU)
CTRL + G        Add Golden Ratio to input field (PHI)
CTRL + C        Copy output to the clipboard
CTRL + Q        Close window

The input field is limited to 64 characters.

Whenever the Enter key is pressed the answer is stored
to ANS and the input field is added to a list which can
be retrieved using the arrow keys.

All angles input and outputs are in radians.

The RAND function takes two arguments, where the first
one is the lower bound and the second one is the upper
bound, both are inclusive.

The log function takes two arguments, where the first
one is the input and the second one is base.""", justify=tkinter.LEFT, font=self.INFO_FONT).grid(column=0, row=3, pady=(0, self.EXTRA_PAD))

        tkinter.ttk.Button(main_frame, text='OK', width=10, command=self.quit_info_window).grid(column=0, row=4, pady=(self.EXTRA_PAD, 0))

    def quit_info_window(self, event=None):
        self.info_window.destroy()
        self.root.deiconify()

    def quit(self, event=None):
        self.root.quit()

    def nothing(self):
        pass
