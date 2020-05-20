#!/usr/bin/env python
# coding: utf-8

# In[1]:


"""
This function return a list of successor states of a state
@param state - an array represents the position of the queens on the board
@param boulderX - the horizontal position of the boulder
@param boulderY - the vertical position of the boulder
"""
def succ(state, boulderX, boulderY):
    succ_list = []
    # Go through each column and change the position of the queen in it
    for i in range(len(state)):
        for j in range(0,len(state)):
            # Abandon the state if the position of the queen is the same
            # as the boulder
            if (i==boulderX and (j==boulderY or state[i]==j)):
                continue
            
            s = list(state)
            s[i] = j
            # If the state is valid and not duplicated, add to the succ list
            if s not in succ_list:
                succ_list.append(s)
    # If the initial state is in the succ list, remove it
    if state in succ_list:
        succ_list.remove(state)
    # Sort the list for the use of other function
    succ_list = sorted(succ_list)
    return succ_list


# In[2]:


"""
This function return the score of a state (number of queens attacked)
@param state - an array represents the position of the queens on the board
@param boulderX - the horizontal position of the boulder
@param boulderY - the vertical position of the boulder
"""
def f(state, boulderX, boulderY):
    score = 0
    # list of possible attackers
    uncheck = list(range(len(state)))
    # Check every queen if it is attacked
    for i in uncheck:
        # Set attacked to false at the beginning of every checking
        attacked = False
        
        # Check if there is any queen in the same row to the right
        for j in uncheck[i+1:]:
            # Stop if blocked by the boulder
            if j==boulderX and state[i]==boulderY:
                break
            # Set attacked to true if found a queen, increase score, and break
            if state[i]==state[j]:
                score = score+1
                attacked = True
                break
        
        # Check if the queen is not attacked
        if not attacked:
            # Check if the queen is attacked by any queen in the same row to the left
            for j in uncheck[1:i+1]:
                # Stop if blocked by the boulder
                if (i-j)==boulderX and state[i]==boulderY:
                    break
                # Set attacked to true if found a queen, increase score, and break
                if state[i]==state[i-j]:
                    score = score+1
                    attacked = True
                    break
                    
        # Check if the queen is not attacked     
        if not attacked:
            # Check if the queen is attack in the upper right diagonal direction
            for j in uncheck[i+1:]:
                # Calculate diagonal position
                upper_diagonal = state[i]-(j-i)
                # Break if reach the end of the board
                if upper_diagonal < 0:
                    break
                # Break if reach the boulder
                if j==boulderX and upper_diagonal==boulderY:
                    break
                # Set attacked to true, increase score, and break if found a queen
                if upper_diagonal==state[j]:
                    score = score+1
                    attacked = True
                    break
                    
        # Check if the queen is not attacked         
        if not attacked:
            # Check the right lower diagonal for possible attackers
            for j in uncheck[i+1:]:
                # Calculate the diagonal position
                lower_diagonal = state[i]+(j-i)
                # Break if reach the end of the board
                if lower_diagonal >= len(state):
                    break
                # Break if reach the boulder
                if j==boulderX and lower_diagonal==boulderY:
                    break
                # Increase score, set attacked to true, and break if found a queen
                if lower_diagonal==state[j]:
                    score = score+1
                    attacked = True
                    break
        
        # Check if the queen is not attacked
        if not attacked:
            # Check the upper diagonal direction to the left
            for j in uncheck[1:i+1]:
                # Calculate the position
                upper_diagonal = state[i]-j
                # Break if reach the end of the board
                if upper_diagonal < 0:
                    break
                # Break if reach the boulder
                if (i-j)==boulderX and upper_diagonal==boulderY:
                    break
                # Increase the score, set attacked to true, and break if found a queen
                if upper_diagonal==state[i-j]:
                    score = score+1
                    attacked = True
                    break

        # Check if the queen is not attacked
        if not attacked:
            # Check the lower diagonal direction to the left
            for j in uncheck[1:i+1]:
                # Calculate the position
                lower_diagonal = state[i]+j
                # Break if reach the end of the board
                if lower_diagonal >= len(state):
                    break
                # Break if reach the boulder
                if (i-j)==boulderX and lower_diagonal==boulderY:
                    break
                # Increase the score, set attacked to true, and break if found a queen
                if lower_diagonal==state[i-j]:
                    score = score+1
                    attacked = True
                    break
                
    return score


