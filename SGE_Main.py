'''
============================== SGE_Main =========================================
             Collection of methods for a single game of poker
=================================================================================
'''
import random
import RankingsSystem

# =========================================================================================================
                # Build a new deck
# =========================================================================================================
def LoadDeck():
    Deck = []
    for y in range(0, 52):                          # Deck is a list of 52 elements
      if y < 13:                                    # where each element is a list of two elements
          suit = 'C'                                # element 1 being the card value, element 2
      elif y < 26:                                  # being the card suit
          suit = 'D'
      elif y < 39:
          suit = 'H'
      else:
          suit = 'S'


      if y <= 8:
          Deck.append([y + 2, suit])                # Card value is index plus 2
      elif 13 <= y < 22:
          Deck.append([y-11, suit])                 # Card value is index plus 2 minus 13
      elif 26 <= y < 35:
          Deck.append([y-24, suit])                 # Card value is index plus 2 minus 26
      elif 39 <= y < 47:
          Deck.append([y-37, suit])                 # Card value is index plus 2 minus 39


      elif y == 9 or y == 22 or y == 35 or y == 48:
        Deck.append(['J',suit])
      elif y == 10 or y == 23 or y == 36 or y == 49:
        Deck.append(['Q',suit])
      elif y == 11 or y == 24 or y == 37 or y == 50:
        Deck.append(['K', suit])
      elif y == 12 or y == 25 or y == 38 or y == 51:
        Deck.append(['A', suit])


    return Deck
# =========================================================================================================
# =========================================================================================================
# =========================================================================================================
                # Return 1 card and modified deck
# =========================================================================================================
def Draw1Card(IncomingDeck):

    YourCard = IncomingDeck.pop()                               # Draw top card from the deck

    return YourCard, IncomingDeck
# =========================================================================================================
# =========================================================================================================
# =========================================================================================================
                # Dealing the first two cards to each player, constructing "Hands"
# =========================================================================================================
def ConstructHands(NumberOfPlayers, InputDeck):
    Hands = []
    flag = 0
    ReturnDeck = InputDeck

    for y in range(0,NumberOfPlayers):

        Card1, ReturnDeck = Draw1Card(ReturnDeck)
        Card2, ReturnDeck = Draw1Card(ReturnDeck)
        Hands.append(Card1)
        Hands.append(Card2)                     # Next loop the return deck is 2 cards lighter

    return Hands, ReturnDeck                    # Hands is a list of all dealt player cards together

def TheFlop(IncomingDeck):                                      # Return the flop cards and a modified deck
    ElFloppo = ["Null", "Null", "Null"]
    ElFloppo[0], ReturnDeck = Draw1Card(IncomingDeck)
    ElFloppo[1], ReturnDeck = Draw1Card(ReturnDeck)
    ElFloppo[2], ReturnDeck = Draw1Card(ReturnDeck)

    return ElFloppo, ReturnDeck
# =========================================================================================================
# =========================================================================================================
# =========================================================================================================
                # Draw 1 card for the turn, return it with the modified deck
# =========================================================================================================
def TheTurn(IncomingDeck):                                      # Return the turn card and a modified deck

    ElTurno, ReturnDeck = Draw1Card(IncomingDeck)

    return ElTurno, ReturnDeck
# =========================================================================================================
# =========================================================================================================
# =========================================================================================================
                # Draw 1 card for the river, return it with the modified deck
# =========================================================================================================
def TheRiver(IncomingDeck):                                     # Return the river card and a modified deck

    ElRivero, ReturnDeck = Draw1Card(IncomingDeck)

    return ElRivero, ReturnDeck

