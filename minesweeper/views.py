import random
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from .utils import cells_to_str, iter_through_points, count_mines_around_point
# Create your views here.

VALUE_MINE = '*' # Define the value of the mine

class Cell:
	"""
		Individual cell of the minefield

		When created it's not flagged and not visible.
		parameters:
	    flagged -- is a flagged cell? (default False)
	    visible -- is a visible cell? (default False)
	"""

	def __init__(self, _value=0, flagged=False, visible=True):
		self.value = _value
		self.flagged = flagged
		self.visible = visible

	def is_mine(self):
		"""
			Check if the cell is a mine.
		"""
		return self.value == VALUE_MINE

	def __str__(self):        
		if not self.visible:
		    return ' '
		if self.flagged:
		    return 'f'
		if self.is_mine():
		    return '*'
		return str(self.value)


class MinefieldViewSet(viewsets.GenericViewSet):

	@action(methods=['POST'], detail=False, url_path='start-game', url_name='start_game')
	def start_game(self, request):
		"""
			Inits the minefield.

			parameters:
		    width -- minefield's width (required)
		    height -- minefield's height (required)
		    num_mines -- minefield's number of mines (required)
		"""
		try:
			width = int(request.data.get('width',''))
		except ValueError:
			return Response({'error':'El ancho debe ser un entero'},status=status.HTTP_400_BAD_REQUEST)

		try:
			height = int(request.data.get('height',''))
		except ValueError:
			return Response({'error':'El alto debe ser un entero'},status=status.HTTP_400_BAD_REQUEST)

		try:
			num_mines = int(request.data.get('num_mines',''))
		except ValueError:
			return Response({'error':'El número de minas ser un entero'},status=status.HTTP_400_BAD_REQUEST)

		if width < 0 or height < 0 or num_mines < 0:
			return Response({'error':'El ancho, alto y/o número de minas ser un entero positivo'},status=status.HTTP_400_BAD_REQUEST)			

		# size of the minefield
		self.cells = [[Cell(0) for _ in range(width) ] for _ in range(height)]
		self.num_mines = num_mines
		self.initialized = False
		
		# set the mines and count them		
		points = list(set(iter_through_points(self.cells))) # get the points
		random.shuffle(points)	# mix the points
		mine_points = points[:self.num_mines] # select points equal to mines
		clean_points = set(points[self.num_mines:]) # the rest of the points are clean

		# set mines in the mines points selected
		for point in mine_points:
			self.cells[point.y][point.x] = Cell(VALUE_MINE)

		# count the mines around the clean points
		for point in clean_points:
		 	self.cells[point.y][point.x] = Cell(count_mines_around_point(point,self.cells))

		return Response({'minefield':cells_to_str(self.cells)},status=status.HTTP_201_CREATED)

