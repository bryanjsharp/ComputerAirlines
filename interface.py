import graph
import parse


def main_menu(graph):
    quit = False
    print("Bryan Sharp CS242 Assignment 2.0\n")
    while quit == False:
        response = input("(L)ist of cities, (C)ity information, (N)etwork information, " +
                         "(M)ap, (E)dit, (J)SON, (P)ath info, (Q)uit: ")
        if response == "Q":
            quit = True
        elif response == "L":
            graph.list_cities()
        elif response == "C":
            city_info_menu(graph)
        elif response == "N":
            network_menu(graph)
        elif response == "M":
            graph.get_map()
        elif response == "E":
            edit_menu(graph)
        elif response == "J":
            json_menu(graph)
        elif response == "P":
            path_menu(graph)


def city_info_menu(graph):
    done = False
    while done == False:
        response = input("Enter city code to get info: ")
        if response == "Q":
            done = True
        if response in graph.g:
            print(response)
            print(graph.get_name(response))
            print(graph.get_country(response))
            print(graph.get_continent(response))
            print(str(graph.get_timezone(response)))
            print(graph.get_coordinates(response))
            print(str(graph.get_population(response)))
            print(str(graph.get_region(response)))
            print(graph.get_routes(response))


def network_menu(graph):
    done = False
    while done == False:
        response = input("(LF) Longest Flight, (SF) Shortest Flight, (AD) Average Distance, " +
                         "(BC) Biggest City, (SC) Smallest City, (AS) Average Size, " +
                         "(LC) List of Continents, (HC) Hub Cities, (Q)uit)")
        if response == "LF":
            print(graph.get_longest_flight())
        elif response == "SF":
            print(graph.get_shortest_flight())
        elif response == "AD":
            print(graph.get_average_distance())
        elif response == "BC":
            print(graph.get_biggest_city())
        elif response == "SC":
            print(graph.get_smallest_city())
        elif response == "AS":
            print(graph.get_average_city_size())
        elif response == "LC":
            print(graph.get_continent_list())
        elif response == "HC":
            print(graph.get_hub_cities())
        elif response == "Q":
            done = True

def edit_menu(graph):
    done = False
    while not done:
        response = input("(RC) Remove City, (RR) Remove Route, (AC) Add City, " +
                         "(AR) Add Route, (E) Edit Existing City (Q) Quit: ")
        if response == "RC":
            graph.remove_city()
        elif response == "RR":
            graph.remove_route()
        elif response == "AC":
            graph.add_city()
        elif response == "AR":
            graph.add_route()
        elif response == "E":
            edit_city_menu(graph)
        elif response == "Q":
            done = True

def edit_city_menu(graph):
    done = False
    city = input("Enter City Code: ")
    if city in graph.g:
        while not done:
            response = input("(1) Name, (2) Country, (3) Continent, (4) Timezone, (5) Coordinates, " +
                             "(6) Population, (7) Region, (Q)uit: ")
            if response == "1":
                graph.edit_name(city)
            elif response == "2":
                graph.edit_country(city)
            elif response == "3":
                graph.edit_continent(city)
            elif response == "4":
                graph.edit_timezone(city)
            elif response == "5":
                graph.edit_coordinates(city)
            elif response == "6":
                graph.edit_population(city)
            elif response == "7":
                graph.edit_region(city)
            elif response == "Q":
                done = True

def json_menu(graph):
    done = False
    while not done:
        filename = input("Enter JSON filename or (Q) when finished: ")
        if filename == "Q":
            return
        read_or_write = input("(R)ead or (W)rite: ")
        if read_or_write == "R":
            parse.load_json(graph, filename)
        elif read_or_write == "W":
            parse.export_json(graph, filename)

def path_menu(graph):
    done = False
    while not done:
        response = input("(1) Shortest Path, (2) Route Information, (Q)uit: ")
        if response == "Q":
            done = True
        elif response == "1":
            graph.shortest_path()
        elif response == "2":
            print(graph.route_info())
        elif response == "99": #debug only
            graph.dijkstra(graph.g, "FIH", "CAI")


if __name__ == '__main__':
    graph = graph.Graph()
    json_menu(graph)
    main_menu(graph)
