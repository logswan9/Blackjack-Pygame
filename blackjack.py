import sys
import time
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
def createDeck(images = [], values = {}, names = []):
    cardDeck = []
    index = 0
    deck_count = 0
    while deck_count < 6:
        for card in images:
            cardDeck.append(Card(card, values[index], names[index]))
            index += 1
        deck_count += 1
        index = 0
    return cardDeck

def showCards(playersCards = [], dealersCards = []):
    #screen.fill((53, 101, 77))

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

def gameOverCheck(playerTotal, dealerTotal, stayCheck):
    if playerTotal == 21 and dealerTotal == 21:

        message = "Wow! You and the dealer have Blackjack! Insane! It's a draw."
        # print("To play again, press Down. To quit, press Escape.")
        return True, message
    elif playerTotal == 21:

        message = "Wow! You got BlackJack. Lucky! You Win!"
        # print("To play again, press Down. To quit, press Escape.")
        return True, message
    elif dealerTotal == 21:

        message = "Wow. The dealer got Blackjack. Unlucky."
        # print("To play again, press Down. To quit, press Escape.")
        return True, message
    elif playerTotal > 21:
        message = "You bust! You lost..."
        return True, message
    elif dealerTotal > 21:
        message = "The dealer bust! You win!"
        return True, message
    elif dealerTotal > playerTotal and stayCheck:
        message = "You stayed but the dealer won..."
        return True, message
    else:
        return False, ""

def determineScores(playerHand = [], dealerHand = []):
    y = 0
    z = 0



    for x in playerHand:
        y += x.card_value

    for x in dealerHand:
        z += x.card_value

    for x in playerHand:
        if y > 21 and x.card_value == 11:
            y -= 10

    for x in dealerHand:
        if z > 21 and x.card_value == 11:
            z -= 10

    return y,z








# Constants
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 1000

pygame.mixer.init()
pygame.init()
screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
pygame.display.set_caption("Blackjack")
clock = pygame.time.Clock()
pygame.display.set_icon(pygame.image.load("images/cards/40.png"))
my_Font = pygame.font.SysFont('Comic Sans MS', 30, bold=True)
pygame.mixer.music.load("sounds/backgroundCasino.wav")
pygame.mixer.music.play(loops = -1)
deck_shuffle_sound = pygame.mixer.Sound("sounds/deckShuffle.wav")
card_dealt_sound = pygame.mixer.Sound("sounds/cardDealt.wav")
humiliation_sound = pygame.mixer.Sound("sounds/humiliation-sound.wav")
staying_sound = pygame.mixer.Sound("sounds/stayingSound.wav")
you_win_sound = pygame.mixer.Sound("sounds/youWin.wav")
dealer_blackjack_loss_sound = pygame.mixer.Sound("sounds/dealerBJ.wav")
player_blackjack_sound = pygame.mixer.Sound("sounds/playerBJ.wav")
both_blackjack_sound = pygame.mixer.Sound("sounds/bothBJ.wav")
bust_sound = pygame.mixer.Sound("sounds/loser.wav")




