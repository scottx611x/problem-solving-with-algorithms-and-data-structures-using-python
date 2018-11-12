import os
import sys

from io import StringIO
from contextlib import contextmanager
from unittest import TestCase, mock

from section1.cards import Deck, Card, HiLo


class CardTest(TestCase):
    def test_init(self):
        card = Card("♥", 2)
        self.assertEqual(card.suit, "♥")
        self.assertEqual(card.rank, 2)

    def test_card_comparison(self):
        lo_card = Card("♥", 2)
        hi_card = Card("♠", "A")

        self.assertGreater(hi_card, lo_card)
        self.assertLess(lo_card, hi_card)
        self.assertEqual(lo_card, Card("♠", 2))


class DeckTest(TestCase):
    def test_deck_length(self):
        deck = Deck()
        self.assertTrue(all(isinstance(c, Card) for c in deck.cards))
        self.assertEqual(len(deck.cards), 52)

    def test_get_cards_by_suit(self):
        deck = Deck()
        for suit in Deck.SUITS:
            self.assertEqual(len(deck.get_cards_by_suit(suit)), 13)

    def test_shuffle(self):
        deck = Deck()
        initial_cards = deck.cards
        deck.shuffle()
        shuffled_cards = deck.cards
        self.assertNotEqual(initial_cards, shuffled_cards)

    def test_deal(self):
        deck = Deck()
        dealt_cards = deck.deal(5)
        self.assertEqual(len(dealt_cards), 5)
        self.assertEqual(len(deck.cards), 47)


