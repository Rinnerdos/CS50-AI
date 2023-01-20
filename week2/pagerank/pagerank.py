import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    # Regardless whether the page is linked to or not, all pages
    # have at least (1 - damp) / #total pages chance to be picked 
    # by the random surfer. For the linked to pages, this chance
    # increased by an additional (damp / #linked pages).
    
    transition_dict = dict()
    corpus_length = len(corpus)

    for key in corpus:
        all_chance = (1 - damping_factor) / (corpus_length)
        transition_dict[key] = all_chance
    
    for key in corpus:
        if key == page:
            number = len(corpus[key]) 

            # If there are no outgoing links, all pages in the corpus
            # should have same chance, total equalling 1.
            if number == 0:
                value_chance = damping_factor / corpus_length
                for key in transition_dict:
                    transition_dict[key] += value_chance
                break    

            value_chance = (damping_factor / number)
            for value in corpus[key]:
                transition_dict[value] += value_chance

    return transition_dict     
            

def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    # Start by choosing a random entry of your corpus. Then, choose
    # from the links it links to (or of all) according to specified chance.
    # Repeat n times, and count how many times you reached each page.
    # In the end, divide this count by n, to obtain the pagerank.

    sample_dict = dict()
    page = random.choice(list(corpus))

    for key in corpus:
        sample_dict[key] = 0
    
    for _ in range(n):
        sample_dict[page] += 1
        
        weights = list()
        trans_model = transition_model(corpus, page, damping_factor)
        for key in trans_model:
            # Use the probabilities given by the transition model
            # to update the page
            weights.append(trans_model[key])

        page = random.choices(list(corpus), weights)[0]
        
    for key in sample_dict:
        sample_dict[key] /= n

    return sample_dict
        

def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    treshold = 0.001
    d = damping_factor
    N = len(corpus)
    isAccurate = False

    target_accuracy = [treshold for _ in range(N)]
    current_accuracy = [1 for _ in range(N)]
    
    #print(f'The list target_accuracy looks like: {target_accuracy}')
    #print(f'The list current_accuracy looks like: {current_accuracy}')

    iterative_dict = dict()
    i_of_page = dict()

    # First construct the iterative dict,
    # with pagerank initialized at 1/N
    for key in corpus:
        iterative_dict[key] = 1/N

    # Then construct a new dict, from which
    # you can obtain the pages i that link to
    # page p. The length of this set of i, is
    # consequently i in the formula. NumLinks(i)
    # is just the length of the corpus[key] of the
    # original.
    for key1 in corpus:
        set_of_i = set()
        for key2 in corpus:
            if key1 in corpus[key2]:
                set_of_i.add(key2)
        i_of_page[key1] = set_of_i

    iterations = 0
    while isAccurate == False:
        index = 0
     
        for key in iterative_dict:
            old_value = iterative_dict[key]
            summation = 0
            for key2 in i_of_page[key]:
                summation += (iterative_dict[key2] / len(corpus[key2])) 
            iterative_dict[key] = ((1 - d) / N) + (d * summation)
            new_value = iterative_dict[key]
            current_accuracy[index] = abs(new_value - old_value)
            index += 1

        count = 0
        for i in range(N):
            if target_accuracy[i] > current_accuracy[i]:
                count += 1
            
            if count == N:
                isAccurate = True # Technically unnecessary
                print(f'The amount of iterations is: {iterations}')
                #print(f'The current_accuracy is: {current_accuracy}')
                return iterative_dict
            elif iterations > 200000: #failsafe for inf loop
                #print(f"Out of bounds :(, current_accuracy: {current_accuracy}")
                #print(f'N = {N} and count = {count}')
                return iterative_dict
            else:
                iterations += 1
            

if __name__ == "__main__":
    main()
