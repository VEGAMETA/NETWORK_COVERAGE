from city import CityGrid

if __name__ == "__main__":
    city = CityGrid(15, 30, 0.6)
    city.optimized_tower_placement()
    city.visualize_coverage()
