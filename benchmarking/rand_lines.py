import sys
import re
import random


def main():
    # guarantee sys.argv has 4 args, a file name and a number k, an output directory, and a test output dir
    # optionally -n at the end means no test case generated
    # guarantee that all files have enough lines so that line_num choose 4 >= k
    TEST = sys.argv[-1] != '-n'
    NUM_LINES = 4

    random.seed(None)
    with open(sys.argv[1]) as file:
        lines = file.readlines()
        line_sets = set()
        test_set  = set()
        if (TEST):
            while len(test_set) < len(lines) // 2:
                # reserve at half for testing
                # only do this for files with >= 10 examples
                test_set.add(random.randrange(len(lines)))
        for num in range(1, NUM_LINES + 1):
            while len(line_sets) < int(sys.argv[2]) * num:
                l = set()
                while len(l) < num:
                    ind = random.randrange(len(lines))
                    if ind not in test_set:
                        l.add(ind)
                l = list(l)
                l.sort()
                line_sets.add(tuple(l))
        for tup in line_sets:
            name_li = re.split('[/\\\\]', sys.argv[1])
            sep = '\\' if '\\' in sys.argv[1] else '/'
            nums = ''
            for i in tup:
                nums += '-' + str(i)
            name_li[-1] = name_li[-1][:-4] + '_randlines' + nums + '.csv'
            path = sys.argv[3] + sep + name_li[-1]
            with open(path, 'w') as f:
                for i in tup:
                    f.write(lines[i])
        if TEST:
            name_li = re.split('[/\\\\]', sys.argv[1])
            sep = '\\' if '\\' in sys.argv[1] else '/'
            name_li[-1] = name_li[-1][:-4] + '_sol.csv'
            sol_path = sys.argv[4] + sep + name_li[-1]
            name_li[-1] = name_li[-1][:-4] + '_test.csv'
            test_path = sys.argv[4] + sep + name_li[-1]
            with open(sol_path, 'w') as f:
                for i in test_set:
                    f.write(lines[i])
            with open(test_path, 'w') as f:
                for i in test_set:
                    cols = re.split(r",(?=')", lines[i])
                    f.write(cols[0] + '\n')

if __name__ == "__main__":
    main()

