# -*- coding: utf-8 -*-
"""
Blackjack Game

@author: Doc
"""

import random


suits = ('Clubs', 'Diamonds', 'Hearts', 'Spades')
ranks = (
        '2', '3', '4', '5', '6', '7', '8', '9', '10',
        'Jack', 'Queen', 'King', 'Ace'
        )
values = {
        '2': 2, '3': 3, '4': 4, '5': 5,
        '6': 6, '7': 7, '8': 8, '9': 9, '10': 10,
        'Jack': 10, 'Queen': 10, 'King': 10, 'Ace': 11
        }
playing = True


class Card:
    # create instance of Card
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    # return card rank and suit ex: 3 of Clubs
    def __str__(self):
        return self.rank + " of " + self.suit


class Deck:
    # create instance of Deck
    def __init__(self):
        self.deck = []  # start with empty list
        for suit in suits:
            for rank in ranks:
                # build Card objects and add to the list
                self.deck.append(Card(suit, rank))

    def __str__(self):
        deck_contents = ''
        # start with empty string
        for card in self.deck:
            deck_contents += '\n ' + card.__str__()
            # add ea Card object's print string
        return 'The deck has: ' + deck_contents

    # shuffle deck contents
    def shuffle(self):
        random.shuffle(self.deck)

    # method for card drawing
    def drawCard(self):
        individual_card = self.deck.pop()
        return individual_card


class Hand:
    def __init__(self):
        self.cards = []  # start w/ empty list
        self.value = 0  # start with 0
        self.aces = 0  # attribute to track aces

    def add_card(self, card):
        self.cards.append(card)
        self.value += values[card.rank]
        if card.rank == 'Ace':
            self.aces += 1  # count another ace

    def ace_adjuster(self):
        while self.value > 21 and self.aces:
            self.value -= 10
            self.aces -= 1


class Money:
    def __init__(self, initial_money):
        self.initial_money = initial_money
        self.total = 0
        self.bet = 0
        self.total += self.initial_money

    def win_bet(self):
        self.total += self.bet

    def lose_bet(self):
        self.total -= self.bet


def bettingMethod(money):

    while True:
        try:
            print("You have $", money.total)
            money.bet = int(input("\nHow much would you like to bet? \n"))
        except ValueError:
            print('Invalid bet entered. Please try again.\n')
            continue
        else:
            if money.bet > money.total or money.bet <= 0:
                print(
                        "\nPlease enter a valid amount to bet. "
                        "Do not exceed $",
                        money.total, " or enter a value below $1.\n"
                        )
            else:
                break


def take_the_hit(deck, hand):

    hand.add_card(deck.drawCard())
    hand.ace_adjuster()


def hit_it_or_quit_it(deck, hand):

    global playing  # control upcoming while loop

    go_hit = 'hit'
    go_stay = 'stay'

    while True:

        x = input(
                "Want to hit or stay where you're at? "
                "Type 'hit' or 'stay': \n"
                )

        if x.lower() == go_hit:
            take_the_hit(deck, hand)  # execute hit func

        elif x.lower() == go_stay:
            print("You stay where you're at. Dealer's turn.\n")
            playing = False

        else:
            print("Please make a valid choice.\n")
            continue
        break


# Show hand functions
def show_some(player, dealer):
    print("\nDealer's Hand: ")
    print("<face down card>")
    print('', dealer.cards[1])
    print("\nPlayer's Hand: ", *player.cards, sep='\n ')


def show_all(player, dealer):
    print("\nDealer's Hand: ", *dealer.cards, sep='\n ')
    print("\nDealer's Hand = ", dealer.value)
    print("\nPlayer's Hand: ", *player.cards, sep='\n ')
    print("\nPlayer's Hand = ", player.value)


# End game scenario functions
def player_bust(player, dealer, money):
    print("\nYou bust.")
    money.lose_bet()


def player_win(player, dealer, money):
    print("\nYou won!")
    money.win_bet()


def dealer_bust(player, dealer, money):
    print("\nThe dealer bust!")
    money.win_bet()


def dealer_win(player, dealer, money):
    print("\nThe dealer won.")
    money.lose_bet()


def tie(player, dealer):
    print("\nLooks like you've tied.")
    print("\nOh well, shit happens.")


def main():

    global playing
    x = str()
    validYes = ["Yes", "yes", "Y", "y"]
    validNo = ["No", "no", "N", "n"]

    while True:
        try:
            x = str(input("Want to play blackjack?\n"))
        except ValueError:
            print("Incorrect input. Try again.\n")
            continue
        if x in validYes or x in validNo:
            break
        else:
            print("Incorrect input. Try again.\n")
            continue

    if x in validYes:

        while True:
            # set up Player's money
            try:
                player_money = Money(
                        int(input('How much $ would you like to start with? '
                                  'Enter an integer between 1 and 250. '))
                        )
            except ValueError:
                print('\nPlease enter an integer.')
            else:
                if player_money.initial_money < 1 or player_money.initial_money > 250:
                    print("\nSorry, you can't start with that amount.")
                else:
                    break

        while True:

            # initialize deck and shuffle it
            deck = Deck()
            deck.shuffle()
            print("\nTime to deal.\n")

            # set up player and dealer hands
            player_hand = Hand()
            player_hand.add_card(deck.drawCard())
            player_hand.add_card(deck.drawCard())

            dealer_hand = Hand()
            dealer_hand.add_card(deck.drawCard())
            dealer_hand.add_card(deck.drawCard())

            # get Player's bet
            bettingMethod(player_money)

            # Show player cards and face up dealer cards
            show_some(player_hand, dealer_hand)

            while playing:  # global variable loop

                # prompt to hit or stay
                hit_it_or_quit_it(deck, player_hand)

                # show cards and face up dealer cards
                show_some(player_hand, dealer_hand)

                # If player hand goes over 21 run bust function and break loop
                if player_hand.value > 21:
                    player_bust(player_hand, dealer_hand, player_money)
                    break

            if player_hand.value <= 21:

                while dealer_hand.value < 17:
                    take_the_hit(deck, dealer_hand)

                # show all cards
                show_all(player_hand, dealer_hand)

                # run winning scenarios
                if dealer_hand.value > 21:
                    dealer_bust(player_hand, dealer_hand, player_money)

                elif dealer_hand.value > player_hand.value:
                    dealer_win(player_hand, dealer_hand, player_money)

                elif dealer_hand.value < player_hand.value:
                    player_win(player_hand, dealer_hand, player_money)

                else:
                    tie(player_hand, dealer_hand)

            # winnings
            print("\nYou walk away with $", player_money.total)

            # Play again?
            new_game = input("Want to play another hand? ")

            if new_game[0].lower() == 'y':
                if player_money.total <= 0:
                    print("You've run out of money.")
                    while True:
                        # set up Player's money
                        try:
                            player_money = Money(
                                    int(input('How much $ would you like to start with? '
                                              'Enter an integer between 1 and 250. '))
                                    )
                        except ValueError:
                            print('\nPlease enter an integer.')
                        else:
                            if player_money.initial_money < 1 or player_money.initial_money > 250:
                                print("\nSorry, you can't start with that amount.")
                            else:
                                break
                playing = True
                continue
            else:
                print("See ya.")
                break

    elif x in validNo:
        quit

if __name__ == "__main__":
    main()
else:
    main()

