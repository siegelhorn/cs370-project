import random

from TerrainMap import TerrainMap
from Moves import Moves
from Directions import Directions
from Point import Point
from State import State
from time import time, sleep
from FileOut import FileOut
from ScoreMap import ScoreMap
from random import randint
from Professor_SharedMemory import Professor_SharedMemory

FILE_OUT = False

def generate_move():
    choice = int(random.uniform(1,5))
    return Moves(choice)

def generate_random_valid_move(terrain_map, prof):
    rand_move = generate_move()
    while not prof.is_valid_move(rand_move):
        rand_move = generate_move()
    return rand_move

def get_smart_move(score_map, possible_states):
    # UNTESTED
    move_counts = {}
    move_counts[Moves.FORWARD]  = 0
    move_counts[Moves.BACKWARD] = 0
    move_counts[Moves.LEFT]     = 0
    move_counts[Moves.RIGHT]    = 0

    for possible_state in possible_states:
        if score_map.get_tile(possible_state.point) is None: continue
        desired_directions = score_map.get_tile(possible_state.point).directions
        for desired_direction in desired_directions:
            desired_move = State.direction_to_move(possible_state.direction, desired_direction)
            move_counts[desired_move] += 1

    max_count = -1
    max_moves_ties = []
    for move in Moves:
        move_count = move_counts[move]
        if move_count > max_count:
            max_count = move_count
            max_moves_ties = [move]
        elif move_count == max_count:
            #tie between max_move and move
            print("********TIE********")
            max_moves_ties.append(move)
            pass

    return max_moves_ties[randint(0,len(max_moves_ties)-1)]


def primary_driver_logic(map_file_name):
    t1 = time()
    t0 = time()
    print("Creating Terrain Map")
    terrain_map = TerrainMap(map_file_name)
    # print(terrain_map)
    print('time take: {} seconds'.format(time() - t1))
    t1 = time()
    print("Creating Score Map")
    score_map = ScoreMap(terrain_map)
    print('time take: {} seconds'.format(time() - t1))
    t1 = time()
    print("Creating Prof")
    prof = Professor_SharedMemory(terrain_map)
    print('time take: {} seconds'.format(time() - t1))
    t1 = time()
    print("====STARTING PLACE====")
    print(prof)

    # possible_states = terrain_map.get_all_traversable_states()
    print("Generating Initial possible_states")
    possible_states = prof.get_all_possible_states(4)
    print('time take: {} seconds'.format(time() - t1))
    t1 = time()
    print("Starting Amount of possible_states: ",len(possible_states))

    i = 0
    print_once = False

    print("===Starting Primary Loop===")
    while prof.state.point.y < terrain_map.height - 1:
        current_surroundings = prof.get_surroundings()
        next_possible_states = []
        t1 = time()
        print("Narrowing States")
        for possible_state in possible_states:
            if prof.is_possible_state(possible_state,current_surroundings):
                next_possible_states.append(possible_state)

        print('time take: {} seconds'.format(time() - t1))
        possible_states = next_possible_states
        if len(possible_states) > 1:
            if FILE_OUT:
                FileOut.to_png(terrain_map=terrain_map,possible_states=possible_states,professor=prof,file_name="steps/step" + str(i))
            i += 1

        print("Num possible states: ",len(possible_states))
        # Now possible states have been trimmed down
        if len(possible_states) <= 1 and not print_once:
            print("++++++++++++++++++++++++++++++++++FOUND PROF++++++++++++++++++++++++++++++++++")
            print(score_map.get_tile(prof.state.point).score)
            print_once = True

        print(prof)
        print("isTraversible() ",terrain_map.get_tile(prof.state.point).is_traversable())

        print("Getting Smart Move")
        t1 = time()
        move = get_smart_move(score_map, possible_states)
        print('time take: {} seconds'.format(time() - t1))
        t1 = time()
        print("Got Smart Move")

        # move = generate_random_valid_move(terrain_map, prof)

        print(move)
        prof.move(move)

        print("Moving All possible_states")
        for possible_state in possible_states:
            possible_state.move(move)

        if FILE_OUT:
            FileOut.to_png(terrain_map=terrain_map,possible_states=possible_states,professor=prof,file_name="steps/step" + str(i))

        i += 1
        if i > terrain_map.height * 1.25:
            print("NOT DONE YET BUT SAVING ISAAC'S SSD")
            break

    print("\n\n====RESTING PLACE===")
    print(prof)

    print("FOUND_PROF")
    t2 = time()
    print('total time take: {} seconds'.format(t2 - t0))
    return t2-t0

# primary_driver_logic()
