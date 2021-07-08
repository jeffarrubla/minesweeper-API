from django.urls import reverse
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status

#for testing to log things
import sys
import unittest
import logging
#with the declarations
logger = logging.getLogger()
logger.level = logging.DEBUG

# Create your tests here.

class StartGameTest(TestCase):

	def setUp(self):
		"""
			Create instance of the API and start the values
		"""
		self.client = APIClient()
		self.init_values = {'width':'2','height':'2','num_mines':'1'}
		
	def test_start_game_succefully(self):
		""" 
			Test to start a game successfully.			

			Parameters:
			----------
				width -- minefield's width? (required)
			    height -- minefield's height? (required)
			    num_mines -- minefield's number of mines? (required)

			Assertions
			----------
				This test is successful starting a game.
		"""		
		
		# get API response
		response = self.client.post(reverse('minesweeper:start_game-start_game'),self.init_values, HTTP_USER_AGENT='Mozilla/5.0', format='json')
		# do assetions
		self.assertEqual(len(response.json()['minefield']), 2) # there are 2 rows
		self.assertEqual(response.status_code, status.HTTP_201_CREATED)

	def test_cannot_start_game_with_num_mines_bigger_than_total_of_cells(self):
		""" 
			Test to start a game successfully, num_mines is bigger than number of cells.

			Parameters:
			----------
				width -- minefield's width? (required)
			    height -- minefield's height? (required)
			    num_mines -- minefield's number of mines? (required)

			Assertions
			----------
				This test fails starting a game num_mines is bigger than number of cells.
		"""		
		# set the num_mines to bigger than number of cells
		self.init_values['num_mines'] = '5'
		# get API response
		response = self.client.post(reverse('minesweeper:start_game-start_game'),self.init_values, HTTP_USER_AGENT='Mozilla/5.0', format='json')
		# do assetions
		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

	def test_cannot_start_game_with_float_width(self):
		""" 
			Test to start a game successfully, width is float.

			Parameters:
			----------
				width -- minefield's width? (required)
			    height -- minefield's height? (required)
			    num_mines -- minefield's number of mines? (required)

			Assertions
			----------
				This test fails starting a game width is float.
		"""		
		# set the width to float
		self.init_values['width'] = '5.954'
		# get API response
		response = self.client.post(reverse('minesweeper:start_game-start_game'),self.init_values, HTTP_USER_AGENT='Mozilla/5.0', format='json')
		# do assetions
		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

	def test_cannot_start_game_succefully_with_float_height(self):
		""" 
			Test to start a game successfully, height is float.

			Parameters:
			----------
				width -- minefield's width? (required)
			    height -- minefield's height? (required)
			    num_mines -- minefield's number of mines? (required)

			Assertions
			----------
				This test fails starting a game height is float.
		"""		
		# set the height to float
		self.init_values['height'] = '5.954'
		# get API response
		response = self.client.post(reverse('minesweeper:start_game-start_game'),self.init_values, HTTP_USER_AGENT='Mozilla/5.0', format='json')
		# do assetions
		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

	def test_cannot_start_game_succefully_with_float_num_mines(self):
		""" 
			Test to start a game successfully, num_mines is float.

			Parameters:
			----------
				width -- minefield's width? (required)
			    height -- minefield's height? (required)
			    num_mines -- minefield's number of mines? (required)

			Assertions
			----------
				This test fails starting a game num_mines is float.
		"""		
		# set the num_mines to float
		self.init_values['num_mines'] = '5.954'
		# get API response
		response = self.client.post(reverse('minesweeper:start_game-start_game'),self.init_values, HTTP_USER_AGENT='Mozilla/5.0', format='json')
		# do assetions
		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

	def test_cannot_start_game_missing_width(self):
		""" 
			Test to start a game successfully without width.			

			Parameters:
			----------
				width -- minefield's width? (required)
			    height -- minefield's height? (required)
			    num_mines -- minefield's number of mines? (required)

			Assertions
			----------
				This test fails starting a game width is missing.
		"""		
		# remove the width
		self.init_values.pop('width')
		# get API response
		response = self.client.post(reverse('minesweeper:start_game-start_game'),self.init_values, HTTP_USER_AGENT='Mozilla/5.0', format='json')
		# do assetions		
		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

	def test_cannot_start_game_missing_height(self):
		""" 
			Test to start a game successfully without height.			

			Parameters:
			----------
				width -- minefield's width? (required)
			    height -- minefield's height? (required)
			    num_mines -- minefield's number of mines? (required)

			Assertions
			----------
				This test fails starting a game height is missing.
		"""		
		# remove the height
		self.init_values.pop('height')
		# get API response
		response = self.client.post(reverse('minesweeper:start_game-start_game'),self.init_values, HTTP_USER_AGENT='Mozilla/5.0', format='json')
		# do assetions		
		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

	def test_cannot_start_game_missing_num_mines(self):
		""" 
			Test to start a game successfully without num_mines.			

			Parameters:
			----------
				width -- minefield's width? (required)
			    height -- minefield's height? (required)
			    num_mines -- minefield's number of mines? (required)

			Assertions
			----------
				This test fails starting a game num_mines is missing.
		"""		
		# remove the num_mines
		self.init_values.pop('num_mines')
		# get API response
		response = self.client.post(reverse('minesweeper:start_game-start_game'),self.init_values, HTTP_USER_AGENT='Mozilla/5.0', format='json')
		# do assetions		
		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

	def test_cannot_start_game_width_str(self):
		""" 
			Test to start a game successfully width str.			

			Parameters:
			----------
				width -- minefield's width? (required)
			    height -- minefield's height? (required)
			    num_mines -- minefield's number of mines? (required)

			Assertions
			----------
				This test fails starting a game width is str.
		"""		
		# set the width as string
		self.init_values['width'] = 'string'
		# get API response
		response = self.client.post(reverse('minesweeper:start_game-start_game'),self.init_values, HTTP_USER_AGENT='Mozilla/5.0', format='json')
		# do assetions		
		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

	def test_cannot_start_game_height_str(self):
		""" 
			Test to start a game successfully height str.			

			Parameters:
			----------
				width -- minefield's width? (required)
			    height -- minefield's height? (required)
			    num_mines -- minefield's number of mines? (required)

			Assertions
			----------
				This test fails starting a game height is str.
		"""		
		# set the height as string
		self.init_values['height'] = 'string'
		# get API response
		response = self.client.post(reverse('minesweeper:start_game-start_game'),self.init_values, HTTP_USER_AGENT='Mozilla/5.0', format='json')
		# do assetions		
		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

	def test_cannot_start_game_num_mines_str(self):
		""" 
			Test to start a game successfully num_mines str.			

			Parameters:
			----------
				width -- minefield's width? (required)
			    height -- minefield's height? (required)
			    num_mines -- minefield's number of mines? (required)

			Assertions
			----------
				This test fails starting a game num_mines is str.
		"""		
		# set the height as string
		self.init_values['num_mines'] = 'string'
		# get API response
		response = self.client.post(reverse('minesweeper:start_game-start_game'),self.init_values, HTTP_USER_AGENT='Mozilla/5.0', format='json')
		# do assetions		
		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

	def test_cannot_start_game_width_is_empty(self):
		""" 
			Test to start a game successfully width is empty.			

			Parameters:
			----------
				width -- minefield's width? (required)
			    height -- minefield's height? (required)
			    num_mines -- minefield's number of mines? (required)

			Assertions
			----------
				This test fails starting a game width is empty.
		"""		
		# set the width as empty
		self.init_values['width'] = ' '
		# get API response
		response = self.client.post(reverse('minesweeper:start_game-start_game'),self.init_values, HTTP_USER_AGENT='Mozilla/5.0', format='json')
		# do assetions		
		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

	def test_cannot_start_game_height_is_empty(self):
		""" 
			Test to start a game successfully height is empty.			

			Parameters:
			----------
				width -- minefield's width? (required)
			    height -- minefield's height? (required)
			    num_mines -- minefield's number of mines? (required)

			Assertions
			----------
				This test fails starting a game height is empty.
		"""		
		# set the height as empty
		self.init_values['height'] = ' '
		# get API response
		response = self.client.post(reverse('minesweeper:start_game-start_game'),self.init_values, HTTP_USER_AGENT='Mozilla/5.0', format='json')
		# do assetions		
		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

	def test_cannot_start_game_num_mines_is_empty(self):
		""" 
			Test to start a game successfully num_mines is empty.			

			Parameters:
			----------
				width -- minefield's width? (required)
			    height -- minefield's height? (required)
			    num_mines -- minefield's number of mines? (required)

			Assertions
			----------
				This test fails starting a game num_mines is empty.
		"""		
		# set the num_mines as empty
		self.init_values['num_mines'] = ' '
		# get API response
		response = self.client.post(reverse('minesweeper:start_game-start_game'),self.init_values, HTTP_USER_AGENT='Mozilla/5.0', format='json')
		# do assetions		
		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

	def test_cannot_start_game_width_is_negative(self):
		""" 
			Test to start a game successfully width is empty.			

			Parameters:
			----------
				width -- minefield's width? (required)
			    height -- minefield's height? (required)
			    num_mines -- minefield's number of mines? (required)

			Assertions
			----------
				This test fails starting a game width is negative.
		"""		
		# set the width as empty
		self.init_values['width'] = '-10'
		# get API response
		response = self.client.post(reverse('minesweeper:start_game-start_game'),self.init_values, HTTP_USER_AGENT='Mozilla/5.0', format='json')
		# do assetions		
		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

	def test_cannot_start_game_height_is_negative(self):
		""" 
			Test to start a game successfully height is empty.			

			Parameters:
			----------
				width -- minefield's width? (required)
			    height -- minefield's height? (required)
			    num_mines -- minefield's number of mines? (required)

			Assertions
			----------
				This test fails starting a game height is negative.
		"""		
		# set the height as empty
		self.init_values['height'] = '-10'
		# get API response
		response = self.client.post(reverse('minesweeper:start_game-start_game'),self.init_values, HTTP_USER_AGENT='Mozilla/5.0', format='json')
		# do assetions		
		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

	def test_cannot_start_game_num_mines_is_negative(self):
		""" 
			Test to start a game successfully num_mines is empty.			

			Parameters:
			----------
				width -- minefield's width? (required)
			    height -- minefield's height? (required)
			    num_mines -- minefield's number of mines? (required)

			Assertions
			----------
				This test fails starting a game num_mines is negative.
		"""		
		# set the num_mines as empty
		self.init_values['num_mines'] = '-10'
		# get API response
		response = self.client.post(reverse('minesweeper:start_game-start_game'),self.init_values, HTTP_USER_AGENT='Mozilla/5.0', format='json')
		# do assetions		
		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)