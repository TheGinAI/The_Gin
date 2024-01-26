from enum import IntEnum
from operator import attrgetter
from random import shuffle


class Suit(IntEnum):
    CLUBS = 0,
    DIAMONDS = 1,
    HEARTS = 2,
    SPADES = 3


class Rank(IntEnum):
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
    __slots__ = ["__card_id", "__rank", "__suit"]

    def __init__(self, card_id):
        assert type(card_id) is int, "card_id must be int"
        self.__card_id = card_id

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
        self.__draw_pile = [Card(x) for x in range(52)]
        shuffle(self.__draw_pile)
        self.__discard_pile = [self.__draw_pile.pop()]

    @property
    def draw_pile(self):
        return tuple(self.__draw_pile)

    @property
    def discard_pile(self):
        return tuple(self.__discard_pile)

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
    def __init__(self, deck, cards):
        self.__deck = deck
        self.__cards = cards

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

    def draw(self, down_or_up):
        if down_or_up:  # True -> draw from face-up discard pile
            self.__cards.append(self.__deck.draw_from_discard_pile())
        else:           # False -> draw from face-down draw pile
            self.__cards.append(self.__deck.draw_from_draw_pile())

        self.__cards.sort()

    def check(self):
        # check sets
        set_1_4 = self.__cards[0].rank == self.__cards[1].rank == self.__cards[2].rank == self.__cards[3].rank
        set_1_3 = set_1_4 or (self.__cards[0].rank == self.__cards[1].rank == self.__cards[2].rank)

        set_4_7 = self.__cards[3].rank == self.__cards[4].rank == self.__cards[5].rank == self.__cards[6].rank
        set_5_7 = set_4_7 or (self.__cards[4].rank == self.__cards[5].rank == self.__cards[6].rank)

        if (set_1_3 and set_4_7) or (set_1_4 and set_5_7):
            return True

        # check runs
        self.__cards.sort(key=attrgetter("suit"))  # utilize stable sorting to maintain default rank ordering but prioritize suit order

        run_1_4 = self.__cards[0].suit == self.__cards[1].suit == self.__cards[2].suit == self.__cards[3].suit and ((self.__cards[0].rank + 3 == self.__cards[1].rank + 2 == self.__cards[2].rank + 1 == self.__cards[3].rank) or (self.__cards[0].rank == Rank.ACE and self.__cards[1].rank == Rank.JACK and self.__cards[2].rank == Rank.QUEEN and self.__cards[3].rank == Rank.KING))
        run_1_3 = run_1_4 or self.__cards[0].suit == self.__cards[1].suit == self.__cards[2].suit and ((self.__cards[0].rank + 2 == self.__cards[1].rank + 1 == self.__cards[2].rank) or (self.__cards[0].rank == Rank.ACE and self.__cards[1].rank == Rank.QUEEN and self.__cards[2].rank == Rank.KING))

        run_4_7 = self.__cards[3].suit == self.__cards[4].suit == self.__cards[5].suit == self.__cards[6].suit and ((self.__cards[3].rank + 3 == self.__cards[4].rank + 2 == self.__cards[5].rank + 1 == self.__cards[6].rank) or (self.__cards[3].rank == Rank.ACE and self.__cards[4].rank == Rank.JACK and self.__cards[5].rank == Rank.QUEEN and self.__cards[6].rank == Rank.KING))
        run_5_7 = run_4_7 or self.__cards[4].suit == self.__cards[4].suit == self.__cards[5].suit and ((self.__cards[4].rank + 2 == self.__cards[5].rank + 1 == self.__cards[6].rank) or (self.__cards[4].rank == Rank.ACE and self.__cards[5].rank == Rank.QUEEN and self.__cards[6].rank == Rank.KING))

        if (run_1_3 and run_4_7) or (run_1_4 and run_5_7):
            return True

        if (run_1_3 and set_4_7) or (run_1_4 and set_5_7) or (set_1_3 and run_4_7) or (set_1_4 and run_5_7) or (
                set_1_3 and run_1_4) or (set_1_4 and run_1_3) or (set_4_7 and run_5_7) or (set_5_7 and run_4_7):
            return True

        self.__cards.sort()
        return False

    def discard(self, key):
        self.__deck.add_to_discard_pile(self.__cards.pop(key))


if __name__ == '__main__':
    c = Card.from_rank_and_suit(Rank.THREE, Suit.SPADES)
    print(c)

    c = 5 + Card(0)
    deck = Deck()

    for card in deck.discard_pile:
        print(card)
    print("-----")

#    deck.discard_pile[0] = 2 + Card(0)

    for card in deck.discard_pile:
        print(card)
    print("-----")

    #assert False
    print(deck)

    hands = deck.deal(2)
    print(deck)

    for hand in hands:
        print(hand)

    for _ in range(36):
        hands[0].draw(False)
        hands[0].discard(-2)

    print(deck)
    print(hands[0])

    hands[0].draw(True)
    hands[0].discard(-2)

    print(deck)
    print(hands[0])
    print(hands[0].check())

    # hand = Hand(deck)

    # hand.cards.append(Card.from_rank_and_suit(Rank.TWO, Suit.SPADES))
    # hand.cards.append(Card.from_rank_and_suit(Rank.TWO, Suit.DIAMONDS))
    # hand.cards.append(Card.from_rank_and_suit(Rank.THREE, Suit.SPADES))
    # hand.cards.append(Card.from_rank_and_suit(Rank.TWO, Suit.HEARTS))
    # hand.cards.append(Card.from_rank_and_suit(Rank.FOUR, Suit.SPADES))
    # hand.cards.append(Card.from_rank_and_suit(Rank.TWO, Suit.CLUBS))
    # hand.cards.append(Card.from_rank_and_suit(Rank.FIVE, Suit.SPADES))

    # hand.cards.sort()

    print(hands[0])

    for ca in hands[0]:
        print(ca)
        ca = Card(0)
    print()
    print(hands[0])