#!/usr/bin/python
import curses
from curses import wrapper
import os
import psutil

def main(stdscr):
    heigh = 22; width = 80
    pad_x = 2; pad_y = 3
    stdscr = curses.initscr()
    curses.start_color()
    curses.init_pair(1, 2, 7)
    curses.init_pair(2, 7, 6)
    curses.init_pair(3, 7, 3)
    curses.init_pair(4, 7, 1)
    curses.init_pair(5, 0, 7)

    win = curses.newwin(heigh, width)
    win.keypad(True)
    win.nodelay(1)
    curses.noecho()
    #pFltPad = curses.newpad(100, 100) # container to show the page faults

    key = curses.KEY_RIGHT
    ord_by = 'pid'
    fields = 'pid,%mem,min_flt,maj_flt,comm,%cpu'
    f = os.popen('ps -eo '+fields)
    pFltInit = 1 # page fault list init to be shown
    """--  Main Loop  --"""
    while key != 27:
        prevKey = key # Previous key pressed
        win.addstr(0, 40, 'Teclas:')
        win.addstr(1, 40, 'UP/DOWN - navegar\tEsc - Sair')
        win.addstr(2, 40, 'm - ordena por uso de memoria')
        win.addstr(3, 40, 'c - ordena por uso de cpu')

        """---   Collecting Memory info   ---"""
        mem = psutil.virtual_memory()
        win.addstr(18, 0, 'Memory Usage: ' + str(mem.percent) + '%')
        for x in range(50):
            win.addstr(19,2+x,' ', curses.color_pair(1))
        for x in range(int(mem.percent/2)):
            win.addstr(19,2+x,' ', curses.color_pair(1+int(mem.percent/25)))
        win.addstr(18, 22, 'Cache: ' + str(mem.cached).rjust(10))

        """---   Collecting swap info   ---"""
        swp = psutil.swap_memory()
        win.addstr(20, 0, 'Swap Usage: ' + str(swp.percent) + '%')
        win.addstr(20, 22, 'Tamanho do Swap: ' + str(swp.total/1000000)[:3] + 'GB')
        for x in range(50):
            win.addstr(21,2+x,' ', curses.color_pair(1))
        for x in range(int(swp.percent/2)):
            win.addstr(21,2+x,' ', curses.color_pair(1+int(swp.percent/25)))
        
        """------       Collecting Processes Data      ------"""
        if ord_by == 'mem':
            f = os.popen('ps -eo '+fields+' --sort -rss')
        elif ord_by == 'cpu':
            f = os.popen('ps -eo '+fields+' --sort -pcpu')       
        else:
            f = os.popen('ps -eo '+fields)
        table = f.read()
        lines = table.split('\n')
        win.addstr(0, 0, lines[0].split()[0].rjust(6))# PID label
        win.addstr(0, 6, 'comando'.rjust(16))# PID label
        if ord_by == 'mem':
            win.addstr(0, 22, '% Memoria'.rjust(10))
        # selected process (highlighted)
        win.addstr(1, 0, lines[pFltInit].split()[0].rjust(6), curses.color_pair(5))
        win.addstr(1, 7, lines[pFltInit].split()[4].rjust(15), curses.color_pair(5))
        if ord_by == 'mem':
            win.addstr(1, 25, lines[pFltInit].split()[1].rjust(6), curses.color_pair(5))
        elif ord_by == 'cpu':
            win.addstr(1, 25, lines[pFltInit].split()[-1].rjust(6), curses.color_pair(5))
        # others
        for i in range(1,16):
            l = lines[i + pFltInit].split()
            win.addstr(i+1, 0, l[0].rjust(6))
            win.addstr(i+1, 7, l[4].rjust(15))
            if ord_by == 'mem':
                win.addstr(i+1, 25, l[1].rjust(6))
            elif ord_by == 'cpu':
                win.addstr(i+1, 25, l[-1].rjust(6))
        

        """- Selected Process information -"""
        ff = os.popen('ps -p ' + lines[pFltInit].split()[0] + ' -eo pid,min_flt,maj_flt')
        sel = ff.read()
        win.addstr(5, 40, 'Process ID: ' + lines[pFltInit].split()[0].rjust(6))
        win.addstr(6, 40, 'Uso de memoria:    ' + lines[pFltInit].split()[1].rjust(8) + '%')
        win.addstr(7, 40, 'minor page faults: ' + lines[pFltInit].split()[2].rjust(8))
        win.addstr(8, 40, 'major page faults: ' + lines[pFltInit].split()[3].rjust(8))


        """---   Getting the user input   ---"""
        event = win.getch()
        key = key if event == -1 else event

        if key == curses.KEY_DOWN:
            pFltInit = min(pFltInit + 1, 100)
            key = prevKey
        elif key == curses.KEY_UP:
            pFltInit = max(pFltInit - 1, 1)
            key = prevKey
        elif key == 109 or key == 77:
            ord_by = 'mem'
        elif key == 67 or key == 99:
            ord_by = 'cpu'


    win.keypad(False)
    curses.echo()
    curses.endwin()

wrapper(main)