import random
import copy

class FourConnect:
    
    def __init__(self):
        self._game = [
                    [0,0,0,0,0,0,0], #row 0 having columns 0 to 6 from left to right
                    [0,0,0,0,0,0,0], #row 1 having columns 0 to 6 from left to right
                    [0,0,0,0,0,0,0], #row 2 having columns 0 to 6 from left to right
                    [0,0,0,0,0,0,0], #row 3 having columns 0 to 6 from left to right
                    [0,0,0,0,0,0,0], #row 4 having columns 0 to 6 from left to right
                    [0,0,0,0,0,0,0]  #row 5 having columns 0 to 6 from left to right
                    ]
        self.winner = None
    
    def _CoinRowAfterAction(self,action):
        g = self._game
        cRow = -1
        c=action
        for r in range(5,-1,-1):
            if g[r][c]==0:
                cRow=r
                break
        return cRow

    def _CheckHorizontal(self,row,col,player):
        g = self._game
        cMin=cMax=col
        while True:
            cMin = cMin-1
            if cMin<0 or g[row][cMin]!=player:
                cMin = cMin+1
                break
        while True:
            cMax = cMax+1
            if cMax>6 or g[row][cMax]!=player:
                cMax = cMax-1
                break
        if cMax-cMin>=3:
            return True
        else:
            return False

    def _CheckVertical(self,row,col,player):
        g = self._game
        rMin=rMax=row
        while True:
            rMin = rMin-1
            if rMin<0 or g[rMin][col]!=player:
                rMin = rMin+1
                break
        while True:
            rMax = rMax+1
            if rMax>5 or g[rMax][col]!=player:
                rMax = rMax-1
                break
        if rMax-rMin>=3:
            return True
        else:
            return False


    def _CheckDiag(self,row,col,player,diag=1):
        g = self._game
        cMin=cMax=col
        rMin=rMax=row
        while True:
            cMin = cMin -1
            rMax = rMax + diag
            if cMin<0 or rMax<0 or rMax>5 or g[rMax][cMin]!=player:
                cMin = cMin +1
                rMax = rMax - diag
                break
        while True:
            cMax = cMax+1
            rMin = rMin-diag
            if cMax>6 or rMin<0 or rMin>5 or g[rMin][cMax]!=player:
                cMax = cMax-1
                rMin = rMin+diag
                break
        if cMax-cMin>=3:
            return True
        else:
            return False

        
    def _CanAPlayerWin(self,row,col,player):
        win = self._CheckHorizontal(row,col,player)
        if win==False:
            win = self._CheckDiag(row,col,player,diag=+1) #Principal diagonal = +1
        if win==False:
            win = self._CheckDiag(row,col,player,diag=-1) #Secondary diagonal = -1
        if win==False:
            win = self._CheckVertical(row,col,player)
        return win

    def _TakeAction(self,action,player):
        row = self._CoinRowAfterAction(action)
        assert row!=-1, "Action {0} cannot be taken.".format(action)
        self._game[row][action] = player
        win = self._CanAPlayerWin(row,action,player)
        if win==True:
            self.winner=player
        #print("Player {0} takes action {1}.".format(player, action))

    
    def PlayerAction(self):
        bestAction = input("Take action (0-6) : ")
        bestAction = int(bestAction)
        while(self._CoinRowAfterAction(bestAction)==-1):
            bestAction = input("Invalid Action. Try again. action (0-6) : ")
            bestAction = int(bestAction)
        self._TakeAction(bestAction,player=1)
    
    def GameTreePlayerAction(self,action):
        assert action>=0 and action<=6, "Invalid game tree player action. Action out of range."
        self._TakeAction(action,player=2)

    def PrintGameState(self,state=None):
        game = self._game if state==None else state
        print(*[0, 1, 2, 3, 4, 5, 6],sep=" ")
        print(*['-','-','-','-','-','-','-'],sep=" ")
        for row in game:
            print(*row,sep=" ")
        print()
    
    def GetCurrentState(self):
        currentState = copy.deepcopy(self._game)
        return currentState
    
    def SetCurrentState(self,gameState):
        self._game = copy.deepcopy(gameState)


def main():
    pass

if __name__=='__main__':
    main()