from city import CityGrid

if __name__ == "__main__":
    city = CityGrid(15, 30, 0.6)
    city.fill_empty_spaces(2)
    city.optimized_tower_placement()
    city.visualize_coverage()
    city.find_reliable_path(5, 5, 8, 8)
