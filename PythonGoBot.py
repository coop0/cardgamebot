from collections import defaultdict as dd
import copy
def stealcard(discard_history, player_no, turns, hand):
    ''' Choses a card to steal from other players
    '''
    # Maximum cards of a value other players can have
    cardsmaxiallow = 3
    # Iterate over each players to find if any have the max cards allowed
    for j in range(1, 4):
        nextplayer = []
        for i in range(0, turns):
            nextplayer.append(discard_history[i][(player_no + j) % 4])
        nextplayerdd = dd(int)
        for cards in nextplayer:
            nextplayerdd[cards[:-1]] += 1
        maxcards = 0
        cardkey = 0
        # Find the value that has the most cards for that player
        for keys in nextplayerdd:
            if nextplayerdd[keys] > maxcards and nextplayerdd[keys] <= 3:
                maxcards = nextplayerdd[keys]
                cardkey = keys
        # Check that the max is 3
        if maxcards >= cardsmaxiallow:
            for cards in hand:
                if cards[:-1] == cardkey:
                    return cards
    # If it cant find a card to steal return 0
    return 0
def comp10001go_play(discard_history, player_no, hand):
    ''' Takes the inputs of discards, own player number and hand and chooses
    a card to be taken and added to their mixture of cards
    '''
    global cardsleft
    valuedict = {'0': 10, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, 
                 '8': 8, '9': 9, '10': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 20}
    cardsdict = dd(int)
    prioritycard = cardsleft[2]  
    # Calculate turns
    turns = 10 - len(hand)
    # On the last turn take the card which is remaining in hand
    if turns  == 9:
        return hand[0]
    nkindsel = False    
    mycards = []
    mydict = dd(int)
    output =False
    maxnumcard = 0
    maxnumcards= []
    
    # Calculates the cards that are in the game
    if turns < 4:
        for cardse in hand:
            cardsleft[0].append(cardse)
        if turns > 0:
            for i in range(turns):
                cardposition = (player_no + i) % 4
                cardsleft[0].remove(discard_history[-1][cardposition])
    # Updates the cards that have been taken after 4 turns
    if turns >= 4:
        for card in discard_history[-1]:
            cardsleft[0].remove(card)
    cards = cardsleft[0]
    # Calculates the cards that it has discarded already
    for i in range(len(discard_history)):
        mycards.append(discard_history[i][player_no])
    for cards in mycards:
        mydict[cards[:-1]] +=1   
    # Calculates what cards the program should go for once it knows all cards
    # That are in play
    if turns == 4:    
        priority = False    
        prioritycard = []
        biggestkey = 0
        # Calcualates the values that are left in the playable deck
        for items in cards:
            cardsdict[items[:-1]] +=1
        # Calculates if it is able to make a 4 of a kind with it
        for keys in cardsdict:
            if cardsdict[keys] == 4 - mydict[keys]:
                cardsleft[2].append(keys)
                priority = True
            # Calculates a three of a kind if it cant make a 4
            if not priority:
                for keys in cardsdict:
                    if cardsdict[keys] == 3 - mydict[keys]:
                        cardsleft[2].append(keys)


    prioritycard = cardsleft[2]
    # Calculate the card which we have the most of that is also in the hand
    for cards in hand:
        if cards[:-1] in mydict:
            if int(mydict[cards[:-1]]) > maxnumcard:
                maxnumcards = []
                nkindsel = True
                maxnumcards.append(cards)
            if int(mydict[cards[:-1]]) == maxnumcard:
                maxnumcards.append(cards)
    # Make a nkind selection based off cards in hand and cards discarded       
    if nkindsel:
        maximum = 0
        for cardsa in maxnumcards:
            if int(valuedict[cardsa[:-1]]) >= maximum:
                outcard = cardsa
            
        return outcard
    

    
    # Make a selection of cards that we can make 3 or 4 of a kind with
    if bool(prioritycard) is not False:
        for card in hand:
            if card[:-1] in prioritycard:
                if int(card[:-1]) > biggestkey:
                    biggestkey = int(card[:-1])
                    outcard = card
                    output = True
    if output:  
        return outcard


    # Defines the priority if no other conditions are met
    prioritydict = {'0': 27, '2': 2, '3': 3, '4': 4, '5': 5, '6': 15, '7': 24,
                    '8': 26, '9': 21, '10': 23, 'J': 28, 'Q': 16, 'K': 13,
                    'A': 1} 
    # Take lower cards after the 7th turn to minimise losses
    if turns >= 7:
        prioritydict = {'0': 10, '2': 30, '3': 29, '4': 28, '5': 27, '6': 26,
                        '7': 25, '8': 24, '9': 23, '10': 22, 'J': 21, 'Q': 16,
                        'K': 13, 'A': 1}    
    # Calculates whether we need to steal a card from a player
    steal = stealcard(discard_history, player_no, turns, hand)
    if steal:
        return steal
    bestchoice = 0
    # Choose a card based on the priority dictionary at the time
    for card in hand:
        value = prioritydict[card[:-1]]
        if value > bestchoice:
            bestchoice = value
            outcard = card
    return outcard

def comp10001go_group(discard_history, player_no):  
    ''' Groups the players discards into scoring groups
    '''
    playerscards = []
    # Calculate the players cards
    for cardl in discard_history:
        playerscards.append(cardl[player_no])
    outputlist = []

    nkind = dd(list)
    # Calculate the amount of cards for each value
    for cards in playerscards:
        nkind[cards[:-1]].append(cards[-1])
    # Create nkind groups 
    for keys in nkind:
        if len(nkind[keys]) > 1:
            outputl = []
            nkindcard = nkind[keys]
            # Remove the items that the groups are made of from primary list
            if keys != 'A':
                for i in range(len(nkindcard)):
                    outputl.append(keys + nkindcard[i])
                    playerscards.remove(keys + nkindcard[i])
                outputlist.append(outputl)
    # The rest of the cards are 'orphan cards'
    for cards in playerscards:
        outputlist.append([cards])
    return outputlist
            
    
cardsleft = [[], 0, []]        

