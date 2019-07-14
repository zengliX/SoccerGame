"""
Create the soccer world
"""

import numpy as np

Avalue = 1
Bvalue = 2


class Player:
    def __init__(self, name, value, pos, hasball):
        """

        :param name: str
        :param value: int
        :param pos: tuple
        :param hasball: bool
        """
        self.name = name
        self.value = value
        self.row = pos[0]
        self.col = pos[1]
        self.hasball = hasball

    def dropball(self):
        self.hasball = False

    def gainball(self):
        self.hasball = True

    @property
    def position(self):
        return self.row, self.col

    def set_position(self, row, col):
        self.row = row
        self.col = col


class World:
    def __init__(self, nrow=2, ncol=4):
        """default grid size is (2, 4) as in the paper

        :param nrow: number of rows (>=1)
        :param ncol: number of columns (>=4)
        """
        assert nrow >= 1 and ncol >= 4
        self.grid = Grid(nrow, ncol)
        self.done = False
        self.nrow = nrow
        self.ncol = ncol
        bcol = (ncol-1)//2
        self.playerA = Player('A', Avalue, [0, bcol + 1], hasball=False)
        self.playerB = Player('B', Bvalue, [0, bcol], hasball=True)
        self.legal_actions = list("EWNS0")

    def random_action(self):
        return np.random.choice(self.legal_actions)

    @property
    def actions(self):
        return self.legal_actions[:]

    def player_state(self, p):
        """

        :param p: str, "A/B"
        """
        assert p in "AB"
        if p == 'A':
            return self.playerA.position + self.playerB.position + (self.playerA.hasball,)
        elif p == 'B':
            return self.playerB.position + self.playerA.position + (self.playerB.hasball,)

    def take_action(self, player, action):
        """

        :param player: str, 'A'/'B'
        :param action: 'E/W/N/S/0', '0' for stick
        :return:
        """
        assert action in self.legal_actions, "action {} not recognized".format(action)
        if player == 'A':
            row, col, reward, hasball, done = self.grid.accept_action(action, self.playerA, self.playerB)
        elif player == 'B':
            row, col, reward, hasball, done = self.grid.accept_action(action, self.playerB, self.playerA)
        else:
            raise Exception("Unknown player: {}".format(player))
        if done:
            self.done = done
        return row, col, reward, hasball, done

    def take_both_actions(self, player1, action1, player2, action2):
        """return information after both players move

        :param player1,2: 'A'/'B', player1 will move first
        :param action1,2: 'E/W/N/S/0', '0' for stick
        """
        # player 1 move
        row1, col1, r1, hasball1, done1 = self.take_action(player1, action1)
        if done1:
            row2, col2, r2, hasball2, done2 = self.take_action(player2, action2)
            return (row1, col1, r1, hasball1, True), (row2, col2, -r1, hasball2, True)
        # player 2 move
        row2, col2, r2, hasball2, done2 = self.take_action(player2, action2)
        if done2:
            r1 = -r2
            done1 = True
        return (row1, col1, r1, hasball1, done1), (row2, col2, r2, hasball2, done2)

    def reset(self):
        """
        reset players to initial positions
        """
        self.grid = Grid(self.nrow, self.ncol)
        self.done = False
        bcol = (self.ncol-1)//2
        self.playerA = Player('A', Avalue, [0, bcol + 1], hasball=False)
        self.playerB = Player('B', Bvalue, [0, bcol], hasball=True)

    def game_done(self):
        """
        is game over
        """
        return self.done

    def render_text(self):
        self.grid.render_text(self.playerA, self.playerB)


class Grid:
    action_map = {'0': [0, 0],
                  'N': [0, -1],
                  'W': [-1, 0],
                  'S': [0, 1],
                  'E': [1, 0]}

    def __init__(self, nrow, ncol):
        # grid
        self.nrow = nrow
        self.ncol = ncol
        self.grid_vals = np.zeros([nrow, ncol])
        self.grid_vals[:, 0] = Avalue
        self.grid_vals[:, -1] = Bvalue

    def accept_action(self, action, action_player, static_player):
        """

        :param action: char
        :param action_player: player who makes the move
        :param static_player: player who is not taking action
        :return:
        """
        icol, irow = self.action_map[action]
        newrow = action_player.row + irow
        newcol = action_player.col + icol
        # if collide with the other player
        if newrow == static_player.row and newcol == static_player.col:
            if action_player.hasball:
                action_player.dropball()
                static_player.gainball()
                # if static_player gains ball, and in the end zone, game over
                reward = -self.player_reward(static_player)
            else:
                reward = 0
            newrow, newcol = action_player.row, action_player.col
        else: # no collision
            newrow, newcol = self.clip_position(newrow, newcol)
            action_player.set_position(newrow, newcol)
            reward = self.player_reward(action_player)

        done = (reward != 0)
        return newrow, newcol, reward, action_player.hasball, done

    def clip_position(self, row, col):
        """
        if new position outside grid, clip it inside
        """
        return max(min(row, self.nrow-1),0), max(min(col, self.ncol-1), 0)

    def player_reward(self, p):
        """
        after player move to a new spot, determine player's reward
        p: Player class object
        """
        if self.grid_vals[p.row, p.col] == 0 or not p.hasball:
            return 0
        elif p.hasball and self.grid_vals[p.row, p.col] == p.value:
            return 100
        elif p.hasball and self.grid_vals[p.row, p.col] != p.value:
            return -100

    def render_text(self, playerA, playerB):
        """create text representation of the world

        :param playerA: Player object
        :param playerB: Player object
        :return:
        """
        # create grid
        self.grid_text = np.array([' ']*(2*self.nrow+1)*(3*self.ncol+1)).reshape(2*self.nrow+1, -1)
        odd_rows = range(0,len(self.grid_text),2)
        self.grid_text[odd_rows,:] = '-'
        even_rows = range(1,len(self.grid_text),2)
        third_cols = range(0,self.grid_text.shape[1],3)
        for irow in even_rows:
            for icol in third_cols:
                self.grid_text[irow, icol] = '|'
        # add player text
        self.grid_text[1 + 2 * playerA.row, 1 + 3 * playerA.col] = 'A'
        self.grid_text[1 + 2 * playerB.row, 1 + 3 * playerB.col] = 'B'
        # add ball
        if playerA.hasball:
            self.grid_text[1 + 2 * playerA.row, 2 + 3 * playerA.col] = '*'
        elif playerB.hasball:
            self.grid_text[1 + 2 * playerB.row, 2 + 3 * playerB.col] = '*'
        # print out
        res = ["A{}B".format(' '*(self.grid_text.shape[1]-2))]
        nrow = len(self.grid_text)
        for i in range(nrow):
            res.append(''.join(self.grid_text[i,:]))
        print('\n'.join(res))
