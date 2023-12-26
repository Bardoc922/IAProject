import socket
import random
import ClientBase
from operator import itemgetter
# IP address and port
TCP_IP = '127.0.0.1'
TCP_PORT = 5000
BUFFER_SIZE = 1024

# Agent
POKER_CLIENT_NAME = 'Random'
CURRENT_HAND = []

class pokerGames(object):
    def __init__(self):
        self.PlayerName = POKER_CLIENT_NAME
        self.Chips = 0
        self.CurrentHand = []
        self.Ante = 0
        self.playersCurrentBet = 0

'''
* Gets the name of the player.
* @return  The name of the player as a single word without space. <code>null</code> is not a valid answer.
'''
def queryPlayerName(_name):
    if _name is None:
        _name = POKER_CLIENT_NAME
    return _name

'''
* Modify queryOpenAction() and add your strategy here
* Called during the betting phases of the game when the player needs to decide what open
* action to choose.
* @param minimumPotAfterOpen   the total minimum amount of chips to put into the pot if the answer action is
*                              {@link BettingAnswer#ACTION_OPEN}.
* @param playersCurrentBet     the amount of chips the player has already put into the pot (dure to the forced bet).
* @param playersRemainingChips the number of chips the player has not yet put into the pot.
* @return                      An answer to the open query. The answer action must be one of
*                              {@link BettingAnswer#ACTION_OPEN}, {@link BettingAnswer#ACTION_ALLIN} or
*                              {@link BettingAnswer#ACTION_CHECK }. If the action is open, the answers
*                              amount of chips in the anser must be between <code>minimumPotAfterOpen</code>
*                              and the players total amount of chips (the amount of chips alrady put into
*                              pot plus the remaining amount of chips).
'''
def queryOpenAction(_minimumPotAfterOpen, _playersCurrentBet, _playersRemainingChips):
    print("Player requested to choose an opening action.")

    # Random Open Action
    def chooseOpenOrCheck():
        if _playersCurrentBet + _playersRemainingChips > _minimumPotAfterOpen:
            #return ClientBase.BettingAnswer.ACTION_OPEN,  iOpenBet
            return ClientBase.BettingAnswer.ACTION_OPEN,  (random.randint(0, 10) + _minimumPotAfterOpen) if _playersCurrentBet + _playersRemainingChips + 10> _minimumPotAfterOpen else _minimumPotAfterOpen
        else:
            return ClientBase.BettingAnswer.ACTION_CHECK

    return {
        0: ClientBase.BettingAnswer.ACTION_CHECK,
        1: ClientBase.BettingAnswer.ACTION_CHECK,
    }.get(random.randint(0, 2), chooseOpenOrCheck())

'''
* Modify queryCallRaiseAction() and add your strategy here
* Called during the betting phases of the game when the player needs to decide what call/raise
* action to choose.
* @param maximumBet                the maximum number of chips one player has already put into the pot.
* @param minimumAmountToRaiseTo    the minimum amount of chips to bet if the returned answer is {@link BettingAnswer#ACTION_RAISE}.
* @param playersCurrentBet         the number of chips the player has already put into the pot.
* @param playersRemainingChips     the number of chips the player has not yet put into the pot.
* @return                          An answer to the call or raise query. The answer action must be one of
*                                  {@link BettingAnswer#ACTION_FOLD}, {@link BettingAnswer#ACTION_CALL},
*                                  {@link BettingAnswer#ACTION_RAISE} or {@link BettingAnswer#ACTION_ALLIN }.
*                                  If the players number of remaining chips is less than the maximum bet and
*                                  the players current bet, the call action is not available. If the players
*                                  number of remaining chips plus the players current bet is less than the minimum
*                                  amount of chips to raise to, the raise action is not available. If the action
*                                  is raise, the answers amount of chips is the total amount of chips the player
*                                  puts into the pot and must be between <code>minimumAmountToRaiseTo</code> and
*                                  <code>playersCurrentBet+playersRemainingChips</code>.
'''
def queryCallRaiseAction(_maximumBet, _minimumAmountToRaiseTo, _playersCurrentBet, _playersRemainingChips):
    print("Player requested to choose a call/raise action.")
    # Random Open Action
    def chooseRaiseOrFold():
        if  _playersCurrentBet + _playersRemainingChips > _minimumAmountToRaiseTo:
            return ClientBase.BettingAnswer.ACTION_RAISE,  (random.randint(0, 10) + _minimumAmountToRaiseTo) if _playersCurrentBet+ _playersRemainingChips + 10 > _minimumAmountToRaiseTo else _minimumAmountToRaiseTo
        else:
            return ClientBase.BettingAnswer.ACTION_FOLD
    return {
        0: ClientBase.BettingAnswer.ACTION_FOLD,
        #1: ClientBase.BettingAnswer.ACTION_ALLIN,
        1: ClientBase.BettingAnswer.ACTION_FOLD,
        2: ClientBase.BettingAnswer.ACTION_CALL if _playersCurrentBet + _playersRemainingChips > _maximumBet else ClientBase.BettingAnswer.ACTION_FOLD
    }.get(random.randint(0, 3), chooseRaiseOrFold())

