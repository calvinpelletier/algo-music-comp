# minerva.py
# Calvin Pelletier
# 1/24/16

import melody
import i_o
import analysis
import music21
import os
import sys
#import song

def run():
    while True:
        command = raw_input("Enter command: ")
        #try:
        if command == "analyze characteristics":
            analyze_characteristics()
        elif command == "analyze examples":
            analyze_examples()
        elif command == "genetic":
            genetic()
        elif command == "quit":
            break
        elif command == "load":
            load()
        else:
            print("Unidentified command.")
        #except:
        #    print("Unexpected error:")
        #    print(sys.exc_info())

def analyze_characteristics():
    n = int(raw_input("Of how many random melodies?: "))
    melodies = melody.create_random_melodies(n)
    analysis.analyze_characteristics(melodies)

def analyze_examples():
    melodies = i_o.melodies_from_sample_folder()
    for m in melodies:
        m.calculate_characteristics()
        m.print_characteristics()
        print("")

def genetic():
    target = set_target()
    generations = int(raw_input("Generations?: "))
    offspring = int(raw_input("Offspring?: "))
    result = melody.genetic_algorithm(target, None, generations, offspring)
    result.print_characteristics()
    while True:
        command = raw_input("Done. Now what?: ")
        if command == "play":
            play(result)
        elif command == "quit":
            print("Going back to menu...")
            break
        elif command == "set generations":
            generations = int(raw_input("Generations?: "))
        elif command == "set offspring":
            offspring = int(raw_input("Offspring?: "))
        elif command == "set target":
            target = set_target()
        elif command == "save":
            name = raw_input("Name?: ")
            save(result, name)
        elif command == "show":
            show(result)
        elif command == "repeat":
            result = melody.genetic_algorithm(target, result, generations, offspring)
            result.print_characteristics()
        elif command == "repeat fresh":
            result = melody.genetic_algorithm(target, None, generations, offspring)
            result.print_characteristics()
        else:
            print("Unidentified command.")

def load():
    filepath = raw_input("Filepath?: ")
    if filepath == "generated-songs":
        melodies = i_o.melodies_from_generated_folder()
    else:
        melodies = []
        melodies.append(i_o.melody_from_txt_file(os.path.join(sys.path[0], filepath)))
    for i, m in enumerate(melodies):
        print("~~~~~%d~~~~~" % i)
        m.calculate_characteristics()
        m.print_characteristics()
    while True:
        command = raw_input("Done. Now what?: ")
        command = command.split(' ')
        if command[0] == "play":
            play(melodies[int(command[1])])
        elif command[0] == "quit":
            print("Going back to menu...")
            break
        elif command[0] == "show":
            show(melodies[int(command[1])])
        else:
            print("Unidentified command.")

# HELPER FUNCTIONS
def set_target():
    target = melody.Target()
    for key, value in target.characteristics.iteritems():
        val = raw_input("%s?: " % key)
        if val == 'x':
            target.characteristics[key] = None
        else:
            target.characteristics[key] = [float(x) for x in val.split('-')]
    return target

def play(m):
    m.get_music21().show('midi')

def save(m, name):
    i_o.save_melody(m, name)

def show(m):
    stream = m.get_music21()
    stream.makeNotation(inPlace=True)
    stream.show()
