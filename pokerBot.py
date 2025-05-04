import random
import time

# we will track game state and action taken
class Node():
    def __init__(self, parent, visits, community_cards, self_cards, unusedCards):
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

def royalFlush(cards):
    # royal flush - 10, J, Q, K, A of the SAME suit
    s1 = {10, 11, 12, 13, 1}
    s2 = {14, 23, 24, 25, 26}
    s3 = {27, 36, 37, 38, 39}
    s4 = {40, 49, 50, 51, 52}
    if s1.issubset(cards) or s2.issubset(cards) or s3.issubset(cards) or s4.issubset(cards):
        return True
    return False

def straightFlush(cards):
    maximum, streak = 0, 0

    # hearts
    for i in range(1, 14):
        if i in cards:
            streak += 1
            maximum = max(maximum, streak)
        else:
            streak = 0
    
    if maximum == 5:
        return True
    
    # spades
    maximum, streak = 0, 0
    for i in range(14, 27):
        if i in cards:
            streak += 1
            maximum = max(maximum, streak)
        else:
            streak = 0

    if maximum == 5:
        return True

    # clover
    maximum, streak = 0, 0
    for i in range(27, 40):
        if i in cards:
            streak += 1
            maximum = max(maximum, streak)
        else:
            streak = 0

    if maximum == 5:
        return True
    
    # diamond
    maximum, streak = 0, 0
    for i in range(40, 53):
        if i in cards:
            streak += 1
            maximum = max(maximum, streak)
        else:
            streak = 0

    if maximum == 5:
        return True
    
    # return False when none apply
    return False

def fourOfAKind(cards):
    for i in range(1, 14):
        # check all multiples
        if i in cards and i + 13 in cards and i + 26 in cards and i + 39 in cards:
            return True
    return False

def fullHouse(cards):
    three, num = 0, 0
    for i in range(1, 14):
        # check all multiples
        if i in cards:
            three += 1
        if i + 13 in cards:
            three += 1
        if i + 26 in cards:
            three += 1
        if i + 39 in cards:
            three += 1

        if three == 3:
            num = i
            break
        
        # reset three
        three = 0

    if three != 3:
        return False

    # now check for doubles
    two = 0
    for i in range(1, 14):
        # check all multiples
        if i in cards and i != num:
            two += 1
        if i + 13 in cards and i != num:
            two += 1
        if i + 26 in cards and i != num:
            two += 1
        if i + 39 in cards and i != num:
            two += 1

        if two >= 2:
            break

        # reset two
        two = 0

    if two >= 2:
        return False

    return True

def flush(cards):
    # hearts
    if sum(1 for i in range(1, 14) if i in cards) >= 5:
        return True
    
    # spades
    if sum(1 for i in range(14, 27) if i in cards) >= 5:
        return True

    # clover
    if sum(1 for i in range(27, 40) if i in cards) >= 5:
        return True
    
    # diamond
    if sum(1 for i in range(40, 53) if i in cards) >= 5:
        return True

    return False

def straight(cards):
    cards = sorted(cards)
    streak, n = 1, len(cards)
    for i in range(1, n):
        if streak == 0:
            streak += 1
        elif cards[i] == cards[i - 1] + 1 or cards[i] == cards[i - 1] + 13 + 1 or cards[i] == cards[i - 1] + 26 + 1 or cards[i] == cards[i - 1] + 39 + 1:
            streak += 1
        else:
            streak = 0
        
    if streak == 5:
        return True
    
    return False

def threeOfAKind(cards):
    three = 0
    for i in range(1, 14):
        # check all multiples
        if i in cards:
            three += 1
        if i + 13 in cards:
            three += 1
        if i + 26 in cards:
            three += 1
        if i + 39 in cards:
            three += 1

        if three == 3:
            break
        
        # reset three
        three = 0

    if three >= 3:
        return True
    
    return False

