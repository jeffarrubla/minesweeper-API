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

			yield Point(x,y)

def count_mines_around_point(point, cells):
	"""
		to count the mines around a point
	"""
	return sum(cells[p.y][p.x].is_mine() for p in cells_around_point(point, cells))

def show_contents_at_point(point, cells):
	"""
		to show the content of the cells
	"""
	point_x, point_y = point
	# is flagged, or visible or is a mine? then return, otherwise show and iterate through next points
	if cells[point_y][point_x].flagged or cells[point_y][point_x].visible or cells[point_y][point_x].is_mine():
		return
	cells[point_y][point_x].set_visible()
	if cells[point_y][point_x].value == 0:
		for p in cells_around_point(point, cells):	
			show_contents_at_point(p, cells)

def all_cells_diplayed(cells):
	"""
		Used to know if all cells are displayed and the mines don't
		Returns boolean
	"""
	el = []
	for row in cells:
		for cell in row:
			el.append(cell.is_mine() or cell.visible)
	return all(el)

def show_contents_all_cells(cells):
	"""
		Used to display all cells (when user lost)
		Returns the cells
	"""
	for y in range(len(cells)):
		for x in range(len(cells[0])):
			cells[y][x].set_visible()

	return cells