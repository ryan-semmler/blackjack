import random
import os


values = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']


class Deck:

    def __init__(self, card_list):
        self.card_list = card_list

    def __repr__(self):
        return str(self.card_list)

    def shuffle_deck(self):
        random.shuffle(self.card_list)


class Player:

    def __init__(self, money):
        self.hand_total = 0
        self.hand_cards = []
        self.money = money

    def update_hand_total(self):
        card_value_list = []
        for card in self.hand_cards:
            if card == 'A':
                card_value_list.append(11)
            elif card in 'JQK':
                card_value_list.append(10)
            else:
                card_value_list.append(int(card))
        self.hand_total = sum(card_value_list)
        ace_count = 0
        while self.hand_total > 21:
            if self.hand_cards.count('A') > ace_count:
                self.hand_total -= 10
                ace_count += 1
            else:
                break


class Dealer(Player):

    def __init__(self, money):
        self.hand_total = 0
        self.hand_cards = []
        self.visible_total = 0
        self.visible_cards = []
        self.money = False

    def update_visible_total(self):
        card_value_list = []
        for card in self.visible_cards:
            if card == 'A':
                card_value_list.append(11)
            elif card in 'JQK':
                card_value_list.append(10)
            else:
                card_value_list.append(int(card))
        self.visible_total = sum(card_value_list)


def create_deck():
    deck_list = []
    for i in range(4):
        for value in values:
            deck_list.append(value)
    return deck_list


def deal(deck, player, dealer):
    player.hand_cards.append(deck.card_list[0])
    dealer.hand_cards.append(deck.card_list[1])
    player.hand_cards.append(deck.card_list[2])
    dealer.hand_cards.append(deck.card_list[3])


def show_table_in_game(player, dealer):
    print("Dealer's hand: ", dealer.visible_cards)
    print(dealer.visible_total, "showing.\n")
    print("Player's hand: ", player.hand_cards)
    print(player.hand_total, "total.")


def show_table_end_game(player, dealer):
    print("Dealer's hand: ", dealer.hand_cards)
    print(dealer.hand_total, "total.\n")
    print("Player's hand: ", player.hand_cards)
    print(player.hand_total, "total.")


def player_turn(deck, player, dealer, top_card_index):
    player_choice = 'h'
    while player_choice == 'h' and player.hand_total <= 21:
        if player.hand_total == 21:
            input("You got 21!")
            break
        show_table_in_game(player, dealer)
        player_choice = input("Hit or stand? ")[0].lower()
        if player_choice == 'h':
            os.system('clear')
            player.hand_cards.append(deck.card_list[top_card_index])
            player.update_hand_total()
            if player.hand_total == 21:
                input("You got 21!")
            top_card_index += 1


def dealer_turn(deck, dealer, top_card_index):
    while dealer.hand_total < 17:
        dealer.hand_cards.append(deck.card_list[top_card_index])
        top_card_index += 1
        dealer.update_hand_total()
        print("Dealer's hand:", dealer.hand_cards)
        print('Total:', dealer.hand_total)
        input()
        os.system('clear')


def get_bet(player):
    while True:
        try:
            bet = int(input("What would you like to bet on this hand? "))
            if bet >= 0 and bet <= player.money:
                return bet
        except ValueError:
            print("That's not a valid bet.")


def game(deck, player, dealer):
    deck.shuffle_deck()
    deal(deck, player, dealer)
    dealer.update_hand_total()
    dealer.visible_cards = dealer.hand_cards[1:]
    dealer.update_visible_total()
    player.update_hand_total()
    if player.hand_total == 21:
        print("Blackjack!")
        return True
    top_card_index = 4
    player_turn(deck, player, dealer, top_card_index)
    if player.hand_total > 21:
        print("Player busts.")
        return False
    dealer_turn(deck, dealer, top_card_index)
    if dealer.hand_total > 21:
        print("Dealer busts.")
        return True
    if player.hand_total > dealer.hand_total:
        return True
    return False


def main():
    player = Player(100)
    play_again = True
    while play_again:
        dealer = Dealer(0)
        player.hand_total = 0
        player.hand_cards = []
        deck = Deck(create_deck())
        deck.shuffle_deck()
        os.system('clear')
        print("You have ${} left.".format(player.money))
        bet = get_bet(player)
        if game(deck, player, dealer):
            print("Player wins!")
            player.money += bet
        else:
            print("Dealer wins.")
            player.money -= bet
        show_table_end_game(player, dealer)
        again = input("Play again? ")
        if again == '':
            play_again = False
        elif again[0].lower() != 'y':
            play_again = False


if __name__ == '__main__':
    main()