# In[3]:


"""
This function return the successor which is the "lowest" and have to lowest score
from the current state
@param curr - an array represents the current position of the queens on the board
@param boulderX - the horizontal position of the boulder
@param boulderY - the vertical position of the boulder
"""
def choose_next(curr, boulderX, boulderY):
    # Generate successor list
    succ_list = succ(curr, boulderX, boulderY)
    score = f(curr, boulderX, boulderY)
    # Default next state is the original state
    solution = [curr]
    temp = 0
    # Go through all succ list to find the best state
    for i in succ_list:
        temp = f(i, boulderX, boulderY)
        # return the state immediately if it is the solution
        if temp==0:
            return i
        # If found a better state, clear all worse solution and add the better one in
        if score > temp:
            score = temp
            solution.clear()
            solution.append(i)
        # If it is a tie, add it to the solution list
        elif score == temp:
            solution.append(i)
    
    # Sort the solution list to get the "lowest" one
    solution = sorted(solution)
    next_state = solution[0]
    
    # If no next state is better than the original solution, return None
    if next_state==curr:
        return None
    
    return next_state


# In[4]:


"""
This function Run the hill climbing algorithm on a given initial state until 
it finds a local minimum and gets stuck (or solves the problem)
@param initial_state - an array represents the initial position of the queens on the board
@param boulderX - the horizontal position of the boulder
@param boulderY - the vertical position of the boulder
"""
def nqueens(initial_state, boulderX, boulderY):
    state = initial_state
    # Print the initial state along with the score
    print(str(initial_state)+' - f='+str(f(state, boulderX, boulderY)))
    
    # Stop finding next state when a solution is found
    while f(state, boulderX, boulderY)!=0:
        # Find a better successor state
        next_state = choose_next(state, boulderX, boulderY)
        # Break if the it stuck
        if next_state == None:
            break
        # Assign next state to state to continue finding solution
        state = next_state
        print(str(state)+' - f='+ str(f(state, boulderX, boulderY)))
        
    return state


# In[5]:


import random
"""
This function is the helper function which generate a new random valid state
where the queens are randomly put on each column but not in the same position
as the boulder
@param n - the size of the square board
@param boulderX - the horizontal position of the boulder
@param boulderY - the vertical position of the boulder
"""
def nqueens_restart_helper(n, boulderX, boulderY):
    state = []
    # Put a queen in a random place in each column
    for i in range(n):
        rand = random.randint(0,n-1)
        # Change the position if the queen is put into the boulder position
        while i==boulderX and rand==boulderY:
            rand = random.randint(0,n-1)
        
        state.append(rand)
    return state


# In[6]:


"""
This function run the hill-climbing algorithm on an n*n board k times with 
random restarts, terminates immediately if solution is found, return
best solution after k times otherwise.
@param n - the size of the square board
@param k - the number of trial
@param boulderX - the horizontal position of the boulder
@param boulderY - the vertical position of the boulder
"""
def nqueens_restart(n, k, boulderX, boulderY):
    final_score = n
    solution = []
    # Run nqueens k times
    for i in range(k):
        state = nqueens_restart_helper(n, boulderX, boulderY)
        score = f(state, boulderX, boulderY)
        # Terminate immediately if solution is randomly generated
        if score == 0:
            print('(output from run '+str(i+1)+': '+str(state)+', puzzle solved)')
            print()
            print(str(state))
            return None
        next_state = nqueens(state, boulderX, boulderY)
        # Print the randomly generated state if nqueens cannot find a better one
        if next_state==None:
            print('(output from run '+str(i+1)+': '+str(state)+', gets stuck at f='+str(score)+')')
            # Keep track of the best solution
            if final_score > score:
                final_score = score
            continue
        next_score = f(next_state, boulderX, boulderY)
        # Terminate immediately if nqueens finds a solution
        if next_score == 0:
            print('(output from run '+str(i+1)+': '+str(next_state)+', puzzle solved)')
            print()
            print(str(next_state))
            return None
        # If better state is found, clear previous solution to add new one
        if final_score > next_score:
            solution.clear()
            solution.append(next_state)
            final_score = next_score
        # If equal state is found, add to the solution list
        elif final_score == next_score:
            solution.append(next_state)
        print('(output from run '+str(i+1)+': '+str(next_state)+', gets stuck at f='+str(next_score)+')')
        
    # Print best solution
    print()
    print(solution)

