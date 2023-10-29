from city import CityGrid

if __name__ == "__main__":
    city = CityGrid(3, 20, 0.8)
    city.optimized_tower_placement(2)
    city.visualize_coverage()
    city.find_reliable_path(5, 5, 8, 8)
