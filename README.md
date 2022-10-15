# solar-calculator
Calculates the solar insolation and position to allow for solar panel optimisation

Work in progress. To run the optimiser simply run the optimiser_test.py test methods. 
Note there are two calculators - one that implements PVEducation's (https://www.pveducation.org/pvcdrom/welcome-to-pvcdrom) formulas, and the other one is a facade that will call the Pysolar library. There are some material differences between the calculators due to their different approaches. Also, the Pysolar calculator is quite a lot slower.
