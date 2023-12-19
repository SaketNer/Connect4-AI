#!/usr/bin/env python3
from FourConnect import * # See the FourConnect.py file
import csv

class GameTreePlayer:
    
    def __init__(self):
        self.maxLookahead=5 # decides the lookahead distance
        pass
    
    def FindBestAction(self,currentState):        
        alpha = float('-inf') 
        beta = float('inf') 
        award,bestAction = self.MaxValue(currentState,self.maxLookahead,alpha,beta)
        return bestAction
    
    def _CoinRowAfterAction(self,board,action):
        cRow = -1
        c=action
        for r in range(5,-1,-1):
            if board[r][c]==0:
                cRow=r
                break
        return cRow

    def _evaluate_window(self,window,player):   #evaluates a given 1D array with windows of len = 4
        score = 0
        score = 0
        for i in range(len(window)-3):
            temp = window[i:i+4]
            if(temp.count(player)==4 and temp.count(0)==0 ):
                score+=10000
            if(temp.count(player)==3 and temp.count(0)==1 ):
                score+=36
            if(temp.count(player)==2 and temp.count(0)==2 ):
                score+=6
            if(temp.count(player)==1 and temp.count(0)==3 ):
                score+=1
        return score
    
    def _score_position(self,board,player):  #give array of board to evaluate , takes center colummn,row,column and diagonals
        score = 0
        
        ## Score center column
        for i in range(7):
            center_array = [[board[0][i],board[1][i],board[2][i],board[3][i],board[4][i],board[5][i]]]
            score += self._evaluate_window(center_array,player) * ((3-abs(3-i)))/3
        
        ## Score Vertical
        for c in range(7):
            col_array = [board[0][c],board[1][c],board[2][c],board[3][c],board[4][c],board[5][c]]
            score += self._evaluate_window(col_array,player)

        ## Score Horizontal
        for r in range(6):
            row_array = board[r]
            score += self._evaluate_window(row_array,player)*1.5
            if(row_array.count(2)==4 and row_array.count(0)==2):
                score+=5
        
        #diagnols \ 
        diagnols = []
        for r in range(6):
                c=0
                i = 0
                window = []
                while r+i<6 and c+i<7:
                    window.append(board[r+i][c+i])
                    i+=1
                if(len(window)>=4):
                    diagnols.append(window)
                    score += self._evaluate_window(window,player)
        for c in range(1,7):
                r = 0
                i = 0
                window = []
                while r+i<6 and c+i<7:
                    window.append(board[r+i][c+i])
                    i+=1
                if(len(window)>=4):
                    diagnols.append(window)
                    score += self._evaluate_window(window,player)
        
        #score for diagnols /
        diagnols = []
        for r in range(6):
            c=6
            i = 0
            window = []
            while r+i<6 and c-i>=0:
                window.append(board[r+i][c-i])
                i+=1
            if(len(window)>=4):
                diagnols.append(window)
                score += self._evaluate_window(window,player)
        for c in range(1,7):
            r = 0
            i = 0
            window = []
            while r+i<6 and c-i>0:
                window.append(board[r+i][c-i])
                i+=1

            if(len(window)>=4):
                diagnols.append(window)
                score += self._evaluate_window(window,player)
                
        return score

    def _scoreAI(self,board): #gives score of player 2 relative to player 1
        return self._score_position(board,2)-self._score_position(board,1)

    def _CheckValidMove(self,currentState,action): # checks if move is valid
        cRow = -1
        c = action
        for r in range(5,-1,-1):
            if currentState[r][c]==0:
                cRow=r
                break
        return cRow

    
    def _isBoardNotFull (self,board):     #checks if gameboard is full
        for i in range (7) :
            if board[0][i] == 0 :
                return True
        return False

    def _MoveOrder(self,currentState,player): # orders move based on the score of the board after move is played
        tempboard = copy.deepcopy(currentState)
        ordered_moves = []
        for a in range(7):
            cRow = self._CheckValidMove(currentState,a)
            if(cRow==-1):
                continue
            row = self._CoinRowAfterAction(tempboard,a)
            tempboard[row][a]=player
            tempscore = self._scoreAI(tempboard)
            ordered_moves.append((tempscore,a))
            tempboard[row][a]=0
        if(player == 2):
            ordered_moves.sort(key=lambda x: x[0], reverse=True)
        else:
            ordered_moves.sort(key=lambda x: x[0], reverse=False)
        return ordered_moves
            

    def MinValue(self,currentState,lookahead,alpha,beta):
        if(abs(self._scoreAI(currentState))>9000 or lookahead==0 or not(self._isBoardNotFull(currentState))):
            return self._scoreAI(currentState)
        v = float('inf') 
        moveOrder = self._MoveOrder(currentState,1)
        for _,a in moveOrder:
            cRow = self._CheckValidMove(currentState,a)
            if(cRow==-1):
                continue
            tempboard = copy.deepcopy(currentState)
            row = self._CoinRowAfterAction(tempboard,a)
            tempboard[row][a]=1
            v2,_ = self.MaxValue(tempboard,lookahead-1,alpha,beta)
            if(v2<v):
                v = v2
            beta = min(beta,v)
            if(alpha>=beta):
                #print("pruned")
                break
        return v
    
    def MaxValue(self,currentState,lookahead,alpha,beta):
        if(abs(self._scoreAI(currentState))>9000 or lookahead==0 or not(self._isBoardNotFull(currentState))):
            return self._scoreAI(currentState),None
        v = float('-inf')
        bestAction=None
        moveOrder = self._MoveOrder(currentState,2)
        for _,a in moveOrder:
        #for a in range(7):
            cRow = self._CheckValidMove(currentState,a)
            if(cRow==-1):
                continue
            fourConnect = FourConnect()
            fourConnect.SetCurrentState(currentState)
            fourConnect.GameTreePlayerAction(a)
            nextstate = fourConnect.GetCurrentState()
            if(fourConnect.winner != None or self._isBoardNotFull(nextstate)==False):
                return self._scoreAI(nextstate),a
            v2 = self.MinValue(nextstate,lookahead-1,alpha,beta)
            if(v2>v):
                bestAction=a
                v = v2
            alpha = max(alpha,v)
            if(alpha>=beta):
                #print("pruned")
                break
        return v,bestAction


def LoadTestcaseStateFromCSVfile():
    testcaseState=list()

    with open('testcase.csv', 'r') as read_obj: 
       	csvReader = csv.reader(read_obj)
        for csvRow in csvReader:
            row = [int(r) for r in csvRow]
            testcaseState.append(row)
        return testcaseState


def PlayGame():
    fourConnect = FourConnect()
    fourConnect.PrintGameState()
    gameTree = GameTreePlayer()
    
    move=0
    while move<42: #At most 42 moves are possible
        if move%2 == 0: #Myopic player always moves first
            fourConnect.PlayerAction()
        else:
            currentState = fourConnect.GetCurrentState()
            gameTreeAction = gameTree.FindBestAction(currentState)
            fourConnect.GameTreePlayerAction(gameTreeAction)
        fourConnect.PrintGameState()
        move += 1
        if fourConnect.winner!=None:
            break
    
    if fourConnect.winner==None:
        print("Game is drawn.")
    else:
        print("Winner : Player {0}\n".format(fourConnect.winner))
    print("Moves : {0}".format(move))
  

def main():
    """
    You can play against AI by running the play game option
    """
    print("You are player 1 and the AI is player 2. Best of Luck!")
    PlayGame()


if __name__=='__main__':
    main()
