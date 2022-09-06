import os, io, math
import numpy as np
import sys
import time

import argparse
import datetime

parser = argparse.ArgumentParser(description='lrc to screen.')
parser.add_argument('lrcpath', metavar='N', type=str,
                    help='filename of lrc')
parser.add_argument('wavpath', nargs="?", type=str,
                    help="wav path", default=None)

args = parser.parse_args()


lrcfile = io.open(args.lrcpath, 'r', encoding='utf-8')
lrclines = [line for line in lrcfile.read().splitlines()]


schedule = [(0, "N")]
longsummary = []
longnumbers = []
numbers = [0]
last = ""

for line in lrclines:
    ltime = line.split(" ")[0].replace("]", "").replace("[", "")
    min = int(ltime[0:2])
    sec = int(ltime[3:5])
    ms = int(ltime[-2:])
    ltime = (min * 60000) + (sec * 1000) + (ms * 10)
    longsummary.append((ltime, line.split(" ")[1]))
    longnumbers.append(ltime)
    if line.split(" ")[1] == "N":
        continue
    if not last == line.split(" ")[1]:
        last = line.split(" ")[1]
    else:
        continue
    schedule.append((ltime, line.split(" ")[1]))
    numbers.append(ltime)


from chords import chordlist, chLtoS, makeSafe, Fret, Shape, Chord



start = 0.0

def tpos():
    global start
    return float((time.time() + 0.5) * 1000) - start


if args.wavpath:
    import playsound
    playsound.playsound(args.wavpath,False)

start = float((time.time() + 0.5) * 1000)

last = None
lastex = None

from rich import print
from rich.layout import Layout
import rich
from rich.align import Align
from rich.table import Table
from rich.console import Console


layout = Layout()
print(layout)
layout.split_column(
    Layout(name="upper"),
    Layout(name="lower")
)
layout['upper'].split_row(
    Layout(name="left"),
    Layout(name="center"),
    Layout(name="right"),
)
rich.align.Align.center(layout['lower'])
print(layout)

from bisect import bisect_right, bisect_left



while True:
    try:
        index = bisect_left(numbers, tpos()) #THIS REALLY WOULD HAVE HELPED LAST TIME
        longindex = bisect_left(longnumbers, tpos())
        if numbers[index] > tpos():
            index -= 1
        if longnumbers[longindex] > tpos():
            longindex -= 1
        cl = schedule[index][1]
        cll = longindex
        if not last == cl:
            last = cl
            os.system("cls")
            prv = ""
            nxt = ""
            if index > 0:
                prv = chLtoS(chordlist[makeSafe(schedule[index - 1][1])][0])
            if index < len(schedule):
                nxt = chLtoS(chordlist[makeSafe(schedule[index + 1][1])][0])
            cn = chLtoS(chordlist[makeSafe(schedule[index][1])][0])
            lwrstrg = ""
            for i in range(longindex - 5, longindex):
                lwrstrg += longsummary[i][1] + " "
            lwrstrg += "[red]" + last + "[/red] "
            for i in range(longindex, longindex + 5):
                lwrstrg += longsummary[i][1] + " "
            prv = ("\n"*3) + prv
            cn = ("\n"*3) + cn
            nxt = ("\n"*3) + nxt
            layout['left'].update(Align.center(prv))
            layout['center'].update(Align.center(cn))
            layout['right'].update(Align.center(nxt))
            print(layout)
        if not lastex == cll:
            lastex = cll
            os.system("cls")
            tl = []
            lwrstrg = ""
            for i in range(longindex - 10, longindex):
                if i > 0:
                    lwrstrg += longsummary[i][1] + " "
                    tl.append(longsummary[i][1])
                else:
                    tl.append(" ")
            tl.append("[red]" + last + "[/red]")
            lwrstrg += "[red]" + last + "[/red] "
            for i in range(longindex + 1, longindex + 10):
                if i < len(longsummary):
                    lwrstrg += longsummary[i][1] + " "
                    tl.append(longsummary[i][1])
                else:
                    tl.append(" ")
            layout['lower'].update(Align.center("%-7s %-7s %-7s %-7s %-7s %-7s %-7s %-7s %s" % (tl[6], tl[7], tl[8], tl[9], tl[10], tl[11],tl[12], tl[13], tl[14] )))
            print(layout)
        sys.stdout.flush()
    except KeyboardInterrupt as e:
        sys.exit(0)
    except:
        pass
