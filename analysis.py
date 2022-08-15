from random import shuffle
import numpy as np
import sys

EVAVU = -1
TYRANU = 1

values = (2,3,4,5,6,7,8,9,10,'J','K','Q','A')

def new_deck():
    """Returns a full shuffled deck of cards
    
    Returns
        :deck: A deck of cards with len 52 where the items are in the domain
         2 to 'A'
    """
    deck = [(v) for v in values for _ in range(4)]
    shuffle(deck)
    return deck

def new_counter():
    """A counter indicates how many of each card are left in the deck.
    
    Returns
        :counter: A counter initialized with 4 for each type of card
    """
    return [4 for _ in values]

def best_choice(counter, head):
    """
    Given a counter and a revealed card, return whether it is better to choose
    TYRANU or EVAVU. Also mutates the counter by subtracting 1 from the revealed
    card.

    Parameters
        :counter: The counter, see function new_counter
        :head:    The card on top 
    Returns
        :choice: The best choice in this scenario, which is one of the constants
        TYRANU or EVAVU. In case of equal odds either of them is returned.
    """
    i = values.index(head)
    # remove the card from the counter
    counter[i] -= 1
    # if there are more cards bvelo
    if sum(counter[:i]) > sum(counter[i+1:]):
        return EVAVU
    else:
        return TYRANU

def play():
    counter = new_counter()
    deck = new_deck()
    correct_guesses = 0
    gaming = True

    while gaming:
        head = deck.pop()
        if len(deck) == 0: # no more cards, the game is over
            correct_guesses += 1
            break
        my_choice = best_choice(counter, head)
        peek = deck[-1]
        fail1 = my_choice == EVAVU and (values.index(peek) > values.index(head))
        fail2 = my_choice == TYRANU and (values.index(peek) < values.index(head))
        if fail1 or fail2:
            gaming = False
        else:
            correct_guesses += 1
    
    return correct_guesses



if __name__ == "__main__":
    filename = ""
    stats_only = False
    stats = None

    # Parse command line arguments
    try:
        filename = sys.argv[1]
    except IndexError:
        print("USAGE: analysis.py [numpy-file] [--stats]")
        sys.exit(0)
    
    try:
        stats_only = sys.argv[2] == "--stats"
    except IndexError:
        pass


    # Print stats and exit
    if stats_only:
        try:
            stats = np.load(filename)
            print(f"""
            {stats.sum():,d} games played.
            {stats[52]} games won.
            So, 1 in {int(stats.sum() / stats[52]):,d} games is a winning game.
            """)
            sys.exit(0)
        except OSError:
            print(f"file {filename} not found")
            sys.exit(1)

    # Run simulations and save them to the specified file when a keyboard
    # interrupt is registered
    if not stats_only:
        try:
            stats = np.load(filename)
        except OSError:
            stats = np.zeros(53, dtype=np.uint)

        try:
            while True:
                stats[play()] += 1
        except KeyboardInterrupt:
            np.save(filename, stats)
            print(f"{np.sum(stats):,} games simulated. Have a nice day!")
            sys.exit(0)
