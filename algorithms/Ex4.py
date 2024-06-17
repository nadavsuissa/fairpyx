# Nadav Suissa


def find_proportional_allocation(instance):
    """
  Finds an allocation of items to agents that is proportional to their
  rankings.

  Args:
      instance (dict): A dictionary containing the following keys:
          * agents (list): A list of agents.
          * items (dict): A dictionary mapping agents to dictionaries of
              items and their values.
          * rankings (dict): A dictionary mapping agents to lists of ranked
              item bundles.

  Returns:
      dict: A dictionary mapping agents to lists of allocated items.

          Example:
        >>> instance = {
        ...     "agents": ["Alice", "Bob", "Charlie"],
        ...     "items": {
        ...         "Alice": {"A": 40, "B": 35, "C": 25},
        ...         "Bob": {"A": 35, "B": 40, "C": 25},
        ...         "Charlie": {"A": 40, "B": 25, "C": 35}
        ...     },
        ...     "rankings": {
        ...         "Alice": [["A"], ["B"], ["C"]],
        ...         "Bob": [["B"], ["A"], ["C"]],
        ...         "Charlie": [["A"], ["C"], ["B"]]
        ...     }
        ... }
        >>> find_proportional_allocation(instance)
        {'Alice': ['A'], 'Bob': ['B'], 'Charlie': ['C']}
  """

    agents = instance["agents"]
    items = instance["items"]
    rankings = instance["rankings"]

    allocation = {agent: [] for agent in agents}
    remaining_items = {item: count for agent_items in items.values() for item, count in agent_items.items()}
    allocated_items = set()

    # Sort agents by the sum of their item values (highest first)
    sorted_agents = sorted(agents, key=lambda agent: sum(items[agent].values()), reverse=True)

    for agent in sorted_agents:
        # Sort the agent's ranked items by their ranking index
        sorted_items = sorted(items[agent], key=lambda item: get_ranking_index(rankings[agent], item))

        for item in sorted_items:
            # Check if the item is available and not already allocated
            if remaining_items[item] > 0 and item not in allocated_items:
                # Check if allocating the item would cause envy
                if not causes_envy(agent, item, allocation, rankings):
                    allocation[agent].append(item)
                    allocated_items.add(item)
                    remaining_items[item] -= 1
                    break

    return allocation


def allocate_minimal_bundles(instance):
    """
    Allocate minimal bundles of items to agents based on their rankings.

    Args:
        instance (dict): Dictionary containing the agents, items, and rankings.

    Returns:
        dict: A dictionary representing the minimal allocation of items to agents.

    Example:
        >>> instance = {
        ...     "agents": ["Alice", "Bob", "Charlie"],
        ...     "items": {
        ...         "Alice": {"A": 40, "B": 35, "C": 25},
        ...         "Bob": {"A": 35, "B": 40, "C": 25},
        ...         "Charlie": {"A": 40, "B": 25, "C": 35}
        ...     },
        ...     "rankings": {
        ...         "Alice": [["A"], ["B"], ["C"]],
        ...         "Bob": [["B"], ["A"], ["C"]],
        ...         "Charlie": [["A"], ["C"], ["B"]]
        ...     }
        ... }
        >>> allocate_minimal_bundles(instance)
        {'Alice': ['A'], 'Bob': ['B'], 'Charlie': ['C']}
    """
    agents = instance["agents"]
    rankings = instance["rankings"]

    allocation = {agent: [] for agent in agents}
    assigned_items = set()

    for agent in agents:
        for bundle in rankings[agent]:
            if all(item not in assigned_items for item in bundle):
                allocation[agent].extend(bundle)
                assigned_items.update(bundle)
                break

    return allocation


def bundle_is_minimal(instance):
    """
    Check if each agent's bundle is minimal based on their rankings.

    Args:
        instance (dict): Dictionary containing the agents, items, and rankings.

    Returns:
        dict: A dictionary indicating if each agent's bundle is minimal.

    Example:
        >>> instance = {
        ...     "agents": ["Alice", "Bob", "Charlie"],
        ...     "items": {
        ...         "Alice": {"A": 40, "B": 35, "C": 25},
        ...         "Bob": {"A": 35, "B": 40, "C": 25},
        ...         "Charlie": {"A": 40, "B": 25, "C": 35}
        ...     },
        ...     "rankings": {
        ...         "Alice": [["A"], ["B"], ["C"]],
        ...         "Bob": [["B"], ["A"], ["C"]],
        ...         "Charlie": [["A"], ["C"], ["B"]]
        ...     }
        ... }
        >>> bundle_is_minimal(instance)
        {'Alice': {'A': True, 'B': True, 'C': True}, 'Bob': {'B': True, 'A': True, 'C': True}, 'Charlie': {'A': True, 'C': True, 'B': True}}
    """
    agents = instance["agents"]
    rankings = instance["rankings"]

    minimal_check = {agent: {item: False for item in sum(rankings[agent], [])} for agent in agents}

    for agent in agents:
        for bundle in rankings[agent]:
            for item in bundle:
                minimal_check[agent][item] = True

    return minimal_check


