def card_suit(card_id):
    poker_deck = {
    0: {'rank_code': '|', 'suit_code': '\U00002663', 'rank': 'A ', 'suit': 'Club'},
    1: {'rank_code': '|', 'suit_code': '\U00002666', 'rank': 'A ', 'suit': 'Diamond'},
    2: {'rank_code': '|', 'suit_code': '\U00002665', 'rank': 'A ', 'suit': 'Heart'},
    3: {'rank_code': '|', 'suit_code': '\U00002660', 'rank': 'A ', 'suit': 'Spade'},
    4: {'rank_code': '|', 'suit_code': '\U00002663', 'rank': '2 ', 'suit': 'Club'},
    5: {'rank_code': '|', 'suit_code': '\U00002666', 'rank': '2 ', 'suit': 'Diamond'},
    6: {'rank_code': '|', 'suit_code': '\U00002665', 'rank': '2 ', 'suit': 'Heart'},
    7: {'rank_code': '|', 'suit_code': '\U00002660', 'rank': '2 ', 'suit': 'Spade'},
    8: {'rank_code': '|', 'suit_code': '\U00002663', 'rank': '3 ', 'suit': 'Club'},
    9: {'rank_code': '|', 'suit_code': '\U00002666', 'rank': '3 ', 'suit': 'Diamond'},
    10: {'rank_code': '|', 'suit_code': '\U00002665', 'rank': '3 ', 'suit': 'Heart'},
    11: {'rank_code': '|', 'suit_code': '\U00002660', 'rank': '3 ', 'suit': 'Spade'},
    12: {'rank_code': '|', 'suit_code': '\U00002663', 'rank': '4 ', 'suit': 'Club'},
    13: {'rank_code': '|', 'suit_code': '\U00002666', 'rank': '4 ', 'suit': 'Diamond'},
    14: {'rank_code': '|', 'suit_code': '\U00002665', 'rank': '4 ', 'suit': 'Heart'},
    15: {'rank_code': '|', 'suit_code': '\U00002660', 'rank': '4 ', 'suit': 'Spade'},
    16: {'rank_code': '|', 'suit_code': '\U00002663', 'rank': '5 ', 'suit': 'Club'},
    17: {'rank_code': '|', 'suit_code': '\U00002666', 'rank': '5 ', 'suit': 'Diamond'},
    18: {'rank_code': '|', 'suit_code': '\U00002665', 'rank': '5 ', 'suit': 'Heart'},
    19: {'rank_code': '|', 'suit_code': '\U00002660', 'rank': '5 ', 'suit': 'Spade'},
    20: {'rank_code': '|', 'suit_code': '\U00002663', 'rank': '6 ', 'suit': 'Club'},
    21: {'rank_code': '|', 'suit_code': '\U00002666', 'rank': '6 ', 'suit': 'Diamond'},
    22: {'rank_code': '|', 'suit_code': '\U00002665', 'rank': '6 ', 'suit': 'Heart'},
    23: {'rank_code': '|', 'suit_code': '\U00002660', 'rank': '6 ', 'suit': 'Spade'},
    24: {'rank_code': '|', 'suit_code': '\U00002663', 'rank': '7 ', 'suit': 'Club'},
    25: {'rank_code': '|', 'suit_code': '\U00002666', 'rank': '7 ', 'suit': 'Diamond'},
    26: {'rank_code': '|', 'suit_code': '\U00002665', 'rank': '7 ', 'suit': 'Heart'},
    27: {'rank_code': '|', 'suit_code': '\U00002660', 'rank': '7 ', 'suit': 'Spade'},
    28: {'rank_code': '|', 'suit_code': '\U00002663', 'rank': '8 ', 'suit': 'Club'},
    29: {'rank_code': '|', 'suit_code': '\U00002666', 'rank': '8 ', 'suit': 'Diamond'},
    30: {'rank_code': '|', 'suit_code': '\U00002665', 'rank': '8 ', 'suit': 'Heart'},
    31: {'rank_code': '|', 'suit_code': '\U00002660', 'rank': '8 ', 'suit': 'Spade'},
    32: {'rank_code': '|', 'suit_code': '\U00002663', 'rank': '9 ', 'suit': 'Club'},
    33: {'rank_code': '|', 'suit_code': '\U00002666', 'rank': '9 ', 'suit': 'Diamond'},
    34: {'rank_code': '|', 'suit_code': '\U00002665', 'rank': '9 ', 'suit': 'Heart'},
    35: {'rank_code': '|', 'suit_code': '\U00002660', 'rank': '9 ', 'suit': 'Spade'},
    36: {'rank_code': '|', 'suit_code': '\U00002663', 'rank': '10', 'suit': 'Club'},
    37: {'rank_code': '|', 'suit_code': '\U00002666', 'rank': '10', 'suit': 'Diamond'},
    38: {'rank_code': '|', 'suit_code': '\U00002665', 'rank': '10', 'suit': 'Heart'},
    39: {'rank_code': '|', 'suit_code': '\U00002660', 'rank': '10', 'suit': 'Spade'},
    40: {'rank_code': '|', 'suit_code': '\U00002663', 'rank': 'J ', 'suit': 'Club'},
    41: {'rank_code': '|', 'suit_code': '\U00002666', 'rank': 'J ', 'suit': 'Diamond'},
    42: {'rank_code': '|', 'suit_code': '\U00002665', 'rank': 'J ', 'suit': 'Heart'},
    43: {'rank_code': '|', 'suit_code': '\U00002660', 'rank': 'J ', 'suit': 'Spade'},
    44: {'rank_code': '|', 'suit_code': '\U00002663', 'rank': 'Q ', 'suit': 'Club'},
    45: {'rank_code': '|', 'suit_code': '\U00002666', 'rank': 'Q ', 'suit': 'Diamond'},
    46: {'rank_code': '|', 'suit_code': '\U00002665', 'rank': 'Q ', 'suit': 'Heart'},
    47: {'rank_code': '|', 'suit_code': '\U00002660', 'rank': 'Q ', 'suit': 'Spade'},
    48: {'rank_code': '|', 'suit_code': '\U00002663', 'rank': 'K ', 'suit': 'Club'},
    49: {'rank_code': '|', 'suit_code': '\U00002666', 'rank': 'K ', 'suit': 'Diamond'},
    50: {'rank_code': '|', 'suit_code': '\U00002665', 'rank': 'K ', 'suit': 'Heart'},
    51: {'rank_code': '|', 'suit_code': '\U00002660', 'rank': 'K ', 'suit': 'Spade'},
    52: {'rank_code': '|', 'suit_code': ' ', 'rank': '  ', 'suit': 'side_blocker'},
    53: {'rank_code': ' ', 'suit_code': '_', 'rank': '__', 'suit': 'up_blocker'},
    54: {'rank_code': ' ', 'suit_code': '_', 'rank': '__', 'suit': 'down_blocker'},
    55: {'rank_code': '', 'suit_code': '\U0001F0A0', 'rank': ' x', 'suit': 'deck'},
    56: {'rank_code': '|', 'suit_code': '?', 'rank': '? ', 'suit': 'unknown'},
}  
    return "".join(poker_deck[card_id][i] for i in ['rank_code','suit_code','rank','rank_code'])

