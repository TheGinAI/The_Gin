import linecache
import random
import sys
from itertools import combinations
from multiprocessing import Pool

from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
from gin_env import Card, Rank


def set_4(ihand):
    ihand = ihand[:]
    hands = combinations(ihand, 4)

    for hand in hands:
        if hand[0].rank == hand[1].rank == hand[2].rank == hand[3].rank:
            ihand.remove(hand[0])
            ihand.remove(hand[1])
            ihand.remove(hand[2])
            ihand.remove(hand[3])

            return ihand
    return ihand


def set_3(ihand):
    ihand = ihand[:]
    hands = combinations(ihand, 3)

    for hand in hands:
        if hand[0].rank == hand[1].rank == hand[2].rank:
            ihand.remove(hand[0])
            ihand.remove(hand[1])
            ihand.remove(hand[2])

            return ihand
    return ihand


def run_4(ihand):
    ihand = ihand[:]
    hands = combinations(ihand, 4)

    for hand in hands:
        if hand[0].suit == hand[1].suit == hand[2].suit == hand[3].suit and (hand[0].rank + 3 == hand[1].rank + 2 == hand[2].rank + 1 == hand[3].rank or (hand[0].rank == Rank.ACE and hand[1].rank == Rank.JACK and hand[2].rank == Rank.QUEEN and hand[3].rank == Rank.KING)):
            ihand.remove(hand[0])
            ihand.remove(hand[1])
            ihand.remove(hand[2])
            ihand.remove(hand[3])

            return ihand
    return ihand


def run_3(ihand):
    ihand = ihand[:]
    hands = combinations(ihand, 3)

    for hand in hands:
        if hand[0].suit == hand[1].suit == hand[2].suit and (hand[0].rank + 2 == hand[1].rank + 1 == hand[2].rank or (hand[0].rank == Rank.ACE and hand[1].rank == Rank.QUEEN and hand[2].rank == Rank.KING)):
            ihand.remove(hand[0])
            ihand.remove(hand[1])
            ihand.remove(hand[2])

            return ihand
    return ihand


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


def out_is_win(hand):
    if is_win(hand):
        return "".join(card.charcode for card in hand)
    else:
        return False


def in_is_win(charcode):
    return [Card.from_charcode(x) for x in charcode]


if __name__ == '__main__':
    if sys.argv[1] == "gen":
        pool = Pool()
        res = pool.imap(out_is_win, combinations([Card(x) for x in range(52)], 8), chunksize=131072)

        for x in res:
            if x:
                print(x)

    elif sys.argv[1] == "load":
        with open("util/bruteforce.txt", "r") as f:
            for line in f:
                for card in in_is_win(line):
                    print(card)
                print("=" * 16)

    elif sys.argv[1] == "check":
        with open("util/bruteforce.txt", "r") as f:
            lc = 0
            for line in f:
                if line != "\n":
                    lc += 1

        for card in in_is_win(linecache.getline("util/bruteforce.txt", random.randint(0, lc)).rstrip()):
            print(card)

    else:
        print("Invalid argument, use gen, load, or check")
