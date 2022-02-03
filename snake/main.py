import os
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"  # noqa
import sys
import time
import random
import pygame


def createBlankWindow():
    blankWindow = pygame.Surface((windowWidth, windowHeight))
    blankWindow.fill(windowBgDark)
    startForX = squareSize

    for y in range(infoHeight, windowHeight, squareSize):
        if (y-infoHeight) % (squareSize * 2):
            startForX = squareSize
        else:
            startForX = 0
        for x in range(startForX, windowWidth, squareSize*2):
            pygame.draw.rect(blankWindow, windowBgLight, (x, y, squareSize, squareSize))

    pygame.draw.rect(blankWindow, infoBg, (0, 0, windowWidth, infoHeight))

    return blankWindow


def createMenus(txt, txtPosX, txtPosYTitle, txtPosYBody, txtPosYBodyDifference, titleSize, bodySize, selectionStart, selectionEnd):
    fonts = []
    fonts.append(pygame.font.SysFont(mainFont, titleSize))
    for i in range(1, len(txt)):
        fonts.append(pygame.font.SysFont(mainFont, bodySize))

    output = []

    for i in range(selectionStart, selectionEnd+1):
        temp = pygame.Surface((windowWidth, windowHeight))
        temp.fill(windowBgDark)
        for j in range(len(txt)):
            if j == i:
                if j == 0:
                    temp.blit(fonts[0].render(txt[0], True, selectedTextColour), (txtPosX, txtPosYTitle))
                else:
                    temp.blit(fonts[j].render(txt[j], True, selectedTextColour), (txtPosX, txtPosYBody+txtPosYBodyDifference*j))
            else:
                if j == 0:
                    temp.blit(fonts[0].render(txt[0], True, textColour), (txtPosX, txtPosYTitle))
                else:
                    temp.blit(fonts[j].render(txt[j], True, textColour), (txtPosX, txtPosYBody+txtPosYBodyDifference*j))
        output.append(temp)

    return output


def createInfoMenu():
    fontOne = pygame.font.SysFont(mainFont, 72)
    fontTwo = pygame.font.SysFont(mainFont, 32)

    lineOne = "INFORMATION"
    lineTwo = "WASD = SNAKE AND MENU NAVIGATION"
    lineThree = "K = SPEED UP SNAKE"
    lineFour = "ESC = PAUSE/UNPAUSE/GO BACK"
    lineFive = "R = RESTART WHEN GAMER OVER"
    lineSix = "Q = QUIT TO MAIN MENU WHEN GAME OVER"
    lineSeven = "CTRL + Q = QUIT PROGRAM"
    lineEight = "BACK TO MAIN MENU"

    infoMenu = pygame.Surface((windowWidth, windowHeight))
    infoMenu.fill(windowBgDark)
    infoMenu.blit(fontOne.render(lineOne, True, textColour), (50, 50))
    infoMenu.blit(fontTwo.render(lineTwo, True, textColour), (50, 150))
    infoMenu.blit(fontTwo.render(lineThree, True, textColour), (50, 200))
    infoMenu.blit(fontTwo.render(lineFour, True, textColour), (50, 250))
    infoMenu.blit(fontTwo.render(lineFive, True, textColour), (50, 300))
    infoMenu.blit(fontTwo.render(lineSix, True, textColour), (50, 350))
    infoMenu.blit(fontTwo.render(lineSeven, True, textColour), (50, 400))
    infoMenu.blit(fontTwo.render(lineEight, True, selectedTextColour), (50, 650))

    return infoMenu


def createGameOverMenu():
    fontOne = pygame.font.SysFont(mainFont, 72)
    fontTwo = pygame.font.SysFont(mainFont, 48)

    lineOne = "GAME OVER"
    lineTwo = "RESTART"
    lineThree = "QUIT"

    one = pygame.Surface((350, 250))
    one.fill(infoBg)
    one.blit(fontOne.render(lineOne, True, textColour), (25, 25))
    one.blit(fontTwo.render(lineTwo, True, selectedTextColour), (100, 125))
    one.blit(fontTwo.render(lineThree, True, textColour), (133, 200))

    two = pygame.Surface((350, 250))
    two.fill(infoBg)
    two.blit(fontOne.render(lineOne, True, textColour), (25, 25))
    two.blit(fontTwo.render(lineTwo, True, textColour), (100, 125))
    two.blit(fontTwo.render(lineThree, True, selectedTextColour), (133, 200))

    return [one, two]


