import tkinter
import tkinter.ttk
import math
import cmath
import random


def getPath(fileName):
    try:
        return os.path.join(sys._MEIPASS, fileName)
    except Exception:
        return "calculator\\resources\\" + fileName


def updateOutput(one=None, two=None, three=None, calledByCode=False, resetCurrentSelection=True):
    if not calledByCode:
        if len(inputText.get()) > 64:
            inputText.set(inputText.get()[:64])

    if resetCurrentSelection:
        global currentSelection
        currentSelection = -1

    inputCopy = inputText.get()
    inputCopy = inputCopy.replace("RANDi", "random.randint")
    inputCopy = inputCopy.replace("RANDf", "random.uniform")
    inputCopy = inputCopy.replace("sin(", "math.sin(")
    inputCopy = inputCopy.replace("cos(", "math.cos(")
    inputCopy = inputCopy.replace("tan(", "math.tan(")
    inputCopy = inputCopy.replace("sin⁻¹", "math.asin")
    inputCopy = inputCopy.replace("cos⁻¹", "math.acos")
    inputCopy = inputCopy.replace("tan⁻¹", "math.atan")
    inputCopy = inputCopy.replace("log", "math.log")
    inputCopy = inputCopy.replace("ln", "math.log")
    inputCopy = inputCopy.replace("^", "**")
    inputCopy = inputCopy.replace("PI", "math.pi")
    inputCopy = inputCopy.replace("TAU", "math.tau")
    inputCopy = inputCopy.replace("PHI", "((1 + 5 ** 0.5) / 2)")
    inputCopy = inputCopy.replace("EXP", "math.e")
    inputCopy = inputCopy.replace("factorial", "math.factorial")
    inputCopy = inputCopy.replace("ANS", str(previousAnswer))

    try:
        global currentAnswer
        currentAnswer = float(eval(inputCopy))
        outputText.set("= " + str(f"{currentAnswer:.8G}"))
    except:
        outputText.set("= 0")


def insertTextToInput(txt, pos):
    if not ((len(inputText.get()) + len(txt)) > 64):
        currPos = inputEntry.index(tkinter.INSERT)
        inputText.set(inputText.get()[:currPos] + txt + inputText.get()[currPos:])
        focusOnInput(cursorPos=currPos+pos, scrollValue=pos)
    else:
        inputEntry.focus()


def focusOnInput(event=None, cursorPos=None, scrollValue=0):
    inputEntry.focus()
    if cursorPos == None and scrollValue == 0:
        inputEntry.icursor(len(inputText.get()))
    else:
        inputEntry.icursor(cursorPos)
        inputEntry.xview_scroll(scrollValue, tkinter.UNITS)


def enterKeyPressed(event=None):
    global currentAnswer, previousAnswer, previousInputs
    previousAnswer = currentAnswer
    previousInputs.insert(0, inputText.get())
    updateOutput(calledByCode=True)


def ansButtonPressed():
    insertTextToInput("ANS", 3)


def randIntButtonPressed():
    insertTextToInput("RANDi(,)", 6)


def previousButtonPressed(event=None):
    global previousInputs, currentSelection, inputTrace
    if len(previousInputs) != 0:
        if (currentSelection + 1) < len(previousInputs):
            currentSelection += 1

        inputText.trace_remove("write", inputTrace)
        inputText.set(previousInputs[currentSelection])
        inputTrace = inputText.trace_add("write", updateOutput)
        updateOutput(calledByCode=True, resetCurrentSelection=False)
    focusOnInput()


def nextButtonPressed(event=None):
    global previousInputs, currentSelection, inputTrace
    if len(previousInputs) != 0:
        if currentSelection == -1:
            currentSelection = 0
        elif currentSelection > 0:
            currentSelection -= 1

        inputText.trace_remove("write", inputTrace)
        inputText.set(previousInputs[currentSelection])
        inputTrace = inputText.trace_add("write", updateOutput)
        updateOutput(calledByCode=True, resetCurrentSelection=False)
    focusOnInput()


