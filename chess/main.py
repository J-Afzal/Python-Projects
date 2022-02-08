import os
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"  # noqa
import sys
import random
import pygame
import chess


def getGridPositionFromCoords(Coords):
    return 8 * int(Coords[1] / squareSize) + int(Coords[0] / squareSize)


def getCoordsFromGridPosition(gridPosition, padding):
    return ((gridPosition % 8) * squareSize + padding, int(gridPosition / 8) * squareSize + padding)


def getRectFromGridPosition(gridPosition):
    return ((gridPosition % 8) * squareSize, int(gridPosition / 8) * squareSize, squareSize, squareSize)


def createBlankBoard():
    blankBoard = pygame.Surface((windowSize, windowSize))
    blankBoard.fill(windowBgDark)
    drawLightRect = False
    for y in range(0, windowSize, squareSize):
        for x in range(0, windowSize, squareSize):
            if drawLightRect:
                pygame.draw.rect(blankBoard, windowBgLight, (x, y, squareSize, squareSize))
            drawLightRect = not drawLightRect
        drawLightRect = not drawLightRect
    return blankBoard


def createMenus(txt, txtPosX, txtPosYTitle, txtPosYBody, txtPosYBodyDifference, titleSize, bodySize, selectionStart, selectionEnd):
    fonts = []
    fonts.append(pygame.font.SysFont(mainFont, titleSize))
    for i in range(1, len(txt)):
        fonts.append(pygame.font.SysFont(mainFont, bodySize))

    output = []

    for i in range(selectionStart, selectionEnd+1):
        temp = pygame.Surface((windowSize, windowSize))
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
    fontTwo = pygame.font.SysFont(mainFont, 28)
    fontThree = pygame.font.SysFont(mainFont, 48)

    lineOne = "INFORMATION"
    lineTwo = "USE THE MOUSE TO DRAG AND DROP PIECES"
    lineThree = "ALL LEGAL MOVES ARE SHOWN FOR A SELECTED PIECE"
    lineFour = "ALL CHESS RULES ENFORCED VIA python-chess LIBRARY"
    lineFive = "R = RESTART WHEN GAMER OVER"
    lineSix = "Q = QUIT TO MAIN MENU"
    lineSeven = "CTRL + Q = QUIT PROGRAM"
    lineEight = "BACK TO MAIN MENU"
# hold down h to hide game over menu and add to info screen
    infoMenu = pygame.Surface((windowSize, windowSize))
    infoMenu.fill(menuWindowBg)
    infoMenu.blit(fontOne.render(lineOne, True, textColour), (50, 50))
    infoMenu.blit(fontTwo.render(lineTwo, True, textColour), (50, 150))
    infoMenu.blit(fontTwo.render(lineThree, True, textColour), (50, 200))
    infoMenu.blit(fontTwo.render(lineFour, True, textColour), (50, 250))
    infoMenu.blit(fontTwo.render(lineFive, True, textColour), (50, 300))
    infoMenu.blit(fontTwo.render(lineSix, True, textColour), (50, 350))
    infoMenu.blit(fontTwo.render(lineSeven, True, textColour), (50, 400))
    infoMenu.blit(fontThree.render(lineEight, True, selectedTextColour), (50, 550))

    return infoMenu


def createGameOverMenu():
    rematchTextSelected = pygame.font.SysFont(mainFont, gameOverFontSize).render("REMATCH", True, selectedTextColour)
    rematchText = pygame.font.SysFont(mainFont, gameOverFontSize).render("REMATCH", True, textColour)
    quitTextSelected = pygame.font.SysFont(mainFont, gameOverFontSize).render("QUIT", True, selectedTextColour)
    quitText = pygame.font.SysFont(mainFont, gameOverFontSize).render("QUIT", True, textColour)

    one = pygame.Surface((gameOverWidth, gameOverHeight))
    one.fill(menuWindowBg)
    one.blit(rematchTextSelected, rematchText.get_rect(center=(gameOverWidth/2, gameOverHeight-85)))
    one.blit(quitText, quitText.get_rect(center=(gameOverWidth/2, gameOverHeight-35)))
    one.blit(piecePNGs["K"], (gameOverWidth/2-piecesSize-50, 0))
    one.blit(piecePNGs["k"], (gameOverWidth/2+50, 0))

    two = pygame.Surface((gameOverWidth, gameOverHeight))
    two.fill(menuWindowBg)
    two.blit(rematchText, rematchText.get_rect(center=(gameOverWidth/2, gameOverHeight-85)))
    two.blit(quitTextSelected, quitText.get_rect(center=(gameOverWidth/2, gameOverHeight-35)))
    two.blit(piecePNGs["K"], (gameOverWidth/2-piecesSize-50, 0))
    two.blit(piecePNGs["k"], (gameOverWidth/2+50, 0))

    return [one, two]