def main():

    humiliation_sound.stop()
    you_win_sound.stop()
    player_blackjack_sound.stop()
    both_blackjack_sound.stop()
    bust_sound.stop()
    dealer_blackjack_loss_sound.stop()




    card_images = []
    card_back_image = pygame.image.load("images/cardBack/Card_Back.png")
    card_back_image = pygame.transform.scale(card_back_image, (80, 100))


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

    # card_values = {0: 10, 1: 10, 2: 11, 3: 11,
    #                4: 10, 5: 2, 6: 4, 7: 3,
    #                8: 4, 9: 3, 10: 4, 11: 4,                 #Testing purpose.
    #                12: 5, 13: 5, 14: 5, 15: 5,
    #                16: 6, 17: 6, 18: 6, 19: 6,
    #                20: 7, 21: 7, 22: 7, 23: 7,
    #                24: 8, 25: 8, 26: 8, 27: 8,
    #                28: 9, 29: 9, 30: 9, 31: 9,
    #                32: 10, 33: 10, 34: 10, 35: 10,
    #                36: 10, 37: 10, 38: 10, 39: 10,
    #                40: 10, 41: 10, 42: 10, 43: 10,
    #                44: 10, 45: 10, 46: 10, 47: 10,
    #                48: 11, 49: 11, 50: 11, 51: 11}


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
    message = ""
    game_message = ""
    dealer_message = ""

    deck = createDeck(card_images, card_values, card_names)
    random.shuffle(deck)


    # Fill screen with casino table green
    screen.fill((53, 101, 77))



    deck_index = 0

    player_total = 0
    dealer_total = 0
    scores_return_list = []
    deal_done = False
    deal_done_single = False


    player_turn_to_draw = False
    dealer_turn_to_draw = False
    player_stayed = False
    dealer_stayed = False


    game_over = False

    total_runtime = 0
    pause_time = 0

    yw_sc = False
    hum_sc = False
    dbj_sc = False
    pbjw_sc = False
    bbj_sc = False
    yl_sc = False


    running = True

    while running:

        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
                    pygame.display.quit()
                    pygame.quit()
                    quit()
                if event.key == K_SPACE and player_turn_to_draw and not game_over and not player_stayed:
                    #dealer_message = ""
                    players_hand = drawCardAndStore(deck[deck_index], players_hand)
                    deck_index += 1
                    card_dealt_sound.play()
                    showCards(players_hand, dealers_hand)

                    scores_return_list = determineScores(players_hand, dealers_hand)
                    screen.blit(my_Font.render("Your Score: " + str(player_total), False, (53, 101, 77)), (0, 0))
                    player_total = scores_return_list[0]
                    dealer_total = scores_return_list[1]
                    screen.blit(my_Font.render("Your Score: " + str(player_total), False, (255, 255, 255)), (0, 0))

                    screen.blit(my_Font.render(message, False, (53, 101, 77)), (50, 450))
                    message = ("You drew " + deck[(deck_index - 1)].card_name + ". Your total is " + str(player_total))
                    screen.blit(my_Font.render(message, False, (255, 255, 255)), (50, 450))

                    end_game_message = my_Font.render(game_message, False, (53, 101, 77))
                    screen.blit(end_game_message, (50, 550))
                    game_over, game_message = gameOverCheck(player_total, dealer_total, player_stayed)
                    pause_time = total_runtime
                    player_turn_to_draw = False
                    dealer_turn_to_draw = True
                    screen.blit(dealers_hand[1].surf, (290, 100))

                if event.key == K_UP and player_turn_to_draw and not game_over:
                    #dealer_message = ""
                    player_turn_to_draw = False
                    player_stayed = True
                    staying_sound.play()
                    user_message = my_Font.render(message, False, (53, 101, 77))
                    screen.blit(user_message, (50, 450))
                    pygame.display.update()
                    message = ("You stayed with an amount of " + str(player_total))
                    pause_time = total_runtime
                    screen.blit(my_Font.render("Press Down to fold" + str(dealer_total), False, (53, 101, 77)),(50, 650))
                    screen.blit(dealers_hand[1].surf, (290, 100))
                    # while dealer_total <= player_total:
                    #     if total_runtime > (pause_time + 3.0) and not game_over:
                    #         dealers_hand = drawCardAndStore(deck[deck_index], dealers_hand)
                    #         deck_index += 1
                    #         showCards(players_hand, dealers_hand)
                    #         scores_return_list = determineScores(players_hand, dealers_hand)
                    #         player_total = scores_return_list[0]
                    #         dealer_total = scores_return_list[1]
                    #         print("Dealer drew " + deck[(deck_index - 1)].card_name + ". Dealer's total is " + str(dealer_total))
                    #         game_over = gameOverCheck(player_total, dealer_total)
                    # if dealer_total > player_total and dealer_total <= 21:
                    #     message = ("The dealer won with " + str(dealer_total) + ". Press down to play again.")



                if event.key == K_DOWN:
                    main()




            elif event.type == QUIT:
                running = False
                pygame.display.quit()
                pygame.quit()
                quit()

        if total_runtime == 0:
            deck_shuffle_sound.play()

        if total_runtime > 1.5 and total_runtime < 1.75 and deck_index == 0:
            players_hand = drawCardAndStore(deck[deck_index], players_hand)
            deck_index += 1
            card_dealt_sound.play()
            showCards(players_hand, dealers_hand)

        if total_runtime > 2 and total_runtime < 2.25 and deck_index == 1:
            dealers_hand = drawCardAndStore(deck[deck_index], dealers_hand)
            deck_index += 1
            card_dealt_sound.play()
            showCards(players_hand, dealers_hand)

        if total_runtime > 2.5 and total_runtime < 2.75 and deck_index == 2:
            players_hand = drawCardAndStore(deck[deck_index], players_hand)
            deck_index += 1
            card_dealt_sound.play()
            showCards(players_hand, dealers_hand)

        if total_runtime > 3 and total_runtime < 3.25 and deck_index == 3:
            dealers_hand = drawCardAndStore(deck[deck_index], dealers_hand)
            deck_index += 1
            card_dealt_sound.play()
            showCards(players_hand, dealers_hand)
            screen.blit(card_back_image, (290, 100))
            #deal_done = True

        if total_runtime > 3.5 and total_runtime < 3.75 and not deal_done_single:
            #player_score = my_Font.render("Your Score: " + str(player_total), False, (53, 101, 77))
            player_score = my_Font.render("Your Score: " + str(player_total), False, (255, 255, 255))
            #dealer_score = my_Font.render("Dealer's Score: " + str(dealer_total), False, (53, 101, 77))
            dealer_score = my_Font.render("Dealer's Score: ??", False, (255, 255, 255))
            user_message = my_Font.render(message, False, (53, 101, 77))
            end_game_message = my_Font.render(game_message, False, (53, 101, 77))
            end_game_control = my_Font.render(dealer_message, False, (53, 101, 77))
            screen.blit(player_score, (0, 0))
            screen.blit(dealer_score, (SCREEN_WIDTH - 285, 0))
            screen.blit(user_message, (50, 450))
            screen.blit(end_game_message, (50, 550))
            screen.blit(end_game_control, (50, 650))
            deal_done = True
            deal_done_single = True






        if deal_done:
            scores_return_list = determineScores(players_hand, dealers_hand)
            screen.blit(my_Font.render("Your Score: " + str(player_total), False, (53, 101, 77)), (0, 0))
            #screen.blit(my_Font.render("Dealer's Score: " + str(dealer_total), False, (53, 101, 77)), (SCREEN_WIDTH - 285, 0))

            player_total = scores_return_list[0]
            dealer_total = scores_return_list[1]
            if dealer_total == 21:
                screen.blit(dealers_hand[1].surf, (290, 100))
            #print("Your total is " + str(player_total) + ". The dealer's total is " + str(dealer_total) + ".")
            end_game_message = my_Font.render(game_message, False, (53, 101, 77))
            screen.blit(end_game_message, (50, 550))
            game_over, game_message = gameOverCheck(player_total, dealer_total, player_stayed)
            # if player_total > dealer_total and not game_over and not player_stayed:
            #     game_message = "Press up if you want to stay. Or press space to draw again."
            # elif player_total <= dealer_total and not game_over and not player_stayed:
            #     game_message = "Press space to draw again."
            #     dealer_message = "Dealer is up " + str(dealer_total - player_total)
            message = ("You drew " + deck[(deck_index - 4)].card_name + " and " + deck[(deck_index - 2)].card_name + ". You have " + str(player_total))
            end_game_control = my_Font.render(dealer_message, False, (53, 101, 77))
            screen.blit(end_game_control, (50, 650))
            if not game_over:
                game_message = "Press up if you want to stay. Or press space to draw again."
                dealer_message = "Press Down to fold"
            user_message = my_Font.render(message, False, (53, 101, 77))
            end_game_message = my_Font.render(game_message, False, (53, 101, 77))
            end_game_control = my_Font.render(dealer_message, False, (53, 101, 77))

            screen.blit(user_message, (50, 450))
            screen.blit(end_game_message, (50, 550))
            screen.blit(end_game_control, (50, 650))
            user_message = my_Font.render(message, False, (255, 255, 255))
            end_game_message = my_Font.render(game_message, False, (255, 255, 255))
            end_game_control = my_Font.render(dealer_message, False, (255, 255, 255))
            screen.blit(user_message, (50, 450))
            screen.blit(end_game_message, (50, 550))
            screen.blit(end_game_control, (50, 650))
            screen.blit(my_Font.render("Your Score: " + str(player_total), False, (255, 255, 255)), (0, 0))
            #screen.blit(my_Font.render("Dealer's Score: " + str(dealer_total), False, (255, 255, 255)), (SCREEN_WIDTH - 285, 0))

            deal_done = False
            pause_time = total_runtime
            player_turn_to_draw = True

        if player_stayed:
            player_turn_to_draw = False
            dealer_turn_to_draw = True

        if player_total > dealer_total and not game_over and not player_stayed and player_turn_to_draw and deck_index > 4:
            end_game_message = my_Font.render(game_message, False, (53, 101, 77))
            screen.blit(end_game_message, (50, 550))

            game_message = "Press up if you want to stay. Or press space to draw again."

            end_game_message = my_Font.render(game_message, False, (255, 255, 255))
            screen.blit(end_game_message, (50, 550))

            end_game_control = my_Font.render(dealer_message, False, (53, 101, 77))
            screen.blit(end_game_control, (50, 650))

            dealer_message = "You are up " + str(player_total - dealer_total)

            end_game_control = my_Font.render(dealer_message, False, (255, 255, 255))
            screen.blit(end_game_control, (50, 650))

        elif player_total <= dealer_total and not game_over and not player_stayed and player_turn_to_draw and deck_index > 4:
            end_game_message = my_Font.render(game_message, False, (53, 101, 77))
            screen.blit(end_game_message, (50, 550))

            game_message = "Press space to draw again."

            end_game_message = my_Font.render(game_message, False, (255, 255, 255))
            screen.blit(end_game_message, (50, 550))
            #screen.blit(my_Font.render("Press Down to fold", False, (53, 101, 77)), (50, 650))

            if not dealer_stayed:
                end_game_control = my_Font.render(dealer_message, False, (53, 101, 77))
                screen.blit(end_game_control, (50, 650))


                dealer_message = "Dealer is up " + str(dealer_total - player_total)

                end_game_control = my_Font.render(dealer_message, False, (255, 255, 255))
                screen.blit(end_game_control, (50, 650))

        elif player_stayed and not game_over:
            end_game_message = my_Font.render(game_message, False, (53, 101, 77))
            #end_game_message.fill((53, 101, 77))
            screen.blit(end_game_message, (50, 550))
            pygame.display.update()
            game_message = ""


        if total_runtime > (pause_time + 1.5) and dealer_turn_to_draw and not game_over:
            if dealer_total > player_total and dealer_total > 16:
                #print("Dealer is staying with a total of " + str(dealer_total))
                dealer_stayed = True
                end_game_message = my_Font.render(game_message, False, (53, 101, 77))
                screen.blit(end_game_message, (50, 550))
                game_over, game_message = gameOverCheck(player_total, dealer_total, player_stayed)
                if not game_over:
                    end_game_control = my_Font.render(dealer_message, False, (53, 101, 77))
                    screen.blit(end_game_control, (50, 650))

                    dealer_message = "Dealer is staying with a total of " + str(dealer_total) + "! Dealer is up " + str(dealer_total - player_total) + "!"

                    end_game_control = my_Font.render(dealer_message, False, (255, 255, 255))
                    screen.blit(end_game_control, (50, 650))

                dealer_turn_to_draw = False
                player_turn_to_draw = True
            else:
                dealers_hand = drawCardAndStore(deck[deck_index], dealers_hand)
                deck_index += 1
                card_dealt_sound.play()
                showCards(players_hand, dealers_hand)
                scores_return_list = determineScores(players_hand, dealers_hand)
                screen.blit(my_Font.render("Dealer's Score: ??" + str(dealer_total), False, (53, 101, 77)), (SCREEN_WIDTH - 285, 0))
                screen.blit(my_Font.render("Dealer's Score: " + str(dealer_total), False, (53, 101, 77)), (SCREEN_WIDTH - 285, 0))
                player_total = scores_return_list[0]
                dealer_total = scores_return_list[1]
                pause_time = total_runtime

                while total_runtime < (pause_time + 0.75):
                    clock.tick(60)
                    total_runtime += 0.01666
                    pygame.display.update()
                if total_runtime > (pause_time + 0.75):

                    while dealer_total < player_total:
                        clock.tick(60)

                        if total_runtime > (pause_time + 0.75):
                            dealers_hand = drawCardAndStore(deck[deck_index], dealers_hand)
                            deck_index += 1
                            card_dealt_sound.play()
                            showCards(players_hand, dealers_hand)
                            pygame.display.update()
                            scores_return_list = determineScores(players_hand, dealers_hand)
                            screen.blit(my_Font.render("Dealer's Score: ??" + str(dealer_total), False, (53, 101, 77)), (SCREEN_WIDTH - 285, 0))
                            screen.blit(my_Font.render("Dealer's Score: " + str(dealer_total), False, (53, 101, 77)), (SCREEN_WIDTH - 285, 0))
                            player_total = scores_return_list[0]
                            dealer_total = scores_return_list[1]
                            pause_time = total_runtime



                        total_runtime += 0.01666


                screen.blit(my_Font.render("Dealer's Score: " + str(dealer_total), False, (255, 255, 255)), (SCREEN_WIDTH - 285, 0))
                #print("Dealer drew " + deck[(deck_index - 1)].card_name + ". Dealer's total is " + str(dealer_total))
                dealer_stayed = False
                end_game_message = my_Font.render(game_message, False, (53, 101, 77))
                screen.blit(end_game_message, (50, 550))
                game_over, game_message = gameOverCheck(player_total, dealer_total, player_stayed)
                dealer_turn_to_draw = False
                player_turn_to_draw = True
                pause_time = total_runtime




        # Add this amount 60 times every second to match as close to seconds passing(60 fps)
        total_runtime += 0.01666


        # player_score = my_Font.render("Your Score: " + str(player_total), False, (255, 255, 255))
        # if deck_index < 5 and not game_over:
        #     dealer_score = my_Font.render("Dealer's Score: " + str(dealer_total), False, (53, 101, 77))
        #     screen.blit(dealer_score, (SCREEN_WIDTH - 285, 0))
        #     dealer_score = my_Font.render("Dealer's Score: ??", False, (255, 255, 255))
        #     screen.blit(dealer_score, (SCREEN_WIDTH - 285, 0))
        # elif deck_index < 5 and game_over:
        #     screen.blit(my_Font.render("Dealer's Score: ??" + str(dealer_total), False, (53, 101, 77)), (SCREEN_WIDTH - 285, 0))
        #     screen.blit(my_Font.render("Dealer's Score: " + str(dealer_total), False, (255, 255, 255)), (SCREEN_WIDTH - 285, 0))
        #     #dealer_score = my_Font.render("Dealer's Score: " + str(dealer_total), False, (255, 255, 255))
        # else:
        #     screen.blit(my_Font.render("Dealer's Score: ??" + str(dealer_total), False, (53, 101, 77)), (SCREEN_WIDTH - 285, 0))
        #     dealer_score = my_Font.render("Dealer's Score: " + str(dealer_total), False, (255, 255, 255))




        # user_message = my_Font.render(message, False, (255, 255, 255))
        # end_game_message = my_Font.render(game_message, False, (255, 255, 255))
        # end_game_control = my_Font.render(dealer_message, False, (255, 255, 255))
        # screen.blit(player_score, (0, 0))
        # screen.blit(dealer_score, (SCREEN_WIDTH - 285, 0))
        # screen.blit(user_message, (50, 450))
        # screen.blit(end_game_message, (50, 550))
        # screen.blit(end_game_control, (50, 650))



        if game_over:
            end_game_message = my_Font.render(game_message, False, (255, 255, 255))
            screen.blit(end_game_message, (50, 550))

            screen.blit(my_Font.render("Dealer's Score: ??", False, (53, 101, 77)), (SCREEN_WIDTH - 285, 0))
            screen.blit(my_Font.render("Dealer's Score: " + str(dealer_total), False, (255, 255, 255)), (SCREEN_WIDTH - 285, 0))
            if game_message == "You stayed but the dealer won..." and not hum_sc:
                humiliation_sound.play()
                hum_sc = True
            elif game_message == "The dealer bust! You win!" and not yw_sc:
                you_win_sound.play()
                yw_sc = True
            elif game_message == "Wow. The dealer got Blackjack. Unlucky." and not dbj_sc:
                dealer_blackjack_loss_sound.play()
                dbj_sc = True
            elif game_message == "Wow! You got BlackJack. Lucky! You Win!" and not pbjw_sc:
                player_blackjack_sound.play()
                pbjw_sc = True
            elif game_message == "Wow! You and the dealer have Blackjack! Insane! It's a draw." and not bbj_sc:
                both_blackjack_sound.play()
                bbj_sc = True
            elif game_message == "You bust! You lost..." and not yl_sc:
                bust_sound.play()
                yl_sc = True
            #screen.blit(my_Font.render("Press Down to fold" + str(dealer_total), False, (53, 101, 77)), (50, 650))
            screen.blit(my_Font.render(dealer_message, False, (53, 101, 77)), (50, 650))
            dealer_message = "Press Down to play again or press escape to quit."
            screen.blit(my_Font.render("Press Down to play again or press escape to quit.", False,
                                       (255, 255, 255)), (50, 650))

        pygame.display.flip()

        message_updated = True
        # 60 Fps
        clock.tick(60)

        if total_runtime > 10000:
            total_runtime = 0

main()

pygame.quit()