# minerva.py
# Calvin Pelletier
# 1/24/16

# create 1000 random melodies
# save selected as my_song
# define best as 10-15-15-40-x
# select best from set
# load my_song
# play
# show text
# show music
# show characteristics
# analyze selected
# mutate 1000 times

import melody
import i_o
import analysis
import music21
import os
import sys

cur_select = None
cur_set = None
target = None

def run():
    while True:
        command = raw_input("Enter command: ").split(" ")
        try:
            if command[0] == "create":
                create(command)
            elif command[0] == "save":
                save(command)
            elif command[0] == "define":
                define(command)
            elif command[0] == "select":
                select(command)
            elif command[0] == "load":
                load(command)
            elif command[0] == "play":
                play(command)
            elif command[0] == "show":
                show(command)
            elif command[0] == "mutate":
                mutate(command)
            elif command[0] == "quit":
                break
            else:
                print("Unidentified command.")
        except:
            print("Unexpected error:")
            print(sys.exc_info()[0])

def create(command):
    global cur_set
    cur_set = melody.create_random_melodies(int(command[1]), 'none')
    for m in cur_set:
        m.calculate_characteristics()

def store(command):
    store[command[3]] = cur_select

def save(command):
    i_o.save_melody(cur_select, command[3])

def define(command):
    global target
    target = melody.Melody()
    nums = command[3].split('-')
    for i in range(len(nums)):
        if nums[i] == 'x':
            nums[i] = None
        else:
            nums[i] = float(nums[i])
    target.energy = nums[0]
    target.progression_dissonance = nums[1]
    target.key_dissonance = nums[2]
    target.rhythmic = nums[3]
    target.rhythmically_thematic = nums[4]

def select(command):
    global cur_select
    if cur_select is None:
        best = cur_set[0]
    else:
        best = cur_select
    for m in cur_set:
        if m.distance_to_target(target) < best.distance_to_target(target):
            best = m
    cur_select = best

def load(command):
    global cur_select
    cur_select = i_o.melody_from_txt_file(os.path.join(sys.path[0], "generated-songs", command[1]))
    cur_select.calculate_characteristics()

def play(command):
    m = cur_select.get_music21()
    song = music21.stream.Score()
    song.insert(m)
    song.insert(cur_select.chord_progression.get_music21(cur_select.duration()))
    song.show('midi')

def show(command):
    if command[1] == 'text':
        print(str(cur_select))
    elif command[1] == 'music':
        m = cur_select.get_music21()
        song = music21.stream.Score()
        song.insert(m)
        song.insert(cur_select.chord_progression.get_music21(cur_select.duration()))
        song.show()
    elif command[1] == 'characteristics':
        cur_select.print_characteristics()

def analyze(command):
    analysis.analyze_characteristics(cur_set)

def mutate(command):
    global cur_set
    cur_set = []
    for i in range(int(command[1])):
        temp = cur_select.mutate()
        temp.calculate_characteristics()
        cur_set.append(temp)
