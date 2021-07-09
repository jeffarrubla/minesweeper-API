# Minesweeper API

A minesweeper API built with Python.

## Requirements in the requirements.txt
- Django
- Djangorestframework

## Considerations

- Use a list of list to create the minefield.
- Each element of the list should be a object Cell
- Each Cell has attributes visible (true or false), value (number of mines around it or mine value) or flagged (true or false) and methods is_mine, set_flag and set_visible
- There should be 2 methods for the API **start game** and **show contents** or flag cell.
- If a game hasn't started and **shows contents** is called then it should returns and error.
- **start game** has mandatory widht, height and number of mines they all have to be positive integers.
- **show contents** has mandatory x, y, the parameter flag is optional and can be true or false. If cell mine display all the field, let the user he lost and return the total of time (hours, minutes and seconds). If he's flagging a cell mark it as flag, or he's just "clicking" on a cell, display its contents, if not mine, display adjacents cells that are not mines (do this with recursion). if all the cells are displayed and the remained are mines display user as winner, returns board, with time and message.

## Routes

- **start game**: api/minesweeper/start-game
- **shows contents**: api/minesweeper/show-or-flag-cell-contents-at-point

## Tests
- Start game (17 tests)
```python manage.py test minesweeper.tests.StartGameTest ```
- shows contents (10 tests)
```python manage.py test minesweeper.tests.ShowOrFlagCellContentsAtPointTest```
