from collections import defaultdict


def fast_non_dominated_sort(population):

    # initialize set of dominated individuals and number of dominating individuals for each member of the population
    S = defaultdict(set)
    n = defaultdict(int)

    # initialize frontiers and rank
    frontiers = defaultdict(set)
    rank = defaultdict(int)

    for p_id, p in enumerate(population):
        for q_id, q in enumerate(population):
            if domination_operator(p, q):
                S[p_id].add(q_id)
            elif domination_operator(q, p):
                n[p_id] += 1

        # add to first level frontier if not dominated by any other individual
        if n[p_id] == 0:
            frontiers[1].add(p_id)

    i = 1
    while len(frontiers[i]) != 0:
        Q = set()
        for p_id in frontiers[i]:
            for q_id in S[p_id]:
                n[q_id] -= 1
                if n[q_id] == 0:
                    rank[q_id] = i + 1
                    Q.add(q_id)
        i += 1
        frontiers[i] = Q

    # assign rank to the corresponding individuals
    for p_id, ind in enumerate(population):
        ind.rank = rank[p_id]
        # also assign negative rank to use 'fitness' (rank) MAXIMIZING deap functions
        ind.neg_rank = -ind.rank

    return population, frontiers


def crouding_operator(left_arg, right_arg):
    return left_arg.rank < right_arg.rank or \
           (left_arg.rank == right_arg.rank and left_arg.distance > right_arg.distance)


def domination_operator(left_arg, right_arg):
    greater_equal = [v_l >= v_r for v_l, v_r in zip(left_arg.fitness.values, right_arg.fitness.values)]
    strictly_greater = [v_l > v_r for v_l, v_r in zip(left_arg.fitness.values, right_arg.fitness.values)]
    return all(greater_equal) and any(strictly_greater)

