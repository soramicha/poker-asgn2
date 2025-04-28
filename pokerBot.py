# are we playing with the bot as opponent?
# if not then the opponent fold or stay would also be random or would we use MCTS as well
# implement shuffling and drawing mechanics, is using randint from random library good enough?
import random
import time

# gets list of cards ls_cards and community_cards if any
# returns true or false
def decideFoldOrStay(ls_cards, community_cards):
    print("decides whether player will fold or stay")

    # if player == 0, which is the bot, compute Monte Carlo
    # and return value based on that
    # based on questions response above

    # returns True if Stay, False for Fold
    # if the bot has win probability of 50% or over, then stay
    # else fold

# gets list of cards ls_cards
def MonteCarloTreeSearch(ls_cards):
    print("apply the mcts")

    # continue only for 10 seconds maximum
    start_time = time.time()
    while time.time() - start_time < 10:
        print("OKKK")
    print('10 seconds have passed!')

# gets an integer num_cards_to_lay and set of unusedCards
# returns the cards in list format
def layCards(num_cards_to_lay, unusedCards):
    res = []
    for _ in range(num_cards_to_lay):
        x = random.randint(1, 52)
        while x not in unusedCards:
            x = random.randint(1, 52)
        res.append(x)
        unusedCards.remove(x)
    # returns a tuple: the cards in list format and an updated unusedCards
    return (res, unusedCards)

def poker():
    # [1 - 13] heart
    # [14 - 26] spade
    # [27 - 39] clover
    # [40 - 52] diamond
    unusedCards = set(i for i in range(1, 53))
    
    # first round: pre-flop
    botCards, unusedCards = layCards(2, unusedCards)
    opponentCards, unusedCards = layCards(2, unusedCards)
    # decide whether players fold or stay
    """
        if (not decideFoldOrStay(botCards, None) or not decideFoldOrStay(opponentCards, None)):
            print("End of gameplay")
            return 0
    """

    # second round: flop
    community_cards, unusedCards = layCards(3, unusedCards)
    """
        if (not decideFoldOrStay(botCards, community_cards) or not decideFoldOrStay(opponentCards, community_cards)):
            print("End of gameplay")
            return 0
    """


    # third round: turn
    turn_card, unusedCards = layCards(1, unusedCards)
    # add the turn card into the list of community cards
    community_cards += turn_card
    """
        if (not decideFoldOrStay(botCards, community_cards) or not decideFoldOrStay(opponentCards, community_cards)):
            print("End of gameplay")
            return 0
    """

    # fourth and last round: river
    river_card, unusedCards = layCards(1, unusedCards)
    # add the turn card into the list of community cards
    community_cards += river_card
    """
        if (not decideFoldOrStay(botCards, community_cards) or not decideFoldOrStay(opponentCards, community_cards)):
            print("End of gameplay")
            return 0
    """

    # decide the winner (since no one has folded at this point!)
    """
    
    
    """
    print(botCards, opponentCards, community_cards, unusedCards)

poker()