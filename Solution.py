class Solution:
    score_matrix = None
    fitness = None
    def __init__(self, order, score=None, evaluation=0):
        self.order = order
        if score == None:
            self.score = Solution.fitness(order, Solution.score_matrix)
        else:
            self.score = score
        self.evaluation_num = evaluation

    def __str__(self):
        return 'evaluation=%d, score=%d, order=%s' % (self.evaluation_num, self.score, str(self.order))

    def __eq__(self, other):
        for o1, o2 in zip(self.order, other.order):
            if o1 != o2:
                return False
        return True

def tofile(rstfile, pop, using_time):
    with open(rstfile, 'a') as f:
        f.write("using time = %f sec, evaluation num = %d\n" %
                (using_time, pop[-1].evaluation_num))
        for p in pop:
            f.write("%s\n" % str(p))
        f.write("\n")