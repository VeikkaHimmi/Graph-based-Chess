import pygame as p
from Engine import Engine
from Piece import Piece
import networkx

SIZE = 720
SQUARES = 8
SQUARE_SIZE = SIZE // SQUARES
IMAGES = {}
SQUARE_COLORS = (p.Color("sienna"), p.Color("burlywood1"))

class Board():
    def __init__(self):
        self.Engine = Engine();
        self.boardpieces = self.Engine.getPieces();
        self.selected = (); #Selected square
        self.confirmation = ();
        
        
        
    def getImages(self,pieces):
        for piece in pieces:
            IMAGES[piece] = p.transform.scale(p.image.load("images/"+piece+".png"), (SQUARE_SIZE,SQUARE_SIZE));
        
    def screen(self):
        self.getImages(self.boardpieces)
        p.init()
        p.display.set_caption('Graph-based-Chess')
        screen = p.display.set_mode((SIZE,SIZE))

        screen.fill(p.Color("white"))

        running = True
        while running:
            for event in p.event.get():
                
                if event.type == p.QUIT:
                    running = False

                elif event.type == p.MOUSEBUTTONDOWN:
                    
                    location = p.mouse.get_pos() #(X,Y)
                    x = location[0]//SQUARE_SIZE
                    y = location[1]//SQUARE_SIZE*10
                    
                    self.confirmation = self.selected
                    self.selected = y + x

                    if self.selected == self.confirmation:
                        self.selected = ()
                        self.confirmation = ()

                    elif self.confirmation != () and self.Engine.getGraph().nodes[self.confirmation]['piece'] != "Empty":
                        selected_Piece = self.Engine.getGraph().nodes[self.confirmation]['Piece']
                        gameState = self.Engine.getGamestate()

                        if (selected_Piece.movePiece(self.selected,gameState)):
                            self.Engine.updatePositions()
                            self.confirmation = ()
                            self.selected = ()
                        
                        
                         
            self.drawBoard(screen)
            self.drawPieces(screen)
            self.checkPaths(screen)
            p.display.flip()
    

    def drawBoard(self,screen):
        
        for row in range(SQUARES):
            for col in range(SQUARES):
                drawcolor = SQUARE_COLORS[((row + col) % 2)] #even = white
                p.draw.rect(screen,drawcolor, p.Rect(col*SQUARE_SIZE, row*SQUARE_SIZE,SQUARE_SIZE,SQUARE_SIZE));

    def checkPaths(self,screen):

        if (self.selected == () or self.Engine.getGamestate() not in self.Engine.getGraph().nodes[self.selected]['piece'] ):
            return;

        drawcolor = p.Color("salmon")
        paths = self.Engine.getGraph().edges([self.selected])
        
        for square in paths:
            cordinates = [*map(int,str(square[1]))]
            if (len(cordinates) == 1): # squares 01 - 08
                col = cordinates[0];
                row = 0
            else: # squares 11 - 88
                col = cordinates[1] # X-axis
                row = cordinates[0] # Y-axis
            
            
            p.draw.rect(screen,drawcolor, p.Rect(col*SQUARE_SIZE, row*SQUARE_SIZE,SQUARE_SIZE,SQUARE_SIZE));

    def drawPieces(self,screen):

        for row in range(SQUARES):
            for col in range(SQUARES):
                check = row * 10 + col
                square_item = self.Engine.getGraph().nodes[check]['piece']
                if square_item == "Empty":
                    continue
                else:
                    screen.blit(IMAGES[square_item], p.Rect(col*SQUARE_SIZE,row*SQUARE_SIZE,SQUARE_SIZE,SQUARE_SIZE));