def card_shown(deck,discard_card,discard_amount,active,*players,**kw):
    assert len(players) <= 7 
    
    print("".join("=" for _ in range(60)))
    print(" The Gin - Interactive AI Card Game")
    
    for p, hand in enumerate(players, start=1):
        print("","".join("_" for _ in range((len(hand)*6)+10)))
        print("|         "," ".join(card_suit(53)for _ in hand),"|")
        
        if active == 0 or active == p:
            print("|player %d:"%p," ".join(card_suit(i) for i in hand),"|")
        else:
            print("|player %d:"%p," ".join(card_suit(56) for _ in hand),"|")
        
        print("|         "," ".join(card_suit(52)for _ in hand),"|")
        print("","".join("-" for _ in range((len(hand)*6)+10)))
        

    print("")
    print(" deck:", "".join(card_suit(55)), str(deck))
    print("           "," ".join(card_suit(53)for _ in range(1)))
    print(" discarded:"," ".join(card_suit(i) for i in [discard_card]),'- amount:',"".join(card_suit(55)), str(discard_amount))
    print("           "," ".join(card_suit(52)for _ in range(1)),"".join(" " for _ in range(12)))
    print("".join("=" for _ in range(60)))
    
#     print("".join("=" for _ in range(60)))

def card_action(hand,action_code):
    if action_code == 2:    
        card_index = input("Enter index number of card you'd like to discard")
        hand.discard(int(card_index)-1)
    else:
        draw_id = input("Which deck would you like to draw from, 1 for discarded and 2 for face-down deck")
        draw_id = int(draw_id)
        if draw_id == 1:
            hand.draw(True)
        else:
            hand.draw(False)
            
def game_play(playeramount=2):
    deck = Deck()
    hands = deck.deal(playeramount)
    
    while True:
        #P1 Action
        card_shown(len(deck.draw_pile),deck.discard_pile_top.card_id,len(deck.discard_pile),0,[card.card_id for card in hands[0]],[card.card_id for card in hands[1]])
        print("Player 1 Action")
        card_action(hands[0],1)
        card_shown(len(deck.draw_pile),deck.discard_pile_top.card_id,len(deck.discard_pile),0,[card.card_id for card in hands[0]],[card.card_id for card in hands[1]])
        if hands[0].check == True:
            break
        print("Player 1 Action")
        card_action(hands[0],2)
        card_shown(len(deck.draw_pile),deck.discard_pile_top.card_id,len(deck.discard_pile),0,[card.card_id for card in hands[0]],[card.card_id for card in hands[1]])
        #P2 Action
        card_shown(len(deck.draw_pile),deck.discard_pile_top.card_id,len(deck.discard_pile),0,[card.card_id for card in hands[0]],[card.card_id for card in hands[1]])
        print("Player 2 Action")
        card_action(hands[1],1)
        card_shown(len(deck.draw_pile),deck.discard_pile_top.card_id,len(deck.discard_pile),0,[card.card_id for card in hands[0]],[card.card_id for card in hands[1]])
        if hands[1].check == True:
            break
        print("Player 2 Action")
        card_action(hands[1],2)
        card_shown(len(deck.draw_pile),deck.discard_pile_top.card_id,len(deck.discard_pile),0,[card.card_id for card in hands[0]],[card.card_id for card in hands[1]])
        
game_play(2)
