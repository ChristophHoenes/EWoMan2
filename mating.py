from deap import tools


def average_parents(partners, ratio=0.5):
    children = []
    for parent1, parent2 in partners:  # zip(partners[::2], partners[1::2]):
        for i in range(len(parent1)):
            parent1[i] *= ratio
            parent1[i] += (1-ratio) * parent2[i]
        children.append(parent1)
    return children


def deap_xover_blend(partners, rate=0.5):
    children = []
    for child1, child2 in partners:
        tools.cxBlend(child1, child2, rate)
        del child1.fitness.values
        del child2.fitness.values
        children.append(child1)
        children.append(child2)
    return children


def deap_xover_onepoint(partners):
    children = []
    for child1, child2 in partners:
        tools.cxOnePoint(child1, child2)
        del child1.fitness.values
        del child2.fitness.values
        children.append(child1)
        children.append(child2)
    return children


def deap_xover_uniform(partners, swap_prob=0.2):
    children = []
    for child1, child2 in partners:
        tools.cxUniform(child1, child2, swap_prob)
        del child1.fitness.values
        del child2.fitness.values
        children.append(child1)
        children.append(child2)
    return children


