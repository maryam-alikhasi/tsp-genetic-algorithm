import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import random
import math
import time

POPULATION_SIZE = 100
NUM_GENERATIONS = 500
CROSSOVER_RATE = 0.9
MUTATION_RATE = 0.05
TOURNAMENT_SIZE = 5
ELITE_SIZE = 10
RANDOM_SEED = 42

random.seed(RANDOM_SEED)
np.random.seed(RANDOM_SEED)

# Generating random coordinates for cities
def generate_cities(num_cities, x_range=(0, 100), y_range=(0, 100)):
    cities = []
    for _ in range(num_cities):
        x = random.uniform(*x_range)
        y = random.uniform(*y_range)
        cities.append((x, y))
    return cities


def euclidean_distance(city1, city2):
    return math.sqrt((city1[0] - city2[0]) ** 2 + (city1[1] - city2[1]) ** 2)


def build_distance_matrix(cities):
    n = len(cities)
    matrix = [[0.0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if i != j:
                matrix[i][j] = euclidean_distance(cities[i], cities[j])
    return matrix


def calculate_tour_length(chromosome, distance_matrix):
    total_length = 0.0
    n = len(chromosome)
    for i in range(n):
        city_from = chromosome[i]
        city_to = chromosome[(i + 1) % n]
        total_length += distance_matrix[city_from][city_to]
    return total_length


def fitness(chromosome, distance_matrix):
    length = calculate_tour_length(chromosome, distance_matrix)
    return 1.0 / length


def create_random_chromosome(num_cities):
    chromosome = list(range(num_cities))
    random.shuffle(chromosome)
    return chromosome


def create_initial_population(population_size, num_cities):
    population = []
    for _ in range(population_size):
        chromosome = create_random_chromosome(num_cities)
        population.append(chromosome)
    return population


def tournament_selection(population, fitness_scores, tournament_size):
    candidates_idx = random.sample(range(len(population)), tournament_size)
    best_idx = candidates_idx[0]
    for idx in candidates_idx[1:]:
        if fitness_scores[idx] > fitness_scores[best_idx]:
            best_idx = idx
    return population[best_idx][:]


def order_crossover(parent1, parent2):
    n = len(parent1)
    point1 = random.randint(0, n - 2)
    point2 = random.randint(point1 + 1, n - 1)
    child = [None] * n
    child[point1:point2 + 1] = parent1[point1:point2 + 1]
    inherited = set(child[point1:point2 + 1])
    p2_remaining = [city for city in parent2 if city not in inherited]
    fill_idx = 0
    for i in range(n):
        if child[i] is None:
            child[i] = p2_remaining[fill_idx]
            fill_idx += 1
    return child


def swap_mutation(chromosome):
    mutant = chromosome[:]
    idx1, idx2 = random.sample(range(len(mutant)), 2)
    mutant[idx1], mutant[idx2] = mutant[idx2], mutant[idx1]
    return mutant


def inversion_mutation(chromosome):
    mutant = chromosome[:]
    n = len(mutant)
    point1 = random.randint(0, n - 2)
    point2 = random.randint(point1 + 1, n - 1)
    mutant[point1:point2 + 1] = mutant[point1:point2 + 1][::-1]
    return mutant


def apply_mutation(chromosome, mutation_rate):
    if random.random() < mutation_rate:
        if random.random() < 0.5:
            return swap_mutation(chromosome)
        else:
            return inversion_mutation(chromosome)
    return chromosome[:]


def genetic_algorithm(cities, population_size=POPULATION_SIZE,
                      num_generations=NUM_GENERATIONS,
                      crossover_rate=CROSSOVER_RATE,
                      mutation_rate=MUTATION_RATE,
                      tournament_size=TOURNAMENT_SIZE,
                      elite_size=ELITE_SIZE):
    n = len(cities)
    distance_matrix = build_distance_matrix(cities)
    population = create_initial_population(population_size, n)

    best_chromosome = None
    best_distance = float('inf')
    convergence_history = []
    snapshot_chromosomes = []
    snapshot_interval = max(1, num_generations // 20)

    print(f"{'generation':>6} | {'best distance':>18} | {'avg distance':>18} | {'time (s)':>10}")
    print("-" * 60)

    start_time = time.time()

    for generation in range(num_generations):
        fitness_scores = [fitness(chrom, distance_matrix) for chrom in population]
        distances = [calculate_tour_length(chrom, distance_matrix) for chrom in population]

        gen_best_idx = distances.index(min(distances))
        gen_best_distance = distances[gen_best_idx]

        # save the best chromosome
        if gen_best_distance < best_distance:
            best_distance = gen_best_distance
            best_chromosome = population[gen_best_idx][:]

        convergence_history.append(best_distance)

        # Save path state for animation creation
        if generation % snapshot_interval == 0 or generation == num_generations - 1:
            snapshot_chromosomes.append(best_chromosome[:])

        if generation % 50 == 0 or generation == num_generations - 1:
            avg_dist = sum(distances) / len(distances)
            elapsed = time.time() - start_time
            print(f"{generation:>6} | {best_distance:>18.4f} | {avg_dist:>18.4f} | {elapsed:>10.2f}")

        sorted_indices = sorted(range(len(distances)), key=lambda i: distances[i])
        elites = [population[i][:] for i in sorted_indices[:elite_size]]

        new_population = elites[:]

        # crossover and mutation
        while len(new_population) < population_size:
            parent1 = tournament_selection(population, fitness_scores, tournament_size)
            parent2 = tournament_selection(population, fitness_scores, tournament_size)

            if random.random() < crossover_rate:
                child = order_crossover(parent1, parent2)
            else:
                child = parent1[:]

            child = apply_mutation(child, mutation_rate)
            new_population.append(child)

        population = new_population[:population_size]

    total_time = time.time() - start_time
    print(f"\nTotal execution time: {total_time:.2f} seconds")
    print(f"Best distance found: {best_distance:.4f}")

    return best_chromosome, best_distance, convergence_history, distance_matrix, snapshot_chromosomes


# Functions for charts and creating animations
def plot_convergence(convergence_history, num_cities):
    plt.figure(figsize=(10, 5))
    plt.plot(convergence_history, color='royalblue', linewidth=2, label='Best Distance')
    plt.title(f'Convergence Plot - TSP with Genetic Algorithm\n({num_cities} Cities)', fontsize=14)
    plt.xlabel('Generation', fontsize=12)
    plt.ylabel('Best Tour Length', fontsize=12)
    plt.legend(fontsize=11)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(f'convergence_plot_{num_cities}.png', dpi=300)
    plt.show()


def plot_best_tour(cities, best_chromosome, best_distance, num_cities):
    fig, ax = plt.subplots(figsize=(10, 8))
    tour_cities = [cities[i] for i in best_chromosome]
    tour_cities.append(tour_cities[0])
    xs = [c[0] for c in tour_cities]
    ys = [c[1] for c in tour_cities]
    ax.plot(xs, ys, 'r-', linewidth=1.5, alpha=0.7, zorder=1)

    cx = [c[0] for c in cities]
    cy = [c[1] for c in cities]
    ax.scatter(cx, cy, s=80, c='royalblue', zorder=3, edgecolors='navy', linewidths=0.8)

    for i, (x, y) in enumerate(cities):
        ax.annotate(str(i), (x, y), textcoords="offset points",
                    xytext=(5, 5), fontsize=7, color='darkblue')

    start_city = cities[best_chromosome[0]]
    ax.scatter(*start_city, s=150, c='green', zorder=4,
               edgecolors='darkgreen', linewidths=1.5, label='Start City')
    ax.set_title(f'Best TSP Tour - Genetic Algorithm\n'
                 f'{num_cities} Cities | Tour Length: {best_distance:.2f}', fontsize=14)
    ax.set_xlabel('X', fontsize=12)
    ax.set_ylabel('Y', fontsize=12)
    ax.legend(fontsize=11)
    ax.grid(True, alpha=0.2)
    plt.tight_layout()
    plt.savefig(f'Best TSP Tour_{num_cities}.png', dpi=300)
    plt.show()


def plot_tour_animation(cities, convergence_chromosomes, convergence_history, num_cities):
    fig, axes = plt.subplots(1, 2, figsize=(16, 7))
    ax_tour = axes[0]
    ax_conv = axes[1]

    cx = [c[0] for c in cities]
    cy = [c[1] for c in cities]

    ax_conv.plot(convergence_history, color='royalblue', linewidth=2)
    ax_conv.set_title(f'Convergence History ({num_cities} Cities)', fontsize=13)
    ax_conv.set_xlabel('Generation')
    ax_conv.set_ylabel('Best Tour Length')
    ax_conv.grid(True, alpha=0.3)
    vline = ax_conv.axvline(x=0, color='red', linestyle='--', linewidth=1.5)

    ax_tour.scatter(cx, cy, s=80, c='royalblue', zorder=3, edgecolors='navy', linewidths=0.8)
    line_tour, = ax_tour.plot([], [], 'r-', linewidth=1.5, alpha=0.7)
    title_tour = ax_tour.set_title('', fontsize=13)
    ax_tour.set_xlabel('X')
    ax_tour.set_ylabel('Y')
    ax_tour.grid(True, alpha=0.2)

    num_frames = len(convergence_chromosomes)
    gen_per_frame = len(convergence_history) // num_frames

    def update(frame):
        chrom = convergence_chromosomes[frame]
        tour = [cities[i] for i in chrom] + [cities[chrom[0]]]
        xs = [c[0] for c in tour]
        ys = [c[1] for c in tour]

        line_tour.set_data(xs, ys)

        gen_num = frame * gen_per_frame
        dist = convergence_history[min(gen_num, len(convergence_history) - 1)]
        title_tour.set_text(f'Generation {gen_num}  |  Distance: {dist:.2f}')
        vline.set_xdata([gen_num])

        return line_tour, title_tour, vline

    ani = animation.FuncAnimation(
        fig,
        update,
        frames=num_frames,
        interval=200,
        blit=False,
        repeat=False
    )

    plt.tight_layout()

    filename = f'tsp_animation_{num_cities}.gif'
    print(f"Saving Animation for {num_cities} cities as {filename} ....")
    ani.save(filename, writer='pillow', fps=5)
    print(f"Animation Saved: {filename}")
    plt.savefig(f'Animation_{num_cities}.png', dpi=300)
    plt.show()
    return ani

# compare different sizes of cities
def compare_city_counts():
    results = {}
    test_sizes = [20, 50, 100]

    for size in test_sizes:
        print(f"\n{'=' * 60}")
        print(f"Running GA for {size} Cities")
        print(f"{'=' * 60}")

        random.seed(RANDOM_SEED)
        np.random.seed(RANDOM_SEED)

        cities = generate_cities(size)

        best_chrom, best_dist, conv_history, distance_matrix, snapshot_chromosomes = genetic_algorithm(cities)

        results[size] = {
            'best_distance': best_dist,
            'history': conv_history,
            'chromosome': best_chrom,
            'cities': cities,
            'snapshots': snapshot_chromosomes
        }

        plot_convergence(conv_history, size)
        plot_best_tour(cities, best_chrom, best_dist, size)
        plot_tour_animation(cities, snapshot_chromosomes, conv_history, size)

    # Final comparison of convergence
    plt.figure(figsize=(12, 6))
    colors = ['royalblue', 'crimson', 'seagreen']
    for (size, color) in zip(test_sizes, colors):
        plt.plot(results[size]['history'], color=color, linewidth=2, label=f'{size} Cities')
    plt.title('Convergence Comparison - Different City Counts', fontsize=14)
    plt.xlabel('Generation', fontsize=12)
    plt.ylabel('Best Tour Length', fontsize=12)
    plt.legend(fontsize=12)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(f'Convergence Comparison.png', dpi=300)
    plt.show()

    # comparison of the best tours side by side
    fig, axes = plt.subplots(1, 3, figsize=(18, 6))
    for ax, size in zip(axes, test_sizes):
        r = results[size]
        tour = [r['cities'][i] for i in r['chromosome']] + [r['cities'][r['chromosome'][0]]]
        xs = [c[0] for c in tour]
        ys = [c[1] for c in tour]
        cx = [c[0] for c in r['cities']]
        cy = [c[1] for c in r['cities']]
        ax.plot(xs, ys, 'r-', linewidth=1.2, alpha=0.7)
        ax.scatter(cx, cy, s=50, c='royalblue', zorder=3, edgecolors='navy')
        ax.set_title(f'{size} Cities\nDist: {r["best_distance"]:.2f}', fontsize=12)
        ax.grid(True, alpha=0.2)
    plt.suptitle('Best Tours for Different City Counts', fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.savefig(f'Best Tours Comparison.png', dpi=300)
    plt.show()

    return results


if __name__ == "__main__":
    all_results = compare_city_counts()