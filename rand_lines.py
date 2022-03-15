import sys
import re
import random

NUM_LINES = 4

def main():
    # guarantee sys.argv has 2 args, a file name and a number k
    # guarantee that all files have enough lines so that line_num choose 4 >= k
    random.seed(None)
    with open(sys.argv[1]) as file:
        lines = file.readlines()
        line_sets = set()
        while len(line_sets) < int(sys.argv[2]):
            l = [random.randrange(len(lines)) for i in range(NUM_LINES)]
            l.sort()
            line_sets.add(tuple(l))
        for tup in line_sets:
            name_li = re.split('[/\\\\]', sys.argv[1])
            sep = '\\' if '\\' in sys.argv[1] else '/'
            nums = ''
            for i in tup:
                nums += '-' + str(i)
            name_li[-1] = name_li[-1][:-4] + '_lines' + nums + '.csv'
            path = sys.argv[3] + sep + name_li[-1]
            with open(path, 'w') as f:
                for i in tup:
                    f.write(lines[i])

if __name__ == "__main__":
    main()

