import networkx as nx
import copy;

class Piece():
    def __init__(self,label,index,Graph):

        self.label = label
        self.allowedX = [];
        self.allowedY = [];
        self.Graph = Graph;
        self.checked_1 = False;
        self.checked_2 = False;
        self.checkmoves = [];
        self.checked_piece = self;
        self.king_check = -1;
        
        if "W-" in label:
            self.country = "W-";
            position = 0;
            self.factor = 1;
        else:
            self.country = "B-";
            position = 70;
            self.factor = -1;

        if "pawn" in label:
            self.position = position + 10*self.factor + index;
        
            self.allowedY = [[1*self.factor,2*self.factor],[1*self.factor],[1*self.factor]];
            self.allowedX = [[0,0],[1],[-1]];

        elif "knight" in label:
            self.position = position + index*5 + 1;

            self.allowedY = [[2],[2],[-2],[-2],[-1],[1],[-1],[1]];
            self.allowedX = [[-1],[1],[-1],[1],[2],[2],[-2],[-2]];

        elif "king" in label:
            self.position = position + 4;

            self.allowedY = [[1],[1],[1],[-1],[-1],[-1],[0],[0]];
            self.allowedX = [[0],[1],[-1],[0],[1],[-1],[1],[-1]];

        elif "bishop" in label:
            self.position = position + index*3 + 2;
        
            self.allowedY = [[1,2,3,4,5,6,7],[-1,-2,-3,-4,-5,-6,-7],[1,2,3,4,5,6,7],[-1,-2,-3,-4,-5,-6,-7]];
            self.allowedX = [[1,2,3,4,5,6,7],[1,2,3,4,5,6,7],[-1,-2,-3,-4,-5,-6,-7],[-1,-2,-3,-4,-5,-6,-7]];

        elif "rook" in label:
            self.position = position + index*7;
        
            self.allowedY = [[1,2,3,4,5,6,7],[-1,-2,-3,-4,-5,-6,-7],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0]];
            self.allowedX = [[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[1,2,3,4,5,6,7],[-1,-2,-3,-4,-5,-6,-7]];

        elif "queen" in label:
            self.position = position + 3;
        
            self.allowedY = [[1,2,3,4,5,6,7],[-1,-2,-3,-4,-5,-6,-7],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[1,2,3,4,5,6,7],[-1,-2,-3,-4,-5,-6,-7],[1,2,3,4,5,6,7],[-1,-2,-3,-4,-5,-6,-7]];
            self.allowedX = [[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[1,2,3,4,5,6,7],[-1,-2,-3,-4,-5,-6,-7],[1,2,3,4,5,6,7],[1,2,3,4,5,6,7],[-1,-2,-3,-4,-5,-6,-7],[-1,-2,-3,-4,-5,-6,-7]];

        self.Graph.nodes[self.position]['piece'] = self.label;
        self.Graph.nodes[self.position]['Piece'] = self;
        

    def setPaths(self):

        if (self.checked_2):
            self.check();
            self.uncheck();
            return;

        self.removePaths()
        
        a = 0;
        king_check = False;
        for moves in self.allowedY:
            i = -1
            pathlist = [];
        
            for allowedY in moves:
                i = i + 1;
                new_position = self.position + 10*allowedY + self.allowedX[a][i];

                path = self.canPath(new_position);
                
                if path == -1:
                    break;
                
                if (king_check):
                    checked_piece.king_check = new_position;
                if (self.checked_1): #can be localised
                    if path == 0:
                        pathlist.append(new_position)
                        continue;
                    
                    if ('king' in self.Graph.nodes[new_position]['piece']) and (self.country not in self.Graph.nodes[new_position]['piece']):
                        pathlist.append(self.position);
                        checked_piece.checked_2 = True;
                        checked_piece.setCheckmoves(pathlist);
                        self.checked_piece = checked_piece;
                        self.checked_1 = False;
                        break;

                    else:
                        self.checked_1 = False;

                        if (checked_piece == self.checked_piece):
                            checked_piece.uncheck();
                            self.checked_piece = self
                        break;

                if path == 0:
                    if 'pawn' in self.label:
                        new_position = self.position + 10*allowedY;
                        if self.canPath(new_position) == 0:
                            self.Graph.add_edge(self.position,new_position); 
                            continue;
                            
                    else:
                        pathlist.append(new_position)
                        self.Graph.add_edge(self.position,new_position);

                if path == 1:
                    allowedpos = [self.position + 10*self.factor,self.position + 20*self.factor]; #positions pawn piece can move
                    
                    if 'pawn' in self.label and new_position in allowedpos:
                        continue;
                        
                    else:
                        self.checked_1 = True;
                        checked_piece = self.Graph.nodes[new_position]['Piece']
                        self.Graph.add_edge(self.position,new_position);

                        if ('king' in checked_piece.getLabel()):
                            pathlist.append(self.position);
                            checked_piece.setCheckmoves(pathlist);
                            checked_piece.checked_2 = True;
                            checked_piece.checking_position = self.position;
                            king_check = True; #better way?
                            continue;
                        
            self.checked_1 = False;
        
            a = a + 1;

    def setCheckmoves(self,possiblemoves):
        self.checkmoves = possiblemoves

    def check(self):
        self.removePaths()
        a = 0;
        for moves in self.allowedY:
            i = -1
        
            for allowedY in moves:
                i = i + 1;
                new_position = self.position + 10*allowedY + self.allowedX[a][i];

                path = self.canPath(new_position);

                if path == 0 or path == 1:

                    if 'king' in self.label:
                        if new_position in self.checkmoves:
                            if new_position == self.checking_position:
                                self.Graph.add_edge(self.position,new_position);
                            continue;
                        else:
                            self.Graph.add_edge(self.position,new_position);


                    elif (new_position in self.checkmoves):
                        allowedpos = [self.position + 10*self.factor,self.position + 20*self.factor]; #positions pawn piece can move forward
                        forwardmove = new_position in allowedpos;
                        nextsquare = self.Graph.nodes[new_position]['piece']; #piece in next square

                        if 'pawn' in self.label and ((forwardmove and nextsquare != "Empty") or (forwardmove == False and nextsquare == "Empty")):
                            continue;

                        self.Graph.add_edge(self.position,new_position);
                else:
                    break;
                
            a = a + 1;

    def uncheck(self):
        self.checked_2 = False;

    def canPath(self,node):

        if (self.Graph.has_node(node) == False): #Square not in map
            return -1;

        if self.country in self.Graph.nodes[node]['piece']: #Own piece on square
            return -1;

        if 'king' in self.getLabel():
            for edge in self.Graph.in_edges(node):
                endnode = edge[0]
                endnode_piece = self.Graph.nodes[endnode]['piece']
                if (self.country not in endnode_piece):
                    if "pawn" in endnode_piece and (endnode + 10*self.factor*-1 == node or endnode + 20*self.factor*-1 == node):
                        continue;
                    
                    return -1;

            if node == self.king_check:
                return -1;


        if self.Graph.nodes[node]['piece'] == "Empty": #Nothing on square
            return 0;
    
        return 1; #Enemy on square

    def setPosition(self,position):

        if self.Graph.nodes[position]['piece'] != 'Empty':
            self.Graph.nodes[position]['Piece'].setLabel(self.label+'-Eaten');

        self.Graph.nodes[position]['piece'] = self.label;
        self.Graph.nodes[position]['Piece'] = self;
        self.position = position;
        self.setPaths();

    def getLabel(self):
        return self.label;

    def setLabel(self, label):
        self.label = label;

    def getCountry(self):
        return self.country;
    def getPosition(self):
        return self.position;

    def getGraph(self):
        return self.Graph;

    def movePiece(self,position,gamestate):    
        
        if gamestate not in self.label:
            return False;

        if self.Graph.has_edge(self.position,position):
            self.checked_piece.uncheck();
            self.checked_piece = self

            if "pawn" in self.label:
                self.allowedY = [[1*self.factor],[1*self.factor],[1*self.factor]];
                self.allowedX = [[0],[1],[-1]];

            if "king" in self.label:
                self.king_check = -1;

            self.Graph.nodes[self.position]['piece'] = "Empty";
            self.removePaths()
            self.setPosition(position)
            return True;

        else:
            return False;

    def removePaths(self):
        outgoing_edges = list(self.Graph.edges([self.position]));
        self.Graph.remove_edges_from(outgoing_edges)
        

