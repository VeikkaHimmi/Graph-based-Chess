import networkx as nx
from Piece import Piece;
import itertools;
import pygame as pg;

chesspieces = [];

class Engine:
    def __init__(self):
        self.graph = nx.DiGraph();
        self.chesspieces = {};
        self.gameState = "W";

        board = [0,1,2,3,4,5,6,7,
            10,11,12,13,14,15,16,17,
            20,21,22,23,24,25,26,27,
            30,31,32,33,34,35,36,37,
            40,41,42,43,44,45,46,47,
            50,51,52,53,54,55,56,57,
            60,61,62,63,64,65,66,67,
            70,71,72,73,74,75,76,77]
    
        for position in board:
            self.graph.add_node(position, piece = "Empty", Piece = "");

        self.pieces = ["W-pawn","W-knight","W-queen","W-bishop","W-rook","W-king","B-pawn","B-knight","B-queen","B-bishop","B-rook","B-king"]
        
        for piece in self.pieces:
            self.chesspieces[piece] = [];

        for piece in self.pieces:
            createPieces(self,piece);
        
        self.updatePositions();

    def getPieces(self):
        return self.pieces;
    
    def getGraph(self):
        return self.graph;
    
    def updatePositions(self):
        self.flipGamestate()

        if self.check():


        for position in self.chesspieces:
            for piece in self.chesspieces[position]:#multiple pieces ie. W-pawn
                if 'Eaten' in piece.getLabel():
                    continue;
                piece.setPaths();

    def flipGamestate(self):
        if self.gameState == "W":
            self.gameState = "B"
        else:
            self.gameState = "W"

    def getGamestate(self):
        return self.gameState;

    def check(self):
        return;
def createPieces(self,label):

    if "pawn" in label:
        i = 0;
        while i < 8:
            piece = Piece(label,i, self.graph);
            self.chesspieces[label].append(piece);
            i = i+1;

    elif "king" in label or "queen" in label:
        piece = Piece(label,0, self.graph);
        self.chesspieces[label].append(piece);
        
    else:
        piece = Piece(label,0, self.graph);
        self.chesspieces[label].append(piece);
        piece = Piece(label,1, self.graph);  
        self.chesspieces[label].append(piece);
   
