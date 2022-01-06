'''
This is a Blackjack game!

'''
import random

suits=('Hearts','Diamonds','Spades','Clubs')
ranks=('Two','Three','Four','Five','Six','Seven','Eight','Nine','Ten','Jack','Queen','King','Ace')
values={'Two':2, 'Three':3, 'Four':4, 'Five':5, 'Six':6, 'Seven':7, 'Eight':8, 'Nine':9, 'Ten':10,
         'Jack':10, 'Queen':10, 'King':10, 'Ace':11}


class Card():

    '''
    Card class contatining info about suit and rank

    '''
    def __init__(self,suit,rank):
        self.suit=suit
        self.rank=rank
        self.value=values[rank]
    
    def __str__(self):
        return self.rank + ' of ' + self.suit



class Deck():

    '''
    Deck class contatining all cards to be split between players after shuffling

    '''

    def __init__(self):
        self.all_cards=[]

        for suit in suits:
            for rank in ranks:
                #create card object
                created_card=Card(suit,rank)
                self.all_cards.append(created_card)

    def shuffle(self):
        random.shuffle(self.all_cards)

    def get_one(self):
        return self.all_cards.pop()

class Player():

    '''
    Player class containing info about players cards

    '''

    def __init__(self, name):
        self.name=name
        self.all_cards=[]

    def remove_one(self):
        return self.all_cards.pop(0)

    def add_cards(self,new_cards):
        if isinstance(new_cards,list):
            self.all_cards.extend(new_cards)
        else:
            self.all_cards.append(new_cards)

    def __str__(self):
        return f'Player {self.name} has {len(self.all_cards)} cards'


class Hand():

    '''
    hand class containing info about players cards in hand

    '''

    def __init__(self):
        self.aces=0
        self.value=0
        self.cards=[]
        for card in self.cards:
            self.value+=card.value

    def add_cards(self,card):
        self.cards.append(card)
        if card.rank=='Ace':
            self.aces+=1
        self.value+=card.value
            

    def adjust_for_ace(self):
        print('Waga twoich kart to: {}'.format(self.value))
        if self.aces>0:
            mala=self.value-10
            print('Waga twoich kart przy malym asie to: {}'.format(mala))
            zmienna=input('jaka chcesz wage asa: ')
            if zmienna=='d':
                pass
            else:
                self.value=mala
            self.aces-=1

    def __str__(self):
        return f'has {len(self.cards)} cards'


class Money():

    def __init__(self,account,name):
        self.name=name
        self.account=account
        self.bet=0
        self.lost=0
    def bet_money(self):
        self.bet=int(input('Ile chcesz wrzucic: '))
        self.account=self.account-self.bet
        print('Gracz obstawia: {}$'.format(self.bet))
    
    def give_back(self):
        oddaj=0
        self.lost+=self.bet
        oddaj=self.bet
        self.bet=0
        return oddaj
    
    def add_money(self,money):
        self.account=self.account+self.bet+money
        self.bet=0

    def __str__(self):
        return f'{self.name} has {self.account} $'


def hit_or_no(deck,hand):
    global player_in_action
    hit=input('czy chcesz pobrac karte?')
    if hit.lower()=='y':
        hand.add_cards(deck.get_one())
        print('Dodano {}'.format(hand.cards[-1]))
        for i in range(len(hand.cards)):
            print('player now has: {}'.format(hand.cards[i]))
        hand.adjust_for_ace()
    if hit.lower()=='n':
        player_in_action=False

def who_wins(dealer,player,player_bet,dealer_bet):
    
    #player win
    if dealer.value<player.value:
        print('player wins!')
        player_bet.add_money(dealer_bet.give_back())

    #dealer win
    if dealer.value>player.value:
        print('dealer wins!')
        dealer_bet.add_money(player_bet.give_back())




def player_busts(player_bet,dealer_bet):
    print('player busts!')
    dealer_bet.add_money(player_bet.give_back())
    return True

def dealer_busts(player_bet,dealer_bet):
    print('dealer busts!')
    player_bet.add_money(dealer_bet.give_back())
    return True


def play_again():
    global GAME_ON
    play=input('Would you like to play next? ')
    if play.lower()=='y':
        pass
    else:
        GAME_ON=False

def show_cards(pl_cards,dl_cards):
    print('player cards are: ',*pl_cards.cards,sep='\n')
    print('\n')
    print('dealer cards are: ',*dl_cards.cards,sep='\n')

       


#GAME SETUP

player_one=Player('Dealer')
player_two=Player('Mateusz')

new_deck=Deck()
new_deck.shuffle()
dealer_cards=Hand()
player_cards=Hand()
player_bet_money=Money(500,'player')
dealer_bet_money=Money(500,'dealer')

GAME_ON=True

#SPLIT 2 CARDS FOR EACH AND PRINT 2 PLAYER AND 1 DEALER
while GAME_ON:
    player_in_action=True
    player_cards.cards=[]
    dealer_cards.cards=[]
    player_cards.value=0
    dealer_cards.value=0
    player_cards.aces=0
    dealer_cards.aces=0

    player_lost=False
    dealer_lost=False
    for i in range(2):
        dealer_cards.add_cards(new_deck.get_one())
        player_cards.add_cards(new_deck.get_one())
        print('Player has: {}'.format(player_cards.cards[i]))
    print('Dealer has: {}'.format(dealer_cards.cards[0]))

    player_cards.adjust_for_ace()

    #HOW MUCH YOU WANNA BET?
    print(f'You account: {player_bet_money.account}')

    #make a bet
    player_bet_money.bet_money()
    dealer_bet_money.bet=player_bet_money.bet
    dealer_bet_money.account=dealer_bet_money.account-dealer_bet_money.bet

    #hit czy nie hit?
    while player_in_action:
        hit_or_no(new_deck,player_cards)
        if player_cards.value>21:
            player_lost=player_busts(player_bet_money,dealer_bet_money)
            break

#tu logika dla dealera

    while dealer_cards.value<17 and player_lost==False:
        dealer_cards.add_cards(new_deck.get_one())

    if dealer_cards.value>21 and player_lost==False:
            dealer_lost=dealer_busts(player_bet_money,dealer_bet_money)


    if player_lost!=True and dealer_lost!=True:
        who_wins(dealer_cards,player_cards,player_bet_money,dealer_bet_money)
    show_cards(player_cards,dealer_cards)
    print(player_bet_money)
    print(dealer_bet_money)

    play_again()