def displayMainMenu():
    currentSelection = 0
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.display.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if (event.key == pygame.K_q and pygame.key.get_mods() & pygame.KMOD_CTRL) or event.key == pygame.K_q:
                    pygame.display.quit()
                    sys.exit()
                elif event.key == pygame.K_UP or event.key == pygame.K_w:
                    if currentSelection == 0:
                        currentSelection = 5
                    else:
                        currentSelection -= 1
                elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    if currentSelection == 5:
                        currentSelection = 0
                    else:
                        currentSelection += 1
                elif event.key == pygame.K_RETURN:
                    if currentSelection == 0:
                        return
                    elif currentSelection == 1:
                        displayMapSizeOptionsMenu()
                    elif currentSelection == 2:
                        displaySnakeSpeedOptionsMenu()
                    elif currentSelection == 3:
                        displayAppleAmountOptionsMenu()
                    elif currentSelection == 4:
                        displayInfoMenu()
                    elif currentSelection == 5:
                        pygame.display.quit()
                        sys.exit()

        window.blit(mainMenus[currentSelection], (0, 0))

        pygame.display.update()


def displayMapSizeOptionsMenu():
    global squareSize, blankWindow
    if squareSize == 64:
        currentSelection = 0
    elif squareSize == 32:
        currentSelection = 1
    elif squareSize == 16:
        currentSelection = 2
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.display.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q and pygame.key.get_mods() & pygame.KMOD_CTRL:
                    pygame.display.quit()
                    sys.exit()
                elif event.key == pygame.K_UP or event.key == pygame.K_w:
                    if currentSelection == 0:
                        currentSelection = 3
                    else:
                        currentSelection -= 1
                elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    if currentSelection == 3:
                        currentSelection = 0
                    else:
                        currentSelection += 1
                elif event.key == pygame.K_RETURN:
                    if currentSelection == 0:
                        squareSize = 64
                    elif currentSelection == 1:
                        squareSize = 32
                    elif currentSelection == 2:
                        squareSize = 16
                    elif currentSelection == 3:
                        pass
                    blankWindow = createBlankWindow()
                    return
                elif event.key == pygame.K_ESCAPE:
                    return

        window.blit(mapSizeMenus[currentSelection], (0, 0))

        pygame.display.update()


def displaySnakeSpeedOptionsMenu():
    global gameSpeed
    if gameSpeed == 5:
        currentSelection = 0
    elif gameSpeed == 10:
        currentSelection = 1
    elif gameSpeed == 15:
        currentSelection = 2
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.display.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q and pygame.key.get_mods() & pygame.KMOD_CTRL:
                    pygame.display.quit()
                    sys.exit()
                elif event.key == pygame.K_UP or event.key == pygame.K_w:
                    if currentSelection == 0:
                        currentSelection = 3
                    else:
                        currentSelection -= 1
                elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    if currentSelection == 3:
                        currentSelection = 0
                    else:
                        currentSelection += 1
                elif event.key == pygame.K_RETURN:
                    if currentSelection == 0:
                        gameSpeed = 5
                        return
                    elif currentSelection == 1:
                        gameSpeed = 10
                        return
                    elif currentSelection == 2:
                        gameSpeed = 15
                        return
                    elif currentSelection == 3:
                        return
                elif event.key == pygame.K_ESCAPE:
                    return

        window.blit(snakeSpeedMenus[currentSelection], (0, 0))

        pygame.display.update()


def displayAppleAmountOptionsMenu():
    global numberOfApples
    if numberOfApples == 1:
        currentSelection = 0
    elif numberOfApples == 3:
        currentSelection = 1
    elif numberOfApples == 5:
        currentSelection = 2
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.display.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q and pygame.key.get_mods() & pygame.KMOD_CTRL:
                    pygame.display.quit()
                    sys.exit()
                elif event.key == pygame.K_UP or event.key == pygame.K_w:
                    if currentSelection == 0:
                        currentSelection = 3
                    else:
                        currentSelection -= 1
                elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    if currentSelection == 3:
                        currentSelection = 0
                    else:
                        currentSelection += 1
                elif event.key == pygame.K_RETURN:
                    if currentSelection == 0:
                        numberOfApples = 1
                        return
                    elif currentSelection == 1:
                        numberOfApples = 3
                        return
                    elif currentSelection == 2:
                        numberOfApples = 5
                        return
                    elif currentSelection == 3:
                        return
                elif event.key == pygame.K_ESCAPE:
                    return

        window.blit(appleAmountMenus[currentSelection], (0, 0))

        pygame.display.update()


