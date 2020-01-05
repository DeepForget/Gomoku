import numpy as np
import constant as c
import copy

# board: 1 means black -1 means white 0 means nothing
# player: BLACK/WHITE player's turn
# game_history allows player to go back
class Game(object):
    def __init__(self):
        self.board = np.zeros((c.SIZE, c.SIZE))
        self.player = c.BLACK_P
        self.game_history = []
        self.mode = 0 #0=uninitialized, 1=pvai, 2=aivp, 3=pvp, 4=aivsai
        self.finish = 0 #0=not finish, 1=BLACK WIN, 2=WHITE WIN

    # return True if legal, False if illegal
    def move(self, pos, record=True):
        # if game ended, cannot precede
        if self.finish:
            return False

        # otherwise place stone
        x, y = pos
        if self.board[x,y] != 0:
            return True
        if record:
            state = (np.copy(self.board), self.player)
            self.game_history.append(state)
        # place piece
        self.board[x,y] = self.player
        self.finish = self.check_win(pos)
        # switch player if no winner
        if self.finish == 0: self.player = -self.player
        return False

    def check_win(self, pos):
        x,y = pos
        row = self.board[x,:]
        col = self.board[:,y]
        diag1, diag2 = [], []
        for off in range(-4, 5):
            if x+off>=0 and x+off<c.SIZE and y+off>=0 and y+off<c.SIZE:
                diag1.append(self.board[x+off, y+off])
            if x+off>=0 and x+off<c.SIZE and y-off>=0 and y-off<c.SIZE:
                diag2.append(self.board[x+off, y-off])
        lines = [row,col,diag1,diag2]
        for line in lines:
            longest = 0
            for e in line:
                if longest*e <= 0: longest = e
                else:
                    longest += e
                    if longest >= 5: return 1
                    elif longest <= -5: return -1
        return 0

    def go_back(self, step_size=1):
        for i in range(step_size):
            state = self.game_history.pop()
        self.board, self.player = state
        self.finish = 0

    def get_msg(self):
        if self.mode == 0:
            return [('BLACK', c.BLACK), ('WHITE', c.WHITE), ('PVP', c.RED), ('AI', c.GREEN)]
        if self.mode==1 or self.mode==2 or self.mode==3:
            return [('GO BACK', c.BLACK), ('CONCEDE', c.RED), ('RESTART', c.GREEN)]
        else:
            return []

    def get_button(self, button):
        if self.mode==0 and button>=1 and button<=4:
            self.mode = button
            return
        # if click "go back button"
        if (self.mode == 1 or self.mode == 2):
            if (button==1 and len(self.game_history)>=2): self.go_back(2)
        if self.mode == 3:
            if (button==1 and len(self.game_history)>=1): self.go_back(1)
        # if click "restart button"
        if self.mode>=1 and self.mode<=3 and button == 3:
            self.__init__()
        # if click "concede button"
        if self.mode>=1 and self.mode<=3 and button == 2 and self.finish==0:
            self.finish = -self.player
