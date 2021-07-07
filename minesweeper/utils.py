def cells_to_str(cells):
	"""
		To format the mainsweeper as a list of list and return it.
	"""
	return [[str(cell) for cell in row] for row in cells]