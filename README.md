# system_simulator_project

Done as a project in the University of Latvia

Currently it has functionality of:

* __Quantum (one-bit) simulator__:
1. Initial quantum state could be set from 0 to 360 degrees, or 0 by default
2. Quantum state can be rotated BY any number of degrees in both directions
3. Quantum state can be reflected OVER imaginary axis in degrees (from basic basis)
4. Current quantum state can be drawn on a unit circle
5. All visited quantum states can be drawn on a unit circle
6. Probability in a current quantum state can be assessed
7. Measurement can be done with current probability (according to the specified number of shots)
8. Measurement can be done with a distribution bar chart
9. Basis of a unit circle can be set to different position together with all previously visited states (TO 0-360 degrees)
10. Current quantum state can be drawn in a previous basis
11. Probabilities of observing state |0> and |1> can be observed for last 2 basis
12. Basis change can be reverted
13. Values of X of all visited states can be plotted on a chart
14. Values of Y of all visited states can be plotted on a chart
15. Values of X and Y of all visited states can be plotted on a chart
16. Probability of observing 0 (X) of all visited states can be plotted on a chart
17. Probability of observing 1 (Y) of all visited states can be plotted on a chart
18. Probabilities of observing 0 (X) and 1 (Y) of all visited states can be plotted on a chart
19. System info can be reviewed - contains a number of visited states and the current number of bases
20. System data can be saved in a file in binary form with the extension of .qssf (quantum simulator state file)
21. System data can be loaded from any valid .qssf file to continue analysis
22. History of analysis can be saved as .txt file 
23. Delete quantum state functionality (NEW)

* __Classical (multi-bit) simulator__:
1. Initial classical state is set to [0.5, 0.5]
2. New bit can be added to the system (0 to 1, can be float, e.g. 0.1)
3. System state vector can be observed
4. System state as a combination of basic linear states can be observed
5. NOT operator can be applied to the specified bit
6. CNOT operator can be applied to the specified control and target bits
7. NOT operator matrix can be generated with user-set parameters
8. CNOT operator matrix can be generated with user-set parameters
9. System data can be saved in a file in binary form with the extension of .cssf (classical simulator state file)
10. System data can be loaded from any valid .cssf file to continue analysis
11. History of analysis can be saved as .txt file
12. Delete classical bit functionality (NEW)



* __Usage/Installation__:
1. Put .py file in one directory with 3 images
2. Run .py file by Python interpreter (all was checked by Python 3.7.4 for 64-bit devices)