def getSelectedPieceAndPosition():
    pieceGridPosition = getGridPositionFromCoords(pygame.mouse.get_pos())
    piece = chessBoard.piece_at(pieceGridPosition)
    if piece == None:
        pieceSymbol = None
    else:
        if piece.color == chessBoard.turn:
            pieceSymbol = piece.symbol()
        else:
            pieceSymbol = None

    return pieceSymbol, pieceGridPosition,


def executeNextMove():
    newGridPosition = getGridPositionFromCoords(pygame.mouse.get_pos())

    try:
        chessBoard.find_move(selectedPieceGridPosition, newGridPosition)
    except ValueError:  # Illegal move
        return False

    if (selectedPiece == "P" and int(newGridPosition / 8) == 7) or (selectedPiece == "p" and int(newGridPosition / 8) == 0):
        chessBoard.push(chess.Move(selectedPieceGridPosition, newGridPosition, getPawnPromotionChoice(newGridPosition)))
    else:
        chessBoard.push(chess.Move(selectedPieceGridPosition, newGridPosition))

    global previousMovesFrom, previousMovesTo, previousMovePiece
    previousMovesFrom.append(selectedPieceGridPosition)
    previousMovesTo.append(newGridPosition)
    previousMovePiece = chessBoard.piece_at(previousMovesTo[-1]).symbol()

    return True


def getPawnPromotionChoice(newGridPosition):
    x = squareSize * (newGridPosition % 8) + piecePadding
    if chessBoard.turn == chess.WHITE:
        pygame.draw.rect(window, pawnPromotionBg, (x - piecePadding, windowSize - squareSize*4, squareSize, squareSize*4))
        window.blit(piecePNGs["Q"], (x, windowSize + piecePadding - squareSize * 1))
        window.blit(piecePNGs["N"], (x, windowSize + piecePadding - squareSize * 2))
        window.blit(piecePNGs["R"], (x, windowSize + piecePadding - squareSize * 3))
        window.blit(piecePNGs["B"], (x, windowSize + piecePadding - squareSize * 4))
    else:
        pygame.draw.rect(window, pawnPromotionBg, (x - piecePadding, 0, squareSize, squareSize*4))
        window.blit(piecePNGs["q"], (x, piecePadding + squareSize * 0))
        window.blit(piecePNGs["n"], (x, piecePadding + squareSize * 1))
        window.blit(piecePNGs["r"], (x, piecePadding + squareSize * 2))
        window.blit(piecePNGs["b"], (x, piecePadding + squareSize * 3))

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
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                x = int(pygame.mouse.get_pos()[0] / squareSize)
                y = int(pygame.mouse.get_pos()[1] / squareSize)
                if x == (newGridPosition % 8):
                    if chessBoard.turn == chess.WHITE:
                        if y == 7:
                            return chess.QUEEN
                        elif y == 6:
                            return chess.KNIGHT
                        elif y == 5:
                            return chess.ROOK
                        elif y == 4:
                            return chess.BISHOP
                    else:
                        if y == 0:
                            return chess.QUEEN
                        elif y == 1:
                            return chess.KNIGHT
                        elif y == 2:
                            return chess.ROOK
                        elif y == 3:
                            return chess.BISHOP


def undoMove():
    global previousMovesFrom, previousMovesTo, previousMovePiece

    try:
        chessBoard.pop()
        previousMovesFrom.pop()
        previousMovesTo.pop()
        previousMovePiece = chessBoard.piece_at(previousMovesTo[-1]).symbol()
    except IndexError:  # No moves to undo
        pass


