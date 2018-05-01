import random
import itertools
import string
import numpy as np
import matplotlib.pyplot as plt
from collections import Counter

def collect_freq(input_file):
    """ Create sorted list of character frequencies from a df and returns it """
    counts = Counter()
    site = None
    with open(input_file, 'r') as df: 
        post_site = False
        for line in df:
            if line.startswith('#'):
                continue
            else:
                if post_site:
                    counts += Counter(line.strip())
                else:
                    site = line.strip()
                    post_site = True
    counts_list = []
    S           = []
    counts = counts.most_common()
    total = 0.0
    for (key,val) in counts:
        total += val
    for (key,val) in counts:
        S.append(key)
        counts_list.append(val/total)
 
    return site, counts_list, S

def indiv_freq(input_file):
    """ Create sorted list of character frequencies for each index up to length of longest password hint """


def brute_force(a, b, ans, S=string.ascii_letters):
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
    return -1

def freq_force(a, b, ans, freq=[1/len(string.ascii_letters) for _ in range(len(string.ascii_letters))], S=string.ascii_letters):
    """ Frequency based Password Cracker

    a    -- min length of password
    b    -- max length of password
    ans  -- actual password
    freq -- sorted list of relative frequency of characters (ascending order), by default this is assumed to be uniform over the set of ascii letters, but can be modified based on avaliabled data
    S    -- set of valids characters
    
    ret: # of attempts, else if fail to find -1 
    
    """

    i = 0
    exc_num = int(len(S)/2) # Number of least freq elements to exclude
    while (exc_num >= 0):
        for length in range(a, b+1):
            for attempt in itertools.product(S[exc_num:], repeat=length):
                i += 1
                attempt = ''.join(attempt)
                if attempt == ans:
                    return str(i)
        if exc_num >= 1:
            exc_num = int(exc_num/2)
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
    # @TODO FINISH FUNCTION 
    return None

def file_force(a, b, ans, common_list):
    
    i = 0
    with open(common_list, 'r') as df:
        for line in df:
            i += 1
            if line.strip() == ans:
                return i
    return -1


def test(x):
    lowercase_freq = []
    lowercase      = ['z', 'j', 'q', 'x', 'k', 'v', 'b', 'p', 'g', 'w', 'y' 'f', 'm', 'c', 'u', 'l', 'd', 'h', 'r', 's', 'n', 'i', 'o', 'a', 't', 'e']
    
    
    test_file   = "input_format.txt"
    test_file2  = "input2.txt"
    common_file = "10-million-password-list-top-1000000.txt" 

    print(brute_force(1,6,"brutes", lowercase))
    print(freq_force(1,6,"brutes", lowercase_freq, lowercase))
    print(file_force(1,6,"brutes", common_file))


    title1, freq_test1, S_test1 = collect_freq(test_file)
    
    if x:
        plt.plot(S_test1, freq_test1, label=title1)
        plt.show()
    
    print(title1)
    print(freq_test1)
    print(S_test1)

# Call Testing or Main Her

x = input('Do you want plots? 1 - Yes, 0 - No')
test(x)
