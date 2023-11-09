import random
from typing import Optional

import matplotlib.pyplot as plt
from tower import Tower

random.seed(0)


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
        self.grid: list = [[GridBlockEnum.EMPTY_UNCOVERED] * m for _ in range(n)]
        self.obstructed_coverage = obstructed_coverage
        self.place_obstructed_blocks()
        self.towers: list[Tower] = []

    def place_obstructed_blocks(self) -> None:
        for i in range(self.n):
            for j in range(self.m):
                if random.random() < self.obstructed_coverage:
                    self.grid[i][j] = GridBlockEnum.OBSTRUCTED_UNCOVERED

    def place_tower(self, x: int = 0, y: int = 0, coverage_range: int = 0, tower: Optional[Tower] = None) -> None:
        if tower:
            self.towers.append(tower)
            self.grid[tower.y][tower.x] = GridBlockEnum.TOWER
        else:
            self.towers.append(Tower(x, y, coverage_range))
            self.grid[y][x] = GridBlockEnum.TOWER

    def count_coverage(self):
        for tower in self.towers:
            for i in range(max(0, tower.x - tower.coverage_range), tower.x + tower.coverage_range + 1):
                for j in range(max(0, tower.y - tower.coverage_range), tower.y + tower.coverage_range + 1):
                    try:
                        if self.grid[j][i] == GridBlockEnum.OBSTRUCTED_UNCOVERED:
                            self.grid[j][i] = GridBlockEnum.OBSTRUCTED_COVERED
                        elif self.grid[j][i] == GridBlockEnum.EMPTY_UNCOVERED:
                            self.grid[j][i] = GridBlockEnum.EMPTY_COVERED
                    except IndexError:
                        pass

    def clear_coverage(self):
        for i in range(self.n):
            for j in range(self.m):
                if self.grid[i][j] is GridBlockEnum.OBSTRUCTED_COVERED:
                    self.grid[i][j] = GridBlockEnum.OBSTRUCTED_UNCOVERED
                if self.grid[i][j] is GridBlockEnum.EMPTY_COVERED:
                    self.grid[i][j] = GridBlockEnum.EMPTY_UNCOVERED

    def count_empty_uncovered(self):
        return sum([line.count(GridBlockEnum.EMPTY_UNCOVERED) for line in self.grid])

    def optimized_tower_placement(self):
        towers_amount = len(self.towers) - 1
        while towers_amount >= 0:
            popped_tower = self.towers.pop(towers_amount)
            self.grid[popped_tower.y][popped_tower.x] = GridBlockEnum.EMPTY_UNCOVERED
            self.clear_coverage()
            self.count_coverage()
            if self.count_empty_uncovered() > 0:
                self.place_tower(tower=popped_tower)
            towers_amount -= 1

    def fill_empty_spaces(self, coverage_range):
        for i in range(self.n):
            for j in range(self.m):
                if self.grid[i][j] in (GridBlockEnum.EMPTY_UNCOVERED, GridBlockEnum.EMPTY_COVERED):
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
                    (tower.x - tower.coverage_range, tower.y - tower.coverage_range),
                    2 * tower.coverage_range,
                    2 * tower.coverage_range,
                    fill=False,
                )
            )
            plt.xlim([-0.5, self.m - 0.5])
            plt.ylim([self.n - 0.5, -0.5])
            plt.xticks(range(self.m))
            plt.yticks(range(self.n))
            plt.tight_layout()
        plt.show()
