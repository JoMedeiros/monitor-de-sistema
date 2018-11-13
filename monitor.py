#!/usr/bin/python
import curses
from curses import wrapper
import os
import psutil

def main(stdscr):
    heigh = 20; width = 80
    pad_x = 2; pad_y = 3
    stdscr = curses.initscr()
    win = curses.newwin(heigh, width)
    win.keypad(True)
    win.nodelay(1)
    curses.noecho()
    #pFltPad = curses.newpad(100, 100) # container to show the page faults

    key = curses.KEY_RIGHT
    msg='Teste'

    pFltInit = 0
    """--  Main Loop  --"""
    while key != 27:
        win.addstr(int(heigh/2), 3, msg)
        prevKey = key # Previous key pressed
        win.addstr(0, 0, 'Pressione Esc para sair')
        win.addstr(1, 0, 'Pressione as teclas ↑ ou ↓ para navergar')

        """---   Collecting Memory info   ---"""
        mem = psutil.virtual_memory()
        win.addstr(2, 0, 'Memory Usage: ' + str(mem.percent) + '%')
        for x in range(int(mem.percent/2)):
            win.addch(3,2+x,'#')

        """------       Collecting Page fault data      ------"""
        f = os.popen('ps -eo min_flt,maj_flt,cmd')
        table = f.read()
        lines = table.split(sep='\n')
        win.addstr(5, 3, lines[0])
        for i in range(1,heigh-6):
            win.addstr(5+i, 3, lines[i + pFltInit])

        """---   Getting the user input   ---"""
        event = win.getch()
        key = key if event == -1 else event

        if key == curses.KEY_DOWN:
            pFltInit = min(pFltInit + 1, 30)
            key = prevKey
        elif key == curses.KEY_UP:
            pFltInit = max(pFltInit - 1, 0)
            key = prevKey

    win.keypad(False)
    curses.echo()
    curses.endwin()

wrapper(main)