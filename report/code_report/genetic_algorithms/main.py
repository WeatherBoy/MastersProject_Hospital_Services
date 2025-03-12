from genetic_algorithms.utils.rank_selection import heatmap_rank_selection

if __name__ == "__main__":
    fitness_scores = [0.05, 0.1111, 0.169, 0.31, 0.33, 0.42, 0.58, 0.69, 0.8, 0.96]
    heatmap_rank_selection(fitness_scores, rank_selection="linear", colormap="plasma")
    heatmap_rank_selection(
        fitness_scores, rank_selection="exponential", colormap="plasma"
    )
