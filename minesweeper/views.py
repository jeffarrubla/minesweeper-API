import random
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .utils import cells_to_str
# Create your views here.

VALUE_MINE = '*' 

class Cell:
	"""
		Individual cell of the minefield

		When created it's not flagged and not visible.
		arguments:
	    flagged -- is a flagged cell? (default False)
	    visible -- is a visible cell? (default False)
	"""

	def __init__(self, _value=0, flagged=False, visible=False):
		self.value = _value
		self.flagged = flagged
		self.visible = visible

	def is_mine(self):
		"""Check if the cell is a mine."""
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

	@action(methods=['GET'], detail=False, url_path='start-game', url_name='start_game')
	def start_game(self, request):
		"""
			Inits the minefield.

			arguments:
		    width -- minefield's width? (required)
		    height -- minefield's height? (required)
		    num_mines -- minefield's number of mines? (required)
		"""
		try:
			width = int(request.GET.get('width',''))
		except ValueError:
			return Response({'error':'El ancho debe ser un entero'})

		try:
			height = int(request.GET.get('height',''))
		except ValueError:
			return Response({'error':'El alto debe ser un entero', })

		try:
			num_mines = int(request.GET.get('num_mines',''))
		except ValueError:
			return Response({'error':'El número de minas ser un entero'})

		self.cells = [[Cell(0) for  _ in range(width) ] for  _ in range(height)]
		self.num_mines = num_mines
		self.initialized = False
		return Response({'minefield':cells_to_str(self.cells)})

