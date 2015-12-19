# http://www.codeskulptor.org/

# "Guess the number" mini-project
import math
import random
import simplegui

# global variables
num_range = 100
num_guesses = 7
secret_number = 0

# helper function to start and restart the game
def new_game():
    # initialize global variables used in your code here
    global secret_number
    
    print "New Game. Range is from 0 to " + str(num_range)
    print "Number of remaining guesses is " + str(num_guesses)
    
    secret_number = random.randrange(0, num_range)

# define event handlers for control panel
def range100():
    # button that changes the range to [0,100) and starts a new game 
    global num_range
    num_range = 100
    new_game()

def range1000():
    # button that changes the range to [0,1000) and starts a new game     
    global num_range
    num_range = 1000
    new_game()
    
def input_guess(guess):
    # main game logic goes here
    global num_guesses
    global secret_number
      
    num_guesses = num_guesses - 1
    
    print ""
    print "Guess was " + guess
    print "Number if remaining guesses is " + str(num_guesses)
    
    if (int(guess) < secret_number):
        print "Higher!"
    elif (int(guess) > secret_number):
        print "Lower!"
    else:
        print "Correct!"

# create frame
frame = simplegui.create_frame("Guess the number", 200, 200)

# register event handlers for control elements and start frame
frame.add_button("Range is [0,100)", range100, 200)
frame.add_button("Range is [0,1000)", range1000, 200)
frame.add_input("Enter a guess", input_guess, 200)

# call new_game 
new_game()


# always remember to check your completed program against the grading rubric
