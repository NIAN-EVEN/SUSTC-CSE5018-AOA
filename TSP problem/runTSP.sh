#!/usr/bin/env bash
# 1.FILENAME 2.CITY_NUM 3.GENERATION 4.RESULT_FILE 5.PROCESS_NUM 6.INIT_METHOD
# 50 times greedy init
#for i in $(seq 1 50)
#do
#    python3 test.py TSP.csv 100 100 greedyInit $i 30
#    python3 test.py TSP.csv 100 100 randomInit $i 30
#done

python3 localSearch.py TSP.csv 100 10000000

# 1.FILENAME 2.POPSIZE 3.GENERATION 4.CITY_NUM
# 5.TIME_LIMIT 6.MAX_STAY_NUM 7.RESULT_FILE 8.PROCESS_NUM
# python3 genetic_algorithm.py TSP.csv 100 300000 100 36000 50 GAresult.csv 20

# python3 localSearch.py TSP.csv 100 100 localResult 20 greedy