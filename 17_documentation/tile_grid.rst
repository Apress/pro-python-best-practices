The Maze Generator
------------------

The module ``maze_run.generate_maze`` is responsible for generating mazes. It creates a **two-dimensional list** with a *fixed size* that can be used to create a graphical representation in Pygame.

The maze consists of corridors represented by dots and walls represented by hashes. The algorithm leaves a circular path close to the border. 

Using the ``generate_maze`` module:

.. doctest::

    >>> from maze_run.generate_maze import create_maze
    >>> import random
    >>> random.seed(0)
    >>> maze = create_maze(14, 7)
    >>> print(maze.strip())
    ##############
    #............#
    #.#.#..#.###.#
    #.#...##.#...#
    #...#....#..##
    #.#....#.....#
    ##############
    >>> len(maze)
    105


Example of a failing doctest
++++++++++++++++++++++++++++

.. doctest::

   >>> 1 + 2
   2

Example of TODO entries
+++++++++++++++++++++++

.. todo::

   Adding caching to the TileGrid class could accelerate graphics a lot.

.. todo::

   Describe how to connect a moving element to a TileGrid.