def twoPair(cards):
    two1, num = 0, 0
    for i in range(1, 14):
        # check all multiples
        if i in cards:
            two1 += 1
        if i + 13 in cards:
            two1 += 1
        if i + 26 in cards:
            two1 += 1
        if i + 39 in cards:
            two1 += 1

        if two1 == 2:
            num = i
            break
        
        # reset two1
        two1 = 0

    if two1 != 2:
        return False

    # now check for another pair
    two2 = 0
    for i in range(1, 14):
        # check all multiples
        if i in cards and i != num:
            two2 += 1
        if i + 13 in cards and i != num:
            two2 += 1
        if i + 26 in cards and i != num:
            two2 += 1
        if i + 39 in cards and i != num:
            two2 += 1

        if two2 >= 2:
            break

        # reset two
        two2 = 0

    if two2 < 2:
        return False

    return True

def onePair(cards):
    two = 0
    for i in range(1, 14):
        # check all multiples
        if i in cards:
            two += 1
        if i + 13 in cards:
            two += 1
        if i + 26 in cards:
            two += 1
        if i + 39 in cards:
            two += 1

        if two == 2:
            break
        
        # reset two
        two = 0

    if two >= 2:
        return True
    
    return False

def highCard(cards):
    maximum = 0
    for i in range(1, 14):
        if i in cards or i + 13 in cards or i + 26 in cards or i + 39 in cards:
            if i == 1:
                return 100
            maximum = max(maximum, i)
    return maximum

# if there's a tie, give point to bot automatically
# variable final is to only print out the last round
def WinOrLose(community_cards, cards, opponentCards, final):
    # calculate best cards for bot
    botCanUse = set(community_cards + cards)
    # calculate best cards for opponent
    oppCanUse = set(community_cards + opponentCards)

    # check for royal flush
    if royalFlush(botCanUse):
        if final: print("Bot won with royal flush!")
        return 1
    if royalFlush(oppCanUse):
        if final: print("Opponent won with royal flush!")
        return -1
    
    # check for straight flush - 5 cards in a row and SAME SUIT but NOT 10 - A
    if straightFlush(botCanUse):
        if final: print("Bot won with straight flush!")
        return 1
    if straightFlush(oppCanUse):
        if final: print("Opponent won with straight flush!")
        return -1
    
    # four of a kind - four cards of the same rank + 1 random other card (ex. 9 9 9 9 and K) don't have to be in same suit
    if fourOfAKind(botCanUse):
        if final: print("Bot won with four of a kind!")
        return 1
    if fourOfAKind(oppCanUse):
        if final: print("Opponent won with four of a kind!")
        return -1

    # full house - 3 cards of one rank and 2 of another rank ex. 8 8 8 6 6
    if fullHouse(botCanUse):
        if final: print("Bot won with full house!")
        return 1
    if fullHouse(oppCanUse):
        if final: print("Opponent won with full house!")
        return -1
    
    # flush - any five cards of SAME SUIT, not in sequence ex. 2 4 6 10 9 of all hearts
    if flush(botCanUse):
        if final: print("Bot won with flush!")
        return 1
    if flush(oppCanUse):
        if final: print("Opponent won with flush!")
        return -1
    
    # straight - five cards in a row, DIFFERENT SUITS ex. 2 diamond 3 heart 4 spade 5 diamond 6 heart
    if straight(botCanUse):
        if final: print("Bot won with straight!")
        return 1
    if straight(oppCanUse):
        if final: print("Opponent won with straight!")
        return -1
    
    # three of a kind - three cards of the same rank ex. 3 3 3 9 K
    if threeOfAKind(botCanUse):
        if final: print("Bot won with three of a kind!")
        return 1
    if threeOfAKind(oppCanUse):
        if final: print("Opponent won with three of a kind!")
        return -1
    
    # two pair - two cards of one rank and two cards of another rank ex. J J 4 4 2
    if twoPair(botCanUse):
        if final: print("Bot won with two pairs!")
        return 1
    if twoPair(oppCanUse):
        if final: print("Opponent won with two pairs!")
        return -1
    
    # one pair - two cards of the same rank ex. Q Q 5 9 2
    if onePair(botCanUse):
        if final: print("Bot won with one pair!")
        return 1
    if onePair(oppCanUse):
        if final: print("Opponent won with one pair!")
        return -1
    
    # high card - when you have nothing else, highest card matters ex. A 7 8 9 5 => A is the highest as Ace
    if highCard(botCanUse) > highCard(oppCanUse):
        if final: print("Bot won with high card!")
        return 1
    else:
        if final: print("Opponent won with high card!")
        return -1

