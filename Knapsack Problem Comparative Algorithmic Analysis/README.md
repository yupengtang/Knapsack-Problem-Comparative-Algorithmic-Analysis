# CSE6140Project
CSE6140

To run Simulated Annealing:
python SA.py -inst <filePath> -alg <algorithm> -time <cutoff> -seed <seed>
<filePath> represents the instance to run, for example "./DATA/DATASET/small_scale/small_1"
<algorithm> represents the algorithm to use, for simulated annealing, it should be "SA"
<cutoff> represents the cutoff time in seconds, for simulated annealing, it should be 3 seconds for small dataset
<seed> represents the random seed to run the algorithm

To generate 100 round to plot QRTD and SQD:
python SAGenerate100rounds.py
python SAPlotLarge1.py
python SAPlotLarge3.py

To run ten rounds to get average best value:
python SA10round.py