def randFloatButtonPressed():
    insertTextToInput("RANDf(,)", 6)


def acButtonPressed(event=None):
    inputText.set("")
    focusOnInput()


def sinButtonPressed():
    insertTextToInput("sin()", 4)


def cosButtonPressed():
    insertTextToInput("cos()", 4)


def tanButtonPressed():
    insertTextToInput("tan()", 4)


def logButtonPressed():
    insertTextToInput("log(,)", 4)


def logTenButtonPressed():
    insertTextToInput("log(,10)", 4)


def lnButtonPressed():
    insertTextToInput("ln()", 3)


def sinInvButtonPressed():
    insertTextToInput("sin⁻¹()", 6)


def cosInvButtonPressed():
    insertTextToInput("cos⁻¹()", 6)


def tanInvButtonPressed():
    insertTextToInput("tan⁻¹()", 6)


def xToXButtonPressed():
    insertTextToInput("()^()", 1)


def tenToSomethingButtonPressed():
    insertTextToInput("10^()", 4)


def eToSomethingButtonPressed():
    insertTextToInput("EXP^()", 5)


def xToSomethingButtonPressed():
    insertTextToInput("^()", 2)


def xToTwoButtonPressed():
    insertTextToInput("^(2)", 4)


def xToThreeButtonPressed():
    insertTextToInput("^(3)", 4)


def xToMinusOneButtonPressed():
    insertTextToInput("^(-1)", 5)


def xFactorialButtonPressed():
    insertTextToInput("factorial()", 10)


def absButtonPressed():
    insertTextToInput("abs()", 4)


def rootButtonPressed():
    insertTextToInput("()^(1/)", 1)


def squareRootButtonPressed():
    insertTextToInput("()^(1/2)", 1)


def cubeRootButtonPressed():
    insertTextToInput("()^(1/3)", 1)


def piButtonPressed(event=None):
    insertTextToInput("PI", 2)


def tauButtonPressed(event=None):
    insertTextToInput("TAU", 3)


def goldenRationButtonPressed(event=None):
    insertTextToInput("PHI", 3)


def copyOutputToClipboard(event=None):
    root.clipboard_clear()
    root.clipboard_append(outputText.get()[2:])


def infoButtonPressed(event=None):
    root.withdraw()
    global infoWindow
    infoWindow = tkinter.Toplevel(root)
    infoWindow.title("Important Information")
    infoWindow.geometry(f"421x775+{int(root.winfo_x()+root.winfo_width()/2-421/2)}+{int(root.winfo_y()+root.winfo_height()/2-775/2)}")
    infoWindow.resizable(width=False, height=False)
    infoWindow.overrideredirect(True)
    infoWindow.protocol("WM_DELETE_WINDOW", nothing)
    infoWindow.focus_force()

    infoWindow.bind("<Return>", quitInfoWindow)
    infoWindow.bind("<Control-q>", quitInfoWindow)

    mainFrame = tkinter.ttk.Frame(infoWindow, padding=framePad)
    mainFrame.grid(column=0, row=0)

    tkinter.ttk.Label(mainFrame,
                      text="***** WARNING *****",
                      justify=tkinter.CENTER,
                      font=infoWindowFont).grid(column=0, row=0, pady=(extraPad, 0))
    tkinter.ttk.Label(mainFrame,
                      text="""This program uses eval() to evaluate the input field
and thus is vulnerable to being exploited.""",
                      justify=tkinter.CENTER,
                      font=infoWindowFont).grid(column=0, row=1, pady=(0, extraPad))

    tkinter.ttk.Label(mainFrame,
                      text="Keyboard Shortcuts",
                      justify=tkinter.CENTER,
                      font=infoWindowFont).grid(column=0, row=2, pady=(extraPad, 0))
    tkinter.ttk.Label(mainFrame,
                      text="""Enter Key       Add input field/output field to memory
CTRL + E        Move cursor focus to input field
CTRL + I        Show info window
CTRL + Up     Retrive older input from memory
CTRL + Down    Retrive newer input from memory
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
one is the input and the second one is base.""",
                      justify=tkinter.LEFT,
                      font=infoWindowFont).grid(column=0, row=3, pady=(0, extraPad))
    # quitInfoWindow function is used as the root window deiconify() function
    # needs to be called after destroying the infoWindow, but calling infoWindow.destroy()
    # does not allow root.deiconify() to be called after infoWindow.mainloop()
    tkinter.ttk.Button(mainFrame,
                       text="OK",
                       width=10,
                       command=quitInfoWindow).grid(column=0, row=4, pady=(extraPad, 0))

    infoWindow.mainloop()


