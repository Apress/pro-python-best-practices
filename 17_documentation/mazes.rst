Maze Generation
===============

Creating a maze from scratch
----------------------------

Use the ``generate_maze`` module:

.. doctest::

    >>> from maze_run.generate_maze import create_grid_string
    >>> dots = [(1,1), (1, 2), (2,2), (2,3), (3,3)]
    >>> maze = create_grid_string(dots, 5, 5)
    >>> print(maze.strip())
    #####
    #.###
    #..##
    ##..#
    #####


This is $\sum_i^n{MAAAATH}!$

.. todo::

    include output for doctest

.. ifconfig:: eggs > 900

    Hello hidden easter eggs!


.. autofunction:: maze_run.generate_maze.create_maze

Whole modules can be discovered this way:

draw_map module
+++++++++++++++

.. automodule:: maze_run.draw_maze
   :members:


