import cPickle
import collections
import string
import sys


def generate_ngram(n, file_name, ngram=None):
    """Create an n-gram frequency dictionary based on the data in the file.

    :param n: the size of the desired n-grams
    :param file_name: the file of the text file to be analyzed for n-gram frequency
    :param ngram: the dictionary to be appended to (defaults to {})
    :return: a dictionary that encodes frequencies of different n-grams
    """
    # open the file
    if ngram is None:
        ngram = {}
    test_file = file(file_name, "r")
    # start a deque to store the words
    word_deque = collections.deque(maxlen=n - 1)
    # run through each line in the file
    for line in test_file:
        # and each word in the line
        for word in line.split():
            # convert to lower case
            word = word.lower()
            # remove punctuation and non ASCII characters
            printable = set(string.printable)
            word = filter(lambda ch: ch not in ",.()'\"!?[]{}_-+=/<>|\\~`@#$%^&*;:" and ch in printable, word)
            # check if n-1 words are in the deque

            if len(word_deque) == n - 1:
                # if so, check if the deque is a key in the dictionary, if not create a dictionary as its value
                tup = tuple(word_deque)
                if tup not in ngram:
                    ngram[tup] = {}
                # then check if the inner dictionary has the next word as a key, if not, initialize it
                if word not in ngram[tup]:
                    ngram[tup][word] = 1
                # increase the count and pop out the left-most (oldest) word
                ngram[tup][word] += 1
                word_deque.popleft()
            # add the new word to the deque
            word_deque.append(word)
    # return the n-gram dictionary
    return ngram


if len(sys.argv) < 2:
    print "usage: python makeNGrams.py text_source1.txt text_source2.txt ..."

else:
    textSources = sys.argv[1:]
    for fileName in textSources:
        for i in range(2, 7):
            nGram = generate_ngram(i, fileName, None)
            savePath = "text_sources/" + fileName[:-4] + "_{0}.ng".format(i)
            print savePath
            cPickle.dump(nGram, open(savePath, "wb"))