def displayBoard():
    window.blit(blankBoard, (0, 0))
    for i in range(64):
        if chessBoard.piece_at(i) != None:
            window.blit(piecePNGs[chessBoard.piece_at(i).symbol()], getCoordsFromGridPosition(i, piecePadding))

    if previousMovesFrom and previousMovesTo:
        pygame.draw.rect(window, previousMoveFromColour, getRectFromGridPosition(previousMovesFrom[-1]))
        pygame.draw.rect(window, previousMoveToColour, getRectFromGridPosition(previousMovesTo[-1]))
        window.blit(piecePNGs[previousMovePiece], getCoordsFromGridPosition(previousMovesTo[-1], piecePadding))

    if chessBoard.is_check():
        kingLocation = chessBoard.king(chessBoard.turn)
        pygame.draw.rect(window, kingInCheckColour, getRectFromGridPosition(kingLocation))
        window.blit(piecePNGs[chessBoard.piece_at(kingLocation).symbol()], getCoordsFromGridPosition(kingLocation, piecePadding))

    if mouseButtonDown and selectedPiece != None:
        pygame.draw.rect(window, pieceSelectedColour, getRectFromGridPosition(selectedPieceGridPosition))
        tempSurface = pygame.Surface((windowSize, windowSize), pygame.SRCALPHA)
        for move in list(chessBoard.legal_moves):
            if move.from_square == selectedPieceGridPosition:
                if (chessBoard.color_at(move.to_square) == chess.BLACK and chessBoard.turn == chess.WHITE) or (chessBoard.color_at(move.to_square) == chess.WHITE and chessBoard.turn == chess.BLACK):
                    pygame.draw.circle(tempSurface, legalMoveCaptureColour, getCoordsFromGridPosition(move.to_square, squareSize/2), legalMoveCaptureRadius, legalMoveCaptureWidth)
                else:
                    pygame.draw.circle(tempSurface, legalMoveColour, getCoordsFromGridPosition(move.to_square, squareSize/2), legalMoveRadius)
        window.blit(tempSurface, (0, 0))
        mousePos = pygame.mouse.get_pos()
        window.blit(piecePNGs[selectedPiece], (mousePos[0]-piecesSize/2, mousePos[1]-piecesSize/2))


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
                        currentSelection = 4
                    else:
                        currentSelection -= 1
                elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    if currentSelection == 4:
                        currentSelection = 0
                    else:
                        currentSelection += 1
                elif event.key == pygame.K_RETURN:
                    if currentSelection == 0:
                        return
                    elif currentSelection == 1:
                        displayNumberOfPayersOptionsMenu()
                    elif currentSelection == 2:
                        displayAIDifficultyOptionsMenu()
                    elif currentSelection == 3:
                        displayInfoMenu()
                    elif currentSelection == 4:
                        pygame.display.quit()
                        sys.exit()

        window.blit(mainMenus[currentSelection], (0, 0))

        pygame.display.update()


def displayNumberOfPayersOptionsMenu():
    global numberOfPlayers
    currentSelection = numberOfPlayers
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
                    if currentSelection != 3:
                        numberOfPlayers = currentSelection
                    return
                elif event.key == pygame.K_ESCAPE:
                    return

        window.blit(numberOfPlayersMenus[currentSelection], (0, 0))

        pygame.display.update()


