import tkinter
import tkinter.ttk as ttk
import os
import sys
import math


class App:
    def __init__(self):
        self.input_font = ("Segoe UI", 32, "normal")
        self.output_font = ("Segoe UI", 64, "normal")
        self.info_font = ("Segoe UI", 12, "normal")
        self.pad = 5
        self.extra_pad = 15
        self.frame_pad = 15

        self.current_answer = "0"
        self.previous_answer = "0"
        self.previous_inputs = []
        self.current_selection = -1

        self.root = tkinter.Tk()
        self.root.title("Calculator")
        self.root.geometry(f"856x834+{int(self.root.winfo_screenwidth() / 2 - 834 / 2)}+{int(self.root.winfo_screenheight() / 2 - 830 / 2)}")
        self.root.resizable(width=False, height=False)
        self.root.iconphoto(True, tkinter.PhotoImage(file=self.get_path("app.png")))
        self.root.tk.call("source", self.get_path("theme\\forest-dark.tcl"))
        ttk.Style().theme_use("forest-dark")

        self.info_window = None

        self.input_text = tkinter.StringVar(value="")
        self.output_text = tkinter.StringVar(value="= 0")

        self.input_trace = self.input_text.trace_add("write", self.update_output)
        self.root.bind("<Return>", self.enter_key_pressed)
        self.root.bind("<Control-e>", self.focus_on_input)
        self.root.bind("<Control-c>", self.copy_output_to_clipboard)
        self.root.bind("<Control-i>", self.info_button_pressed)
        self.root.bind("<Control-Up>", self.previous_pressed)
        self.root.bind("<Control-Down>", self.next_pressed)
        self.root.bind("<Control-Delete>", self.ac_pressed)
        self.root.bind("<Control-p>", self.pi_pressed)
        self.root.bind("<Control-t>", self.tau_pressed)
        self.root.bind("<Control-g>", self.golden_ration_pressed)
        self.root.bind("<Control-q>", self.quit_main_window)

        self.ans = tkinter.PhotoImage(file=self.get_path("ans.png"))
        self.rand_int = tkinter.PhotoImage(file=self.get_path("rand int.png"))
        self.prev = tkinter.PhotoImage(file=self.get_path("previous.png"))
        self.info = tkinter.PhotoImage(file=self.get_path("info.png"))
        self.next = tkinter.PhotoImage(file=self.get_path("next.png"))
        self.rand_float = tkinter.PhotoImage(file=self.get_path("rand float.png"))
        self.ac = tkinter.PhotoImage(file=self.get_path("ac.png"))

        self.sin = tkinter.PhotoImage(file=self.get_path("sin.png"))
        self.cos = tkinter.PhotoImage(file=self.get_path("cos.png"))
        self.tan = tkinter.PhotoImage(file=self.get_path("tan.png"))
        self.log = tkinter.PhotoImage(file=self.get_path("log.png"))
        self.log_ten = tkinter.PhotoImage(file=self.get_path("log10.png"))
        self.ln = tkinter.PhotoImage(file=self.get_path("ln.png"))

        self.sin_inv = tkinter.PhotoImage(file=self.get_path("sinInv.png"))
        self.cos_inv = tkinter.PhotoImage(file=self.get_path("cosInv.png"))
        self.tan_inv = tkinter.PhotoImage(file=self.get_path("tanInv.png"))
        self.x_to_x = tkinter.PhotoImage(file=self.get_path("x^x.png"))
        self.ten_to_x = tkinter.PhotoImage(file=self.get_path("10^x.png"))
        self.e_to_x = tkinter.PhotoImage(file=self.get_path("e^x.png"))

        self.x_to = tkinter.PhotoImage(file=self.get_path("x^.png"))
        self.x_to_two = tkinter.PhotoImage(file=self.get_path("x^2.png"))
        self.x_to_three = tkinter.PhotoImage(file=self.get_path("x^3.png"))
        self.x_to_minus_one = tkinter.PhotoImage(file=self.get_path("x^-1.png"))
        self.x_factorial = tkinter.PhotoImage(file=self.get_path("x!.png"))
        self.abs = tkinter.PhotoImage(file=self.get_path("abs.png"))

        self.blank_root = tkinter.PhotoImage(file=self.get_path("root.png"))
        self.square_root = tkinter.PhotoImage(file=self.get_path("sqrt.png"))
        self.cube_root = tkinter.PhotoImage(file=self.get_path("cube root.png"))
        self.pi = tkinter.PhotoImage(file=self.get_path("pi.png"))
        self.tau = tkinter.PhotoImage(file=self.get_path("tau.png"))
        self.golden_ratio = tkinter.PhotoImage(file=self.get_path("golden ratio.png"))

        self.entry_frame = tkinter.ttk.Frame(self.root, padding=self.frame_pad)
        self.entry_frame.grid(column=0, row=0)

        self.input_entry = tkinter.ttk.Entry(self.entry_frame, width=34, textvariable=self.input_text, font=self.input_font)
        self.input_entry.grid(column=0, row=0, pady=(0, 20))

        tkinter.ttk.Entry(self.entry_frame, width=17, textvariable=self.output_text, justify=tkinter.RIGHT, state="readonly", font=self.output_font).grid(column=0, row=1)

        self.topFrame = tkinter.ttk.Frame(self.root, padding=self.frame_pad)
        self.topFrame.grid(column=0, row=1)

        ttk.Button(self.topFrame, image=self.ans, command=self.ans_pressed).grid(column=0, row=0, padx=self.pad)
        ttk.Button(self.topFrame, image=self.rand_int, command=self.rand_int_pressed).grid(column=1, row=0, padx=self.pad)
        ttk.Button(self.topFrame, image=self.prev, command=self.previous_pressed).grid(column=2, row=0, padx=(self.extra_pad + 9, self.pad))
        ttk.Button(self.topFrame, image=self.info, command=self.info_button_pressed).grid(column=3, row=0, padx=self.pad)
        ttk.Button(self.topFrame, image=self.next, command=self.next_pressed).grid(column=4, row=0, padx=(self.pad, self.extra_pad + 9))
        ttk.Button(self.topFrame, image=self.rand_float, command=self.rand_float_pressed).grid(column=5, row=0, padx=self.pad)
        ttk.Button(self.topFrame, image=self.ac, command=self.ac_pressed).grid(column=6, row=0, padx=self.pad)

        main_frame = tkinter.ttk.Frame(self.root, padding=self.frame_pad)
        main_frame.grid(column=0, row=2)

        ttk.Button(main_frame, image=self.sin, command=self.sin_pressed).grid(column=0, row=0, padx=self.pad, pady=(self.extra_pad, self.pad))
        ttk.Button(main_frame, image=self.cos, command=self.cos_pressed).grid(column=1, row=0, padx=self.pad, pady=(self.extra_pad, self.pad))
        ttk.Button(main_frame, image=self.tan, command=self.tan_pressed).grid(column=2, row=0, padx=(self.pad, self.extra_pad), pady=(self.extra_pad, self.pad))
        ttk.Button(main_frame, image=self.log, command=self.log_pressed).grid(column=3, row=0, padx=(self.extra_pad, self.pad), pady=(self.extra_pad, self.pad))
        ttk.Button(main_frame, image=self.log_ten, command=self.log_ten_pressed).grid(column=4, row=0, padx=self.pad, pady=(self.extra_pad, self.pad))
        ttk.Button(main_frame, image=self.ln, command=self.ln_pressed).grid(column=5, row=0, padx=self.pad, pady=(self.extra_pad, self.pad))

        ttk.Button(main_frame, image=self.sin_inv, command=self.sin_inv_pressed).grid(column=0, row=1, padx=self.pad, pady=(self.pad, self.extra_pad))
        ttk.Button(main_frame, image=self.cos_inv, command=self.cos_inv_pressed).grid(column=1, row=1, padx=self.pad, pady=(self.pad, self.extra_pad))
        ttk.Button(main_frame, image=self.tan_inv, command=self.tan_inv_pressed).grid(column=2, row=1, padx=(self.pad, self.extra_pad), pady=(self.pad, self.extra_pad))
        ttk.Button(main_frame, image=self.x_to_x, command=self.x_to_x_pressed).grid(column=3, row=1, padx=(self.extra_pad, self.pad), pady=(self.pad, self.extra_pad))
        ttk.Button(main_frame, image=self.ten_to_x, command=self.ten_to_x_pressed).grid(column=4, row=1, padx=self.pad, pady=(self.pad, self.extra_pad))
        ttk.Button(main_frame, image=self.e_to_x, command=self.e_to_x_pressed).grid(column=5, row=1, padx=self.pad, pady=(self.pad, self.extra_pad))

        ttk.Button(main_frame, image=self.x_to, command=self.x_to_pressed).grid(column=0, row=2, padx=self.pad, pady=self.extra_pad)
        ttk.Button(main_frame, image=self.x_to_two, command=self.x_to_two_pressed).grid(column=1, row=2, padx=self.pad, pady=self.extra_pad)
        ttk.Button(main_frame, image=self.x_to_three, command=self.x_to_three_pressed).grid(column=2, row=2, padx=(self.pad, self.extra_pad), pady=self.extra_pad)
        ttk.Button(main_frame, image=self.x_to_minus_one, command=self.x_to_minus_one_pressed).grid(column=3, row=2, padx=(self.extra_pad, self.pad), pady=self.extra_pad)
        ttk.Button(main_frame, image=self.x_factorial, command=self.x_factorial_pressed).grid(column=4, row=2, padx=self.pad, pady=self.extra_pad)
        ttk.Button(main_frame, image=self.abs, command=self.abs_pressed).grid(column=5, row=2, padx=self.pad, pady=self.extra_pad)

        ttk.Button(main_frame, image=self.blank_root, command=self.blank_root_pressed).grid(column=0, row=3, padx=self.pad, pady=(self.extra_pad, self.pad))
        ttk.Button(main_frame, image=self.square_root, command=self.square_root_pressed).grid(column=1, row=3, padx=self.pad, pady=(self.extra_pad, self.pad))
        ttk.Button(main_frame, image=self.cube_root, command=self.cube_root_pressed).grid(column=2, row=3, padx=(self.pad, self.extra_pad), pady=(self.extra_pad, self.pad))
        ttk.Button(main_frame, image=self.pi, command=self.pi_pressed).grid(column=3, row=3, padx=(self.extra_pad, self.pad), pady=(self.extra_pad, self.pad))
        ttk.Button(main_frame, image=self.tau, command=self.tau_pressed).grid(column=4, row=3, padx=self.pad, pady=(self.extra_pad, self.pad))
        ttk.Button(main_frame, image=self.golden_ratio, command=self.golden_ration_pressed).grid(column=5, row=3, padx=self.pad, pady=(self.extra_pad, self.pad))

        self.focus_on_input()

        self.root.mainloop()

    # noinspection PyMethodMayBeStatic
    def get_path(self, file_name):
        try:
            # noinspection PyProtectedMember
            return os.path.join(sys._MEIPASS, file_name)
        except AttributeError:
            return "calculator\\resources\\" + file_name

    def update_output(self, one=None, two=None, three=None, called_by_code=False, reset_current_selection=True):
        if not called_by_code:
            if len(self.input_text.get()) > 64:
                self.input_text.set(self.input_text.get()[:64])

        if reset_current_selection:
            self.current_selection = -1

        input_copy = self.input_text.get()
        input_copy = input_copy.replace("RANDi", "random.randint")
        input_copy = input_copy.replace("RANDf", "random.uniform")
        input_copy = input_copy.replace("sin(", "math.sin(")
        input_copy = input_copy.replace("cos(", "math.cos(")
        input_copy = input_copy.replace("tan(", "math.tan(")
        input_copy = input_copy.replace("sin⁻¹", "math.asin")
        input_copy = input_copy.replace("cos⁻¹", "math.acos")
        input_copy = input_copy.replace("tan⁻¹", "math.atan")
        input_copy = input_copy.replace("log", "math.log")
        input_copy = input_copy.replace("ln", "math.log")
        input_copy = input_copy.replace("^", "**")
        input_copy = input_copy.replace("PI", "math.pi")
        input_copy = input_copy.replace("TAU", "math.tau")
        input_copy = input_copy.replace("PHI", "((1 + 5 ** 0.5) / 2)")
        input_copy = input_copy.replace("EXP", "math.e")
        input_copy = input_copy.replace("factorial", "math.factorial")
        input_copy = input_copy.replace("ANS", str(self.previous_answer))

        try:
            self.current_answer = float(eval(input_copy))
            self.output_text.set("= " + str(f"{self.current_answer:.8G}"))
        except Exception:
            self.output_text.set("= 0")

    def insert_text_to_input(self, txt, pos):
        if not ((len(self.input_text.get()) + len(txt)) > 64):
            currPos = self.input_entry.index(tkinter.INSERT)
            self.input_text.set(self.input_text.get()[:currPos] + txt + self.input_text.get()[currPos:])
            self.focus_on_input(cursor_pos=currPos + pos, scroll_value=pos)
        else:
            self.input_entry.focus()

    def focus_on_input(self, event=None, cursor_pos=None, scroll_value=None):
        self.input_entry.focus()
        if cursor_pos is None and scroll_value is None:
            self.input_entry.icursor(len(self.input_text.get()))
        else:
            self.input_entry.icursor(cursor_pos)
            self.input_entry.xview_scroll(scroll_value, tkinter.UNITS)

    def enter_key_pressed(self, event=None):
        self.previous_answer = self.current_answer
        self.previous_inputs.insert(0, self.input_text.get())
        self.update_output(called_by_code=True)

    def ans_pressed(self):
        self.insert_text_to_input("ANS", 3)

    def rand_int_pressed(self):
        self.insert_text_to_input("RANDi(,)", 6)

    def previous_pressed(self, event=None):
        if len(self.previous_inputs) != 0:
            if (self.current_selection + 1) < len(self.previous_inputs):
                self.current_selection += 1

            self.input_text.trace_remove("write", self.input_trace)
            self.input_text.set(self.previous_inputs[self.current_selection])
            self.input_trace = self.input_text.trace_add("write", self.update_output)
            self.update_output(called_by_code=True, reset_current_selection=False)

        self.focus_on_input()

    def next_pressed(self, event=None):
        if len(self.previous_inputs) != 0:
            if self.current_selection == -1:
                self.current_selection = 0
            elif self.current_selection > 0:
                self.current_selection -= 1

            self.input_text.trace_remove("write", self.input_trace)
            self.input_text.set(self.previous_inputs[self.current_selection])
            self.input_trace = self.input_text.trace_add("write", self.update_output)
            self.update_output(called_by_code=True, reset_current_selection=False)
        self.focus_on_input()

    def rand_float_pressed(self):
        self.insert_text_to_input("RANDf(,)", 6)

    def ac_pressed(self, event=None):
        self.input_text.set("")
        self.focus_on_input()

    def sin_pressed(self):
        self.insert_text_to_input("sin()", 4)

    def cos_pressed(self):
        self.insert_text_to_input("cos()", 4)

    def tan_pressed(self):
        self.insert_text_to_input("tan()", 4)

    def log_pressed(self):
        self.insert_text_to_input("log(,)", 4)

    def log_ten_pressed(self):
        self.insert_text_to_input("log(,10)", 4)

    def ln_pressed(self):
        self.insert_text_to_input("ln()", 3)

    def sin_inv_pressed(self):
        self.insert_text_to_input("sin⁻¹()", 6)

    def cos_inv_pressed(self):
        self.insert_text_to_input("cos⁻¹()", 6)

    def tan_inv_pressed(self):
        self.insert_text_to_input("tan⁻¹()", 6)

    def x_to_x_pressed(self):
        self.insert_text_to_input("()^()", 1)

    def ten_to_x_pressed(self):
        self.insert_text_to_input("10^()", 4)

    def e_to_x_pressed(self):
        self.insert_text_to_input("EXP^()", 5)

    def x_to_pressed(self):
        self.insert_text_to_input("^()", 2)

    def x_to_two_pressed(self):
        self.insert_text_to_input("^(2)", 4)

    def x_to_three_pressed(self):
        self.insert_text_to_input("^(3)", 4)

    def x_to_minus_one_pressed(self):
        self.insert_text_to_input("^(-1)", 5)

    def x_factorial_pressed(self):
        self.insert_text_to_input("factorial()", 10)

    def abs_pressed(self):
        self.insert_text_to_input("abs()", 4)

    def blank_root_pressed(self):
        self.insert_text_to_input("()^(1/)", 1)

    def square_root_pressed(self):
        self.insert_text_to_input("()^(1/2)", 1)

    def cube_root_pressed(self):
        self.insert_text_to_input("()^(1/3)", 1)

    def pi_pressed(self, event=None):
        self.insert_text_to_input("PI", 2)

    def tau_pressed(self, event=None):
        self.insert_text_to_input("TAU", 3)

    def golden_ration_pressed(self, event=None):
        self.insert_text_to_input("PHI", 3)

    def copy_output_to_clipboard(self, event=None):
        self.root.clipboard_clear()
        self.root.clipboard_append(self.output_text.get()[2:])

    def info_button_pressed(self, event=None):
        self.root.withdraw()
        self.info_window = tkinter.Toplevel(self.root)
        self.info_window.title("Important Information")
        self.info_window.geometry(f"421x775+{int(self.root.winfo_x() + self.root.winfo_width() / 2 - 421 / 2)}+"
                                  f"{int(self.root.winfo_y() + self.root.winfo_height() / 2 - 775 / 2)}")
        self.info_window.resizable(width=False, height=False)
        self.info_window.overrideredirect(True)
        self.info_window.protocol("WM_DELETE_WINDOW", self.nothing)
        self.info_window.focus_force()

        self.info_window.bind("<Return>", self.quit_info_window)
        self.info_window.bind("<Control-q>", self.quit_info_window)

        mainFrame = tkinter.ttk.Frame(self.info_window, padding=self.frame_pad)
        mainFrame.grid(column=0, row=0)

        ttk.Label(mainFrame, text="***** WARNING *****", justify=tkinter.CENTER, font=self.info_font).grid(column=0, row=0, pady=(self.extra_pad, 0))
        ttk.Label(mainFrame, text="This program uses eval() to evaluate the input field\nand thus is vulnerable to being exploited.",
                  justify=tkinter.CENTER, font=self.info_font).grid(column=0, row=1, pady=(0, self.extra_pad))

        ttk.Label(mainFrame, text="Keyboard Shortcuts", justify=tkinter.CENTER, font=self.info_font).grid(column=0, row=2, pady=(self.extra_pad, 0))
        ttk.Label(mainFrame, text="""Enter Key       Add input field/output field to memory
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
one is the input and the second one is base.""", justify=tkinter.LEFT, font=self.info_font).grid(column=0, row=3, pady=(0, self.extra_pad))
        # quit_info_window function is used as the root window deiconify() function
        # needs to be called after destroying the info_window, but calling info_window.destroy()
        # does not allow root.deiconify() to be called after info_window.mainloop()
        tkinter.ttk.Button(mainFrame, text="OK", width=10, command=self.quit_info_window).grid(column=0, row=4, pady=(self.extra_pad, 0))

        self.info_window.mainloop()

    def quit_info_window(self, event=None):
        self.info_window.destroy()
        self.root.deiconify()

    def quit_main_window(self, event=None):
        self.root.quit()

    def nothing(self):
        pass
