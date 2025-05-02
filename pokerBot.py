# are we playing with the bot as opponent?
# if not then the opponent fold or stay would also be random or would we use MCTS as well
# implement shuffling and drawing mechanics, is using randint from random library good enough?
import random
import time
import math

class Node():
    def __init__(self, ucb1, parent, visits, round, play, community_cards, self_cards, unusedCards):
        # for my info; can delete later
        self.round = round
        self.play = play

        # track visits
        self.visits = visits
        # track ucb1
        self.ucb1 = ucb1
        # track parent for backpropagation
        self.parent = parent

        # track cards
        self.community_cards = community_cards
        self.self_cards = self_cards
        self.unusedCards = unusedCards

        # use left and right to create a binary tree because player can either only fold or stay
        self.left = None
        self.right = None

        # track wins and losses
        self.wins = 0
        self.losses = 0

def SelectAndExpand(root):
    print(root.round, root.play)
    ucb1_left, ucb1_right = 0, 0
    
    if root.left:
        print("yes there's left")
        ucb1_left = (root.left.wins / root.left.visits) + (math.sqrt(2) * math.sqrt(math.log(root.visits) / root.left.visits))
        # update ucb1
        root.left.ucb1 = ucb1_left
    else:
        # stop selection process, append a new child, and return it as the selected node
        ucb1_left = (0 / 1) + (math.sqrt(2) * math.sqrt(math.log(root.visits) / 1))

        # add a child
        root.left = Node(ucb1_left, root, 1, root.round + 1, "Stay", None, None, None)
        print("New left child")
        return root.left

    if root.right:
        print("yes there's right")
        ucb1_right = (root.right.wins / root.right.visits) + (math.sqrt(2) * math.sqrt(math.log(root.visits) / root.right.visits))
        # update ucb1
        root.right.ucb1 = ucb1_right
    else:
        # stop selection process, append a new child, and return it as the selected node
        ucb1_right = (0 / 1) + (math.sqrt(2) * math.sqrt(math.log(root.visits) / 1))

        # add a child
        root.right = Node(ucb1_right, root, 1, root.round + 1, "Fold", None, None, None)
        print("New right child")
        return root.right

    # otherwise, compare ucb1 values and visit the node with the higher value
    if ucb1_left >= ucb1_right:
        if root.left.visits <= 1:
            return root.left
        else:
            return SelectAndExpand(root.left)
    else:
        if root.right.visits <= 1:
            return root.right
        else:
            return SelectAndExpand(root.right)
    
def simulateFrom(node):
    curr_round = node.round

    # 5 rounds because that's how many times we play in poker
    while curr_round != 5:
        # 0 = fold, 1 = stay
        action = random.randint(0, 1)

        if action == 0:
            return -1

        # increment round played by 1
        curr_round += 1
    
    return 1

# gets list of cards ls_cards
def MonteCarloTreeSearch(root):

    # continue only for 10 seconds maximum
    #start_time = time.time()
    #while time.time() - start_time < 10:

    # play one random simulation
    # select and expand the node with the highest UCB1 value
    node = SelectAndExpand(root)
    print(node.round, node.play)

    # simulation
    res = simulateFrom(node)

    print(res)

    # backpropagation
    while node != None:
        node.visits += 1

        if res == 1:
            # add player win
            node.wins += 1
        else:
            node.losses += 1
        
        node = node.parent
        

   

    return 50

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
    opponentCards, unusedCards = layCards(2, unusedCards)

    # define root node
    root = Node(0, None, 1, 0, None, [], botCards, unusedCards)

    # decide whether players fold or stay
    if not decideFoldOrStay(root):
        print("End of gameplay")
        return 0

    # second round: flop
    """community_cards, unusedCards = layCards(3, unusedCards)

    # define new root node
    root = Node(0, None, 1, 0, None, community_cards, botCards, unusedCards)

    if not decideFoldOrStay(botCards, community_cards, root):
        print("End of gameplay")
        return 0


    # third round: turn
    turn_card, unusedCards = layCards(1, unusedCards)
    # add the turn card into the list of community cards
    community_cards += turn_card
    if not decideFoldOrStay(botCards, community_cards, root):
        print("End of gameplay")
        return 0

    # fourth and last round: river
    river_card, unusedCards = layCards(1, unusedCards)
    # add the turn card into the list of community cards
    community_cards += river_card
    if not decideFoldOrStay(botCards, community_cards, root):
        print("End of gameplay")
        return 0

    # decide the winner (since no one has folded at this point!)
    
    
    
    
    print(botCards, opponentCards, community_cards, unusedCards)
    """

poker()