def displayAIDifficultyOptionsMenu():
    global AIDifficulty
    currentSelection = AIDifficulty
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
                    if currentSelection != 3:
                        AIDifficulty = currentSelection
                    return
                elif event.key == pygame.K_ESCAPE:
                    return

        window.blit(AIDifficultyMenus[currentSelection], (0, 0))

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
    global whiteScore, blackScore
    if chessBoard.outcome().winner == chess.WHITE:
        whiteScore += 1
    elif chessBoard.outcome().winner == chess.BLACK:
        blackScore += 1

    score = pygame.font.SysFont(mainFont, 72).render(f"{whiteScore}-{blackScore}", True, textColour)
    hideMenu = False
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
            window.blit(gameOverMenu[currentSelection], (windowSize/2-gameOverWidth/2, windowSize/2-gameOverHeight/2))

            window.blit(score, score.get_rect(center=(windowSize/2, windowSize/2-gameOverHeight/2+piecesSize/2+10)))

            if chessBoard.outcome().winner == chess.WHITE:
                window.blit(gameOutcomes[0], gameOutcomes[0].get_rect(center=(windowSize/2, 295)))
            elif chessBoard.outcome().winner == chess.BLACK:
                window.blit(gameOutcomes[1], gameOutcomes[1].get_rect(center=(windowSize/2, 295)))
            else:  # Draw
                window.blit(gameOutcomes[chessBoard.outcome().termination.value], gameOutcomes[chessBoard.outcome().termination.value].get_rect(center=(windowSize/2, 295)))
        else:
            displayBoard()

        pygame.display.update()


def getNextMoveFromUser():
    global selectedPiece, selectedPieceGridPosition, mouseButtonDown, goImmediatelyToMainMenu, goToMainMenu
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.display.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q and pygame.key.get_mods() & pygame.KMOD_CTRL:
                    pygame.display.quit()
                    sys.exit()
                if event.key == pygame.K_BACKSPACE:
                    undoMove()
                if event.key == pygame.K_q:
                    goImmediatelyToMainMenu = True
                    goToMainMenu = True
                    return
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                selectedPiece, selectedPieceGridPosition = getSelectedPieceAndPosition()
                mouseButtonDown = True
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                validMove = executeNextMove()
                selectedPiece = None
                selectedPieceGridPosition = None
                mouseButtonDown = False
                if validMove:
                    return

        displayBoard()
        pygame.display.update()


def getNextMoveFromAI():
    global goImmediatelyToMainMenu, goToMainMenu
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.display.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q and pygame.key.get_mods() & pygame.KMOD_CTRL:
                pygame.display.quit()
                sys.exit()
            if event.key == pygame.K_q:
                goImmediatelyToMainMenu = True
                goToMainMenu = True
                return

    chessBoard.push(random.choice(list(chessBoard.legal_moves)))


