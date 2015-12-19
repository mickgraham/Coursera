# http://www.codeskulptor.org/

# implementation of card game - Memory

import simplegui
import random

point_top = [0, 0]
point_text = [0, 70]
point_bottom = [0, 100]
turns = 0

# helper function to initialize globals
def new_game():
    global state, turns, card_deck, exposed_deck, card_one_index, card_two_index
    
    # Reset the counters
    state = 0
    turns = 0
    label.set_text("Turns = " + str(turns))
    
    # Create and shuffle two sets of numbers from 0 to 7
    card_deck = range(8)
    card_deck.extend(range(8))
    random.shuffle(card_deck)
    
    # Initialise a set of booleans values indicating if the card is exposed
    exposed_deck = []
    for n in card_deck:
        exposed_deck.append(False)
    
    # Initialise the indexes of the currently selected cards
    card_one_index = -1
    card_two_index = -1
    
     
# define event handlers
def mouseclick(pos):
    global state, turns, card_deck, exposed_deck, card_one_index, card_two_index
    
    # Set the selected card index
    index = (pos[0] // 50)
    
    # Only process selecting an unexposed card
    if (exposed_deck[index] == False):
        # State machine 0->1->2->1->2...
        if state == 0:
            # First pick case just note the selection as card one index
            card_one_index = index
            state = 1
        elif state == 1:
            # Note the selection as card two index
            card_two_index = index
            
            # Increment the turn counter
            turns += 1
            label.set_text("Turns = " + str(turns))
                
            state = 2
        else:
            # Flip over cards that are not matching
            if (card_deck[card_one_index] != card_deck[card_two_index]):
                exposed_deck[card_one_index] = False
                exposed_deck[card_two_index] = False

            # Note the selection as card two index and reset card two index
            card_one_index = index
            card_two_index = -1
                
            state = 1
        
        # The selected unexposed card is always exposed
        exposed_deck[index] = True

    
# cards are logically 50x100 pixels in size    
def draw(canvas):
    global card_deck, exposed_deck

    # Craw a card or card back at each card index
    for index in range(16):
        if (exposed_deck[index] == True):
            # Draw a card
            point_text[0] = (index * 50) + 10
            canvas.draw_text(str(card_deck[index]), point_text, 60, "White")
        else:
            # Draw a card back (green rectangle)
            point_top[0] = (index * 50) + 25
            point_bottom[0] = (index * 50) + 25
            canvas.draw_line(point_top, point_bottom, 49, "Green")
        

# create frame and add a button and labels
frame = simplegui.create_frame("Memory", 800, 100)
frame.add_button("Reset", new_game)
label = frame.add_label("Turns = " + str(turns))

# register event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)

# get things rolling
new_game()
frame.start()


# Always remember to review the grading rubric