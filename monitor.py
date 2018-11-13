#!/usr/bin/python
import curses
from curses import wrapper
import os
import psutil

def main(stdscr):
    heigh = 20; width = 80
    pad_x = 2; pad_y = 3
    stdscr = curses.initscr()
    curses.start_color()
    curses.init_pair(1, 2, 7)
    curses.init_pair(2, 6, 7)
    curses.init_pair(3, 3, 7)
    curses.init_pair(4, 1, 7)
    curses.init_pair(5, 0, 7)

    win = curses.newwin(heigh, width)
    win.keypad(True)
    win.nodelay(1)
    curses.noecho()
    #pFltPad = curses.newpad(100, 100) # container to show the page faults

    key = curses.KEY_RIGHT
    msg='Teste'

    pFltInit = 1 # page fault list init to be shown
    """--  Main Loop  --"""
    while key != 27:
        win.addstr(int(heigh/2), 3, msg)
        prevKey = key # Previous key pressed
        win.addstr(0, 40, 'Pressione Esc para sair')
        win.addstr(1, 40, 'Pressione as teclas ↑ ou ↓ para navergar')

        """---   Collecting Memory info   ---"""
        mem = psutil.virtual_memory()
        win.addstr(18, 0, 'Memory Usage: ' + str(mem.percent) + '%')
        for x in range(50):
            win.addstr(19,2+x,' ', curses.color_pair(1))
        for x in range(int(mem.percent/2)):
            win.addstr(19,2+x,'█', curses.color_pair(1+int(mem.percent/25)))

        """------       Collecting Page fault data      ------"""
        f = os.popen('ps -eo pid,min_flt,maj_flt,cmd')
        table = f.read()
        lines = table.split(sep='\n')
        win.addstr(0, 3, lines[0])
        win.addstr(1, 3, lines[pFltInit], curses.color_pair(5))
        for i in range(2,heigh-4):
            win.addstr(i, 3, lines[i + pFltInit])

        """---   Getting the user input   ---"""
        event = win.getch()
        key = key if event == -1 else event

        if key == curses.KEY_DOWN:
            pFltInit = min(pFltInit + 1, 100)
            key = prevKey
        elif key == curses.KEY_UP:
            pFltInit = max(pFltInit - 1, 1)
            key = prevKey

    win.keypad(False)
    curses.echo()
    curses.endwin()

wrapper(main)