import os
import sys
import random
import itertools
import string
import operator
import numpy as np
import matplotlib.pyplot as plt
from collections import Counter
from termcolor import cprint
from pyfiglet import figlet_format


LIMIT = 1000000000

def common_substrings(input_file):
    """ Takes input file of passwords and returns most common substrings i.e. ALL LENGTH SUBSTRINGS (will take very long time to run)"""
    counts = Counter()
    with open(input_file, 'r') as df:
        for line in df:
            sline = line.strip()
            counts += Counter(sline[i:j+1] for j in range(len(sline)) for i in range(j+1))
    counts = counts.most_common()
    total = 0.0
    counts_list = []
    S           = []
    for (key,val) in counts:
        total += val
    for (key,val) in counts:
        S.append(key)
        counts_list.append(val/total)
    return counts_list, S

def length_n_substrings(input_file, n):
    """ Similiar to common_substrings except now it will only count occurences of length n substrings and return a sorted list by their frequencies 
    """
    counts = Counter()
    with open(input_file, 'r') as df:
        for line in df:
            sline = line.strip()
            counts += Counter(sline[j:j+n] for j in range(len(sline)-n+1))
    counts = counts.most_common()
    total = 0.0
    counts_list = []
    S           = []
    for (key,val) in counts:
        total += val
    for (key,val) in counts:
        S.append(key)
        counts_list.append(val/total)
    return counts_list, S

def collect_freq(input_file):
    """ Create sorted list of character frequencies from a df and returns it """
    counts = Counter()
    with open(input_file, 'r') as df: 
        for line in df:
            counts += Counter(line.strip())
    counts_list = []
    S           = []
    counts = counts.most_common()
    total = 0.0
    for (key,val) in counts:
        total += val
    for (key,val) in counts:
        S.append(key)
        counts_list.append(val/total) 
    return counts_list, S

def indiv_freq(input_file):
    """ Create sorted list of character frequencies for each index up to length of longest password hint """
    counts_list = [{} for _ in range(1000)]
    with open(input_file, 'r') as df:
        for line in df:
            line2 = line.strip()
            for idx,ch in enumerate(line2):
                if ch in counts_list[idx]:
                    (counts_list[idx])[ch] += 1.0
                else:
                    (counts_list[idx])[ch] = 1.0

    counts_list = [x for x in counts_list if x != {}]
    
    sorted_list = []
    for counts in counts_list:
        sorted_list.append(sorted(counts.items(), key=operator.itemgetter(1)))
    
    S_list = [[] for _ in range(len(counts_list))]
    c_list = [[] for _ in range(len(counts_list))]
    for idx,counts in enumerate(sorted_list):
        total = 0.0
        for (key,val) in counts:
            total += val
        for (key,val) in counts:
            S_list[idx].append(key)
            c_list[idx].append(val/total)
    
    return c_list, S_list

def brute_force(a, b, ans, S=string.ascii_letters):
    global LIMIT
    """ Password Cracker

    a   -- min length of password
    b   -- max length of password
    ans -- actual password
    S   -- set of valid characters (ascii letters by default)

    ret: # of attempts, else if fail to find -1 
    
    """
    i = 0
    for length in range(a, b+1): 
        for attempt in itertools.product(S, repeat=length):
            i += 1
            attempt = ''.join(attempt)
            if attempt == ans:
                return str(i)
            if i >= LIMIT:
                print("Exceeding attempt limit ...giving up now")
                return -1
    return -1

def freq_force(a, b, ans, freq=[1/len(string.ascii_letters) for _ in range(len(string.ascii_letters))], S=string.ascii_letters):
    global LIMIT
    """ Frequency based Password Cracker

    a    -- min length of password
    b    -- max length of password
    ans  -- actual password
    freq -- sorted list of relative frequency of characters (ascending order), by default this is assumed to be uniform over the set of ascii letters, but can be modified based on avaliabled data
    S    -- set of valids characters
    
    ret: # of attempts, else if fail to find -1 
    
    """
    i = 0
    exc_num = int(len(S)/2.0) # Number of least freq elements to exclude
    while (exc_num >= 0):
        for length in range(a, b+1):
            for attempt in itertools.product(S[exc_num:], repeat=length):
                i += 1
                attempt = ''.join(attempt)
                if attempt == ans:
                    return str(i)
                if i >= LIMIT:
                    print("Exceeding attempt limit ...giving up now")
                    return -1
        if exc_num >= 1:
            exc_num = int(exc_num/2.0)
        else:
            exc_num = -1
    return -1

def freq_indiv_force(a, b, ans, freq_list, S_list):
    """ Individual index frequency Password Cracker

    a   -- min length of password
    b   -- max length of password
    ans -- actual password
    freq_list -- list of freq distributions for each index 
    S_list    -- list of allowed characters for each index
    
    """
    global LIMIT
    attempts = 0
    exc_num = [int(len(S_list[i])/2.0) for i in range(len(S_list))]
    
    while (sum(exc_num) >= 0):
        for length in range(a, b+1):
            for guess in itertools.product(*[(S_list[i])[exc_num[i]:] for i in range(length)]):
                i += 1
                guess = ''.join(guess)
                if guess == ans:
                    return str(i)
                if i >= LIMIT:
                    print("Exceeding attempt limit ...giving up now")
                    return -1
        for i in range(len(exc_num)):
            if exc_num[i] >= 1:
                exc_num[i] = int(exc_num[i]/2)
            else:
                exc_num[i] = 0
    return -1

def file_force(a, b, ans, common_list):
    """ Uses list of 1000000 most common passwords to crack ans and        returns number of attempts
    """
    i = 0
    with open(common_list, 'r') as df:
        for line in df:
            i += 1
            if line.strip() == ans:
                return i
    print("password not in lookup file")
    return -1

