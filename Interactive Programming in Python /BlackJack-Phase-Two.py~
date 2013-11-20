# Mini-project #6 - Blackjack
# http://www.codeskulptor.org/#user25_Freh0wu6J3_0.py
import simplegui
import random

# load card sprite - 949x392 - source: jfitz.com
CARD_SIZE = (73, 98)
CARD_CENTER = (36.5, 49)
card_images = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/cards.jfitz.png")

CARD_BACK_SIZE = (71, 96)
CARD_BACK_CENTER = (35.5, 48)
card_back = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/card_back.png")    

# default message
YOU_HAVE_BUSTED = "You have busted!"
YOU_WIN = "Player wins!"
YOU_LOSE = "Player lose!"
DEALER_WIN = "Dealer wins!"
DEALER_BUSTED = "Dealer busted!"
NEW_DEAL = "New deal?"
HIT_OR_STAND = "Hit or stand?"
INVALID_DEAL = "Pressed 'Deal' in the middle of the game!"

# initialize some useful global variables
in_play = False
player_busted = False
outcome = ""
invalid_deal = False
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

    def __str__(self):
        output = ""
        for item in self.cards:
            output += str(item) + " "
        return output

    def add_card(self, card):
        self.cards.append(card)

    def get_value(self):
        # count aces as 1, if the hand has an ace, then add 10 to hand value if it doesn't bust
        # compute the value of the hand, see Blackjack video
        score = 0
        aces = 0
        for item in self.cards:
            score += VALUES[item.rank]
            if item.rank == 'A':
                aces += 1
                
        while aces > 0:
            if score + 10 <= 21:
                score += 10
                aces -= 1
            else:
                aces = 0
        return score
   
    def draw(self, canvas, pos):
        # draw a hand on the canvas, use the draw method for cards
        index = 0
        for item in self.cards:
            item.draw(canvas, (pos[0] + CARD_SIZE[0] * index + 10 * index, pos[1]))
            index+=1
     
# define deck class 
class Deck:
    def __init__(self):
        self.cards = []
        for s in SUITS:
            for r in RANKS:
                self.cards.append(Card(s,r))

    def shuffle(self):
        # shuffle the deck 
        random.shuffle(self.cards)

    def deal_card(self):
        # deal a card object from the deck
        return self.cards.pop(0)
    
    def __str__(self):
        # return a string representing the deck
        output = ""
        for item in self.cards:
            output += " " + str(item)
        return output
    
# draw the back card
def card_draw_back(canvas, pos):
    canvas.draw_image(card_back, CARD_BACK_CENTER, CARD_BACK_SIZE, [pos[0] + CARD_BACK_CENTER[0], pos[1] + CARD_BACK_CENTER[1]], CARD_BACK_SIZE)

def is_invalid_deal(condition):
    global invalid_deal, score 
    invalid_deal = ""
    if condition:
        invalid_deal = INVALID_DEAL + " " + YOU_LOSE
        score -= 1

#define event handlers for buttons
def deal():
    global outcome, in_play, player_hands, score
    global dealer_hands, deck, player_busted

    is_invalid_deal(in_play)

    outcome = HIT_OR_STAND
        
    player_busted = False
    in_play = True    

    #setup game
    player_hands = Hand()
    dealer_hands = Hand()
    deck = Deck()
    deck.shuffle()
    
    # add two card to the player hand
    player_hands.add_card(deck.deal_card())
    player_hands.add_card(deck.deal_card())
    
    # add two card to the dealer hand
    dealer_hands.add_card(deck.deal_card())
    dealer_hands.add_card(deck.deal_card())


def hit():
    # if the hand is in play, hit the player
    # if busted, assign a message to outcome, update in_play and score
    global outcome, in_play, player_busted, score
    global invalid_deal
    is_invalid_deal(False)
    if player_busted:
        outcome = YOU_HAVE_BUSTED + " " + NEW_DEAL
    else:
        if player_hands.get_value() <= 21:
            player_hands.add_card(deck.deal_card())
    
        if player_hands.get_value() > 21:
            score -= 1
            outcome = YOU_HAVE_BUSTED + " " + NEW_DEAL
            in_play = False
            player_busted = True
        else:
            outcome = HIT_OR_STAND 
       
def stand():
    global outcome, in_play, player_busted, score
    # if hand is in play, repeatedly hit dealer until his hand has value 17 or more
    # assign a message to outcome, update in_play and score
    in_play = False
    is_invalid_deal(in_play)
    if player_busted:
        outcome = YOU_HAVE_BUSTED + " " + NEW_DEAL
    else:
        while dealer_hands.get_value() < 17:
            dealer_hands.add_card(deck.deal_card())
            
        if dealer_hands.get_value() > 21:
            score += 1
            outcome = DEALER_BUSTED + " " + YOU_WIN + " " + NEW_DEAL
        elif dealer_hands.get_value() >= player_hands.get_value():
            score -=1
            outcome = DEALER_WIN + " " + NEW_DEAL
        else:
            score += 1
            outcome = YOU_WIN + " " + NEW_DEAL
            
            
# draw handler    
def draw(canvas):
    # test to make sure that card.draw works, replace with your code below
    canvas.draw_text('Blackjack', (40, 90), 100, 'Yellow')
    
    # dealer canvas
    dText = ""
    dealer_pos = (40, 170)
    dealer_hands.draw(canvas, dealer_pos)
    if in_play:
        card_draw_back(canvas, (41, 171))
        dText = "Dealer (?)"
    else:
        dText = "Dealer (" + str(dealer_hands.get_value()) + ")"
    canvas.draw_text(dText, (40, 150), 30, 'Black')

    # player canvas
    player_hands.draw(canvas, (40, 340))
    pText = "Player (" + str(player_hands.get_value()) + ")"
    canvas.draw_text(pText, (40, 320), 30, 'Black')

    # messages
    canvas.draw_text(outcome, (40, 480), 30, 'Black')
    canvas.draw_text("Score: " + str(score), (40, 520), 30, 'Black')
    # alert message
    canvas.draw_text(invalid_deal, (40, 560), 25, 'Red')

    
# setup enviroment (players and deck)
player_hands = Hand()
dealer_hands = Hand()
deck = Deck()
    
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