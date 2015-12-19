# http://www.codeskulptor.org/

# Mini-project #6 - Blackjack

import simplegui
import random

# load card sprite - 936x384 - source: jfitz.com
CARD_SIZE = (72, 96)
CARD_CENTER = (36, 48)
card_images = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/cards_jfitz.png")

CARD_BACK_SIZE = (72, 96)
CARD_BACK_CENTER = (36, 48)
card_back = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/card_jfitz_back.png")    

# initialize some useful global variables
in_play = False
outcome = ""
question = ""
score = 0

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}


# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
        
# define hand class
class Hand:
    def __init__(self):
        self.cards = []
        self.value = 0
        self.contains_ace = False

    def __str__(self):
        # return a string representation of a hand
        return_value = "Hand contains"
        for i in range(len(self.cards)):
            return_value += " " +  str(self.cards[i])
        return return_value

    def add_card(self, card):
        self.cards.append(card)
        cardValue = VALUES[card.get_rank()]
        self.value += cardValue
        if (cardValue == 1):
            self.contains_ace = True

    def get_value(self):
        # count aces as 1, if the hand has an ace, then add 10 to hand value if it doesn't bust
        # compute the value of the hand, see Blackjack video
        if (self.contains_ace and self.value <= 11):
            return self.value + 10
        else:
            return self.value
   
    def draw(self, canvas, pos):
        # draw a hand on the canvas, use the draw method for cards
        index = 0
        for card in self.cards:
            card.draw(canvas, [pos[0] + index, pos[1]])
            index += CARD_SIZE[1]
 
        
# define deck class 
class Deck:
    def __init__(self):
        self.cards = []
        for suit in SUITS:
            for rank in RANKS:
                self.cards.append(Card(suit, rank))

    def shuffle(self):
        # shuffle the deck 
        random.shuffle(self.cards)

    def deal_card(self):
        return self.cards.pop(self.cards.index(random.choice(self.cards)))
    
    def __str__(self):
        return_value = "Deck contains"
        for i in range(len(self.cards)):
            return_value += " " + str(self.cards[i])
        return return_value  


#define event handlers for buttons
def deal():
    global deck, dealer_hand, player_hand, outcome, question, score, in_play

    if (in_play == True):
        outcome = "Dealer wins. Player redeal!"
        question = "New deal?"
        score -= 1
        in_play = False
        return
    
    # your code goes here
    deck = Deck()
    deck.shuffle()
    
    dealer_hand = Hand()
    player_hand = Hand()
    
    dealer_hand.add_card(deck.deal_card())
    dealer_hand.add_card(deck.deal_card())
    player_hand.add_card(deck.deal_card())
    player_hand.add_card(deck.deal_card())

    in_play = True
    outcome = ""
    question = "Hit or Stand?"
    
    
def hit():
    # if the hand is in play, hit the player
    global player_hand, outcome, question, score, in_play
    
    if (in_play == False):
        return
    
    player_hand.add_card(deck.deal_card())

    # if busted, assign a message to outcome, update in_play and score
    if (player_hand.get_value() > 21):
        outcome = "Dealer wins. Player busted!"
        question = "New deal?"
        score -= 1
        in_play = False
       
def stand():
    global deck, dealer_hand, player_hand, outcome, question, score, in_play

    if (in_play == False):
        return
    
    # if hand is in play, repeatedly hit dealer until his hand has value 17 or more
    while (dealer_hand.get_value() < 17):
        dealer_hand.add_card(deck.deal_card())

    # assign a message to outcome, update in_play and score
    if (dealer_hand.get_value() > 21):
        outcome = "Player Wins. Dealer busted!"
        question = "New deal?"
        score += 1
    elif (player_hand.get_value() > dealer_hand.get_value()):
        outcome = "Player Wins!"
        question = "New deal?"
        score += 1
    else:
        outcome = "Dealer Wins!"
        question = "New deal?"
        score -= 1
        
    in_play = False

# draw handler    
def draw(canvas):
    # test to make sure that card.draw works, replace with your code below
    global deck, dealer_hand, player_hand
    
    canvas.draw_text("Blackjack", [100, 100], 50, "Black", "serif")
    canvas.draw_text("Score = " + str(score), [400, 100], 30, "Black", "serif")
    
    if (in_play):
        canvas.draw_text("Dealer", [40, 200], 30, "Black", "serif")
    else:
        canvas.draw_text("Dealer (" + str(dealer_hand.get_value()) + ")", [40, 200], 30, "Black", "serif")
    canvas.draw_text(outcome, [200, 200], 30, "Black", "serif")
    dealer_hand.draw(canvas, [40, 230])
    if (in_play):
        canvas.draw_image(card_back,
                          CARD_BACK_CENTER,
                          CARD_BACK_SIZE,
                          [CARD_CENTER[0] + 40, CARD_CENTER[1] + 230],
                          CARD_BACK_SIZE)
    
    canvas.draw_text("Player (" + str(player_hand.get_value()) + ")", [40, 400], 30, "Black", "serif")
    canvas.draw_text(question, [200, 400], 30, "Black", "serif")
    player_hand.draw(canvas, [40, 430])
    

# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)


# get things rolling
deal()
frame.start()


# remember to review the gradic rubric