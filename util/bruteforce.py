import sys
import time
from itertools import combinations
from multiprocessing import Pool

from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
from gin_env import Deck, Card, Rank, win_lookup


# Script to generate a lookup table for winning hands

# Check if any 4-card combination is a valid set, then remove the cards that form the set and return the remainder so that they can be forwarded to further checks
def set_4(ihand):
    ihand = ihand[:]
    hands = combinations(ihand, 4)

    for hand in hands:
        # Check if combination consists of cards of same rank, which implies different suits
        if hand[0].rank == hand[1].rank == hand[2].rank == hand[3].rank:
            ihand.remove(hand[0])
            ihand.remove(hand[1])
            ihand.remove(hand[2])
            ihand.remove(hand[3])

            return ihand
    return ihand


# Check if any 3-card combination is a valid set, then remove the cards that form the set and return the remainder so that they can be forwarded to further checks
def set_3(ihand):
    ihand = ihand[:]
    hands = combinations(ihand, 3)

    for hand in hands:
        # Check if combination consists of cards of same rank, which implies different suits
        if hand[0].rank == hand[1].rank == hand[2].rank:
            ihand.remove(hand[0])
            ihand.remove(hand[1])
            ihand.remove(hand[2])

            return ihand
    return ihand


# Check if any 4-card combination is a valid run, then remove the cards that form the run and return the remainder so that they can be forwarded to further checks
def run_4(ihand):
    ihand = ihand[:]
    hands = combinations(ihand, 4)

    for hand in hands:
        # Check if combination consists of cards of same suit and ascending rank
        if hand[0].suit == hand[1].suit == hand[2].suit == hand[3].suit and (hand[0].rank + 3 == hand[1].rank + 2 == hand[2].rank + 1 == hand[3].rank or (hand[0].rank == Rank.ACE and hand[1].rank == Rank.JACK and hand[2].rank == Rank.QUEEN and hand[3].rank == Rank.KING)):
            ihand.remove(hand[0])
            ihand.remove(hand[1])
            ihand.remove(hand[2])
            ihand.remove(hand[3])

            return ihand
    return ihand


# Check if any 3-card combination is a valid run, then remove the cards that form the run and return the remainder so that they can be forwarded to further checks
def run_3(ihand):
    ihand = ihand[:]
    hands = combinations(ihand, 3)

    for hand in hands:
        # Check if combination consists of cards of same suit and ascending rank
        if hand[0].suit == hand[1].suit == hand[2].suit and (hand[0].rank + 2 == hand[1].rank + 1 == hand[2].rank or (hand[0].rank == Rank.ACE and hand[1].rank == Rank.QUEEN and hand[2].rank == Rank.KING)):
            ihand.remove(hand[0])
            ihand.remove(hand[1])
            ihand.remove(hand[2])

            return ihand
    return ihand


# Check if hand (Hand Class) has a winning combination
def is_win(hand):
    len_win = len(hand) - 7
    hand = list(hand)

    return (
            len(set_4(set_3(hand))) == len_win or
            len(set_3(set_4(hand))) == len_win or

            len(run_4(run_3(hand))) == len_win or
            len(run_3(run_4(hand))) == len_win or

            len(set_4(run_3(hand))) == len_win or
            len(set_3(run_4(hand))) == len_win or

            len(run_4(set_3(hand))) == len_win or
            len(run_3(set_4(hand))) == len_win
    )


# CHeck if hand is winning and encode as [a-zA-Z]
def out_is_win(hand):
    if is_win(hand):
        return "".join(card.charcode for card in hand)
    else:
        return False


# Decode winning hand
def in_is_win(charcode):
    return [Card.from_charcode(x) for x in charcode]


# Accepts arguments gen, load, or bench
if __name__ == '__main__':
    if sys.argv[1] == "gen":
        pool = Pool()

        # Check all 8-card hands (where cards in each combination are in sorted order, as they appear in gin_env.py) for winning hands
        res = pool.imap(out_is_win, combinations([Card(x) for x in range(52)], 8), chunksize=131072)

        # Print out all winning hands, can be used in conjunction with redirection, e.g. python bruteforce.py gen > bruteforce.txt
        for x in res:
            if x:
                print(x)

    # Read and print all winning hands in the order they were written to allow validation of algorithm correctness
    elif sys.argv[1] == "load":
        with open("util/bruteforce.txt", "r") as f:
            for line in f:
                for card in in_is_win(line.rstrip()):
                    print(card)
                print("=" * 16)

    # Benchmark to compare performance of checking winning cards on demand vs. precomputed lookup table
    elif sys.argv[1] == "bench":
        n = 10_000

        start = time.time()
        for _ in range(n):
            deck = Deck()
            hands = deck.deal(2)
            t = hands[0] in win_lookup
        lookup_t = time.time() - start

        start = time.time()
        for _ in range(n):
            deck = Deck()
            hands = deck.deal(2)
            t = is_win(hands[0])
        compute_t = time.time() - start

        print("Compute:", round(n / compute_t), "checks/s")
        print("Lookup:", round(n / lookup_t), "checks/s")


    else:
        print("Invalid argument, use gen, load, or check")