def quitInfoWindow(event=None):
    infoWindow.destroy()
    root.deiconify()


def nothing():
    pass


def quitMainWindow(event=None):
    root.quit()


if __name__ == "__main__":
    inputFont = ("Segoe UI", 32, "normal")
    outputFont = ("Segoe UI", 64, "normal")
    infoWindowFont = ("Segoe UI", 12, "normal")
    btnpad = 5
    extraPad = 15
    framePad = 15

    currentAnswer = "0"
    previousAnswer = "0"
    previousInputs = []
    currentSelection = -1

    root = tkinter.Tk()
    root.title("Calculator")
    root.geometry(f"856x834+{int(root.winfo_screenwidth()/2-834/2)}+{int(root.winfo_screenheight()/2-830/2)}")
    root.resizable(width=False, height=False)
    root.iconphoto(True, tkinter.PhotoImage(file=getPath("app.png")))
    root.tk.call("source", getPath("theme\\forest-dark.tcl"))
    tkinter.ttk.Style().theme_use("forest-dark")

    inputText = tkinter.StringVar(value="")
    outputText = tkinter.StringVar(value="= 0")

    inputTrace = inputText.trace_add("write", updateOutput)
    root.bind("<Return>", enterKeyPressed)
    root.bind("<Control-e>", focusOnInput)
    root.bind("<Control-c>", copyOutputToClipboard)
    root.bind("<Control-i>", infoButtonPressed)
    root.bind("<Control-Up>", previousButtonPressed)
    root.bind("<Control-Down>", nextButtonPressed)
    root.bind("<Control-Delete>", acButtonPressed)
    root.bind("<Control-p>", piButtonPressed)
    root.bind("<Control-t>", tauButtonPressed)
    root.bind("<Control-g>", goldenRationButtonPressed)
    root.bind("<Control-q>", quitMainWindow)

    ansImg = tkinter.PhotoImage(file=getPath("ans.png"))
    randIntImg = tkinter.PhotoImage(file=getPath("randInt.png"))
    previousImg = tkinter.PhotoImage(file=getPath("previous.png"))
    infoImg = tkinter.PhotoImage(file=getPath("info.png"))
    nextImg = tkinter.PhotoImage(file=getPath("next.png"))
    randfloatImg = tkinter.PhotoImage(file=getPath("randfloat.png"))
    acImg = tkinter.PhotoImage(file=getPath("ac.png"))

    sinImg = tkinter.PhotoImage(file=getPath("sin.png"))
    cosImg = tkinter.PhotoImage(file=getPath("cos.png"))
    tanImg = tkinter.PhotoImage(file=getPath("tan.png"))
    logImg = tkinter.PhotoImage(file=getPath("log.png"))
    logTenImg = tkinter.PhotoImage(file=getPath("log10.png"))
    lnImg = tkinter.PhotoImage(file=getPath("ln.png"))

    sinInvImg = tkinter.PhotoImage(file=getPath("sinInv.png"))
    cosInvImg = tkinter.PhotoImage(file=getPath("cosInv.png"))
    tanInvImg = tkinter.PhotoImage(file=getPath("tanInv.png"))
    xToXImg = tkinter.PhotoImage(file=getPath("x^x.png"))
    tenToXImg = tkinter.PhotoImage(file=getPath("10^x.png"))
    eToXImg = tkinter.PhotoImage(file=getPath("e^x.png"))

    xToImg = tkinter.PhotoImage(file=getPath("x^.png"))
    xToTwoImg = tkinter.PhotoImage(file=getPath("x^2.png"))
    xToThreeImg = tkinter.PhotoImage(file=getPath("x^3.png"))
    xToMinusOneImg = tkinter.PhotoImage(file=getPath("x^-1.png"))
    xFactorialImg = tkinter.PhotoImage(file=getPath("x!.png"))
    absImg = tkinter.PhotoImage(file=getPath("abs.png"))

    rootImg = tkinter.PhotoImage(file=getPath("root.png"))
    squareRootImg = tkinter.PhotoImage(file=getPath("sqrt.png"))
    cubeRootImg = tkinter.PhotoImage(file=getPath("cube root.png"))
    piImg = tkinter.PhotoImage(file=getPath("pi.png"))
    tauImg = tkinter.PhotoImage(file=getPath("tau.png"))
    goldenRatioImg = tkinter.PhotoImage(file=getPath("golden ratio.png"))

    entryFrame = tkinter.ttk.Frame(root, padding=framePad)
    entryFrame.grid(column=0, row=0)

    inputEntry = tkinter.ttk.Entry(entryFrame,
                                   width=34,
                                   textvariable=inputText,
                                   font=inputFont)
    inputEntry.grid(column=0, row=0, pady=(0, 20))

    outputEntry = tkinter.ttk.Entry(entryFrame,
                                    width=17,
                                    textvariable=outputText,
                                    justify=tkinter.RIGHT,
                                    state="readonly",
                                    font=outputFont).grid(column=0, row=1)

    topFrame = tkinter.ttk.Frame(root, padding=framePad)
    topFrame.grid(column=0, row=1)

    tkinter.ttk.Button(topFrame, image=ansImg, command=ansButtonPressed).grid(column=0, row=0, padx=btnpad)
    tkinter.ttk.Button(topFrame, image=randIntImg, command=randIntButtonPressed).grid(column=1, row=0, padx=btnpad)
    tkinter.ttk.Button(topFrame, image=previousImg, command=previousButtonPressed).grid(column=2, row=0, padx=(extraPad+9, btnpad))
    tkinter.ttk.Button(topFrame, image=infoImg, command=infoButtonPressed).grid(column=3, row=0, padx=btnpad)
    tkinter.ttk.Button(topFrame, image=nextImg, command=nextButtonPressed).grid(column=4, row=0, padx=(btnpad, extraPad+9))
    tkinter.ttk.Button(topFrame, image=randfloatImg, command=randFloatButtonPressed).grid(column=5, row=0, padx=btnpad)
    tkinter.ttk.Button(topFrame, image=acImg, command=acButtonPressed).grid(column=6, row=0, padx=btnpad)

    mainFrame = tkinter.ttk.Frame(root, padding=framePad)
    mainFrame.grid(column=0, row=2)

    tkinter.ttk.Button(mainFrame, image=sinImg, command=sinButtonPressed).grid(column=0, row=0, padx=btnpad, pady=(extraPad, btnpad))
    tkinter.ttk.Button(mainFrame, image=cosImg, command=cosButtonPressed).grid(column=1, row=0, padx=btnpad, pady=(extraPad, btnpad))
    tkinter.ttk.Button(mainFrame, image=tanImg, command=tanButtonPressed).grid(column=2, row=0, padx=(btnpad, extraPad), pady=(extraPad, btnpad))
    tkinter.ttk.Button(mainFrame, image=logImg, command=logButtonPressed).grid(column=3, row=0, padx=(extraPad, btnpad), pady=(extraPad, btnpad))
    tkinter.ttk.Button(mainFrame, image=logTenImg, command=logTenButtonPressed).grid(column=4, row=0, padx=btnpad, pady=(extraPad, btnpad))
    tkinter.ttk.Button(mainFrame, image=lnImg, command=lnButtonPressed).grid(column=5, row=0, padx=btnpad, pady=(extraPad, btnpad))

    tkinter.ttk.Button(mainFrame, image=sinInvImg, command=sinInvButtonPressed).grid(column=0, row=1, padx=btnpad, pady=(btnpad, extraPad))
    tkinter.ttk.Button(mainFrame, image=cosInvImg, command=cosInvButtonPressed).grid(column=1, row=1, padx=btnpad, pady=(btnpad, extraPad))
    tkinter.ttk.Button(mainFrame, image=tanInvImg, command=tanInvButtonPressed).grid(column=2, row=1, padx=(btnpad, extraPad), pady=(btnpad, extraPad))
    tkinter.ttk.Button(mainFrame, image=xToXImg, command=xToXButtonPressed).grid(column=3, row=1, padx=(extraPad, btnpad), pady=(btnpad, extraPad))
    tkinter.ttk.Button(mainFrame, image=tenToXImg, command=tenToSomethingButtonPressed).grid(column=4, row=1, padx=btnpad, pady=(btnpad, extraPad))
    tkinter.ttk.Button(mainFrame, image=eToXImg, command=eToSomethingButtonPressed).grid(column=5, row=1, padx=btnpad, pady=(btnpad, extraPad))

    tkinter.ttk.Button(mainFrame, image=xToImg, command=xToSomethingButtonPressed).grid(column=0, row=2, padx=btnpad, pady=extraPad)
    tkinter.ttk.Button(mainFrame, image=xToTwoImg, command=xToTwoButtonPressed).grid(column=1, row=2, padx=btnpad, pady=extraPad)
    tkinter.ttk.Button(mainFrame, image=xToThreeImg, command=xToThreeButtonPressed).grid(column=2, row=2, padx=(btnpad, extraPad), pady=extraPad)
    tkinter.ttk.Button(mainFrame, image=xToMinusOneImg, command=xToMinusOneButtonPressed).grid(column=3, row=2, padx=(extraPad, btnpad), pady=extraPad)
    tkinter.ttk.Button(mainFrame, image=xFactorialImg, command=xFactorialButtonPressed).grid(column=4, row=2, padx=btnpad, pady=extraPad)
    tkinter.ttk.Button(mainFrame, image=absImg, command=absButtonPressed).grid(column=5, row=2, padx=btnpad, pady=extraPad)

    tkinter.ttk.Button(mainFrame, image=rootImg, command=rootButtonPressed).grid(column=0, row=3, padx=btnpad, pady=(extraPad, btnpad))
    tkinter.ttk.Button(mainFrame, image=squareRootImg, command=squareRootButtonPressed).grid(column=1, row=3, padx=btnpad, pady=(extraPad, btnpad))
    tkinter.ttk.Button(mainFrame, image=cubeRootImg, command=cubeRootButtonPressed).grid(column=2, row=3, padx=(btnpad, extraPad), pady=(extraPad, btnpad))
    tkinter.ttk.Button(mainFrame, image=piImg, command=piButtonPressed).grid(column=3, row=3, padx=(extraPad, btnpad), pady=(extraPad, btnpad))
    tkinter.ttk.Button(mainFrame, image=tauImg, command=tauButtonPressed).grid(column=4, row=3, padx=btnpad, pady=(extraPad, btnpad))
    tkinter.ttk.Button(mainFrame, image=goldenRatioImg, command=goldenRationButtonPressed).grid(column=5, row=3, padx=btnpad, pady=(extraPad, btnpad))

    focusOnInput()

    root.mainloop()