def SelectAndExpand(root):
    # when we encounter unexpanded node
    if root.unusedCards != []:
        # create a child
        child = Node(root, 1, [i for i in root.community_cards], root.self_cards, [i for i in root.unusedCards])
        # get a random community_card; update root.unusedCards
        community_card, child.unusedCards = layCards(1, child.unusedCards)
        # child will add a new community card
        child.community_cards += community_card
        # root will add child
        root.children.append(child)
        # return the node we will use for simulation
        return child
    # otherwise keep traveling
    else:
        for child in root.children:
            return SelectAndExpand(child)
    
def simulateFrom(node):
    community_cards = [i for i in node.community_cards]
    unusedCards = [i for i in node.unusedCards]

    # randomly simulate opponent cards
    opponentCards, unusedCards = layCards(2, unusedCards)

    # 5 rounds because that's how many times we play in poker
    while len(community_cards) < 5:
        # get a community card
        card, unusedCards = layCards(1, unusedCards)

        # add that card to the rest of community_cards
        community_cards += card

    # decide win or not
    return WinOrLose(community_cards, node.self_cards, opponentCards, False)

# gets list of cards ls_cards
def MonteCarloTreeSearch(root):
    totalWins = 0
    totalSimulations = 0
    
    # continue only for 10 seconds maximum
    start_time = time.time()
    while True:
        if time.time() - start_time >= 10:
            print("10 seconds already ran! Stopping Monte Carlo Tree Search...")
            break

        # select and expand the node
        node = SelectAndExpand(root)

        # simulation
        res = simulateFrom(node)

        if res == 1:
            totalWins += 1

        # increment number of simulations
        totalSimulations += 1

    print(totalSimulations, "total simulations", totalWins, "total wins")
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
    oppCards, _ = layCards(2, unusedCards)

    # define root node
    root = Node(None, 1, [], botCards, unusedCards)

    # decide whether players fold or stay
    if not decideFoldOrStay(root):
        print("Bot folded. End of gameplay at Pre-Flop")
        return 0

    # second round: flop
    community_cards, unusedCards = layCards(3, unusedCards)

    # define new root node
    root = Node(0, None, community_cards, botCards, unusedCards)

    if not decideFoldOrStay(root):
        print("Bot folded. End of gameplay at Flop")
        return 0

    # third round: turn
    turn_card, unusedCards = layCards(1, unusedCards)
    # add the turn card into the list of community cards
    community_cards += turn_card

    # define new root node
    root = Node(0, None, community_cards, botCards, unusedCards)

    if not decideFoldOrStay(root):
        print("Bot folded. End of gameplay at Turn")
        return 0

    # fourth and last round: river
    river_card, unusedCards = layCards(1, unusedCards)
    # add the turn card into the list of community cards
    community_cards += river_card

    # define new root node
    root = Node(0, None, community_cards, botCards, unusedCards)

    if not decideFoldOrStay(root):
        print("Bot folded. End of gameplay at River")
        return 0

    # decide the actual winner (since no one has folded at this point!)    
    _ = WinOrLose(community_cards, botCards, oppCards, True) == 1
    print(botCards, community_cards, oppCards)

poker()