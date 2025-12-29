from read_bayesnet import BayesNet
import operator


def min_parents(net: BayesNet) -> list:
    """
    Orders nodes in a bayesian network in ascending order of number of parents (least-incoming-arcs-first).
    Args:
        net: Bayesian network to find the elimination order for.

    Returns: a list of nodes in ascending order of number of parents

    """
    # Parents contains a dictionary of var: var parents
    parents = net.parents

    # Sort each item in dictionary by number of parents
    sorted_dict = sorted(parents.items(), key=operator.itemgetter(1))

    # Collect just the variable name from the sorted dictionary
    sorted_variables = [item[0] for item in sorted_dict]

    return sorted_variables


def min_factors(net: BayesNet) -> list:
    """
    Orders nodes in a bayesian network in ascending order of number of factors the node appears in
    (contained-in-fewest-factors-first)
    Args:
        net: Bayesian network to find the elimination order for.

    Returns: a list of nodes in ascending order of number of factors the node appears in

    """
    # Dictionary of variable: factor counts
    factor_count = {}

    nodes = net.nodes
    probabilities = net.probabilities

    # Collect the counts for each variable
    for node in nodes:
        count = 0
        for key, value in probabilities.items():

            if node in value.columns:
                count += 1
        factor_count[node] = count

    # Sort the dictionary by count
    sorted_items = sorted(factor_count.items(), key=operator.itemgetter(1))

    # Extract out just the variable names from sorted dictionary
    sorted_vars = [item[0] for item in sorted_items]

    return sorted_vars
