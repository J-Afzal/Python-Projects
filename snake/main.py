import os
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"  # noqa
import sys
import time
import random
import pygame


def createBlankWindow():
    blankWindow = pygame.Surface((windowWidth, windowHeight))
    blankWindow.fill(windowBgDark)

    drawLightRect = False
    for y in range(infoHeight, windowHeight, squareSize):
        for x in range(0, windowWidth, squareSize):
            if drawLightRect:
                pygame.draw.rect(blankWindow, windowBgLight, (x, y, squareSize, squareSize))
            drawLightRect = not drawLightRect
        drawLightRect = not drawLightRect

    pygame.draw.rect(blankWindow, menuWindowBg, (0, 0, windowWidth, infoHeight))

    return blankWindow


def createMenus(txt, txtPosX, txtPosYTitle, txtPosYBody, txtPosYBodyDifference, titleSize, bodySize, selectionStart, selectionEnd):
    fonts = []
    fonts.append(pygame.font.SysFont(mainFont, titleSize))
    for i in range(1, len(txt)):
        fonts.append(pygame.font.SysFont(mainFont, bodySize))

    output = []

    for i in range(selectionStart, selectionEnd+1):
        temp = pygame.Surface((windowWidth, windowHeight))
        temp.fill(menuWindowBg)
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
    fontThree = pygame.font.SysFont(mainFont, 48)

    lineOne = "INFORMATION"
    lineTwo = "WASD = SNAKE AND MENU NAVIGATION"
    lineThree = "K = SPEED UP SNAKE"
    lineFour = "ESC = PAUSE/UNPAUSE/GO BACK"
    lineFive = "H = HIDE GAME OVER MESSAGE"
    lineSix = "R = RESTART WHEN GAMER OVER"
    lineSeven = "Q = QUIT TO MAIN MENU"
    lineEight = "CTRL + Q = QUIT PROGRAM"
    lineNine = "BACK TO MAIN MENU"

    infoMenu = pygame.Surface((windowWidth, windowHeight))
    infoMenu.fill(menuWindowBg)
    infoMenu.blit(fontOne.render(lineOne, True, textColour), (50, 50))
    infoMenu.blit(fontTwo.render(lineTwo, True, textColour), (50, 150))
    infoMenu.blit(fontTwo.render(lineThree, True, textColour), (50, 200))
    infoMenu.blit(fontTwo.render(lineFour, True, textColour), (50, 250))
    infoMenu.blit(fontTwo.render(lineFive, True, textColour), (50, 300))
    infoMenu.blit(fontTwo.render(lineSix, True, textColour), (50, 350))
    infoMenu.blit(fontTwo.render(lineSeven, True, textColour), (50, 400))
    infoMenu.blit(fontTwo.render(lineEight, True, textColour), (50, 450))
    infoMenu.blit(fontThree.render(lineNine, True, selectedTextColour), (50, 700))

    return infoMenu


def createGameOverMenu():
    gameOverText = pygame.font.SysFont(mainFont, gameOverFontSize).render("GAME OVER", True, textColour)
    rematchTextSelected = pygame.font.SysFont(mainFont, gameOverOptionsFontSize).render("REMATCH", True, selectedTextColour)
    rematchText = pygame.font.SysFont(mainFont, gameOverOptionsFontSize).render("REMATCH", True, textColour)
    quitTextSelected = pygame.font.SysFont(mainFont, gameOverOptionsFontSize).render("QUIT", True, selectedTextColour)
    quitText = pygame.font.SysFont(mainFont, gameOverOptionsFontSize).render("QUIT", True, textColour)

    one = pygame.Surface((gameOverWidth, gameOverHeight))
    one.fill(menuWindowBg)
    one.blit(gameOverText, gameOverText.get_rect(center=(gameOverWidth/2, 50)))
    one.blit(rematchTextSelected, rematchTextSelected.get_rect(center=(gameOverWidth/2, gameOverHeight-115)))
    one.blit(quitText, quitText.get_rect(center=(gameOverWidth/2, gameOverHeight-35)))

    two = pygame.Surface((gameOverWidth, gameOverHeight))
    two.fill(menuWindowBg)
    two.blit(gameOverText, gameOverText.get_rect(center=(gameOverWidth/2, 50)))
    two.blit(rematchText, rematchText.get_rect(center=(gameOverWidth/2, gameOverHeight-115)))
    two.blit(quitTextSelected, quitTextSelected.get_rect(center=(gameOverWidth/2, gameOverHeight-35)))

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
                    elif currentSelection == 1:
                        gameSpeed = 10
                    elif currentSelection == 2:
                        gameSpeed = 15
                    elif currentSelection == 3:
                        pass
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
                    elif currentSelection == 1:
                        numberOfApples = 3
                    elif currentSelection == 2:
                        numberOfApples = 5
                    elif currentSelection == 3:
                        pass
                    return
                elif event.key == pygame.K_ESCAPE:
                    return

        window.blit(appleAmountMenus[currentSelection], (0, 0))

        pygame.display.update()