class HiLoTest(TestCase):
    def setUp(self):
        with mock.patch.object(HiLo, "play") as play_mock:
            with mock.patch.object(Deck, "shuffle"):
                self.hi_lo = HiLo()
        self.assertTrue(play_mock.called)

    def test_init(self):
        self.assertTrue(isinstance(self.hi_lo.deck, Deck))
        self.assertEqual(len(self.hi_lo.grid), 9)
        self.assertTrue(
            all(isinstance(c, Card) for c in self.hi_lo.grid)
        )
        self.assertIsNone(self.hi_lo.message)

    def test_clear_screen(self):
        with mock.patch.object(os, "system") as os_system_mock:
            self.hi_lo._clear_screen()
        os_system_mock.assert_called_with("clear")

    @mock.patch.object(HiLo, "play")
    def test__check_valid_rank(self, play_mock):
        for rank in Deck.RANKS:
            self.assertIsNone(self.hi_lo._check_valid_rank(rank))

    def test_get_cards_in_grid(self):
        with mock.patch.object(Deck, "shuffle"):
            self.assertEqual(
                self.hi_lo._get_cards_in_grid(),
                Deck().cards[:9]
            )

    def test_get_cards_in_grid_with_x(self):
        self.hi_lo.grid[0] = HiLo.bad_stack_char
        with mock.patch.object(Deck, "shuffle"):
            self.assertEqual(
                self.hi_lo._get_cards_in_grid(),
                Deck().cards[1:9]
            )
            self.hi_lo.grid[-1] = HiLo.bad_stack_char
            self.assertEqual(
                self.hi_lo._get_cards_in_grid(),
                Deck().cards[1:8]
            )

    def test_get_dead_piles_on_grid(self):
        self.hi_lo.grid[0] = HiLo.bad_stack_char
        self.assertEqual(len(self.hi_lo._get_dead_piles_in_grid()), 1)

    @mock.patch.object(HiLo, "_clear_screen")
    def test_display_grid(self, clear_screen_mock):
        with captured_output() as output:
            self.hi_lo.refresh_grid()

        self.assertTrue(clear_screen_mock.called)
        self.assertMultiLineEqual(
            output.getvalue(),
            '''2♠  2♥  2♦ 

2♣  3♠  3♥ 

3♦  3♣  4♠ 

-----------------

43 left. 

'''
        )

    def test_display_messages_no_message(self):
        with captured_output() as output:
            self.hi_lo._display_messages()
        self.assertMultiLineEqual(output.getvalue(),
                                  '-----------------\n\n43 left. \n\n')

    def test_display_messages_with_message(self):
        message = "You Lost!"
        self.hi_lo.message = message
        with captured_output() as output:
            self.hi_lo._display_messages()
        self.assertIn(message, output.getvalue())

    def test__get_next_card(self):
        next_card = self.hi_lo.deck.cards[0]
        self.assertEqual(self.hi_lo._get_next_card(), next_card)

    def test_get_user_input(self):
        with mock.patch("builtins.input", return_value="hi 2") as input_mock:
            self.hi_lo.get_user_input()
        self.assertTrue(input_mock.called)

    @mock.patch.object(HiLo, "play")
    def test_get_user_input_invalid_hi_lo(self, play_mock):
        with mock.patch("builtins.input", return_value="high 2"):
            self.hi_lo.get_user_input()
        self.assertEqual(self.hi_lo.message,
                         "hi_lo must be: ['hi', 'lo'] not high")
        self.assertTrue(play_mock.called)

    @mock.patch.object(HiLo, "play")
    def test_get_user_input_invalid_rank(self, play_mock):
        with mock.patch("builtins.input", return_value="hi 12"):
            self.hi_lo.get_user_input()
        self.assertEqual(
            self.hi_lo.message,
            "12 is not a valid rank. Must be in: "
            "['2', '3', '4', '5', '6', '7', '8', '9', "
            "'10', 'J', 'Q', 'K', 'A']"
        )
        self.assertTrue(play_mock.called)

    @mock.patch.object(HiLo, "play")
    def test_get_user_input_invalid_input(self, play_mock):
        with mock.patch("builtins.input", return_value="ergerger"):
            self.hi_lo.get_user_input()
        self.assertEqual(
            self.hi_lo.message,
            "'ergerger' is invalid input, try again..."
        )
        self.assertTrue(play_mock.called)

    def test_get_user_input_bad_card_choice_too_low(self):
        self.hi_lo.grid[1:] = [
            HiLo.bad_stack_char for i in self.hi_lo.grid[1:]
        ]
        with mock.patch("builtins.input", return_value="lo 2"):
            with captured_output() as output:
                self.hi_lo.play()
        self.assertIn("4♥ >= 2", output.getvalue())

    def test_get_user_input_bad_card_choice_too_high(self):
        self.hi_lo.grid[:-1] = [
            HiLo.bad_stack_char for i in self.hi_lo.grid[:-1]
        ]
        with mock.patch("builtins.input", return_value="hi 4"):
            with captured_output() as output:
                self.hi_lo.play()
        print(output.getvalue())
        self.assertIn("4♥ <= 4♠", output.getvalue())

    def test__check_win_lose_loser(self):
        self.hi_lo.grid = [HiLo.bad_stack_char for c in self.hi_lo.grid]
        with captured_output() as output:
            self.hi_lo._continue_playing()
        self.assertIn("You lost HiLo with 43 cards remaining.",
                      output.getvalue())

    def test__check_win_lose_winner(self):
        self.hi_lo.deck.cards = []
        self.hi_lo.grid[0] = HiLo.bad_stack_char
        with captured_output() as output:
            self.hi_lo._continue_playing()
        self.assertIn(
            "You won HiLo with 1 dead pile(s) on the board! Congrats!",
            output.getvalue()
        )

    def test_simulate_win(self):
        with mock.patch(
            "builtins.input",
            side_effect=[
                f"hi {card.rank}" for card in [
                    card for card in self.hi_lo.grid + self.hi_lo.deck.cards
                ]
            ]
        ):
            with captured_output() as output:
                self.hi_lo.play()
        self.assertIn(
            "You won HiLo with 0 dead pile(s) on the board! Congrats!",
            output.getvalue()
        )

@contextmanager
def captured_output():
    new_out = StringIO()
    old_out = sys.stdout
    try:
        sys.stdout = new_out
        yield sys.stdout
    finally:
        sys.stdout = old_out