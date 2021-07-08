import json
import random
from django.shortcuts import render
from json import JSONEncoder
from django.core.serializers.json import DjangoJSONEncoder
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from .utils import Point, cells_to_str, iter_through_points, count_mines_around_point, show_contents_at_point, all_cells_diplayed, show_contents_all_cells
# Create your views here.

VALUE_MINE = '*' # Define the value of the mine

class Cell:
	"""
		Individual cell of the minefield

		When created it's not flagged and not visible.
		parameters:
		value -- mine: *, 0 no mines arround, > 0 count of mines
	    flagged -- is a flagged cell? (default False)
	    visible -- is a visible cell? (default False)
	"""

	def __init__(self, value=0, flagged=False, visible=False):
		self.value = value
		self.flagged = flagged
		self.visible = visible

	def is_mine(self):
		"""
			Check if the cell is a mine.
		"""
		return self.value == VALUE_MINE

	def set_flag(self,state):
		self.flagged = state

	def set_visible(self):
		self.visible = True		

	def __str__(self):        
		if not self.visible:
		    return ' '
		if self.flagged:
		    return 'F'
		if self.is_mine():
		    return '*'
		return str(self.value)

class CellEncoder(JSONEncoder):
	"""
		To enconde the Cell as Json to store on the session
	"""
	def default(self, o):
		return o.__dict__

class MinefieldViewSet(viewsets.GenericViewSet):
	
	@action(methods=['POST'], detail=False, url_path='start-game', url_name='start_game')
	def start_game(self, request):
		"""
			Inits the minefield.

			parameters:
		    width -- minefield's width (required)
		    height -- minefield's height (required)
		    num_mines -- minefield's number of mines (required)

		    returns:
		    The minefield list
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

		if num_mines > width * height:
			return Response({'error':'El número de minas ser menor o igual que el número de celdas'},status=status.HTTP_400_BAD_REQUEST)

		# size of the minefield
		self.cells = [[Cell(0) for _ in range(width) ] for _ in range(height)]
		self.num_mines = num_mines		
		
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
		
		# Store the data on the session
		request.session['initialized'] = True
		request.session['cells'] = json.dumps(self.cells, indent=4, cls=CellEncoder)	# serializer the object to store as json
		request.session['width'] = width
		request.session['height'] = height
		# Return the minefield
		return Response({'minefield':cells_to_str(self.cells)},status=status.HTTP_201_CREATED)

	@action(methods=['POST'], detail=False, url_name='show_or_flag_cell_contents_at_point', url_path='show-or-flag-cell-contents-at-point')
	def show_or_flag_cell_contents_at_point(self, request):
		# define the cell list
		self.cells = [[Cell(0) for _ in range(request.session['width']) ] for _ in range(request.session['height'])]
		
		if 'initialized' not in request.session or not request.session['initialized']:
			return Response({'error':'Inicializa primero el juego'},status=status.HTTP_400_BAD_REQUEST)

		try:
			x = int(request.data.get('x',''))
		except ValueError:
			return Response({'error':'El valor de x debe ser un entero'},status=status.HTTP_400_BAD_REQUEST)

		try:
			y = int(request.data.get('y',''))
		except ValueError:
			return Response({'error':'El valor de y debe ser un entero'},status=status.HTTP_400_BAD_REQUEST)

		if x >= request.session['width']:
			return Response({'error':'El valor de x no debe ser mayor que el ancho'},status=status.HTTP_400_BAD_REQUEST)

		if y >= request.session['height']:
			return Response({'error':'El valor de y no debe ser mayor que el alto'},status=status.HTTP_400_BAD_REQUEST)

		# get the contents fron json 
		temp = json.loads(request.session['cells'])
		# to fill the list with the objects and its current values.
		for py, row in enumerate(temp):
		 	for px in range(len(row)):		 		
	 			self.cells[py][px] = Cell(row[px]['value'],row[px]['flagged'],row[px]['visible'])
		 		
	 	# is to flag a cell?
		if bool(request.data.get('flag',False)):			
			self.cells[y][x].set_flag(True)

		if self.cells[y][x].is_mine():			
			return Response({'minefield':cells_to_str(show_contents_all_cells(self.cells)),'information':"Haz perdido"},status=status.HTTP_200_OK)
		
		show_contents_at_point(Point(x,y), self.cells)		

		self.cells[y][x].set_visible()

		request.session['cells'] = json.dumps(self.cells, indent=4, cls=CellEncoder) # update the session

		if all_cells_diplayed(self.cells):
			return Response({'minefield':cells_to_str(self.cells),'information':"Haz ganado"},status=status.HTTP_200_OK)			
		
		return Response({'minefield':cells_to_str(self.cells),'[y][x]':str(y)+str(x),'temp':temp},status=status.HTTP_200_OK)