def displayInfoMenu():
    window.blit(infoMenu, (0, 0))
    pygame.display.update()
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

        if not pygame.key.get_pressed()[pygame.K_h]:
            window.blit(gameOverMenu[currentSelection], (windowSize/2-gameOverWidth/2, windowSize/2-gameOverHeight/2+infoHeight))
            pygame.display.update()
        else:
            displaySnake()


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

    pygame.display.update()

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

    pygame.display.update()


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

    checkForApple()


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
    windowSize = 640
    infoHeight = 128
    windowWidth = windowSize
    windowHeight = windowSize + infoHeight
    windowMidX = int(windowWidth / 2)
    windowMidY = int((windowHeight - infoHeight) / 2) + infoHeight

    pygame.init()
    pygame.display.set_caption("Snake")
    pygame.display.set_icon(pygame.image.load("snake\\resources\\app.ico"))
    window = pygame.display.set_mode((windowWidth, windowHeight))
    clock = pygame.time.Clock()

    squareSize = 32
    gameSpeed = 10
    numberOfApples = 3

    windowBgDark = (16, 16, 16)
    windowBgLight = (24, 24, 24)
    menuWindowBg = (8, 8, 8)

    colourMin = 32
    colourMax = 196

    mainFont = "Video Game Font"
    textColour = (255, 255, 255)
    selectedTextColour = (0, 128, 156)

    gameOverWidth = 350
    gameOverHeight = 250
    gameOverFontSize = 72
    gameOverOptionsFontSize = 48

    highScore = 0

    blankWindow = createBlankWindow()
    mainMenus = createMenus(["PLAY SNAKE", "MAP SIZE", "SNAKE SPEED", "NUMBER OF APPLES", "INFO", "QUIT"], 50, 50, 200, 100, 110, 48, 0, 5)
    mapSizeMenus = createMenus(["MAP SIZES", "10 x 10", "20 x 20", "40 x 40", "BACK TO MAIN MENU"], 50, 50, 300, 100, 72, 48, 1, 4)
    snakeSpeedMenus = createMenus(["SNAKE SPEED", "5", "10", "15", "BACK TO MAIN MENU"], 50, 50, 300, 100, 72, 48, 1, 4)
    appleAmountMenus = createMenus(["NUMBER OF APPLES", "1", "3", "5", "BACK TO MAIN MENU"], 50, 50, 300, 100, 72, 48, 1, 4)
    infoMenu = createInfoMenu()
    gameOverMenu = createGameOverMenu()

    goToMainMenu = True
    while True:
        if goToMainMenu:
            displayMainMenu()

        snakeDirection = "RIGHT"
        pointsX = [windowMidX, windowMidX - squareSize, windowMidX - squareSize * 2]
        pointsY = [windowMidY, windowMidY, windowMidY]
        applePositions = []
        applePositions = createNewApplePositions()
        elapsedTime = 0.0
        startTime = time.time()

        goImmediatelyToMainMenu = False
        while not gameOver() and not goImmediatelyToMainMenu:
            if pygame.key.get_pressed()[pygame.K_k]:
                clock.tick(gameSpeed * 2)
            else:
                clock.tick(gameSpeed)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.display.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q and pygame.key.get_mods() & pygame.KMOD_CTRL:
                        pygame.display.quit()
                        sys.exit()
                    elif event.key == pygame.K_q:
                        goImmediatelyToMainMenu = True
                        goToMainMenu = True
                    elif event.key == pygame.K_ESCAPE:
                        gameIsPaused()
                    elif (event.key == pygame.K_UP or event.key == pygame.K_w) and snakeDirection != "DOWN":
                        snakeDirection = "UP"
                    elif (event.key == pygame.K_DOWN or event.key == pygame.K_s) and snakeDirection != "UP":
                        snakeDirection = "DOWN"
                    elif (event.key == pygame.K_LEFT or event.key == pygame.K_a) and snakeDirection != "RIGHT":
                        snakeDirection = "LEFT"
                    elif (event.key == pygame.K_RIGHT or event.key == pygame.K_d) and snakeDirection != "LEFT":
                        snakeDirection = "RIGHT"

            updateSnakePosition()

            displaySnake()

        if not goImmediatelyToMainMenu:
            goToMainMenu = displayGameOverMenu()
