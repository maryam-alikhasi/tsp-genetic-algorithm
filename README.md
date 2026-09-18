# Traveling Salesperson Problem with Genetic Algorithm

This project implements and visualizes the **Traveling Salesperson Problem (TSP)** using a **Genetic Algorithm (GA)**.

The goal is to find a short tour that visits every city exactly once and returns to the starting city. Since the number of possible tours grows factorially with the number of cities, a Genetic Algorithm is used to efficiently search for a near-optimal solution.

The project includes a complete implementation of the genetic algorithm from scratch, along with convergence plots, best-tour visualization, and an animation showing how the solution evolves across generations.

---

## Project Summary

* **Problem**: Traveling Salesperson Problem (TSP)
* **Optimization Method**: Genetic Algorithm
* **Representation**: Permutation-based chromosome
* **Distance Metric**: Euclidean Distance
* **Selection**: Tournament Selection
* **Crossover**: Order Crossover (OX)
* **Mutation**: Swap Mutation + Inversion Mutation
* **Elitism**: Top 10 individuals preserved in each generation
* **Visualization**: Matplotlib
* **Test Cases**: 20, 50, and 100 cities

---

## Problem Formulation

Each city is represented by a two-dimensional coordinate:

```text
(x, y)
```

For every pair of cities, the Euclidean distance is calculated:

```text
d(i, j) = √((xi - xj)² + (yi - yj)²)
```

A complete distance matrix is constructed before running the genetic algorithm.

A chromosome represents a complete tour as a permutation of city indices.

For example:

```text
[3, 1, 4, 2]
```

represents the tour:

```text
3 → 1 → 4 → 2 → 3
```

The distance from the last city back to the first city is also included when calculating the total tour length.

---

## Fitness Function

The objective of TSP is to minimize the total tour length.

Since the Genetic Algorithm uses a fitness value that should be maximized, the fitness function is defined as:

```text
Fitness = 1 / Tour Length
```

Therefore, shorter tours receive higher fitness values.

---

## Genetic Algorithm

The Genetic Algorithm consists of the following main steps:

```text
Generate Initial Population
          │
          ▼
Calculate Fitness
          │
          ▼
Tournament Selection
          │
          ▼
Order Crossover (OX)
          │
          ▼
Mutation
          │
          ▼
Elitism
          │
          ▼
Create New Generation
          │
          ▼
Repeat for Multiple Generations
```

The best solution found during the entire optimization process is stored and used to generate the final visualizations.

---

## Population Initialization

The initial population consists of randomly generated permutations of all cities.

Each chromosome contains every city exactly once, ensuring that the initial solutions satisfy the TSP constraint.

---

## Selection

The project uses **Tournament Selection**.

For each selection:

1. A random subset of individuals is selected.
2. Their fitness values are compared.
3. The individual with the highest fitness is selected as a parent.

The tournament size is set to:

```text
Tournament Size = 5
```

This selection method is used to choose both parents for crossover.

---

## Crossover

The project uses **Order Crossover (OX)**, which is designed for permutation-based problems such as TSP.

The process is:

1. Two random crossover points are selected.
2. A segment from the first parent is copied to the child.
3. The remaining positions are filled using cities from the second parent that are not already present in the copied segment.

This preserves the permutation constraint and prevents duplicate cities in the resulting chromosome.

The crossover probability is:

```text
Crossover Rate = 0.9
```

---

## Mutation

Two permutation-specific mutation operators are implemented:

### Swap Mutation

Two randomly selected cities exchange their positions.

```text
Before: [0, 1, 2, 3, 4]
After:  [0, 3, 2, 1, 4]
```

### Inversion Mutation

A randomly selected segment of the chromosome is reversed.

```text
Before: [0, 1, 2, 3, 4]
After:  [0, 3, 2, 1, 4]
```

For every mutation operation, the implementation randomly chooses between Swap Mutation and Inversion Mutation.

The mutation probability is:

```text
Mutation Rate = 0.05
```

---

## Elitism

To preserve high-quality solutions between generations, the best individuals are directly copied into the next generation.

The number of elite individuals is:

```text
Elite Size = 10
```

This helps prevent good solutions from being lost during crossover and mutation.

---

## Training Configuration

The main Genetic Algorithm parameters are:

| Parameter             | Value |
| --------------------- | ----: |
| Population Size       |   100 |
| Number of Generations |   500 |
| Crossover Rate        |   0.9 |
| Mutation Rate         |  0.05 |
| Tournament Size       |     5 |
| Elite Size            |    10 |
| Random Seed           |    42 |

The same random seed is used for reproducibility.

---

## Visualization

The project provides several visualizations to analyze the optimization process.

### 1. Convergence Plot

The convergence plot shows the best tour length discovered up to each generation.

```text
X-axis → Generation
Y-axis → Best Tour Length
```

This allows the improvement of the solution over generations to be observed.

### 2. Best Tour Visualization

The final best route is displayed on a two-dimensional coordinate plane.

The visualization shows:

* City locations
* Connections between cities
* City indices
* Starting city
* Final tour length

The resulting route is saved as an image for each tested number of cities.

### 3. Tour Animation

An animation is generated to show how the best tour changes throughout the optimization process.

The animation displays:

* The current best tour
* Current generation
* Current best distance
* Convergence history

The animation is saved as a GIF file.

---

## Comparison of Different Problem Sizes

To study the effect of the number of cities, the algorithm is tested with:

```text
20 Cities
50 Cities
100 Cities
```

For each problem size, the algorithm runs independently and generates:

* Convergence plot
* Best-tour visualization
* Tour animation

The project also produces comparison plots for the convergence behavior and final tours of the three problem sizes.

---

## Generated Outputs

The program generates output files such as:

```text
convergence_plot_20.png
convergence_plot_50.png
convergence_plot_100.png

Best TSP Tour_20.png
Best TSP Tour_50.png
Best TSP Tour_100.png

tsp_animation_20.gif
tsp_animation_50.gif
tsp_animation_100.gif

Convergence Comparison.png
Best Tours Comparison.png
```

---

## Technologies Used

* **Programming Language**: Python
* **Numerical Computing**: NumPy
* **Visualization**: Matplotlib
* **Animation**: Matplotlib Animation
* **Utilities**: Random, Math, Time

The Genetic Algorithm itself is implemented directly in the project rather than relying on a ready-made GA library.

---

## How to Run

### 1. Install Dependencies

```bash
pip install numpy matplotlib
```

### 2. Run the Project

```bash
python tsp_genetic_algorithm.py
```

The program automatically runs the algorithm for **20, 50, and 100 cities** and generates the corresponding visualizations and animations.

---

## Course Information

This project was developed as part of the **Computational Intelligence** course at the **University of Isfahan**, focusing on solving and visualizing the **Traveling Salesperson Problem (TSP)** using a Genetic Algorithm.