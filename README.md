# Allocation Algorithms 

The following code consists of functions to solve the course allocation problem for Fall 2023 Umass Amherst courses. The algorithms are the current SPIRE algorithm (used currently by the UMass), Round Robin, and the proposed by Viswanathan and Zick(2023), Yankee Swap.


## Prerequisites

- Pandas
- Numpy
- Networkx
- openpyxl


## Preliminary results

The three algorithms were run and compared for 50 different seeds. The algorithms are deterministic, however randomness was introduced by randomply generating students preferences for 50 students. The obtained values for Utilitarian Welfare and Nash Welfare (in logarithm and nuber of zeros) are shown below.

![Utilitarian Walfare](util_50.png)

![Nash Walfare](nash_50.png)

![Nash Walfare, number of zeros](nashZeros_50.png)

In some cases, welfare from the SPIRE algorithm goes above RR and YS, which is problematic since it's mathematically proven that RR and YS should be always weekly higher than SPIRE. Code needs further debugging.
