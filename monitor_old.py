#!/usr/bin/python
import curses
from curses import wrapper
import time
import os

def main(stdscr):
    height = 20; width = 40
    begin_x = 0; begin_y = 0
    pad_x = 2; pad_y = 3
    
    stdscr = curses.initscr()
    curses.start_color()
    if curses.has_colors() == False:
        curses.endwin()
        print('Terminal não tem suporte a cor\n')
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_WHITE)
    win = curses.newwin(height, width, begin_y, begin_x)
    curses.noecho()
    curses.cbreak()
    stdscr.keypad(True)

    pFltPad = curses.newpad(100, 100)
    key = curses.KEY_RIGHT

    while key != 27:
        prevKey = key
        event = win.getch()
        key = key if event == -1 else event

        """------       Collecting Page fault data      ------"""
        f = os.popen('ps -eo min_flt,maj_flt,cmd')
        table = f.read()
        lines = table.split(sep='\n')
        for i, line in enumerate(lines):
            pFltPad.addstr(pad_y+i, pad_x, line, curses.color_pair(1))
            #cells = line.split()
            #print(cells)
        """---------------------------------------------------------------"""

        #pad.refresh(0,0,5,5,20,75)
        #pad=curses.newpad(100,100)
        pFltPad.refresh(0,0,pad_x,pad_x,height-1,width-1)
        #pad.addstr(0,0, "RED ALERT!", curses.color_pair(1))
        #time.sleep(2)

    
    #time.sleep(3)

    curses.nocbreak()
    stdscr.keypad(False)
    curses.echo()

    curses.endwin()

wrapper(main)