if __name__ == "__main__":
    windowSize = 640
    piecesSize = 88
    squareSize = int(windowSize/8)
    piecePadding = int((squareSize - piecesSize) / 2)

    pygame.init()
    pygame.display.set_caption("Chess")
    pygame.display.set_icon(pygame.image.load("chess\\resources\\app.ico"))
    window = pygame.display.set_mode((windowSize, windowSize))

    windowBgDark = (81, 42, 42)
    windowBgLight = (124, 76, 62)
    menuWindowBg = (8, 8, 8)
    pawnPromotionBg = (162, 84, 84)

    pieceSelectedColour = (192, 192, 75)
    previousMoveFromColour = (128, 128, 50)
    previousMoveToColour = (192, 192, 75)

    kingInCheckColour = (247, 119, 105)

    legalMoveColour = (255, 255, 255, 100)
    legalMoveCaptureColour = (255, 0, 0, 100)
    legalMoveRadius = 12
    legalMoveCaptureRadius = squareSize / 2
    legalMoveCaptureWidth = 8

    mainFont = "Video Game Font"
    textColour = (255, 255, 255)
    selectedTextColour = (0, 156, 128)

    gameOverWidth = 350
    gameOverHeight = 250
    gameOverFontSize = 48
    gameOverOutcomeFontSize = 20

    numberOfPlayers = 0
    AIDifficulty = 0
    humanPlayer = chess.WHITE

    piecePNGs = {
        "K": pygame.transform.smoothscale(pygame.image.load("chess\\resources\\white king.png"), (piecesSize, piecesSize)),
        "Q": pygame.transform.smoothscale(pygame.image.load("chess\\resources\\white queen.png"), (piecesSize, piecesSize)),
        "B": pygame.transform.smoothscale(pygame.image.load("chess\\resources\\white bishop.png"), (piecesSize, piecesSize)),
        "R": pygame.transform.smoothscale(pygame.image.load("chess\\resources\\white rook.png"), (piecesSize, piecesSize)),
        "N": pygame.transform.smoothscale(pygame.image.load("chess\\resources\\white knight.png"), (piecesSize, piecesSize)),
        "P": pygame.transform.smoothscale(pygame.image.load("chess\\resources\\white pawn.png"), (piecesSize, piecesSize)),
        "k": pygame.transform.smoothscale(pygame.image.load("chess\\resources\\black king.png"), (piecesSize, piecesSize)),
        "q": pygame.transform.smoothscale(pygame.image.load("chess\\resources\\black queen.png"), (piecesSize, piecesSize)),
        "b": pygame.transform.smoothscale(pygame.image.load("chess\\resources\\black bishop.png"), (piecesSize, piecesSize)),
        "r": pygame.transform.smoothscale(pygame.image.load("chess\\resources\\black rook.png"), (piecesSize, piecesSize)),
        "n": pygame.transform.smoothscale(pygame.image.load("chess\\resources\\black knight.png"), (piecesSize, piecesSize)),
        "p": pygame.transform.smoothscale(pygame.image.load("chess\\resources\\black pawn.png"), (piecesSize, piecesSize)),
    }

    gameOutcomes = [
        pygame.font.SysFont(mainFont, gameOverOutcomeFontSize).render("(WHITE WINS)", True, textColour),
        pygame.font.SysFont(mainFont, gameOverOutcomeFontSize).render("(BLACK WINS)", True, textColour),
        pygame.font.SysFont(mainFont, gameOverOutcomeFontSize).render("(DRAW DUE TO STALEMATE)", True, textColour),
        pygame.font.SysFont(mainFont, gameOverOutcomeFontSize).render("(DRAW DUE TO INSUFFICIENT MATERIAL)", True, textColour),
        pygame.font.SysFont(mainFont, gameOverOutcomeFontSize).render("(DRAW DUE TO SEVENTYFIVE MOVES RULE)", True, textColour),
        pygame.font.SysFont(mainFont, gameOverOutcomeFontSize).render("(DRAW DUE TO FIVEFOLD REPETITION RULE)", True, textColour),
        pygame.font.SysFont(mainFont, gameOverOutcomeFontSize).render("(DRAW DUE TO FIFTY MOVES RULE)", True, textColour),
        pygame.font.SysFont(mainFont, gameOverOutcomeFontSize).render("(DRAW DUE TO THREEFOLD REPETITION RULE)", True, textColour),
    ]

    blankBoard = createBlankBoard()
    mainMenus = createMenus(["PLAY CHESS", "NO. OF PLAYERS", "AI DIFFICULTY", "INFO", "QUIT"], 50, 50, 150, 100, 120, 48, 0, 4)
    numberOfPlayersMenus = createMenus(["NO. OF PLAYERS", "0", "1", "2", "BACK TO MAIN MENU"], 50, 50, 150, 100, 90, 48, 1, 4)
    AIDifficultyMenus = createMenus(["AI DIFFICULTY", "EASY", "MEDIUM", "HARD", "BACK TO MAIN MENU"], 50, 50, 150, 100, 90, 48, 1, 4)
    infoMenu = createInfoMenu()
    gameOverMenu = createGameOverMenu()

    goToMainMenu = True
    while True:
        if goToMainMenu:
            displayMainMenu()
            whiteScore = 0
            blackScore = 0

        mouseButtonDown = False
        selectedPieceGridPosition = None
        selectedPiece = None

        previousMovesFrom = []
        previousMovesTo = []
        previousMovePiece = None

        chessBoard = chess.Board()
        goImmediatelyToMainMenu = False
        while chessBoard.outcome() == None and not goImmediatelyToMainMenu:
            displayBoard()
            pygame.display.update()

            if numberOfPlayers == 2:
                getNextMoveFromUser()
            elif numberOfPlayers == 1:
                if chessBoard.turn == humanPlayer:
                    getNextMoveFromUser()
                else:
                    getNextMoveFromAI()
            elif numberOfPlayers == 0:
                getNextMoveFromAI()

            displayBoard()
            pygame.display.update()

        if not goImmediatelyToMainMenu:
            goToMainMenu = displayGameOverMenu()