def test():
    lowercase_freq = []
    # Ascending order of letter freq in standard english
    lowercase      = ['z', 'j', 'q', 'x', 'k', 'v', 'b', 'p', 'g', 'w', 'y' 'f', 'm', 'c', 'u', 'l', 'd', 'h', 'r', 's', 'n', 'i', 'o', 'a', 't', 'e']
     
    test_file   = os.path.dirname(os.path.realpath('__file__')) + "/inputfiles/input_file1.txt"
    common_file = "random_1mill.txt" 
    example_file = "examplefile.txt"

    # Generate indiv freq for large test file
    freq_large_list, S_large_list = indiv_freq(common_file)
    # Generate overall freq for large file
    freqo_large_list, So_large_list = collect_freq(common_file)
    
    print("Freq Force Attempts")
    print(freq_force(4,6, "jesus", freqo_large_list, So_large_list[::-1]))
    print("Indiv Freq Force Attempts")
    print(freq_indiv_force(4,6,"jesus",freq_large_list, S_large_list))
    
    # Uncomment for simple example of brute,freq, and file crackers
    """
    freq_list, S_list = indiv_freq(example_file)
    print("Brute Force Attempts")
    print(brute_force(1,6,"brutes", lowercase))
    print("Frequency Force Attempts")
    print(freq_force(1,6,"brutes", lowercase_freq, lowercase))
    print("File Lookup Force Attempts")
    print(file_force(1,6,"brutes", common_file))
    print("Indiv Freq Force Attempts")
    print(freq_indiv_force(1, 6, "brutes", freq_list, S_list))
    """

    """ Uncomment for display of first 10 char freq for testfile1

    list_freq_test1, list_S_test1 = indiv_freq(test_file)
    for i in range(10):
        plt.plot(list_S_test1[i], list_freq_test1[i])
        plt.title("Char Freq. for " + str(i) + "th index")
        plt.show()
    """
    
    # Uncomment for display of simple overall char freq
    # freq_test1, S_test1 = collect_freq(test_file)
    # plt.plot(S_test1, freq_test1)
    # plt.title("Overall Char Freq")
    # plt.show()
    
    
    # Uncomment for most common substrings of any length
    # warning: will probably take 1h+
    # sub_test1, S_sub1 = common_substrings(test_file)
    # plt.title("Top 30 Most Common Substring Freq.")
    # plt.plot(S_sub1[:30], sub_test1[:30])
    # plt.show()    

    # subn_test1, Sn_sub1 = length_n_substrings(test_file, 6)
    # plt.title("Top 30 Most common length 4 substring Freq.")
    # plt.plot(Sn_sub1[:30], subn_test1[:30])
    # plt.show()
    

def demo(input_file, test_file):
    
    # Plot to demonstrate functionality of substrings
    # It's much prefered to look at printed out list since x-axis gets so crowded
    # cl, sl = length_n_substrings("examplefile.txt", 6)
    # plt.plot(sl, cl)
    # plt.title("Most common substrings")
    # plt.show()

    os.path.expanduser(u"~")

    common_file = "random_1mill.txt" 
    
    # TRAIN AND PROCESS FILES     
    freqi_list, Si_list = indiv_freq(input_file)
    freqc_list, Sc_list = collect_freq(input_file)
    print('Finished Training ...')
    

    x = input("Do you want to see character frequency plots? 1 = Yes, 0 = No : ")
    if x:
        plt.plot(Sc_list, freqc_list)
        plt.title("Overall Char Freq")
        plt.show()

        for i in range(10):
            plt.plot(Si_list[i], freqi_list[i])
            plt.title("Char Freq. for " + str(i) + "th index")
            plt.show()
    
    # Grab three random lines (file was already randomized so adjacent passwords aren't related)
    rand = random.randint(0, 49998)
    lines = []
    with open(test_file) as f:
        lines = list(itertools.islice(f, rand, rand+3))
    
    chl = []
    
    # For the sake of fast demo I only attempt to crack truncated size
    for trunc, line in enumerate(lines):
        chl.append(line[:4+trunc])
    
    chl.append("bambanek")

    for line in chl:

        ans = line.strip()

        print("Attempting to Brute Force : " + ans)
        tries = brute_force(len(ans),len(ans),ans, string.letters + string.digits + string.punctuation)
        if tries != -1:
            print("Brute Force attempts on " + ans + " :" + str(tries))
        
        print("Attempting to Freq Force : " + ans)
        tries = freq_force(len(ans),len(ans),ans, freqc_list, Sc_list[::-1])
        if tries != -1:
            print("Freq Force attempts on " + ans + " :" + str(tries))
            
        print("Attempting to Indiv Freq Force : " + ans)
        tries = freq_indiv_force(len(ans), len(ans), ans, freqi_list, Si_list)
        if tries != -1:
            print("Indiv Freq attempts on " + ans + " :" + str(tries))
    
    print("Exiting")

def main():
    cprint(figlet_format('pwd-cracker', font='smkeyboard'))
    cprint(figlet_format('@MarkJankovec', font='small'))
    
    df  = input('Please specify a training file number [1-10]: ')
    while (df not in [x+1 for x in range(10)]):
        df  = input('Please specify a training file number [1-10]: ')
    train = os.path.dirname(os.path.realpath('__file__')) + "/inputfiles/" + 'input_file' + str(df) + '.txt'
    test  = os.path.dirname(os.path.realpath('__file__')) + "/inputfiles/" + 'test_file' + str(df) + '.txt'
    print("Using " + train)
    
    demo(train,test)

main()
# test()
