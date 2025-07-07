"""
File: babygraphics.py
Name: Meg
--------------------------------
SC101 Baby Names Project
Adapted from Nick Parlante's Baby Names assignment by
Jerry Liao.
"""

import tkinter
import babynames
import babygraphicsgui as gui

FILENAMES = [
    'data/full/baby-1900.txt', 'data/full/baby-1910.txt',
    'data/full/baby-1920.txt', 'data/full/baby-1930.txt',
    'data/full/baby-1940.txt', 'data/full/baby-1950.txt',
    'data/full/baby-1960.txt', 'data/full/baby-1970.txt',
    'data/full/baby-1980.txt', 'data/full/baby-1990.txt',
    'data/full/baby-2000.txt', 'data/full/baby-2010.txt',
    'data/full/baby-2020.txt'
]
CANVAS_WIDTH = 1080
CANVAS_HEIGHT = 600
YEARS = [1900, 1910, 1920, 1930, 1940, 1950,
         1960, 1970, 1980, 1990, 2000, 2010, 2020]
GRAPH_MARGIN_SIZE = 20
COLORS = ['red', 'purple', 'green', 'blue']
TEXT_DX = 2
LINE_WIDTH = 2
MAX_RANK = 1000


def get_x_coordinate(width, year_index):
    """
    Given the width of the canvas and the index of the current year
    in the YEARS list, returns the x coordinate of the vertical
    line associated with that year.

    Input:
        width (int): The width of the canvas
        year_index (int): The index where the current year is in the YEARS list
    Returns:
        x_coordinate (int): The x coordinate of the vertical line associated
                            with the current year.
    """
    space = (width-GRAPH_MARGIN_SIZE*2)/len(YEARS)     # The space between 2 lines
    x = GRAPH_MARGIN_SIZE + space*year_index
    return x


def draw_fixed_lines(canvas):
    """
    Draws the fixed background lines on the canvas.

    Input:
        canvas (Tkinter Canvas): The canvas on which we are drawing.
    """
    canvas.delete('all')            # delete all existing lines from the canvas

    # ----- Write your code below this line ----- #

    canvas.create_line(GRAPH_MARGIN_SIZE, GRAPH_MARGIN_SIZE, (CANVAS_WIDTH - GRAPH_MARGIN_SIZE), GRAPH_MARGIN_SIZE, width=LINE_WIDTH, fill='black')
    canvas.create_line(GRAPH_MARGIN_SIZE, (CANVAS_HEIGHT-GRAPH_MARGIN_SIZE), (CANVAS_WIDTH - GRAPH_MARGIN_SIZE), (CANVAS_HEIGHT-GRAPH_MARGIN_SIZE), width=LINE_WIDTH, fill='black')
    for i in range(len(YEARS)):
        year_index = i
        x = get_x_coordinate(CANVAS_WIDTH, year_index)
        canvas.create_line(x, 0, x, CANVAS_HEIGHT, width=LINE_WIDTH, fill='black')
        canvas.create_text(x+TEXT_DX, CANVAS_HEIGHT-GRAPH_MARGIN_SIZE, text=YEARS[year_index], anchor=tkinter.NW)


def draw_names(canvas, name_data, lookup_names):
    """
    Given a dict of baby name data and a list of name, plots
    the historical trend of those names onto the canvas.

    Input:
        canvas (Tkinter Canvas): The canvas on which we are drawing.
        name_data (dict): Dictionary holding baby name data
        lookup_names (List[str]): A list of names whose data you want to plot

    Returns:
        This function does not return any value.
    """
    draw_fixed_lines(canvas)        # draw the fixed background grid

    # ----- Write your code below this line ----- #
    for i in range(len(lookup_names)):
        search_name = lookup_names[i]
        if i <= len(COLORS)-1:
            color = COLORS[i]
        elif i % 4 == 0:
            color = COLORS[0]
        elif i % 4 == 1:
            color = COLORS[1]
        elif i % 4 == 2:
            color = COLORS[2]
        else:
            color = COLORS[3]
        one_name_data = {}                                          # One name with all its data
        if search_name in name_data:
            one_name_data[search_name] = name_data[search_name]     # ex. one_name_data  = {'Kylie': {'2010': '57', '2000': '104'}}
            information = one_name_data[search_name]                # information(dict), ex information = {'2010': '57', '2000': '104'}
            for j in range(len(YEARS)):
                search_year = YEARS[j]
                if str(search_year) not in information:
                    information[str(search_year)] = '*'             # information(dict), ex information = {'2010': '57', '2000': '104', '1900': '*'}
            num = 0
            for year, rank in sorted(information.items()):          # ex. [('1900': '*'), ... ('2000', '104'), ('2010', '57')...]
                if num < len(sorted(information.items()))-1:
                    year_index_1 = num
                    year_index_2 = num + 1
                    x_position_1 = get_x_coordinate(CANVAS_WIDTH, year_index_1)
                    if (year, rank)[1] is '*':
                        y_position_1 = CANVAS_HEIGHT-GRAPH_MARGIN_SIZE
                    else:
                        y_position_1 = GRAPH_MARGIN_SIZE + (CANVAS_HEIGHT-GRAPH_MARGIN_SIZE*2)/MAX_RANK*int((year, rank)[1])
                    x_position_2 = get_x_coordinate(CANVAS_WIDTH, year_index_2)
                    if (sorted(information.items())[num + 1])[1] is '*':
                        y_position_2 = CANVAS_HEIGHT-GRAPH_MARGIN_SIZE
                    else:
                        y_position_2 = GRAPH_MARGIN_SIZE + (CANVAS_HEIGHT-GRAPH_MARGIN_SIZE*2)/MAX_RANK*int((sorted(information.items())[num + 1])[1])
                    canvas.create_line(x_position_1, y_position_1, x_position_2, y_position_2, width=LINE_WIDTH, fill=color)
                    canvas.create_text(x_position_1 + TEXT_DX, y_position_1, text=f"{lookup_names[i]} {(year, rank)[1]}", anchor=tkinter.SW, fill=color)
                    num += 1
                else:
                    if (year, rank)[1] is '*':
                        y_position = CANVAS_HEIGHT - GRAPH_MARGIN_SIZE
                    else:
                        y_position = GRAPH_MARGIN_SIZE + (CANVAS_HEIGHT-GRAPH_MARGIN_SIZE*2)/MAX_RANK*int((year, rank)[1])
                    canvas.create_text(CANVAS_WIDTH - GRAPH_MARGIN_SIZE - ((CANVAS_WIDTH - GRAPH_MARGIN_SIZE * 2) / len(YEARS)) + TEXT_DX, y_position, text=f"{lookup_names[i]} {(year, rank)[1]}", anchor=tkinter.SW, fill=color)


# main() code is provided, feel free to read through it but DO NOT MODIFY
def main():
    # Load data
    name_data = babynames.read_files(FILENAMES)

    # Create the window and the canvas
    top = tkinter.Tk()
    top.wm_title('Baby Names')
    canvas = gui.make_gui(top, CANVAS_WIDTH, CANVAS_HEIGHT, name_data, draw_names, babynames.search_names)

    # Call draw_fixed_lines() once at startup so we have the lines
    # even before the user types anything.
    draw_fixed_lines(canvas)

    # This line starts the graphical loop that is responsible for
    # processing user interactions and plotting data
    top.mainloop()


if __name__ == '__main__':
    main()