def ArrangeForChecking(NumOfPlayers, PlayerHands, Flop, Turn, River):
    Cards = ["Null"]                                             # Cards is a list for ranking the hand of each player
    for x in range(0, NumOfPlayers):                             # Arrange Cards for inspection for each player
        Cards[x] = [PlayerHands[x][0], PlayerHands[x][1], Flop[0], Flop[1], Flop[2], Turn, River]
        Cards.append("Null")                                     # Extend cards list by another entry
    del Cards[NumOfPlayers]                                      # After looping delete the last empty Cards entry


    for x in range(0, NumOfPlayers):                             # Cards is the array of 7 card hands
        for y in range(0, 7):                                    # This loop replaces all of the face card
            if Cards[x][y][0] == 'J':                            # string objects with numbers for easier calculation
                Cards[x][y][0] = 11
            if Cards[x][y][0] == 'Q':
                Cards[x][y][0] = 12
            if Cards[x][y][0] == 'K':
                Cards[x][y][0] = 13
            if Cards[x][y][0] == 'A':
                Cards[x][y][0] = 14

    return Cards

def DetermineWinner(NumOfPlayers, PlayerHands, Flop, Turn, River):

    Winner = [0]
    BestHands = ["Null"]

    Cards = ArrangeForChecking(NumOfPlayers, PlayerHands, Flop, Turn, River)            # Format 7 card hands
    for x in range(0,NumOfPlayers):                                                     # Here we find the best hand
        BestHands[x] = RankingsSystem.BestOfSeven(Cards[x])                             # for each individual player
        BestHands.append("")                                                            # BestHands should be indexed
                                                                                        # five best cards per player
    BestHands.pop()

    TopHand = ["Null"]
    x = 0

    while True:
        if x >= NumOfPlayers:
            break
        if x == 0:
            TopHand = BestHands[0]

        if RankingsSystem.Compare(TopHand[1], BestHands[x][1]) == "Hand1":
            pass
        elif RankingsSystem.Compare(TopHand[1], BestHands[x][1]) == "Hand2":
            TopHand = BestHands[x]
            Winner = [x]
        else:
            Winner.append(x)
        x +=1

    print("\n \n AND THE WINNER IS ... \n \n \n")
    print("Player ... ", Winner)

# =========================================================================================================
# =========================================================================================================
# =========================================================================================================
                # A single game of poker, intake from OGE is the # of players, return is winner # and $
# =========================================================================================================
def Game(NumOfPlayers):

    print("\n=========================\n")
    print("     A New Hand!        \n")
    print("========================= \n \n \n \n")

    PlayerHands = []
    TheDeck = LoadDeck()                                         # Call a new, ordered, deck
    random.shuffle(TheDeck)                                      # Randomize the deck
    Hands, TheDeck = ConstructHands(NumOfPlayers, TheDeck)       # Hands is unsorted list of player's cards

    for x in range(0,NumOfPlayers):                              # Creates empty PlayerHands list sized NumPlayers
        PlayerHands.append("Null")
    for x in range(0,NumOfPlayers):                              # Gathers 2 cards and assigns to indexed PlayerHands
        PlayerHands[x] = [Hands.pop(), Hands.pop()]              # so PlayerHands[0] is 0th player's 2-cards

    Flop, TheDeck = TheFlop(TheDeck)                             # Draw flop - 3 cards
    Turn, TheDeck = TheTurn(TheDeck)                             # Draw turn - 1 card
    River, TheDeck = TheRiver(TheDeck)                           # Draw river - 1 card

    for x in range(0,NumOfPlayers):
        print("Player hand #", x)
        print(PlayerHands[x])

    print("\n", "Flop is: ")
    print(Flop)
    print("\n", "Turn is: ")
    print(Turn)
    print("\n", "River is: ")
    print(River)

# TODO: Build a series of interrupts for betting in between the above rounds. Eventually modify the entire Game()
# TODO: file to accept pot values and pass back again to OGE

    DetermineWinner(NumOfPlayers, PlayerHands, Flop, Turn, River)   # For now we have no betting, just pick a winner



# The below is just when testing within the SGE
if __name__ == "__main__":
    Game(3)