def displayInfoMenu():
    window.blit(infoMenu, (0, 0))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.display.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q and pygame.key.get_mods() & pygame.KMOD_CTRL:
                    pygame.display.quit()
                    sys.exit()
                elif event.key == pygame.K_RETURN or event.key == pygame.K_ESCAPE:
                    return

        pygame.display.update()


def displayGameOverMenu():
    currentSelection = 0
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.display.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q and pygame.key.get_mods() & pygame.KMOD_CTRL:
                    pygame.display.quit()
                    sys.exit()
                elif event.key == pygame.K_r:
                    return False
                elif event.key == pygame.K_q:
                    return True
                elif event.key == pygame.K_UP or event.key == pygame.K_w:
                    if currentSelection == 0:
                        currentSelection = 1
                    else:
                        currentSelection -= 1
                elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    if currentSelection == 1:
                        currentSelection = 0
                    else:
                        currentSelection += 1
                elif event.key == pygame.K_RETURN:
                    if currentSelection == 0:
                        return False
                    elif currentSelection == 1:
                        return True

        window.blit(gameOverMenu[currentSelection], (145, 323))

        pygame.display.update()


def gameOver():
    for x, y in zip(pointsX, pointsY):
        if x < 0 or x > windowWidth - squareSize:
            return True
        if y < infoHeight or y > windowHeight - squareSize:
            return True

    for i in range(1, len(pointsX)):
        if pointsX[i] == pointsX[0] and pointsY[i] == pointsY[0]:
            return True
    return False


def gameIsPaused():
    global elapsedTime, startTime
    elapsedTime += time.time() - startTime

    colourStep = (colourMax - colourMin)/len(pointsX)
    for i in range(len(applePositions)):
        pygame.draw.rect(window, (colourMax, colourMax, colourMax), (applePositions[i][0], applePositions[i][1], squareSize, squareSize))
    for i in range(0, len(pointsX)):
        pygame.draw.rect(window, (colourMax-colourStep*i, colourMax-colourStep*i, colourMax-colourStep*i), (pointsX[i], pointsY[i], squareSize, squareSize))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.display.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q and pygame.key.get_mods() & pygame.KMOD_CTRL:
                    pygame.display.quit()
                    sys.exit()
                elif event.key == pygame.K_ESCAPE:
                    startTime = time.time()
                    return

        pygame.display.update()


def displaySnake():
    global highScore
    highScore = max(highScore, len(pointsX)-3)
    colourStep = (colourMax - colourMin)/len(pointsX)
    fontOne = pygame.font.SysFont(mainFont, 48)
    fontTwo = pygame.font.SysFont(mainFont, 32)

    window.blit(blankWindow, (0, 0))

    currentScoreString = fontOne.render(f"Score: {len(pointsX)-3}", True, textColour)
    highScoreString = fontTwo.render(f"High Score: {highScore}", True, textColour)
    elapsedTimeString = fontTwo.render("Time Elapsed: " + time.strftime("%M:%S", time.gmtime(time.time()-startTime+elapsedTime)), True, textColour)
    window.blit(currentScoreString, (currentScoreString.get_rect(center=(windowWidth/2, 25))))
    window.blit(highScoreString, (highScoreString.get_rect(center=(windowWidth/2, 65))))
    window.blit(elapsedTimeString, (elapsedTimeString.get_rect(center=(windowWidth/2, 100))))

    for i in range(len(applePositions)):
        pygame.draw.rect(window, (colourMax, 0, 0), (applePositions[i][0], applePositions[i][1], squareSize, squareSize))

    for i in range(len(pointsX)):
        pygame.draw.rect(window, (0, colourMax-colourStep*i, 0), (pointsX[i], pointsY[i], squareSize, squareSize))


def updateSnakePosition():
    if snakeDirection == "UP":
        pointsX.insert(0, pointsX[0])
        pointsY.insert(0, pointsY[0] - squareSize)
        pointsX.pop()
        pointsY.pop()

    elif snakeDirection == "DOWN":
        pointsX.insert(0, pointsX[0])
        pointsY.insert(0, pointsY[0] + squareSize)
        pointsX.pop()
        pointsY.pop()

    elif snakeDirection == "LEFT":
        pointsX.insert(0, pointsX[0] - squareSize)
        pointsY.insert(0, pointsY[0])
        pointsX.pop()
        pointsY.pop()

    else:  # RIGHT
        pointsX.insert(0, pointsX[0] + squareSize)
        pointsY.insert(0, pointsY[0])
        pointsX.pop()
        pointsY.pop()


