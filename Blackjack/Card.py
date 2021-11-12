import pygame
class Card(pygame.sprite.Sprite):
	def __init__(self, playing_card_image, playing_card_value, playing_card_name):
		super(Card, self).__init__()
		self.surf = playing_card_image
		self.rect = self.surf.get_rect()
		self.card_value = playing_card_value
		self.card_name = playing_card_name

		
		