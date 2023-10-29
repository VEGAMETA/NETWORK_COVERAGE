import random
import matplotlib.pyplot as plt
from tower import Tower


class GridBlockEnum:
    EMPTY_UNCOVERED = 0
    EMPTY_COVERED = 1
    OBSTRUCTED_UNCOVERED = 2
    OBSTRUCTED_COVERED = 3
    TOWER = 4


class CityGrid:
    def __init__(self, n: int, m: int, obstructed_coverage: float = 0.5) -> None:
        self.n = n
        self.m = m
        self.grid: list[GridBlockEnum] = [
            [GridBlockEnum.EMPTY_UNCOVERED] * m for _ in range(n)
        ]
        self.obstructed_coverage = obstructed_coverage
        self.place_obstructed_blocks()
        self.towers: list[Tower] = []

    def place_obstructed_blocks(self) -> None:
        for i in range(self.n):
            for j in range(self.m):
                if random.random() < self.obstructed_coverage:
                    self.grid[i][j] = GridBlockEnum.OBSTRUCTED_UNCOVERED

    def place_tower(self, x: int, y: int, coverage_range: int) -> None:
        self.towers.append(Tower(x, y, coverage_range))
        self.grid[y][x] = GridBlockEnum.TOWER
        for i in range(max(0, x - coverage_range), min(x + coverage_range, self.m) + 1):
            for j in range(
                max(0, y - coverage_range), min(y + coverage_range, self.n) + 1
            ):
                try:
                    if self.grid[j][i] == GridBlockEnum.OBSTRUCTED_UNCOVERED:
                        self.grid[j][i] = GridBlockEnum.OBSTRUCTED_COVERED
                    elif self.grid[j][i] == GridBlockEnum.EMPTY_UNCOVERED:
                        self.grid[j][i] = GridBlockEnum.EMPTY_COVERED
                except IndexError:
                    pass

    def optimized_tower_placement(self, coverage_range):
        for _ in range(self.n * self.m):
            empty = 0
            obstructed = 0
            for i in range(self.n):
                for j in range(self.m):
                    if self.grid[i][j] == GridBlockEnum.EMPTY_UNCOVERED:
                        self.place_tower(j, i, coverage_range)

    def find_reliable_path(self, start_x, start_y, end_x, end_y):
        ...

    def visualize_coverage(self) -> None:
        plt.imshow(self.grid, cmap="viridis")
        colorbar = plt.colorbar(ticks=[0, 1, 2, 3, 4])
        colorbar.set_ticklabels(
            [
                "Empty Uncovered",
                "Empty Covered",
                "Obstructed Uncovered",
                "Obstructed Covered",
                "Tower",
            ]
        )
        for tower in self.towers:
            plt.plot(tower.x, tower.y, "ro")
            plt.gca().add_patch(
                plt.Rectangle(
                    (tower.x - tower.coverage, tower.y - tower.coverage),
                    2 * tower.coverage,
                    2 * tower.coverage,
                    fill=False,
                )
            )
            plt.xlim([-0.5, self.m - 0.5])
            plt.ylim([self.n - 0.5, -0.5])
            plt.xticks(range(self.m))
            plt.yticks(range(self.n))
            plt.tight_layout()
        plt.show()
