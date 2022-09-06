import json, io
from dataclasses import dataclass
from math import lgamma
from operator import le
import pandas as pd

#the name chrods is a joke name. i know how to spell chords.

chr = pd.read_csv("chorddict.csv")


@dataclass
class Fret():
    enable: bool
    number: int

@dataclass
class Shape:
    LowE: Fret
    LowA: Fret
    LowD: Fret
    LowG: Fret
    HighB: Fret
    HighE: Fret


@dataclass
class Chord:
    name: str
    shape: Shape


chordlist = {}

las = None

for chsn in chr.iterrows():
    chs = chsn[1]
    le = Fret(False if chs[1] == 1 else True, int(chs[7]))
    la = Fret(False if chs[2] == 1 else True, int(chs[8]))
    ld = Fret(False if chs[3] == 1 else True, int(chs[9]))
    lg = Fret(False if chs[4] == 1 else True, int(chs[10]))
    hb = Fret(False if chs[5] == 1 else True, int(chs[11]))
    he = Fret(False if chs[6] == 1 else True, int(chs[12]))
    sh = Shape(le,la,ld,lg,hb,he)
    ch = Chord(chs[0], sh)
    if any(chs[0] == bruh for bruh in chordlist):
        pass
    else:
        chordlist[chs[0]] = []
    chordlist[chs[0]].append(ch)


def chToTxt(chord):
    ends = []
    ends.append(["X", "X", "X", "X", "X", "X"])
    ends.append(["E", "A", "D", "G", "B", "E"])
    ends.append(["|", "|", "|", "|", "|", "|"])
    ends.append(["|", "|", "|", "|", "|", "|"])
    ends.append(["|", "|", "|", "|", "|", "|"])
    ends.append(["|", "|", "|", "|", "|", "|"])
    ends.append(["|", "|", "|", "|", "|", "|"])
    ends.append(["|", "|", "|", "|", "|", "|"])
    ends.append(["|", "|", "|", "|", "|", "|"])
    ends.append(["|", "|", "|", "|", "|", "|"])
    ends.append(["|", "|", "|", "|", "|", "|"])


    offs = 2

    lowest = 99

    for x in [chord.shape.LowE, chord.shape.LowA, chord.shape.LowD, chord.shape.LowG, chord.shape.HighB, chord.shape.HighE]:
        if x.number > 1 and x.number < lowest:
            lowest = x.number
    
    if lowest == 99:
        lowest = ""
    
    #ends[offs] += " " + str(lowest)

    
    j = [chord.shape.LowE, chord.shape.LowA, chord.shape.LowD, chord.shape.LowG, chord.shape.HighB, chord.shape.HighE]
    k = ["E", "A", "D", "G", "B", 'e']

    for x in range(6):
        if j[x].number == 0 and j[x].enable == True:
            ends[1][x] = k[x]
            ends[0][x] = "O"
            continue
        if j[x].enable == False:
            ends[1 + j[x].number][x] = "|"
        else:
            ends[1 + j[x].number][x] = str(j[x].number)
            ends[0][x] = "v"
        ends[1][x] = k[x]
    
    return ends


def chLtoS(cl):
    testp = chToTxt(cl)
    xz = ""
    for x in testp:
        xz += " ".join(x) + "\r\n"
    xz += "      " + cl.name + "\r\n"
    return xz

def makeSafe(ins):
    ins = ins.replace("Eb", "D#")
    ins = ins.replace("Bb", "A#")
    ins = ins.replace("Db", "C#")
    ins = ins.replace("Gb", "F#")
    ins = ins.replace("Ab", "G#")
    return ins
