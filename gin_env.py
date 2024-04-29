from enum import IntEnum
from random import shuffle

# Script to model a game of Straight Gin

# Load lookup table of winning hands
win_lookup = set()
with open("util/bruteforce.txt", "r") as f:
    for line in f:
        win_lookup.add(line.rstrip())


class Suit(IntEnum):
    UNDEFINED = -1,
    CLUBS = 0,
    DIAMONDS = 1,
    HEARTS = 2,
    SPADES = 3


class Rank(IntEnum):
    UNDEFINED = -1,
    ACE = 0,
    TWO = 1,
    THREE = 2,
    FOUR = 3,
    FIVE = 4,
    SIX = 5,
    SEVEN = 6,
    EIGHT = 7,
    NINE = 8,
    TEN = 9,
    JACK = 10,
    QUEEN = 11,
    KING = 12


class Card:
    __slots__ = ["__card_id", "__charcode", "__rank", "__suit"]
    alphabet = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ-"  # '-' is for undefined card

    def __init__(self, card_id):
        assert type(card_id) is int, "card_id must be int"
        self.__card_id = card_id  # card_id is a composite value of Suit and Rank using the formula 4 * Rank + Suit

        if card_id == -1:
            self.__rank, self.__suit = Rank.UNDEFINED, Suit.UNDEFINED
        else:
            quotient, remainder = divmod(self.__card_id, 4)
            self.__rank, self.__suit = Rank(quotient), Suit(remainder)

    @classmethod
    def from_rank_and_suit(cls, rank, suit):
        assert Rank.__contains__(rank), "rank must be enum Rank (or int in range of Rank)"
        assert Suit.__contains__(suit), "suit must be enum Suit (or int in range of Suit)"

        card = super().__new__(cls)
        card.__card_id = rank * 4 + suit
        card.__rank = Rank(rank)
        card.__suit = Suit(suit)

        return card

    @property
    def card_id(self):
        return self.__card_id

    # Get charcode representation of Card for writing out win lookup table
    @property
    def charcode(self):
        return self.alphabet[self.__card_id]

    # Instantiate Card from charcode representation for reading in win lookup table
    @classmethod
    def from_charcode(cls, charcode):
        return cls(cls.alphabet.index(charcode))

    @property
    def rank(self):
        return self.__rank

    @property
    def suit(self):
        return self.__suit

    def __str__(self):
        return "{} OF {}".format(self.__rank.name, self.__suit.name)

    def __add__(self, other):
        assert type(other) is int, "Can only modify card values using ints"
        return Card(self.__card_id + other)

    def __radd__(self, other):
        return self.__add__(other)

    def __iadd__(self, other):
        raise AttributeError("May not modify card in place")

    def __sub__(self, other):
        assert type(other) is int, "Can only modify card values using ints"
        return Card(self.__card_id - other)

    def __rsub__(self, other):
        return self.__sub__(other)

    def __isub__(self, other):
        raise AttributeError("May not modify card in place")

    def __eq__(self, other):
        assert isinstance(other, Card), "Can only compare Card to another Card"
        return self.__card_id == other.__card_id

    def __lt__(self, other):
        assert isinstance(other, Card), "Can only compare Card to another Card"
        return self.__card_id < other.__card_id

    def __le__(self, other):
        assert isinstance(other, Card), "Can only compare Card to another Card"
        return self.__card_id <= other.__card_id

    def __gt__(self, other):
        assert isinstance(other, Card), "Can only compare Card to another Card"
        return self.__card_id > other.__card_id

    def __ge__(self, other):
        assert isinstance(other, Card), "Can only compare Card to another Card"
        return self.__card_id >= other.__card_id


class Deck:
    __slots__ = ["__draw_pile", "__discard_pile"]

    def __init__(self):
        # Instantiate Deck by generating all cards in deck, shuffling the deck, and then placing the first card in the discard pile
        self.__draw_pile = [Card(x) for x in range(52)]
        shuffle(self.__draw_pile)
        self.__discard_pile = [self.__draw_pile.pop()]

    # Face-down part of the deck
    @property
    def draw_pile(self):
        return tuple(self.__draw_pile)

    # Face-up part of the deck
    @property
    def discard_pile(self):
        return tuple(self.__discard_pile)

    # Get card from the top of the discard pile
    @property
    def discard_pile_top(self):
        try:
            return self.__discard_pile[-1]
        except IndexError:
            return Card(-1)

    def __str__(self):
        s = ""

        s += "Cards in deck:\n"
        for card in self.__draw_pile:
            s += card.__str__() + "\n"

        s += "\nCards in discard:\n"
        for card in self.__discard_pile:
            s += card.__str__() + "\n"

        return s

    def deal(self, hand_count):
        while True:
            # create list of lists for cards of each hand
            hands = [[] for _ in range(hand_count)]

            # deal cards to the hands
            for _ in range(7):
                for hand in hands:
                    hand.append(self.__draw_pile.pop())

            # sort the cards in each hand
            for hand in hands:
                hand.sort()

            # convert lists into hands
            hands = [Hand(self, hand) for hand in hands]

            # regenerate if a winning hand was dealt
            for hand in hands:
                if hand.check():
                    continue

            return hands

    def draw_from_draw_pile(self):
        return self.__draw_pile.pop()

    def draw_from_discard_pile(self):
        return self.__discard_pile.pop()

    def add_to_discard_pile(self, card):
        self.__discard_pile.append(card)

        if len(self.__draw_pile) == 0:
            self.__draw_pile = self.__discard_pile
            shuffle(self.__draw_pile)
            self.__discard_pile = [self.__draw_pile.pop()]


class Hand:
    __slots__ = ["__deck", "__cards"]

    def __init__(self, deck, cards):
        self.__deck = deck
        self.__cards = cards

    # Encode entire Hand as charcode string to check if it is in the win lookup table
    @property
    def charcode(self):
        return "".join(card.charcode for card in self.__cards)

    def __str__(self):
        s = "Cards on hand:\n"

        for card in self.__cards:
            s += str(card) + "\n"

        return s

    def __len__(self):
        return len(self.__cards)

    def __getitem__(self, key):
        return self.__cards[key]

    def __iter__(self):
        return iter(self.__cards)

    def draw_from_draw_pile(self):
        self.__cards.append(self.__deck.draw_from_draw_pile())
        self.__cards.sort()

    def draw_from_discard_pile(self):
        self.__cards.append(self.__deck.draw_from_discard_pile())
        self.__cards.sort()

    def check(self):
        return self.charcode in win_lookup

    def discard(self, key):
        self.__deck.add_to_discard_pile(self.__cards.pop(key))

    def reward(self):
        return -1


# Example usage
if __name__ == '__main__':
    # Instantiate new deck
    deck = Deck()

    # Deal two hands from the deck
    hands = deck.deal(2)

    for hand in hands:
        print(hand)

    # Show top of the discard pile
    print(deck.discard_pile_top)

    # Draw a card from the discard pile into the 1st players hand
    hands[0].draw_from_discard_pile()

    # Check if the 1st player holds a winning hand
    print(hands[0].check())

    # Show the 1st players hand after drawing the card, and then discard he 6th card
    print(hands[0])
    hands[0].discard(5)