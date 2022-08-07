from random import choices, randint
from typing import TypeVar, List, Callable, Tuple, Optional

Genome = TypeVar("Genome")
Population = List[Genome]
RatedPopulation = List[Tuple[Genome, int]]
FitnessFunc = Callable[[Population], List[int]]
PopulateFunc = Callable[[], Population]
SelectionFunc = Callable[[RatedPopulation], Tuple[Genome, Genome]]
CrossoverFunc = Callable[[Genome, Genome], Tuple[Genome, Genome]]
MutationFunc = Callable[[Genome], Genome]
StatusFunc = Callable[[int, RatedPopulation], None]


def selection_pair(population: RatedPopulation) -> Tuple[Genome, Genome]:
    selection = choices(
        population=[p[0] for p in population],
        weights=[p[1] for p in population],
        k=2
    )
    return selection[0], selection[1]


def single_point_crossover(a: Genome, b: Genome) -> Tuple[Genome, Genome]:
    if len(a) != len(b):
        raise ValueError("Genomes a and b must be of same length")

    length = len(a)
    if length < 2:
        return a, b

    p = randint(1, length - 1)
    return a[0:p] + b[p:], b[0:p] + a[p:]


def run_evolution(
        populate_func: PopulateFunc,
        fitness_func: FitnessFunc,
        fitness_limit: int,
        selection_func: SelectionFunc,
        crossover_func: CrossoverFunc,
        mutation_func: MutationFunc,
        generation_limit: int = 100,
        status_func: Optional[StatusFunc] = None
) -> Tuple[Population, int]:
    population = populate_func()
    i = 0

    for i in range(generation_limit):

        fitness = fitness_func(population)
        rated_population = zip(population, fitness)
        rated_population = sorted(
            rated_population,
            key=lambda entry: entry[1],
            reverse=True
        )

        if status_func is not None:
            status_func(i, rated_population)

        if rated_population[0][1] >= fitness_limit:
            break

        next_generation = [p[0] for p in rated_population[0:2]]

        for j in range(int(len(population) / 2) - 1):
            parents = selection_func(rated_population)
            offspring_a, offspring_b = crossover_func(parents[0], parents[1])
            offspring_a = mutation_func(offspring_a)
            offspring_b = mutation_func(offspring_b)
            next_generation += [offspring_a, offspring_b]

        population = next_generation

    fitness = fitness_func(population)
    rated_population = zip(population, fitness)
    rated_population = sorted(
        rated_population,
        key=lambda entry: entry[1],
        reverse=True
    )

    return rated_population, i