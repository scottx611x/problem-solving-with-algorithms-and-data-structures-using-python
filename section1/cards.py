import os
import random


class Card:
    def __init__(self, suit, rank):
        self.rank_map = {
            "J": 11,
            "Q": 12,
            "K": 13,
            "A": 14
        }
        self.suit = suit
        self.rank = rank

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return f"{self.rank}{self.suit}"

    def __eq__(self, card):
        my_rank, their_rank = self.get_ranks(card)
        return my_rank == their_rank

    def __gt__(self, card):
        my_rank, their_rank = self.get_ranks(card)
        return my_rank > their_rank

    def __lt__(self, card):
        my_rank, their_rank = self.get_ranks(card)
        return my_rank < their_rank

    def get_ranks(self, card):
        if self.rank in self.rank_map:
            my_rank = self.rank_map[self.rank]
        else:
            my_rank = int(self.rank)

        if card.rank in self.rank_map.keys():
            their_rank = self.rank_map[card.rank]
        else:
            their_rank = int(card.rank)
        return my_rank, their_rank


class Deck:
    SUITS = ["♠", "♥", "♦", "♣"]
    RANKS = [str(n) for n in range(2, 10 + 1)] + ["J", "Q", "K", "A"]

    def __init__(self):
        self.cards = [
            Card(suit, rank)
            for rank in self.RANKS for suit in self.SUITS
        ]
        self.shuffle()

    def get_cards_by_suit(self, suit):
        return [c for c in self.cards if c.suit == suit]

    def shuffle(self):
        self.cards = sorted(self.cards, key=lambda k: random.random())

    def deal(self, number_of_cards):
        cards = self.cards
        self.cards = cards[number_of_cards:]
        return cards[:number_of_cards]


class HiLo:
    accepted_values = ["hi", "lo"]
    bad_stack_char = "X"

    def __init__(self, message=None):
        self.deck = Deck()
        self.grid = self.deck.deal(9)
        self.message = message
        self.should_play = True
        self.play()

    def _check_valid_rank(self, user_rank):
        available_ranks = [c.rank for c in self._get_cards_in_grid()]

        if user_rank not in available_ranks:
            self.message = \
                f"There are no {user_rank}'s on the grid: {self.grid}"
            if user_rank not in Deck.RANKS:
                self.message = f"{user_rank} is not a valid rank. " \
                    f"Must be in: {Deck.RANKS}"
            self.play()

    def _continue_playing(self):
        continue_playing = True
        if all(str(c) == self.bad_stack_char for c in self.grid):
            self.message = \
                f"You lost HiLo with {len(self.deck.cards)} cards remaining."
            continue_playing = False

        if not self.deck.cards:
            self.message = \
                f"You won HiLo with {len(self._get_dead_piles_in_grid())} "\
                f"dead pile(s) on the board! Congrats!"
            continue_playing = False

        if not continue_playing:
            self.refresh_grid()
        return continue_playing

    def _clear_screen(self):
        os.system('clear')

    def refresh_grid(self):
        self._clear_screen()

        grid = [str(c) for c in self.grid]

        while grid:
            print("  ".join(grid[:3]), "\n")
            grid = grid[3:]

        self._display_messages()

    def _display_messages(self):
        print("-----------------\n")
        print(f"{len(self.deck.cards)} left. \n")
        if self.message is not None:
            print(f"{self.message}\n")
            self.message = None

    def _get_cards_in_grid(self):
        return [card for card in self.grid if isinstance(card, Card)]

    def _get_dead_piles_in_grid(self):
        return [pile for pile in self.grid if not isinstance(pile, Card)]

    def _get_next_card(self):
        return self.deck.deal(1)[0]

    def get_user_input(self):
        user_input = input("Input a hi/lo choice followed by a rank >>> ")
        return self._validate_input(user_input)

    def play(self):
        while True:
            self.refresh_grid()
            user_hilo, user_rank = self.get_user_input()
            new_card = self._get_next_card()

            for index, card in enumerate(self.grid):
                if isinstance(card, Card) and card.rank == user_rank:
                    error = None
                    if user_hilo == "hi":
                        if not new_card > card:
                            error = "<="
                    else:
                        if not new_card < card:
                            error = ">="
                    if error is not None:
                        self.grid[index] = self.bad_stack_char
                        self.message = f" {new_card} {error} {card}."
                        self.refresh_grid()
                        if not self._continue_playing():
                            break
                    else:
                        self.grid[index] = new_card
                    break

            if not self._continue_playing():
                break

    def _validate_input(self, user_input):
        try:
            hilo, rank = user_input.split()
        except Exception:
            self.message = f"'{user_input}' is invalid input, try again..."
            self.play()
        else:
            hilo = hilo.lower()
            self._check_valid_rank(rank)
            if hilo not in self.accepted_values:
                self.message = \
                    f"hi_lo must be: {self.accepted_values} not {hilo}"
                self.play()
            return hilo, rank

# HiLo()