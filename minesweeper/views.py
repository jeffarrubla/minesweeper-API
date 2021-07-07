from django.shortcuts import render

# Create your views here.

VALUE_MINE = '*' 

class Cell:
	"""
		Individual cell of the minefield

		When created it's not flagged and not visible.
	"""

	def __init__(self, value=0, flagged=False, visible=False):
		self._value = value
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