'''
* Modify queryCardsToThrow() and add your strategy to throw cards
* Called during the draw phase of the game when the player is offered to throw away some
* (possibly all) of the cards on hand in exchange for new.
* @return  An array of the cards on hand that should be thrown away in exchange for new,
*          or <code>null</code> or an empty array to keep all cards.
* @see     #infoCardsInHand(ca.ualberta.cs.poker.Hand)
'''
def queryCardsToThrow(_hand):
    print("Requested information about what cards to throw")
    print(_hand)
    return _hand[random.randint(0,4)] + ' '

# InfoFunction:

'''
* Called when a new round begins.
* @param round the round number (increased for each new round).
'''
def infoNewRound(_round):
    #_nrTimeRaised = 0
    print('Starting Round: ' + _round )

'''
* Called when the poker server informs that the game is completed.
'''
def infoGameOver():
    print('The game is over.')

'''
* Called when the server informs the players how many chips a player has.
* @param playerName    the name of a player.
* @param chips         the amount of chips the player has.
'''
def infoPlayerChips(_playerName, _chips):
    print('The player ' + _playerName + ' has ' + _chips + 'chips')

'''
* Called when the ante has changed.
* @param ante  the new value of the ante.
'''
def infoAnteChanged(_ante):
    print('The ante is: ' + _ante)

'''
* Called when a player had to do a forced bet (putting the ante in the pot).
* @param playerName    the name of the player forced to do the bet.
* @param forcedBet     the number of chips forced to bet.
'''
def infoForcedBet(_playerName, _forcedBet):
    print("Player "+ _playerName +" made a forced bet of "+ _forcedBet + " chips.")


'''
* Called when a player opens a betting round.
* @param playerName        the name of the player that opens.
* @param openBet           the amount of chips the player has put into the pot.
'''
def infoPlayerOpen(_playerName, _openBet):
    print("Player "+ _playerName + " opened, has put "+ _openBet +" chips into the pot.")

'''
* Called when a player checks.
* @param playerName        the name of the player that checks.
'''
def infoPlayerCheck(_playerName):
    print("Player "+ _playerName +" checked.")

'''
* Called when a player raises.
* @param playerName        the name of the player that raises.
* @param amountRaisedTo    the amount of chips the player raised to.
'''
def infoPlayerRise(_playerName, _amountRaisedTo):
    print("Player "+_playerName +" raised to "+ _amountRaisedTo+ " chips.")

'''
* Called when a player calls.
* @param playerName        the name of the player that calls.
'''
def infoPlayerCall(_playerName):
    print("Player "+_playerName +" called.")

'''
* Called when a player folds.
* @param playerName        the name of the player that folds.
'''
def infoPlayerFold(_playerName):
    print("Player "+ _playerName +" folded.")

'''
* Called when a player goes all-in.
* @param playerName        the name of the player that goes all-in.
* @param allInChipCount    the amount of chips the player has in the pot and goes all-in with.
'''
def infoPlayerAllIn(_playerName, _allInChipCount):
    print("Player "+_playerName +" goes all-in with a pot of "+_allInChipCount+" chips.")

'''
* Called when a player has exchanged (thrown away and drawn new) cards.
* @param playerName        the name of the player that has exchanged cards.
* @param cardCount         the number of cards exchanged.
'''
def infoPlayerDraw(_playerName, _cardCount):
    print("Player "+ _playerName + " exchanged "+ _cardCount +" cards.")

'''
* Called during the showdown when a player shows his hand.
* @param playerName        the name of the player whose hand is shown.
* @param hand              the players hand.
'''
def infoPlayerHand(_playerName, _hand):
    print("Player "+ _playerName +" hand " + str(_hand))

'''
* Called during the showdown when a players undisputed win is reported.
* @param playerName    the name of the player whose undisputed win is anounced.
* @param winAmount     the amount of chips the player won.
'''
def infoRoundUndisputedWin(_playerName, _winAmount):
    print("Player "+ _playerName +" won "+ _winAmount +" chips undisputed.")

'''
* Called during the showdown when a players win is reported. If a player does not win anything,
* this method is not called.
* @param playerName    the name of the player whose win is anounced.
* @param winAmount     the amount of chips the player won.
'''
def infoRoundResult(_playerName, _winAmount):
    print("Player "+ _playerName +" won " + _winAmount + " chips.")

Ranks = {
    '2': 1,
    '3': 2,
    '4': 3,
    '5': 4,
    '6': 5,
    '7': 6,
    '8': 7,
    '9': 8,
    'T': 9,
    'J': 10,
    'Q': 11,
    'K': 12,
    'A': 13
}

Suits = {
    'd': 1,
    'c': 2,
    'h': 3,
    's': 4
}

Types = {
    'HighCard':      1,
    'OnePair':       2,
    'TwoPairs':      3,
    '3OfAKind':      4,
    'Straight':      5,
    'Flush':         6,
    'FullHouse':     7,
    '4OfAKind':      8,
    'StraightFlush': 9
}

