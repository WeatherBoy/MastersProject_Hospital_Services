import matplotlib.pyplot as plt
import numpy as np


def heatmap_rank_selection(
    fitness_scores: list[float],
    rank_selection: str = "linear",
    selection_pressures: np.ndarray = None,
    weights: np.ndarray = None,
    colormap: str = "viridis",
    dpi: int = 300,
    verbose: bool = True,
) -> None:
    """
    Plots a heatmap to show the effect of rank selection on fitness scores.
    Can switch between linear and exponential rank selection methods.
    """
    n = len(fitness_scores)
    y_tick_labels = None
    y_label = None
    save_path = "../figures/Genetic_Algorithms/"

    match rank_selection.lower():
        case "linear":
            y_tick_labels, y_label, title, file_name, fitness_matrix = handle_linear_rank_case(fitness_scores, selection_pressures)
            save_path += file_name

        case "exponential":
            y_tick_labels, y_label, title, file_name, fitness_matrix = handle_exponential_rank_case(fitness_scores, weights)
            save_path += file_name

        case _:
            raise ValueError("Invalid rank selection method")

    plt.figure(figsize=(10, 6))
    plt.imshow(fitness_matrix, cmap=colormap, aspect="auto")
    plt.colorbar(label="New Fitness Score")
    plt.xlabel("Rank (Index)")
    plt.ylabel(y_label)
    plt.xticks(ticks=range(n), labels=range(1, n + 1))  # Show ranks from 1 to 10
    plt.yticks(ticks=range(n), labels=y_tick_labels)
    plt.title(title)
    plt.savefig(save_path, bbox_inches="tight", dpi=dpi)
    plt.close()

    if verbose:
        print(f"Heatmap saved at {save_path}")


def handle_linear_rank_case(fitness_scores: list[float], selection_pressures: np.ndarray = None) -> tuple[list[str], str, str, str, np.ndarray]:
    """
    Handles the linear rank selection case and returns the required values for plotting the heatmap.
    :return: y_tick_labels, y_label, title, file_name, fitness_matrix
    """
    n = len(fitness_scores)
    if selection_pressures is None:
        selection_pressures = np.linspace(1, 2, n)
    selection_pressures = np.sort(selection_pressures)

    y_tick_labels = [f"{sp:.2f}" for sp in selection_pressures]
    y_label = "Selection Pressure (sp)"
    title = "Effect of Linear Rank Selection on Fitness Scores"
    file_name = "linear_rank_selection_selection_pressure_effect.png"

    fitness_matrix = np.array([linear_rank_selection(fitness_scores, sp) for sp in selection_pressures])

    return y_tick_labels, y_label, title, file_name, fitness_matrix


def handle_exponential_rank_case(fitness_scores: list[float], weights: np.ndarray = None) -> tuple[list[str], str, str, str, np.ndarray]:
    """
    Handles the exponential rank selection case and returns the required values for plotting the heatmap.
    :return: y_tick_labels, y_label, title, file_name, fitness_matrix
    """
    n = len(fitness_scores)
    if weights is None:
        weights = np.linspace(0, 1, n)
    weights = np.sort(weights)[::-1]

    y_tick_labels = [f"{w:.2f}" for w in weights]
    y_label = "Weight (w)"
    title = "Effect of Exponential Rank Selection on Fitness Scores"
    file_name = "exponential_rank_selection_weight_effect.png"

    fitness_matrix = np.array([exponential_rank_selection(fitness_scores, w) for w in weights])

    return y_tick_labels, y_label, title, file_name, fitness_matrix


def naive_rank_selection(fitness_scores: list[float]) -> list[float]:
    ranks = ranking(fitness_scores)
    fitness = [rank / sum(ranks) for rank in ranks]
    return fitness


def linear_rank_selection(fitness_scores: list[float], selection_pressure: float) -> list[float]:
    assert 1 <= selection_pressure <= 2, "Selection pressure must be between 1 and 2"

    ranks = ranking(fitness_scores)
    n = len(ranks)
    sp = selection_pressure

    fitness = []
    for rank in ranks:
        fitness.append((2 - sp + 2 * (sp - 1) * ((rank - 1) / (n - 1))) / n)

    return fitness


def exponential_rank_selection(fitness_scores: list[float], weight: float) -> list[float]:
    assert 0 <= weight <= 1, "Weight must be between 0 and 1"

    ranks = ranking(fitness_scores)
    n = len(ranks)
    weight_sum = sum([weight**i for i in range(n)])

    fitness = []
    for rank in ranks:
        fitness.append((weight) ** (n - rank) / weight_sum)

    return fitness


def ranking(fitness_scores: list[float]) -> list[int]:
    """
    Ranks the fitness scores in ascending order from 1 to N ('num elements'). But retains the original index of the fitness score.
    """
    sorting_indices = get_sorting_indices(fitness_scores)
    ranks = get_rank_from_sorting_indices(sorting_indices)

    return ranks


def get_rank_from_sorting_indices(sorting_indices: list[int]) -> list[int]:
    """
    Returns the rank of each element in the list from the sorting indices.
    """
    n = len(sorting_indices)
    ranks = [sorting_indices.index(i) + 1 for i in range(n)]
    return ranks


def get_sorting_indices(some_list: list) -> list[int]:
    """
    Returns the indices that would sort the list in ascending order.
    """
    n = len(some_list)
    sorting_indices = sorted(range(n), key=some_list.__getitem__)
    return sorting_indices
