from collections import namedtuple

Point = namedtuple('Point', ['x', 'y']) # To manage the x,y cells

def cells_to_str(cells):
	"""
		To format the mainsweeper as a list of list and return it.
	"""
	return [[str(cell) for cell in row] for row in cells]

def iter_through_points(cells):
	"""
		Iterate through the cells, the (x, y) points.
	"""
	for y, row in enumerate(cells):
		for x in range(len(row)):
			yield Point(x, y)

def cells_around_point(point, cells):
	"""
		to find the cells around a point
	"""
	point_x, point_y = point
	width = len(cells[0]) -1	# To know the max width
	heigth = len(cells) -1		# to know the max height
	for x in range(point_x - 1, point_x + 2):
		for y in range(point_y - 1, point_y + 2):
			# indexes equal to point or any index out of bound, then continue
			if (x == point_x and y == point_y) or x <0 or y < 0 or x > width or y > heigth:
				continue
			
			yield cells[y][x]		

def count_mines_around_point(point, cells):
	"""
		to count the mines around a point
	"""
	return sum(cell.is_mine() for cell in cells_around_point(point, cells))
