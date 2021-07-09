import time
import json
import random
from django.shortcuts import render
from json import JSONEncoder
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
		"""
			to set flag to a cell
		"""
		self.flagged = state

	def set_visible(self):
		"""
			to show the contents of a cell
		"""
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
			It validates that  width, height and num_mines are positive integers
			if so generate a list of lists with each element of type Cell,
			Then gets the elements of the list shuffle them and get the the number 
			of mines and clean cell, fill the mines cell with the value
			and count the mines arount the clean points.
			Stores the data on session and returns the minefield

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
		request.session['lost'] = False
		request.session['won'] = False
		request.session['cells'] = json.dumps(self.cells, indent=4, cls=CellEncoder)	# serializer the object to store as json
		request.session['width'] = width
		request.session['height'] = height
		request.session['start'] = time.time()
		# Return the minefield
		return Response({'minefield':cells_to_str(self.cells)},status=status.HTTP_201_CREATED)

	@action(methods=['POST'], detail=False, url_name='show_or_flag_cell_contents_at_point', url_path='show-or-flag-cell-contents-at-point')
	def show_or_flag_cell_contents_at_point(self, request):
		"""
			Shows or flags a cell at a point.
			Checks if has won, lost or not initializated a game.
			If has lost or win shows the respective message.
			Checks that x and y be positive integers and they are
			in the range of width and height.
			create the cell size with the information from session,
			loads the data from the session and then fill up the 
			cells with the values of it.
			If flags cell, flags it else checks if mine if so displays
			the whole minefield and return it and the time, else 
			displays the cells next to it that doesn't have a mine.
			then displays the cell selected and store the cells in 
			the session, checks if all cells are shown or with mine
			if so is a winner returns the whole board and the time
			otherwise returns the board and the time.			

			parameters:
				flag -- is flag or showing? (required, true or false)
				x -- x coordinate (required)
				y -- y coordinate (required)

			returns:
				The minefield list (if not lost or won) and time
		"""
			
		if 'won' not in request.session or 'lost' not in request.session or 'initialized' not in request.session or not request.session['initialized']:
			return Response({'error':'Inicializa primero el juego'},status=status.HTTP_400_BAD_REQUEST)

		if request.session['lost']:
			return Response({'error':'Haz perdido, Inicializa un nuevo juego'},status=status.HTTP_400_BAD_REQUEST)

		if request.session['won']:
			return Response({'error':'Ya haz ganado, Inicializa un nuevo juego'},status=status.HTTP_400_BAD_REQUEST)
			
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

		# define the cell list
		self.cells = [[Cell(0) for _ in range(request.session['width']) ] for _ in range(request.session['height'])]

		# get the contents fron json 
		temp = json.loads(request.session['cells'])
		# to fill the list with the objects and its current values.
		for py, row in enumerate(temp):
		 	for px in range(len(row)):		 		
	 			self.cells[py][px] = Cell(row[px]['value'],row[px]['flagged'],row[px]['visible'])
		 		
	 	# is to flag a cell?
		if bool(request.data.get('flag',False)):			
			self.cells[y][x].set_flag(True)
		elif self.cells[y][x].is_mine():	
			request.session['lost'] = True
			t_diff = time.localtime(time.time() - request.session['start'])
			return Response({'minefield':cells_to_str(show_contents_all_cells(self.cells)),'information':"Haz perdido",'time':'{h}h {m}m {s}s'.format(h=t_diff.tm_hour, m=t_diff.tm_min, s=t_diff.tm_sec)},status=status.HTTP_200_OK)
		else:
			show_contents_at_point(Point(x,y), self.cells)		

		self.cells[y][x].set_visible()

		request.session['cells'] = json.dumps(self.cells, indent=4, cls=CellEncoder) # update the session

		# are all the cells displayed or with mine? then won
		if all_cells_diplayed(self.cells):
			request.session['won'] = True
			t_diff = time.localtime(time.time() - request.session['start'])
			return Response({'minefield':cells_to_str(self.cells),'information':"Haz ganado",'time':'{h}h {m}m {s}s'.format(h=t_diff.tm_hour, m=t_diff.tm_min, s=t_diff.tm_sec)},status=status.HTTP_200_OK)			
		
		t_diff = time.localtime(time.time() - request.session['start'])
		return Response({'minefield':cells_to_str(self.cells),'time':'{h}h {m}m {s}s'.format(h=t_diff.tm_hour, m=t_diff.tm_min, s=t_diff.tm_sec)},status=status.HTTP_200_OK)