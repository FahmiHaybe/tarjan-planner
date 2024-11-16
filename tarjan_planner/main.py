import logging
import re

from graph_builder import create_complete_graph, plot_route
from relatives_manager import RelativesManager, Relative
from route_planner import find_efficient_brute_force
from transports_manager import Transport, TransportsManager

# Configure logging
logging.basicConfig(
    filename='tarjan_planner.log',
    level=logging.ERROR,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)


def validate_input(prompt, pattern, error_message):
    while True:
        user_input = input(prompt).strip()
        if re.match(pattern, user_input):
            return user_input
        else:
            print(error_message)


def manage_entities(manager, entity_name, entity_class, fields):
    while True:
        print(f"\n{entity_name} Management Options:")
        print("1. Show all")
        print(f"2. Add a {entity_name}")
        print(f"3. Delete a {entity_name}")
        print("4. Go back")

        choice = validate_input("Choose an option (1-4): ", r"^[1-4]$",
                                "Invalid option. Please enter a number between 1 and 4.")

        if choice == '1':
            manager.show_all()
        elif choice == '2':
            entity_data = {field: input(f"Enter the {field}: ") for field in fields}
            new_entity = entity_class(**entity_data)
            manager.add(new_entity)
        elif choice == '3':
            name = input(f"Enter the name of the {entity_name} to delete: ")
            manager.delete(name)
        elif choice == '4':
            print("Returning to the main menu...")
            break


def main(mode, relatives, home, transports):
    G = create_complete_graph(relatives, home, transports, weight=mode)
    print("\nNetwork Statistics:")
    print(f"Number of locations: {G.number_of_nodes()}")
    print(f"Number of transport connections: {G.number_of_edges()}")

    total_weight = sum(d['weight'] for _, _, d in G.edges(data=True))
    print(f"Total network {mode}: {total_weight:.2f}")

    # Get the efficient route and transport modes
    tsp_route, transport_modes, min_time = find_efficient_brute_force(G, home.street_name)

    print("\nEfficient Route (TSP):")
    # Print each consecutive route segment and transport mode
    for i in range(len(tsp_route) - 1):
        start = tsp_route[i]
        end = tsp_route[i + 1]
        mode = transport_modes[i]
        print(f"From {start} to {end} using {mode}")

    print(f"Minimum time: {min_time:.2f}")

    plot_route(G, tsp_route)


if __name__ == "__main__":
    print("Welcome to the Tarjan Planner")
    relatives_manager = RelativesManager("relatives_file.json")
    transport_manager = TransportsManager("transport_modes.json")

    while True:
        try:
            print("\nOptions:")
            print("1. Find the most efficient route")
            print("2. Manage relatives")
            print("3. Manage transport modes")
            print("4. Quit")

            choice = validate_input("Choose an option (1-4): ", r"^[1-4]$",
                                    "Invalid option. Please enter a number between 1 and 4.")

            if choice == '1':
                input_mode = validate_input("Enter the weight for the graph edges (time or cost): ", r"^(time|cost)$",
                                            "Invalid weight. Please enter 'time' or 'cost'.")
                main(input_mode, relatives_manager.relatives, relatives_manager.home, transport_manager.transports)
            elif choice == '2':
                manage_entities(relatives_manager, "relative", Relative,
                                ["name", "street_name", "district", "lat", "lng"])
            elif choice == '3':
                manage_entities(transport_manager, "transport mode", Transport,
                                ["name", "speed_kmh", "transfer_time_min", "cost_per_km"])
            elif choice == '4':
                print("Exiting the planner. Goodbye!")
                break
        except KeyboardInterrupt:
            print("\nExiting the planner. Goodbye!")
            break
