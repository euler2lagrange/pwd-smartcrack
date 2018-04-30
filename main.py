import random
import itertools
import string

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
    return None




def test():
    lowercase_freq = []
    lowercase      = ['z', 'j', 'q', 'x', 'k', 'v', 'b', 'p', 'g', 'w', 'y' 'f', 'm', 'c', 'u', 'l', 'd', 'h', 'r', 's', 'n', 'i', 'o', 'a', 't', 'e']
    
    print(brute_force(1,5,"brute", lowercase))
    print(freq_force(1,5,"brute", lowercase_freq, lowercase))
    


test()
