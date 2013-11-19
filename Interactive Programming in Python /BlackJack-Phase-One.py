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

# initialize some useful global variables
in_play = False
player_busted = False
outcome = ""
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
        pass    # draw a hand on the canvas, use the draw method for cards
 
        
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



#define event handlers for buttons
def deal():
    global outcome, in_play, player_hands
    global dealer_hands, deck, player_busted

    outcome = ""
    score = 0
    player_busted = False
    player_hands = Hand()
    dealer_hands = Hand()
    deck = Deck()
    deck.shuffle()

    player_hands.add_card(deck.deal_card())
    player_hands.add_card(deck.deal_card())

    dealer_hands.add_card(deck.deal_card())
    dealer_hands.add_card(deck.deal_card())
    
    print "Player hands: " + str(player_hands)
    print "Dealer hands: " + str(dealer_hands)
    in_play = True

def hit():
    # if the hand is in play, hit the player
    # if busted, assign a message to outcome, update in_play and score
    global outcome, in_play, player_busted, score
    if player_busted:
        outcome = "You have busted"
        print outcome
    else:
        print "Player score: " + str(player_hands.get_value())
        if player_hands.get_value() <= 21:
            player_hands.add_card(deck.deal_card())
    
        if player_hands.get_value() > 21:
            outcome = "You have busted"
            in_play = True
            player_busted = True
            print outcome
    
        score = player_hands.get_value()
        print "Player score: " + str(score)
 

       
def stand():
    global outcome, in_play, player_busted, score
    # if hand is in play, repeatedly hit dealer until his hand has value 17 or more
    # assign a message to outcome, update in_play and score
    if player_busted:
        outcome = "You have busted"
    else:
        dealer_win = False
        print "Dealer score: " + str(dealer_hands.get_value())
        while dealer_hands.get_value() < 17:
            dealer_hands.add_card(deck.deal_card())
            print "Dealer score: " + str(dealer_hands.get_value())

        if dealer_hands.get_value() > 21:
            outcome = "Dealer busted!"
            outcome += "Player wins!"
        elif dealer_hands.get_value() >= player_hands.get_value():
            outcome = "Dealer wins!"          
        else:
            outcome = "Player wins!"          
            
    print outcome
# draw handler    
def draw(canvas):
    # test to make sure that card.draw works, replace with your code below
    
    card = Card("S", "A")
    card.draw(canvas, [300, 300])


# players
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


# remember to review the gradic rubricpy