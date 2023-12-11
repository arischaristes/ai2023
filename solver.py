from collections import deque
from datetime import timedelta, datetime
from math import floor, ceil, sqrt
import sys

class node:
    def __init__(self, parent, value, instruction, cost):
        self.parent      = parent
        self.value       = value
        self.instruction = instruction
        self.cost        = cost

def heuristic(current, target):
    return abs(target - current)

def search(start, target, method):

    steps = 0
    currentNode = node(None, start, "start", 0)

    queue = deque()
    append = {
        'breadth':  queue.appendleft,
        'depth':    queue.append,
        'best':     queue.appendleft,
        'astar':    queue.appendleft
    }

    node_list = []
    visited = set()
    append[method](currentNode)
    node_list.append(currentNode)

    found = False
    timeOut = False
    timer = datetime.now() + timedelta(minutes = 1)
    init_timer = datetime.now()

    while not timeOut and queue:

        if method == 'best' or method == 'astar':
            print(' '.join(str(obj.value) for obj in queue))

            currentNode = min(queue, key=lambda node: (node.cost if method == 'astar' else 0) + heuristic(node.value, target))
            queue.remove(currentNode)
            print("value: %s cost: %s"%(currentNode.value, (currentNode.cost if method == 'astar' else 0) + heuristic(currentNode.value, target)))
        else:
            currentNode = queue.pop()

        steps += 1

        if currentNode.value == target:
            found = True
            break

        if timer < datetime.now():
            timeOut = True

        if method == 'depth' or method == 'best' or method == 'astar':
            while currentNode.value in visited:
                if method == 'best' or method == 'astar':
                    currentNode = min(queue, key=lambda node: (node.cost if method == 'astar' else 0) + heuristic(node.value, target))
                    queue.remove(currentNode)
                else:
                    currentNode = queue.pop()
            visited.add(currentNode.value)

        print("current: ", currentNode.value)
        if currentNode.value < 10 ** 9:
            current_increase = node(currentNode, currentNode.value + 1, "increase", 2)
            append[method](current_increase)
            node_list.append(current_increase)
        
        if currentNode.value > 0:
            current_decrease = node(currentNode, currentNode.value - 1, "decrease", 2)
            append[method](current_decrease)
            node_list.append(current_decrease)

        if currentNode.value > 0 and currentNode.value * 2 <= 10 ** 9:
            current_double = node(currentNode, currentNode.value * 2, "double", ceil(currentNode.value / 2) + 1)
            append[method](current_double)
            node_list.append(current_double)

        if currentNode.value > 0:
            current_half = node(currentNode, floor(currentNode.value / 2), "half", ceil(currentNode.value / 4) + 1)
            append[method](current_half)
            node_list.append(current_half)

        val_square = currentNode.value ** 2
        if val_square < 10 ** 9:
            current_square = node(currentNode, currentNode.value ** 2, "square", ((val_square - currentNode.value) / 4) + 1)
            append[method](current_square)
            node_list.append(current_square)

        val_sqrt = sqrt(currentNode.value)
        if currentNode.value > 1 and val_sqrt.is_integer():
            current_sqrt = node(currentNode, int(sqrt(currentNode.value)), "root", ((currentNode.value - val_sqrt) / 4) + 1)
            append[method](current_sqrt)
            node_list.append(current_sqrt)

    timeToSolve = (datetime.now() - init_timer).total_seconds()

    results = []
    if found:
        while currentNode.parent != None:
            currentNode.value = currentNode.parent.value
            results.append(currentNode)
            currentNode = currentNode.parent
        results.reverse()
        return results, timeToSolve, steps
    else:
        return results, False, steps

def main():

    methods = ['breadth', 'depth', 'best', 'astar']

    if len(sys.argv) != 5:
        print("Something is wrong with the arguments given.\nExample usage: python(3) test.py breadth 5 18 solution.txt")
        sys.exit()
    
    method = sys.argv[1]
    try:
        start = int(sys.argv[2])
    except:
        print("Starting number must be an int")
        sys.exit()

    try:
        target = int(sys.argv[3])
        if target >= 10 ** 9:
            print("Target number cant be bigger than 10^9")
            sys.exit()
    except:
        print("Target number must be an int")
        sys.exit()

    output_file = sys.argv[4]

    if method in methods and start > 0 and target > 0 and target >= start and output_file:

        if target == start:
            print("Starting number is same as Target number")
            sys.exit()

        solution, time, steps = search(int(start), int(target), method)
        print("steps: ", steps)
        if solution:

            with open(output_file, 'w') as output:
                
                output.write('N=' + str(len(solution)) + " C=" + str(sum([instruction.cost for instruction in solution])) + "\n")
                
                for node in solution:
                    output.write(str(node.instruction) + ' ' + str(node.value) + ' ' + str(node.cost) + "\n")

            print("Found solution in", time, "seconds")
        else:
            print("No solution found in current time limit")
    else:
        print("Something is wrong with the arguments given.\nExample usage: python(3) test.py breadth 5 18 solution.txt")
        sys.exit()

if __name__ == "__main__":
    main()