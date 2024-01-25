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
    def __init__(self, card_id):
        self.card_id = card_id
        self.rank, self.suit = self.to_rank_and_suit()

    def __str__(self):
        return "{} OF {}".format(self.rank.name, self.suit.name)

    def __eq__(self, other):
        return self.card_id == other.card_id

    def __lt__(self, other):
        return self.card_id < other.card_id

    def __add__(self, other):
        assert type(other) is int, "Can only modify card values using ints"
        return Card(self.card_id + other)

    def __sub__(self, other):
        assert type(other) is int, "Can only modify card values using ints"
        return Card(self.card_id - other)

    @classmethod
    def from_rank_and_suit(cls, rank, suit):
        return cls(rank * 4 + suit)

    def to_rank_and_suit(self):
        quotient, remainder = divmod(self.card_id, 4)
        return Rank(quotient), Suit(remainder)


class Deck:
    def __init__(self):
        self.cards = [Card(x) for x in range(52)]
        shuffle(self.cards)
        self.discard = [self.cards.pop()]

    def __str__(self):
        s = ""

        s += "Cards in deck:\n"
        for card in self.cards:
            s += card.__str__() + "\n"

        s += "\nCards in discard:\n"
        for card in self.discard:
            s += card.__str__() + "\n"

        return s

    def deal(self, hand_count):
        while True:
            hands = [Hand(self) for _ in range(hand_count)]

            for _ in range(7):
                for hand in hands:
                    hand.draw()

            for hand in hands:
                hand.cards.sort()

                # regenerate if a winning hand is dealt
                if hand.check_win():
                    continue

            return hands


class Hand:
    def __init__(self, deck):
        self.deck = deck
        self.cards = []

    def __str__(self):
        s = "Cards on hand:\n"

        for card in self.cards:
            s += str(card) + "\n"

        return s

    def draw(self):
        self.cards.append(self.deck.cards.pop())
        self.cards.sort()

    def check_win(self):
        # check sets
        set_1_4 = self.cards[0].rank == self.cards[1].rank == self.cards[2].rank == self.cards[3].rank
        set_1_3 = set_1_4 or (self.cards[0].rank == self.cards[1].rank == self.cards[2].rank)

        set_4_7 = self.cards[3].rank == self.cards[4].rank == self.cards[5].rank == self.cards[6].rank
        set_5_7 = set_4_7 or (self.cards[4].rank == self.cards[5].rank == self.cards[6].rank)

        if (set_1_3 and set_4_7) or (set_1_4 and set_5_7):
            return True

        # check runs
        self.cards.sort(key=attrgetter(
            "suit"))  # utilize stable sorting to maintain default rank ordering but prioritize suit order

        run_1_4 = self.cards[0].suit == self.cards[1].suit == self.cards[2].suit == self.cards[3].suit and ((self.cards[0].rank + 3 == self.cards[1].rank + 2 == self.cards[2].rank + 1 == self.cards[3].rank) or (self.cards[0].rank == Rank.ACE and self.cards[1].rank == Rank.JACK and self.cards[2].rank == Rank.QUEEN and self.cards[3].rank == Rank.KING))
        run_1_3 = run_1_4 or self.cards[0].suit == self.cards[1].suit == self.cards[2].suit and ((self.cards[0].rank + 2 == self.cards[1].rank + 1 == self.cards[2].rank) or (self.cards[0].rank == Rank.ACE and self.cards[1].rank == Rank.QUEEN and self.cards[2].rank == Rank.KING))

        run_4_7 = self.cards[3].suit == self.cards[4].suit == self.cards[5].suit == self.cards[6].suit and ((self.cards[3].rank + 3 == self.cards[4].rank + 2 == self.cards[5].rank + 1 == self.cards[6].rank) or (self.cards[3].rank == Rank.ACE and self.cards[4].rank == Rank.JACK and self.cards[5].rank == Rank.QUEEN and self.cards[6].rank == Rank.KING))
        run_5_7 = run_4_7 or self.cards[4].suit == self.cards[4].suit == self.cards[5].suit and ((self.cards[4].rank + 2 == self.cards[5].rank + 1 == self.cards[6].rank) or (self.cards[4].rank == Rank.ACE and self.cards[5].rank == Rank.QUEEN and self.cards[6].rank == Rank.KING))

        if (run_1_3 and run_4_7) or (run_1_4 and run_5_7):
            return True

        if (run_1_3 and set_4_7) or (run_1_4 and set_5_7) or (set_1_3 and run_4_7) or (set_1_4 and run_5_7) or (
                set_1_3 and run_1_4) or (set_1_4 and run_1_3) or (set_4_7 and run_5_7) or (set_5_7 and run_4_7):
            return True

        self.cards.sort()
        return False

    def discard(self, card):
        self.cards.remove(card)  # raises error when does not have that card; good
        self.deck.discard.append(card)

        if len(self.deck.cards) == 0:
            self.deck.cards = self.deck.discard
            shuffle(self.deck.cards)
            self.deck.discard = [self.deck.cards.pop()]


if __name__ == '__main__':
    deck = Deck()
    print(deck)

    hands = deck.deal(2)
    print(deck)

    for hand in hands:
        print(hand)

    for _ in range(36):
        hands[0].draw()
        hands[0].discard(hands[0].cards[-2])

    print(deck)
    print(hands[0])

    hands[0].draw()
    hands[0].discard(hands[0].cards[-2])

    print(deck)
    print(hands[0])
    hands[0].check_win()

    # hand = Hand(deck)

    # hand.cards.append(Card.from_rank_and_suit(Rank.TWO, Suit.SPADES))
    # hand.cards.append(Card.from_rank_and_suit(Rank.TWO, Suit.DIAMONDS))
    # hand.cards.append(Card.from_rank_and_suit(Rank.THREE, Suit.SPADES))
    # hand.cards.append(Card.from_rank_and_suit(Rank.TWO, Suit.HEARTS))
    # hand.cards.append(Card.from_rank_and_suit(Rank.FOUR, Suit.SPADES))
    # hand.cards.append(Card.from_rank_and_suit(Rank.TWO, Suit.CLUBS))
    # hand.cards.append(Card.from_rank_and_suit(Rank.FIVE, Suit.SPADES))

    # hand.cards.sort()

    print(hand.check_win())