numberOfTypes = {
    1:              0,
    2:              13,
    3:              26,  #13 + 13
    4:              182, #26 + 156
    5:              195, #182 + 13
    6:              208, #195 + 13
    7:              209, #208 + 1
    8:              365, #209 + 156
    9:              378, #365 + 13
}

def identify_hand(Hand_):

    # Get the type of Hand
    def evaluateHand(Hand_):
        count = 0
        for card1 in Hand_:
            for card2 in Hand_:
                if (card1[0] == card2[0]) and (card1[1] != card2[1]):
                    count += 1
        return count

    # Use the "count" to analyse hand
    count_ = evaluateHand(Hand_)

    sub1 = 0
    score = [' ', ' ', ' ']

    if count_ == 12:
        for card1 in Hand_:
            for card2 in Hand_:
                if (card1[0] == card2[0]) and (card1[1] != card2[1]):
                    sub1 += 1
            if sub1 == 3:
                score = ['4OfAKind', card1[0], card1[1]]
                break

    elif count_ == 8:
        for card1 in Hand_:
            for card2 in Hand_:
                if (card1[0] == card2[0]) and (card1[1] != card2[1]):
                    sub1 += 1
            if sub1 == 1:
                sub1 = 0
            if sub1 == 2:
                score = ['FullHouse', card1[0], card1[1], card2[0], card2[1]]
                break

    elif count_ == 6:
        for card1 in Hand_:
            for card2 in Hand_:
                if (card1[0] == card2[0]) and (card1[1] != card2[1]):
                    sub1 += 1
            if sub1 == 2:
                score = ['3OfAKind', card1[0], card1[1]]
                break

    elif count_ == 4:
        needCard1 = ['', '']
        needCard2 = ['', '']
        for card1 in Hand_:
            for card2 in Hand_:
                # card1 keep the first hand card, card1 use every card to compare the card1
                if card1[0] == card2[0] and card1[1] != card2[1]:
                    if Suits[card1[1]] > Suits[card2[1]]:
                        if needCard1 == ['', '']:
                            needCard1 = card1
                    else:
                        if needCard1 == ['', '']:
                            needCard1 = card2
                if card1[0] == card2[0] and card1[1] != card2[1] \
                        and card1[0] != needCard1[0] and card2[0] != needCard1[0]:
                    if Suits[card1[1]] > Suits[card2[1]]:
                        if needCard2 == ['', '']:
                            needCard2 = card1
                    else:
                        if needCard2 == ['', '']:
                            needCard2 = card2
        if Ranks[needCard1[0]] > Ranks[needCard2[0]]:
            score = ['TwoPairs', needCard1[0], needCard2[1], needCard2[0], needCard2[1]]
        else:
            score = ['TwoPairs', needCard2[0], needCard2[1], needCard1[0], needCard2[1]]

    elif count_ == 2:
        for card1 in Hand_:
            for card2 in Hand_:
                if (card1[0] == card2[0]) and (card1[1] > card2[1]):
                    sub1 += 1
            if sub1 == 1:
                score = ['OnePair', card1[0], card1[1]]
                break

    elif count_ == 0:
        def sortHand(Hand_):
            hand_sorted_ = sorted([[card_, Ranks[card_[0]]] for card_ in Hand_], key=itemgetter(1))[:]
            return [card_[0] for card_ in hand_sorted_]

        Hand_ = sortHand(Hand_)
        score = ['HighCard', Hand_[4][0], Hand_[4][1]]

        if Hand_[0][1] == Hand_[1][1] == Hand_[2][1] == Hand_[3][1] == Hand_[4][1]:
            score = ['Flush', Hand_[4][0], Hand_[4][1]]

        if (Ranks[Hand_[4][0]] - Ranks[Hand_[3][0]] == 1 or 9) \
                and (Ranks[Hand_[3][0]] - Ranks[Hand_[2][0]] == 1) \
                and (Ranks[Hand_[2][0]] - Ranks[Hand_[1][0]] == 1) \
                and (Ranks[Hand_[1][0]] - Ranks[Hand_[0][0]] == 1):
            
            score = ['Straight', Hand_[4][0], Hand_[4][1]]
            if(Ranks[Hand_[4][0]] - Ranks[Hand_[3][0]] == 9):
                score = ['Straight', Hand_[3][0], Hand_[3][1]]
            if Hand_[0][1] == Hand_[1][1] == Hand_[2][1] == Hand_[3][1] == Hand_[4][1]:
                score = ['StraightFlush', Hand_[4][0], Hand_[4][1]]
                if(Ranks[Hand_[4][0]] - Ranks[Hand_[3][0]] == 9):
                    score = ['StraightFlush', Hand_[3][0], Hand_[3][1]]
            
            
                
    else:
        exit(5664)
    return score


def identify_score(hand):
    types = Types[hand[0]]
    card1 = 1
    card2 = 1
    if(len(hand)> 3):
        card2 = Ranks[hand[3]]
    if(types != 6):
        card1 = Ranks[hand[1]]
    score = numberOfTypes[types] + (card1 * card2)
    return score