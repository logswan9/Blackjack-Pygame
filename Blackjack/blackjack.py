import sys
import pygame
import random
from Card import Card
import os
from pygame.locals import (
	RLEACCEL,
	K_UP,
	K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    K_SPACE,
    KEYDOWN,
    QUIT,
)

# Method for creating the deck object. Making a deck of Card() objects. We pass images, values, then names.
def createDeck(deck = [], values = {}, names = []):
    cardDeck = []
    index = 0
    for card in deck:
        cardDeck.append(Card(card, values[index], names[index]))
        index += 1
    return cardDeck

def showCards(playersCards = [], dealersCards = []):
    xAxis = 200
    for x in playersCards:
        screen.blit(x.surf, (xAxis, 300))
        xAxis += 90
    xAxis = 200
    for x in dealersCards:
        screen.blit(x.surf, (xAxis, 100))
        xAxis += 90

def drawCardAndStore(card, hand = []):
    hand.append(card)
    return hand

def gameOverCheck(playerTotal, dealerTotal):
    if playerTotal == 21 and dealerTotal == 21:

        print("Wow! Both the player and the dealer have Blackjack! It's a draw.")
        print("To play again, press Space. To quit, press Escape.")
        return True
    elif playerTotal == 21:

        print("Wow! You got BlackJack. Lucky! You Win!")
        print("To play again, press Space. To quit, press Escape.")
        return True
    elif dealerTotal == 21:

        print("Wow. The dealer got Blackjack. Unlucky.")
        print("To play again, press Space. To quit, press Escape.")
        return True
    elif playerTotal > 21:
        print("You bust! You lost... Press Space to play again or press escape to quit.")
        return True
    elif dealerTotal > 21:
        print("The dealer bust! You win! Press Space to play again or press escape to quit.")
        return True
    else:
        return False

def determineScores(playerHand = [], dealerHand = []):
    y = 0
    z = 0
    p_ace = False
    d_ace = False


    for x in playerHand:
        y += x.card_value
        if x.card_value == 11:
            p_ace = True
        if y > 21 and p_ace:
            y -= 10

    for x in dealerHand:
        z += x.card_value
        if x.card_value == 11:
            d_ace = True
        if z > 21 and d_ace:
            z -= 10

    return y,z








# Constants
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 1000


pygame.init()
screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
pygame.display.set_caption("Blackjack")
clock = pygame.time.Clock()
pygame.display.set_icon(pygame.image.load("images/cards/40.png"))