def get_ranking_index(ranking_list, item):
    """
    Helper function to return the index of an item in the ranking list.

    Args:
        ranking_list (list): The ranking list.
        item (str): The item to find.

    Returns:
        int: The index of the item in the ranking list, or infinity if not found.
    """
    for i, rank in enumerate(ranking_list):
        if item in rank:
            return i
    return float('inf')


def causes_envy(agent, item, allocation, rankings):
  for other_agent, allocated_items in allocation.items():
    if other_agent != agent and allocated_items:  # Check if allocation is not empty
      if item in rankings[other_agent] and item in rankings[agent]:
        if get_ranking_index(rankings[other_agent], item) < get_ranking_index(rankings[agent], item):
          return True
  return False


def total_value(instance):
    """
    Calculate the total value of a bundle of items for a given agent.

    Args:
        instance (dict): Dictionary containing the bundle, player, and items.

    Returns:
        int: The total value of the bundle for the player.

    Example:
        >>> instance = {
        ...     "bundle": ['A'],
        ...     "player": "Alice",
        ...     "items": {
        ...         "Alice": {"A": 40, "B": 35, "C": 25},
        ...         "Bob": {"A": 35, "B": 40, "C": 25},
        ...         "Charlie": {"A": 40, "B": 25, "C": 35}
        ...     }
        ... }
        >>> total_value(instance)
        40
    """
    bundle = instance["bundle"]
    player = instance["player"]
    items = instance["items"]

    return sum(items[player][item] for item in bundle)


def is_envy_free(instance):
    """
    Check if an allocation is envy-free.

    Args:
        instance (dict): Dictionary containing the allocation, agents, items, and rankings.

    Returns:
        bool: True if the allocation is envy-free, False otherwise.

    Example:
        >>> instance = {
        ...     "allocation": {'Alice': ['A'], 'Bob': ['B'], 'Charlie': ['C']},
        ...     "agents": ["Alice", "Bob", "Charlie"],
        ...     "items": {
        ...         "Alice": {"A": 40, "B": 35, "C": 25},
        ...         "Bob": {"A": 35, "B": 40, "C": 25},
        ...         "Charlie": {"A": 40, "B": 25, "C": 35}
        ...     },
        ...     "rankings": {
        ...         "Alice": [["A"], ["B"], ["C"]],
        ...         "Bob": [["B"], ["A"], ["C"]],
        ...         "Charlie": [["A"], ["C"], ["B"]]
        ...     }
        ... }
        >>> is_envy_free(instance)
        True
    """
    allocation = instance["allocation"]
    agents = instance["agents"]
    items = instance["items"]
    rankings = instance["rankings"]

    for agent in agents:
        agent_allocation = allocation[agent]
        for other_agent in agents:
            if other_agent != agent:
                other_allocation = allocation[other_agent]
                # Check if the total value of the other agent's allocation is greater
                if total_value({"bundle": other_allocation, "player": other_agent, "items": items}) > total_value({"bundle": agent_allocation, "player": agent, "items": items}):
                    # Additionally check if any item in other_agent's allocation is ranked higher by agent
                    for item in other_allocation:
                        if item in rankings[agent] and get_ranking_index(rankings[agent], item) < get_ranking_index(rankings[other_agent], item):
                            return False
    return True



def is_pareto_optimal(instance):
    """
    Check if an allocation is Pareto optimal.

    Args:
        instance (dict): Dictionary containing the allocation, agents, and items.

    Returns:
        bool: True if the allocation is Pareto optimal, False otherwise.

    Example:
        >>> instance = {
        ...     "allocation": {'Alice': ['A'], 'Bob': ['B'], 'Charlie': ['C']},
        ...     "agents": ["Alice", "Bob", "Charlie"],
        ...     "items": {
        ...         "Alice": {"A": 40, "B": 35, "C": 25},
        ...         "Bob": {"A": 35, "B": 40, "C": 25},
        ...         "Charlie": {"A": 40, "B": 25, "C": 35}
        ...     }
        ... }
        >>> is_pareto_optimal(instance)
        True
    """
    allocation = instance["allocation"]
    agents = instance["agents"]
    items = instance["items"]

    current_utilities = {agent: sum(items[agent][item] for item in allocation[agent]) for agent in agents}

    for agent in agents:
        for item in items[agent]:
            for other_agent in agents:
                if other_agent != agent and item in allocation[agent]:
                    new_allocation = {k: v[:] for k, v in allocation.items()}
                    new_allocation[agent].remove(item)
                    new_allocation[other_agent].append(item)
                    new_utilities = {a: sum(items[a][i] for i in new_allocation[a]) for a in agents}

                    if new_utilities[other_agent] > current_utilities[other_agent] and all(
                            new_utilities[a] >= current_utilities[a] for a in agents if a != other_agent
                    ):
                        return False
    return True

