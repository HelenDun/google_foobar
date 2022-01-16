# Gas Cloud - Level 5

## The Problem
The gas cloud problem was theme'd about shrinking nebula clouds. For this problem, a nebula cloud is represented by a 2D array, with an 'x' representing a pocket of gas and '.' representing empty space. When a nebula cloud shrinks, every 2x2 of the nebula becomes a correlating coordinate of the new, shrunken nebula cloud. If there is one and only one pocket of gas in the 2x2, the correlating coordinate will be a pocket of gas. Otherwise, the correlating coordinate will be empty. For the following examples, Cloud 2 correlates to a pocket of gas, 'x' and Clouds 1 and 3 correlate to empty space.

#### Cloud 1
    ..
    ..

#### Cloud 2
    x.
    ..

#### Cloud 3
    .x
    xx

Here are some bigger examples of nebula clouds before and after shrinking:

#### Nebula 1 - Before
    .x.
    ...
    .xx

#### Nebula 1 - After
    xx
    x.

#### Nebula 2 - Before
    xx.x.x.xx.
    xx....xxx.
    xx.......x
    .x....xx..

#### Nebula 2 - After
    ..xxx....
    .....x...
    .....x.xx

The smallest nebula cloud possible that can shrink must be at least of size 2x2. When a nebula cloud shrinks, it goes from some size **N x M** to size **(N - 1) x (M - 1)**. The length and height do not need to be the same.

With all of that explained, the problem is this: given an input cloud, determine how many clouds would shrink to become the input cloud. The input cloud has length with range [3,40] and height with range [3,9].


## My Solution
Since a gas cloud or empty space in the input nebula can only be shrunk to by a limited number of 2x2s, I used this knowledge to try to incrementally build possible clouds through incrementally determining the values for each 2x2 that correlates to the 2x2. For my first iteration, v1, my program uses a forward search and backtracking algorithm to incrementally build possible clouds that would shrink to the input cloud. This is done by using a queue that tracked some current possible cloud and all possible clouds still untried/unbuilt.


First, the program begins with the top-left corner (0,0). This I hard-coded the possibilities for. Then, second, it builds the top row, (0,0) to (N,0), from the top-left corner to the top-right corner in 2x2 blocks, using what values are already in the current build's 2x2 and the correspondiing coordinate of the input nebula. Third, it builds the left column, (0,0) to (0,M), from the top-left corner to the bottom-left corner, same as the top row. Fourth, and finally, the rest of the graph is filled.


If, at any point, the current cloud cannot build any possible clouds that correlate to the input cloud, the algorithm will backtrack and build a different possible cloud it hasn't tried yet. Each time a build is fully completed, it is counted and the algorithm will backtrack. 


After creating unit tests and debugging my program, I found that my program was too slow to pass Google Foobar's later tests. Thus I created the improved v2 of my program, which differs from v1 by
- removing unnecessary functions
- converting unnecessary code into variables
- records only possibilities at a coordinate of the graph being built, instead of recording a full copy of the graph for every possibility


However, v2 was still too slow. I discussed the problem with my father, who suggested simplifying my numerous functions to just the 4th algorithm. I decided against following this, as I did not think it would affect the speed of my program much and was a bit confused on how such an algorithm would start. For v3 of my program, I adjusted the 4th part of algorithm to use dynamic programming in hopes that this might be faster, but it was still too slow.


Both my father and I being confused and defeated on how to make my program fast enough (he even ended up coding his own version in C++), I looked up solutions for Google Foobar and found the article "Exploring my journey through Google’s Foobar coding challenge" by Shrey Shah:
https://pages.cs.wisc.edu/~shrey/2020/08/10/google-foobar.html


This is the only problem I looked up the solution for, and I am and was conflicted about looking up the solution, but ultimately decided at the time that I did not want all my effort on Google Foobar to be for naught. Shrey Shah's code is in the file gas_cloud_vC.py, which I have included if you wish to compare her solution and my final solution. I tried to use as much of the previous code I had written as I could, which was a surprising amount.


To explain how it works, first let me set some variables: say we have 2 columns of the input cloud that are located one after the other- columns X and Y. What the meat of Shrey Shah's algorithm does is it builds all possible clouds, size 2 x (M + 1), that correlate to Y. Then it checks for matches between the 1st column of each possible cloud and the 2nd column of all of the possible clouds built from X. 


In this manner, Shrey Shah's algorithm goes through each of the columns, size 1 x M, of the input cloud. This may sound inefficient, but let me explain. Each 1st column and 2nd column can be serialized into a small binary number, due to the boolean nature of each space being either empty or gas-filled. The possible clouds built from a column often have repeat 1st or 2nd columns. 


Since only the count of how many possible clouds correlate to the input cloud is wanted, the program keeps track of the number of possibilities per unique column using a dictionary with the binary of the column as the key. For the very first column of the input cloud, as there is no previous column X, the program simply counts how many times it builds the 2nd column of the built cloud. 


For each column of the input cloud after that, the clouds built from Y should have 1st columns that match the 2nd columns of the clouds built from X which are recorded in the dictionary. The program creates a new dictionary and, for each possibility where the 1st column built from Y matches the 2nd column built from X, adds the number of possibilites for the 2nd column built from X to the 2nd column built from Y. This is done repeatedly. At the end, the algorithm returns the sum of the values of the dictionary.


Below is an example of how all this works. First, an example of the serialization:

    x
    x
    x
    .

This would correlate to the binary 1110, or decimal 14. With a column of height 4, there are 16 unique columns, or 16 keys for the dictionary. Therefore I will be using the range of numbers [0,15] to refer to each possible column.


Let the following be an input cloud:

    .xx
    ..x
    xx.

Many clouds can be built from the first column. The two examples below have 2nd columns that serialize to 0 and 12 respectively.

    ..
    ..
    ..
    x.

    xx
    xx
    x.
    ..

The dictionary looks like this after building the first column of the input cloud, with any unrepresented keys being at count 0:
    
    {   
        1: 3, 
        3: 5, 
        5: 5, 
        7: 6, 
        9: 2, 
        11: 2, 
        13: 2, 
        15: 4
    }

Next, we move on to the next column of the input cloud and create another empty dictionary. Suppose the following cloud is then built from the second column:

    .x
    ..
    ..
    x.

The first column serializes to 0001, or 1. There were 3 possibilities where the 2nd column built from the previous column of the input cloud was 1. Thus we add 3 possibilities to the number of possibilities for the 2nd column of the above cloud in the new dictionary.

So it goes, until every column has all of its possibilities built and counted and we return the sum of the last dictionary made.