def main():
    card_images = []


    for file in os.listdir('images/cards'):
        card_file = pygame.image.load("images/cards/" + file)
        card_file = pygame.transform.scale(card_file, (80, 100))
        card_images.append(card_file)






    card_values = {0:2, 1:2, 2:2, 3:2,
                   4:3, 5:3, 6:3, 7:3,
                   8:4, 9:4, 10:4, 11:4,
                   12:5, 13:5, 14:5, 15:5,
                   16:6, 17:6, 18:6, 19:6,
                   20:7, 21:7, 22:7, 23:7,
                   24:8, 25:8, 26:8, 27:8,
                   28:9, 29:9, 30:9, 31:9,
                   32:10, 33:10, 34:10, 35:10,
                   36:10, 37:10, 38:10, 39:10,
                   40:10, 41:10, 42:10, 43:10,
                   44:10, 45:10, 46:10, 47:10,
                   48:11, 49:11, 50:11, 51:11}

    card_names = ["2 of Diamonds", "2 of Hearts", "2 of Spades", "2 of Clubs",
                  "3 of Clubs", "3 of Diamonds", "3 of Hearts", "3 of Spades",
                  "4 of Clubs", "4 of Hearts", "4 of Spades", "4 of Diamonds",
                  "5 of Clubs", "5 of Diamonds", "5 of Hearts", "5 of Spades",
                  "6 of Clubs", "6 of Diamonds", "6 of Hearts", "6 of Spades",
                  "7 of Clubs", "7 of Diamonds", "7 of Hearts", "7 of Spades",
                  "8 of Clubs", "8 of Diamonds", "8 of Hearts", "8 of Spades",
                  "9 of Clubs", "9 of Diamonds", "9 of Hearts", "9 of Spades",
                  "10 of Clubs", "10 of Diamonds", "10 of Hearts", "10 of Spades",
                  "Jack of Clubs", "Jack of Diamonds", "Jack of Hearts", "Jack of Spades",
                  "Queen of Hearts", "Queen of Spades", "Queen of Clubs", "Queen of Diamonds",
                  "King of Clubs", "King of Diamonds", "King of Hearts", "King of Spades",
                  "Ace of Clubs", "Ace of Diamonds", "Ace of Hearts", "Ace of Spades"]





    dealers_hand = []
    players_hand = []
    dealers_chance = 0


    deck = createDeck(card_images, card_values, card_names)
    random.shuffle(deck)

    # Fill screen with casino table green
    screen.fill((53, 101, 77))



    deck_index = 0

    player_total = 0
    dealer_total = 0
    scores_return_list = []
    deal_done = False


    player_turn_to_draw = False
    dealer_turn_to_draw = False


    game_over = False

    total_runtime = 0
    pause_time = 0





    running = True

    while running:

        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
                    pygame.display.quit()
                    pygame.quit()
                    quit()
                if event.key == K_SPACE and player_turn_to_draw and not game_over:
                    players_hand = drawCardAndStore(deck[deck_index], players_hand)
                    deck_index += 1
                    showCards(players_hand, dealers_hand)
                    scores_return_list = determineScores(players_hand, dealers_hand)
                    player_total = scores_return_list[0]
                    dealer_total = scores_return_list[1]
                    print("You drew " + deck[(deck_index - 1)].card_name + ". Your total is " + str(player_total))
                    game_over = gameOverCheck(player_total, dealer_total)
                    pause_time = total_runtime
                    player_turn_to_draw = False
                    dealer_turn_to_draw = True


                if event.key == K_DOWN:
                    main()




            elif event.type == QUIT:
                running = False
                pygame.display.quit()
                pygame.quit()
                quit()

        if total_runtime > 1 and total_runtime < 2 and deck_index == 0:
            players_hand = drawCardAndStore(deck[deck_index], players_hand)
            deck_index += 1
            showCards(players_hand, dealers_hand)

        if total_runtime > 2 and total_runtime < 3 and deck_index == 1:
            dealers_hand = drawCardAndStore(deck[deck_index], dealers_hand)
            deck_index += 1
            showCards(players_hand, dealers_hand)

        if total_runtime > 3 and total_runtime < 4 and deck_index == 2:
            players_hand = drawCardAndStore(deck[deck_index], players_hand)
            deck_index += 1
            showCards(players_hand, dealers_hand)

        if total_runtime > 4 and total_runtime < 5 and deck_index == 3:
            dealers_hand = drawCardAndStore(deck[deck_index], dealers_hand)
            deck_index += 1
            showCards(players_hand, dealers_hand)
            deal_done = True


        if deal_done:
            scores_return_list = determineScores(players_hand, dealers_hand)
            player_total = scores_return_list[0]
            dealer_total = scores_return_list[1]
            print("Your total is " + str(player_total) + ". The dealer's total is " + str(dealer_total) + ".")
            game_over = gameOverCheck(player_total, dealer_total)
            deal_done = False
            pause_time = total_runtime
            player_turn_to_draw = True


        if total_runtime > (pause_time + 3.0) and dealer_turn_to_draw and not game_over:
            dealers_hand = drawCardAndStore(deck[deck_index], dealers_hand)
            deck_index += 1
            showCards(players_hand, dealers_hand)
            scores_return_list = determineScores(players_hand, dealers_hand)
            player_total = scores_return_list[0]
            dealer_total = scores_return_list[1]
            print("Dealer drew " + deck[(deck_index - 1)].card_name + ". Dealer's total is " + str(dealer_total))
            game_over = gameOverCheck(player_total, dealer_total)
            dealer_turn_to_draw = False
            player_turn_to_draw = True


        # Add this amount 60 times every second to match as close to seconds passing(60 fps)
        total_runtime += 0.01666




        pygame.display.update()

        # 60 Fps
        clock.tick(60)

main()

pygame.quit()