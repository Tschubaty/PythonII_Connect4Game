import Connect4Game
import DanielBatyrev2AI as DanielAI
import copy
import func_timeout
import matplotlib.pyplot as plt
import YosefBirnbaumAI
import ShmulyStudentAI
import shmueflugAI
import MordechaiSingerAI
import BasyaRosenthalAI

competitor_list = [BasyaRosenthalAI.BasyaRosenthalAI(),MordechaiSingerAI.MinimaxStrategy()]

MAX_WAIT_TIME = 1
winners = list()
random_choice = DanielAI.RandomStrategy2()

for game_nr in range(100):
    print(game_nr + 1)
    tie = False
    game = Connect4Game.Connect4Game()
    while game.winner is None:
        game_safety_copy = copy.deepcopy(game)
        try:
            move = func_timeout.func_timeout(
                MAX_WAIT_TIME, competitor_list[game.current_player - 1].strategy, [game_safety_copy])
        except func_timeout.FunctionTimedOut:
            print(f'time out limit exceeded: {competitor_list[game.current_player - 1].name} performs random move')
            move = random_choice.strategy(game_safety_copy)
        game.make_move(move)
        if 0 == sum(map(game.is_valid_move, range(7))):
            tie = True
            break
    if tie:
        winners.append("tie")
    else:
        winners.append(competitor_list[game.current_player - 1].name)
    competitor_list.reverse()

dictionary = {}
for item in winners:
    dictionary[item] = dictionary.get(item, 0) + 1

print(dictionary)

plt.figure(figsize=(8, 6))
plt.bar(dictionary.keys(), dictionary.values(), color=['blue', 'green', 'red'])
plt.title("Connect 4 Results Analysis", fontsize=16)
plt.xlabel("Result", fontsize=14)
plt.ylabel("Number of Wins", fontsize=14)
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)
for i, value in enumerate(dictionary.values()):
    plt.text(i, value + 5, str(value), ha='center', fontsize=12)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.show()