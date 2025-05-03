# are we playing with the bot as opponent?
# if not then the opponent fold or stay would also be random or would we use MCTS as well
# implement shuffling and drawing mechanics, is using randint from random library good enough?
import random
import time
import math

# we will track game state and action taken
class Node():
    def __init__(self, parent, visits, round, community_cards, self_cards, unusedCards):
        # for my info; can delete later
        self.round = round

        # track visits
        self.visits = visits
        # track parent for backpropagation
        self.parent = parent

        # track cards
        self.community_cards = community_cards
        self.self_cards = self_cards
        self.unusedCards = unusedCards

        # track children
        self.children = []

        # track wins and losses
        self.wins = 0
        self.losses = 0

def SelectAndExpand(root):
    print("Selecting...", root.round)
    # when we encounter unexpanded node
    if root.unusedCards != []:
        # create a child
        child = Node(root, 1, root.round + 1, [i for i in root.community_cards], root.self_cards, [i for i in root.unusedCards])
        # get a random community_card; update root.unusedCards
        community_card, root.unusedCards = layCards(1, root.unusedCards)
        # child will add a new community card
        child.community_cards += community_card
        # root will add child
        root.children.append(child)
        # return the node we will use for simulation
        return child
    # otherwise keep traveling
    else:
        print("USED ALL COMBOS")
        for child in root.children:
            return SelectAndExpand(child)
    
def simulateFrom(node):
    print("Simulation starting!")
    community_cards = [i for i in node.community_cards]
    unusedCards = [i for i in node.unusedCards]
    print("Ok")
    # randomly simulate opponent cards
    opponentCards, unusedCards = layCards(2, unusedCards)
    print("Laui")
    # 5 rounds because that's how many times we play in poker
    while len(community_cards) < 5:
        card, unusedCards = layCards(1, unusedCards)
        print("lol", len(community_cards), unusedCards)
        # add to community_cards
        community_cards += card

    # decide win or not
    print(community_cards, node.self_cards, opponentCards)
    return WinOrLose(community_cards, node.self_cards, opponentCards)

# if there's a tie, give point to bot automatically
def WinOrLose(community_cards, cards, opponentCards):
    # calculate best cards for opponent
    botCanUse = set(community_cards + cards)
    oppCanUse = set(community_cards + opponentCards)

    # royal flush - 10, J, Q, K, A of the SAME suit
    s1 = {10, 11, 12, 13, 1}
    s2 = {14, 23, 24, 25, 26}
    s3 = {27, 36, 37, 38, 39}
    s4 = {40, 49, 50, 51, 52}
    if s1.issubset(botCanUse) or s2.issubset(botCanUse) or s3.issubset(botCanUse) or s4.issubset(botCanUse):
        return 1
    elif s1.issubset(oppCanUse) or s2.issubset(oppCanUse) or s3.issubset(oppCanUse) or s4.issubset(oppCanUse):
        return -1
    
    # straight flush - 5 cards in a row and SAME SUIT but NOT 10 - A
    maxBot, maxOpp = 0, 0
    streakBot, streakOpp = 0, 0
    for i in range(1, 14):
        if i in botCanUse:
            streakBot += 1
            maxBot = max(maxBot, streakBot)
        else:
            streakBot = 0
        
        if i in oppCanUse:
            streakOpp += 1
            maxOpp = max(maxOpp, streakOpp)
        else:
            streakOpp = 0

    # check potential win/loss
    if maxBot == 5:
        return 1
    if maxOpp == 5:
        return -1
    

    # [1 - 13] heart
    # [14 - 26] spade
    # [27 - 39] clover
    # [40 - 52] diamond
    # TODO later
    return 1

    # calculate best cards for bot
    """
    - Four of a kind:
        - four cards of the same rank + 1 random other card (ex. 9 9 9 9 and K) don't have to be in same suit
    - full house:
        - 3 cards of one rank and 2 of another rank
            - ex. 8 8 8 6 6
    - flush:
        - any five cards of SAME SUIT, not in sequence
            - ex. 2 4 6 10 9 of all hearts
    - straight:
        - five cards in a row, DIFFERENT SUITS
            - ex. 2 diamond 3 heart 4 spade 5 diamond 6 heart
    - three of a kind:
        - three cards of the same rank
            - ex. 3 3 3 9 K
    - two pair:
        - two cards of one rank and two cards of another rank
            - ex. J J 4 4 2
    - one pair:
        - two cards of the same rank
            - Q Q 5 9 2
    - high card:
        - When you have nothing else, highest card matters:
            - ex. A 7 8 9 5 => A is the highest as Ace
    """


# gets list of cards ls_cards
def MonteCarloTreeSearch(root):
    totalWins = 0
    totalSimulations = 1
    
    # continue only for 10 seconds maximum
    start_time = time.time()
    while time.time() - start_time < 10:
        print("ROOT: ", root.community_cards)
        # select and expand the node
        node = SelectAndExpand(root)
        print(node.round, node.unusedCards, node.community_cards, "Picked node")

        # if we run out of unused cards, break
        if len(node.unusedCards) < 5 - len(node.community_cards) + 2:
            break

        # simulation
        res = simulateFrom(node)

        if res == 1:
            totalWins += 1

        print(res, "result")

        # backpropagation
        while node != None:
            node.visits += 1

            if res == 1:
                # add player win
                node.wins += 1
            else:
                node.losses += 1

            node = node.parent

        # increment number of simulations
        totalSimulations += 1

    print(totalSimulations, totalWins)
    return float(totalWins / totalSimulations) * 100

# gets list of cards ls_cards and community_cards if any
# returns true or false
def decideFoldOrStay(root):
    # compute Monte Carlo
    # returns True if Stay, False for Fold
    # if the bot has win probability of 50% or over, then stay else fold
    return True if MonteCarloTreeSearch(root) >= 50 else False

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

    # define root node
    root = Node(None, 1, 0, [], botCards, unusedCards)

    # decide whether players fold or stay
    if not decideFoldOrStay(root):
        print("End of gameplay at Pre-Flop")
        return 0

    # second round: flop
    community_cards, unusedCards = layCards(3, unusedCards)

    # define new root node
    root = Node(0, None, 1, community_cards, botCards, unusedCards)

    if not decideFoldOrStay(root):
        print("End of gameplay at Flop")
        return 0

    # third round: turn
    turn_card, unusedCards = layCards(1, unusedCards)
    # add the turn card into the list of community cards
    community_cards += turn_card

    # define new root node
    root = Node(0, None, 1, community_cards, botCards, unusedCards)

    if not decideFoldOrStay(root):
        print("End of gameplay at Turn")
        return 0

    # fourth and last round: river
    river_card, unusedCards = layCards(1, unusedCards)
    # add the turn card into the list of community cards
    community_cards += river_card

    # define new root node
    root = Node(0, None, 1, community_cards, botCards, unusedCards)

    if not decideFoldOrStay(root):
        print("End of gameplay at River")
        return 0

    # decide the winner (since no one has folded at this point!)
    
    
    
    
    print(botCards, community_cards, unusedCards)

poker()