def checkForApple():
    for i in range(len(applePositions)):
        if (pointsX[0] == applePositions[i][0] and pointsY[0] == applePositions[i][1]):
            pointsX.append(pointsX[-1])
            pointsY.append(pointsY[-1])
            applePositions.pop(i)
            createNewApplePositions()


def createNewApplePositions():
    for i in range(numberOfApples-len(applePositions)):
        currentApple = [0, 0]
        applePositionInvalid = True
        while applePositionInvalid:
            currentApple[0] = random.randrange(0, windowWidth, squareSize)
            currentApple[1] = random.randrange(infoHeight, windowHeight, squareSize)
            applePositionInvalid = False
            for x, y in zip(pointsX, pointsY):
                if (currentApple[0] == x and currentApple[1] == y):
                    applePositionInvalid = True
            for anApple in applePositions:
                if (currentApple[0] == anApple[0] and currentApple[1] == anApple[0]):
                    applePositionInvalid = True
        applePositions.append(currentApple)
    return applePositions


if __name__ == "__main__":
    highScore = 0
    squareSize = 32
    gameSpeed = 10
    numberOfApples = 3

    windowSize = 640
    infoHeight = 128

    windowWidth = windowSize
    windowHeight = windowSize + infoHeight
    windowMidX = int(windowWidth / 2)
    windowMidY = int((windowHeight - infoHeight) / 2) + infoHeight

    infoBg = (8, 8, 8)
    windowBgDark = (16, 16, 16)
    windowBgLight = (24, 24, 24)

    colourMin = 32
    colourMax = 196

    mainFont = "Video Game Font"
    textColour = (255, 255, 255)
    selectedTextColour = (0, 128, 156)

    pygame.init()
    pygame.display.set_caption("Snake")
    pygame.display.set_icon(pygame.image.load("snake\\resources\\app.ico"))
    window = pygame.display.set_mode((windowWidth, windowHeight))
    clock = pygame.time.Clock()

    blankWindow = createBlankWindow()
    mainMenus = createMenus(["PLAY", "MAP SIZE", "SNAKE SPEED", "NUMBER OF APPLES", "INFO", "QUIT"], 50, 50, 200, 100, 128, 48, 0, 5)
    mapSizeMenus = createMenus(["MAP SIZES", "10 x 10", "20 x 20", "30 x 30", "BACK TO MAIN MENU"], 50, 50, 150, 100, 72, 48, 1, 4)
    snakeSpeedMenus = createMenus(["SNAKE SPEED", "5", "10", "15", "BACK TO MAIN MENU"], 50, 50, 150, 100, 72, 48, 1, 4)
    appleAmountMenus = createMenus(["NUMBER OF APPLES", "1", "3", "5", "BACK TO MAIN MENU"], 50, 50, 150, 100, 72, 48, 1, 4)
    infoMenu = createInfoMenu()
    gameOverMenu = createGameOverMenu()

    goToMainMenu = True
    programIsRunning = True
    while programIsRunning:
        if goToMainMenu:
            displayMainMenu()

        snakeDirection = "RIGHT"
        pointsX = [windowMidX, windowMidX - squareSize, windowMidX - squareSize * 2]
        pointsY = [windowMidY, windowMidY, windowMidY]
        applePositions = []
        applePositions = createNewApplePositions()
        elapsedTime = 0.0
        startTime = time.time()

        while not gameOver():
            displaySnake()

            if pygame.key.get_pressed()[pygame.K_k]:
                clock.tick(gameSpeed * 2)
            else:
                clock.tick(gameSpeed)

            inputReceived = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.display.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q and pygame.key.get_mods() & pygame.KMOD_CTRL:
                        pygame.display.quit()
                        sys.exit()
                    elif event.key == pygame.K_ESCAPE:
                        gameIsPaused()
                    elif (event.key == pygame.K_UP or event.key == pygame.K_w) and snakeDirection != "DOWN" and not inputReceived:
                        snakeDirection = "UP"
                        inputReceived = True
                    elif (event.key == pygame.K_DOWN or event.key == pygame.K_s) and snakeDirection != "UP" and not inputReceived:
                        snakeDirection = "DOWN"
                        inputReceived = True
                    elif (event.key == pygame.K_LEFT or event.key == pygame.K_a) and snakeDirection != "RIGHT" and not inputReceived:
                        snakeDirection = "LEFT"
                        inputReceived = True
                    elif (event.key == pygame.K_RIGHT or event.key == pygame.K_d) and snakeDirection != "LEFT" and not inputReceived:
                        snakeDirection = "RIGHT"
                        inputReceived = True

            updateSnakePosition()
            checkForApple()

            pygame.display.update()

        goToMainMenu = displayGameOverMenu()
