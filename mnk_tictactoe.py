# -*- coding: utf-8 -*-
"""
Spyder Editor

@author: Naturedrag
"""

import numpy as np
import random

class mnk_tictactoe:

    def __init__(self):
        self.m = 0 # number of rows
        self.n = 0 # number of coloums
        self.max_move = self.m*self.n # maximum possible moves, game ends when self.count == self.max_move
        self.count = 0 # tracks the number of moves that have been made
        self.k = 0 # the win condition, ie. number of consicutive required for a win
        self.board = np.zeros([self.m,self.n]) #initalization of the board
        self.ai = 0 # by default the ai level is 0
        self.next_pos = -1
        self.aicol = -1
        self.airow = -1
        self.comp = ''
        self.mode = 0
    
    def usr_input(self):
            urow = int(input("Enter row: "))
            ucol = int(input("Enter coloumn: "))       
            valid = self.check_valid(urow,ucol)
            if valid is True:
                self.update_board(urow,ucol)
            elif valid is False:
                print("Not a valid move")
                self.usr_input()
            return

    def comp_input(self):    # this function will make a random  move on the board. 
        crow = np.random.randint(1,self.m+1)
        ccol = np.random.randint(1,self.n+1)
        x = self.check_valid(crow,ccol) #checks the validity of the move
        if x == True:
            self.update_board(crow,ccol) 
        elif x == False:
            self.comp_input() #if the move is not valid, it calls the function again to make another move. 
        return

    def comp_input_ai(self):
    	if self.ai > 0 and self.next_pos != -1: #if a directed move cannot be made, the ai will make a random move
    		self.aicol += 1 # needed to add this cause of indexing issues while updating the board
    		self.airow += 1 
    		self.update_board(self.airow,self.aicol) 
    		self.next_pos = -1
    		self.aicol = -1
    		self.airow = -1
    	else:
    		self.comp_input()
    	return
    
    def update_board(self,row,col): # takes the row and coloumn and places them on the board                    
        if (self.count)%2 == 0: # move by player one
            self.board[row - 1,col - 1] = 1 #this will be printed as 'O' in the print_board function
        elif (self.count)%2 == 1:
            self.board[row - 1,col - 1] = 2 #this will be printed as 'X' in the print_board function
        self.count += 1 # Tracks the number of moves made
        return

    def check_valid(self,row,col): # Checks the validity of the move, if there is something already in that location False is returned
        if self.board[row-1,col-1] == 0.:
            return True
        else:
            return False
    
    def check_win(self): # checks if a win condition has been met. 
    	if self.check_row() or self.check_clm() or self.check_d1() or self.check_d2(): #If there is any direction in which a win happens this if statement willl become true
    		return True 
    	else:
    		if self.count == self.max_move: # if the maximum number of moves have been made the game draws
    			return "Draw"
    		return False # This will continue the game

    def check_row(self): # Goes through each row for win condiotions
    	rowindex = 0 
    	while rowindex < self.n:
    		ls = self.board[rowindex,:]
    		if self.ai == 0:
    			scr = self.check_score(ls) 
    		else:
    			scr = self.check_score_1(ls)
    			if self.next_pos > -1 and self.aicol == -1: #only updates the next position if these values have been updater in check_score_1
	    			self.airow = rowindex
    				self.aicol = self.next_pos
    		rowindex+=1
    		if scr >= self.k or scr <= -(self.k): # if score matches win contition, True is returned and the loop breaks to end the game. 
    			return True
    		else:
    			x = False
    	return x
            
    def check_clm(self): # goes through each coloumn	
    	clmindex = 0 
    	while clmindex < self.n:
    		ls = self.board[:,clmindex]
    		if self.ai == 0:
    			scr = self.check_score(ls)
    		else:
    			scr = self.check_score_1(ls)
    			if self.next_pos > -1 and self.aicol == -1:
    				self.aicol = clmindex
    				self.airow = self.next_pos
    		clmindex+=1
    		if scr >= self.k or scr <= -(self.k): 
    			return True
    		else:
    			x = False
    	return x
    		
    def check_d1(self): # goes through each diagonal from top left to bottom right
    	j = -(self.m - self.k) 
    	while j <= (self.n -self.k): 
    		ls = self.board.diagonal(j)
    		if self.ai == 0:
    			scr = self.check_score(ls)
    		else:
    			scr = self.check_score_1(ls)
    			scr = self.check_score(ls)
    			if self.next_pos > -1 and self.aicol == -1: 
	    			if j > 0: # j controls the position of the diagonal and updates the next move accordingly
	    				self.airow = self.next_pos
	    				self.aicol = j + self.next_pos
	    			if j < 0:
	    				self.airow = abs(j) + self.next_pos
	    				self.aicol = self.next_pos
	    			if j == 0:
	    				self.airow = self.next_pos
	    				self.aicol = self.next_pos
    		j+=1
    		if scr >= self.k or scr <= -(self.k): 
    			return True
    		else:
    			x = False
    	return x
    			
    def check_d2(self): # goes through each diagonal from top right to bottom left
    	j = -(self.m - self.k)
    	temp = np.flip(self.board, 1) #flipping the board to access the diagonals in the opposite directions. 
    	while j <= (self.n - self.k):
    		ls = temp.diagonal(j)
    		if self.ai == 0:
    			scr = self.check_score(ls)
    		else:
    			scr = self.check_score_1(ls)
    			scr = self.check_score(ls)
    			if self.next_pos > -1 and self.aicol == -1:
	    			if j > 0:
	    				self.airow = self.next_pos
	    				self.aicol = self.n - (j + self.next_pos) - 1
	    			if j < 0:
	    				self.airow = abs(j) + self.next_pos
	    				self.aicol = self.n - self.next_pos - 1
	    			if j == 0:
	    				self.airow = self.next_pos
	    				self.aicol = self.n - self.next_pos -1
    		j+=1
    		if scr >= self.k or scr <= -(self.k): 
    			return True
    		else:
    			x = False
    	return x

    def check_score(self,ls): 
        '''
        A simlified version of the check score function, called when there is 
        no need for the ai to track a possible move or when the ai difficulty 
        is set to 0
        '''
        scr = 0
        maxscr = 0
        for ele in ls:
        	if ele == 2. and scr >= 0:
        		scr += 1
        	if ele == 2. and scr < 0:
        		scr = 1 
        	if ele == 1. and scr <= 0:
        		scr -= 1
        	if ele == 1. and scr > 0:
        		scr = -1
        	if ele == 0.:
        		scr = 0
        	if maxscr < abs(scr):
        		maxscr = scr
        return maxscr

    def check_score_1(self,ls): #called when ai needs the track a possible win condition
        '''
        This function will calculate the score, but also keep track of possible
        gaps where a move could be made to either stop the player or allow the 
        ai to win the game. Only one gap is tracked, the moment a second gap is 
        encountered the possible score resets. The pos_scr tracks the maximum 
        possible score,and if it is equal to k(win condition) it save the  
        position of the gap where the next move is to be made. Thew cur_scr only  
        tracks the current max score, this is used only to check if the game has  
        been won when cur_scr matches k.
        '''
    
        def score(ele,pos_scr,cur_scr,gap,i,maxscr):  
            gap_pos = -1                              
            if ele == 2. and pos_scr >=0:              
                pos_scr += 1                          
                cur_scr += 1                         
            if ele == 2. and pos_scr <0:
                gap = False
                pos_scr = 1
                cur_scr = 1
            if ele == 1. and pos_scr <=0:
                pos_scr -= 1
                cur_scr -= 1
            if ele == 1. and pos_scr >0:
                gap = False
                pos_scr = -1
                cur_scr = -1
            if ele == 0. and gap == True:
                pos_scr = 0
                cur_scr = 0
            if ele == 0. and gap == False and pos_scr!=0:
                gap = True
                gap_pos = i
                cur_scr = 0
                if pos_scr < 0:
                    pos_scr -= 1
                if pos_scr > 0:
                    pos_scr += 1
            if abs(pos_scr) == self.k and self.next_pos == -1:
                if self.ai == 1 and ((self.comp == 'First' and pos_scr > 0) or (self.comp == 'Second' and pos_scr < 0)): #This is used by ai1 to prevent it from blocking winning moves by the opponent
                    gap_pos = -1
                self.next_pos = gap_pos # updates the posiotion of the gap when contiotions are met
            if maxscr < abs(cur_scr):
                maxscr = cur_scr
            i+=1
            return maxscr,pos_scr,cur_scr,gap
    	
        pos_scr = 0
        cur_scr = 0
        gap = False
        maxscr = 0
        i = 0
    	
        for ele in ls:
            maxscr,pos_scr,cur_scr,gap = score(ele,pos_scr,cur_scr,gap,i,maxscr)
            i+=1

        if self.next_pos == -1: #if no gap is found, the list is reveresed and checked backwards to account for gaps that could start in the begining of a clm, row or diagonal. 
            pos_scr = 0
            cur_scr = 0
            gap = False
            maxscr = 0
            for ele in reversed(ls):
                i-=1
                maxscr,pos_scr,cur_scr,gap = score(ele,pos_scr,cur_scr,gap,i,maxscr)

        return maxscr

    def printboard (self):
        '''
        Function to print the current state of the board, 0 is replaced by '_', 1 by 'O' ,and 2 by 'X'
        '''
        print (f'Board state after {self.count} moves')
        for row in self.board:
            for ele in row:
                if ele == 0.:
                	print ('_', end = ' ')
                if ele == 1.:
                	print ('O', end = ' ')
                if ele == 2.:
                	print ('X', end = ' ')    		
            print ('\n')

    def game_input(self):
        '''
        Function to set the board size and winning conditions
        '''
        self.m = int(input("Enter number of Rows: "))
        self.n = int(input("Enter number of Coloums: "))
        self.k = int(input("Enter win condition: "))
        if self.k > self.m or self.k > self.n:
            print ("This is not an acceptable win condition, enter values again")
            self.game_input()

    def start(self):
        print ('Game start')
        self.count = 0
        self.game_input()
        self.max_move = self.m*self.n # setting the max move limit
        self.board = np.zeros([self.m,self.n]) # initalising the board
        self.ai = int(input("enter ai difficulty (0/1/2): ")) 
        self.move = random.choice([1,2]) # Chooses who will have the first move
        if self.move == 1:
            print ('Player begins')
            self.comp = 'Second'
        elif self.move == 2:
            print ('Computer begins')
            self.comp = 'First'
        while self.count < self.max_move: # This loop will alternate between the user and the ai
            if self.move%2 == 1:
                self.usr_input()
            elif self.move%2 == 0:
                self.comp_input_ai()
            win = self.check_win() # Checks for the win condition
            self.printboard()
            if win == True:
                if self.move%2 == 1:
                    print ('Winner is: Player')
                    break
                elif self.move%2 == 0:
                    print ('Winner is: Computer')
                    break
            elif win == "Draw":
                print ('Draw')
            self.move+=1 # increments after each move is made to keep track of how many moves have been made

mnk_tictactoe().start()

