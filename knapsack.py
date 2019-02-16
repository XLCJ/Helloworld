from __future__ import division
import time
import re
import sys
import threading

# Dynamic programming to solve the knapsack problem


def knapsack_topdown(items, knapsack_size):
    # recursive top down approach, solve subproblems as needed
    N = len(items)
    mem_dict = dict()

    def recursion(i, w):
        if i < 0:
            return 0
        if w <= 0:
            return 0
        if (i, w) in mem_dict:
            return mem_dict[(i, w)]

        value, weight = items[i]
        if i == 0 and w >= weight:
            maxvalue = value
        elif i == 0 and w < weight:
            maxvalue = 0
        else:
            rec_a = recursion(i - 1, w)
            if (i - 1, w) not in mem_dict:
                mem_dict[(i - 1, w)] = rec_a
            if w >= weight:
                rec_b = recursion(i - 1, w - weight)
                if (i - 1, w - weight) not in mem_dict:
                    mem_dict[(i - 1, w - weight)] = rec_b
                maxvalue = max(rec_a, rec_b + value)
            else:
                maxvalue = rec_a

        mem_dict[(i, w)] = maxvalue
        return maxvalue

    return recursion(N - 1, knapsack_size)


def knapsack_bottomup(items, knapsack_size):
    # bottom-up approach of saving all the subproblems in cache
    # if just want the optimal value, not the specific optimal items selected, can use just two columns
    # because all we care is the one iteration before
    # knapsack_size is an integer
    # Problem is we computed many w that won't be used. It takes large amount of time and space
    best_i1 = dict()
    best_i2 = dict()
    N_items = len(items)

    for i, item in enumerate(items):
        # print(i)
        # print(item)
        if i > 1:
            # best_i1 = dict()
            best_i1 = best_i2.copy()
        for w in range(1, knapsack_size + 1):
            value, weight = item
            if i == 0:
                if weight <= w:
                    best_i1[w] = value
                else:
                    best_i1[w] = 0
                # print(best_i1)
                continue
            if w >= weight:
                temp = best_i1[w - weight] if w > weight else 0
                best_i2[w] = max(best_i1[w], temp + value)
            else:
                best_i2[w] = best_i1[w]

    return best_i2[knapsack_size]


def import_items(file_path):
    # import the item values and their weights
    with open(file_path, 'r') as f:
        items = list()
        header = True
        for line in f:
            target = re.split(r"\s+", line.rstrip('\n'))
            target = list(filter(None, target))
            if header:
                knapsack_size = int(target[0])
                num_items = int(target[1])
                header = False
                continue
            value, weight = int(target[0]), int(target[1])

            items.append((value, weight))

    print('Total number of items is %d' % len(items))
    assert num_items == len(items)

    print(items[:5])
    return items, knapsack_size


def homework():
    filename = 'data/Class3_PSET4_2.txt'
    items, knapsack_size = import_items(filename)

    start = time.time()
    best_val = knapsack_topdown(items, knapsack_size)
    end = time.time()

    print(best_val)
    print('Topdown runtime = ', end - start)

    # start = time.time()
    # best_val = knapsack_bottomup(items, knapsack_size)
    # end = time.time()
    # print(best_val)
    # print('Bottom-up runtime = ', end - start)


def main():
    homework()


if __name__ == '__main__':
    threading.stack_size(67108864)
    sys.setrecursionlimit(2 ** 20)
    main()
