import networkx as nx

class Piece():
    def __init__(self,label,index,Graph):

        self.label = label
        self.allowedX = [];
        self.allowedY = [];
        self.Graph = Graph;
    
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
        
            self.allowedY = [[1*self.factor],[1*self.factor],[1*self.factor], [2*self.factor]];
            self.allowedX = [[0],[1],[-1], [0]];

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
        
        self.removePaths()
        a = 0;
        for moves in self.allowedY:
            i = 0
        
            for allowedY in moves:
                new_position = self.position + 10*allowedY + self.allowedX[a][i];

                path = self.canPath(new_position);

                if path == -1:
                    break;

                elif path == 0:
                    if 'pawn' in self.label:
                        new_position = self.position + 10*allowedY;
                        if self.canPath(new_position) == 0:
                            self.Graph.add_edge(self.position,new_position); 
                            continue;
                            
                    else:
                        self.Graph.add_edge(self.position,new_position);

                elif path == 1:
                    allowedpos = [self.position + 10,self.position - 10,self.position+20,self.position - 20];
                    if 'pawn' in self.label and new_position in allowedpos:
                        continue;
                        
                    else:
                        self.Graph.add_edge(self.position,new_position);
                        break;

                i = i + 1;
        
            a = a + 1;
        
        
    def canPath(self,node):
    
        if (self.Graph.has_node(node) == False): #Square not in map
            return -1;

        if self.country in self.Graph.nodes[node]['piece']: #Own piece on square
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

    def getLabel(self):
        return self.label;

    def setLabel(self, label):
        self.label = label;

    def getPosition(self):
        return self.position;

    def getGraph(self):
        return self.Graph;

    def movePiece(self,position,gamestate):    
        
        if gamestate not in self.label:
            return False;

        if "pawn" in self.label:
            self.allowedY = [[1*self.factor],[1*self.factor],[1*self.factor]];
            self.allowedX = [[0],[1],[-1]];

        if self.Graph.has_edge(self.position,position):
            self.Graph.nodes[self.position]['piece'] = "Empty";
            self.removePaths()
            self.setPosition(position)
            return True;

        else:
            return False;

    def removePaths(self):
        outgoing_edges = list(self.Graph.edges([self.position]));
        self.Graph.remove_edges_from(outgoing_edges)
        

