import sys
import heapq


class Graph:
    def __init__(self):
        # this is a dictionary that will hold dictionaries
        self.g = {}
        self.longestFlight = 0
        self.longestFlightSource = ""
        self.longestFlightDest = ""
        self.shortestFlight = sys.maxsize
        self.shortestFlightSource = ""
        self.shortestFlightDest = ""
        self.numRoutes = 0

    def add_vertex(self, key):
        if key in self.g:
            return
        else:
            self.g[key] = {}
            self.g[key]["destinations"] = {}
            self.g[key]["info"] = {}
        return

    # add edge as an edge to 'vertex' and add vertex as an edge to 'edge'
    def add_edge(self, source, dest, distance):
        if distance < self.shortestFlight:
            self.shortestFlight = distance
            self.shortestFlightSource = source
            self.shortestFlightDest = dest
        if distance > self.longestFlight:
            self.longestFlight = distance
            self.longestFlightSource = source
            self.longestFlightDest = dest
        if source not in self.g:
            self.add_vertex(source)
        if dest not in self.g:
            self.add_vertex(dest)
        if source in self.g:
            if dest not in self.g[source]["destinations"]:
                self.g[source]["destinations"][dest] = distance
                self.numRoutes += 1

    # returns the distance between destinations if it exists, otherwise returns -1
    def get_distance(self, source, dest):
        if source in self.g:
            if dest in self.g[source]["destinations"]:
                return self.g[source]["destinations"][dest]
        else:
            return -1

    def get_name(self, code):
        return self.g[code]["info"]["name"]

    def get_country(self, code):
        return self.g[code]["info"]["country"]

    def get_continent(self, code):
        return self.g[code]["info"]["continent"]

    def get_timezone(self, code):
        return str(self.g[code]["info"]["timezone"])

    def get_coordinates(self, code):
        coords = ""
        if "S" in self.g[code]["info"]["coordinates"]:
            coords = coords + "S :" + str(self.g[code]["info"]["coordinates"]["S"])
        elif "N" in self.g[code]["info"]["coordinates"]:
            coords = coords + "N: " + str(self.g[code]["info"]["coordinates"]["N"])
        coords = coords + " "
        if "E" in self.g[code]["info"]["coordinates"]:
            coords = coords + "E: " + str(self.g[code]["info"]["coordinates"]["E"])
        elif "W" in self.g[code]["info"]["coordinates"]:
            coords = coords + "W: " + str(self.g[code]["info"]["coordinates"]["W"])
        return coords

    def get_population(self, code):
        return self.g[code]["info"]["population"]

    def get_region(self, code):
        return self.g[code]["info"]["region"]

    # prints all routes to screen
    def get_routes(self, code):
        routes = "Routes from " + code + ": "
        for dest in self.g[code]["destinations"]:
            routes = routes + dest + ", "
        return routes

    # metro is a dictionary that contains: code, name, country, continent,
    # timezone, coordinaties, population and region
    def add_info(self, metro):
        self.g[metro["code"]]["info"] = metro.copy()

    def get_longest_flight(self):
        return self.longestFlightSource + " -> " + self.longestFlightDest + ": " + str(self.longestFlight)

    def get_shortest_flight(self):
        return self.shortestFlightSource + " -> " + self.shortestFlightDest + ": " + str(self.shortestFlight)

    def get_average_distance(self):
        totaldistance = 0
        totalroutes = 0
        for item in self.g:
            for r in self.g[item]["destinations"]:
                totaldistance += self.g[item]["destinations"][r]
                totalroutes += 1
        return totaldistance / totalroutes

    def get_biggest_city(self):
        biggestcity = 0
        biggestcityName = ""
        for city in self.g:
            if self.g[city]["info"]["population"] > biggestcity:
                biggestcity = self.g[city]["info"]["population"]
                biggestcityName = self.g[city]["info"]["name"]
        return biggestcityName + ": " + str(biggestcity)

    def get_smallest_city(self):
        smallestcity = sys.maxsize
        smallestcityName = ""
        for city in self.g:
            if self.g[city]["info"]["population"] < smallestcity:
                smallestcity = self.g[city]["info"]["population"]
                smallestcityName = self.g[city]["info"]["name"]
        return smallestcityName + ": " + str(smallestcity)

    def get_average_city_size(self):
        popOfAllCities = 0
        for city in self.g:
            popOfAllCities += self.g[city]["info"]["population"]

        return popOfAllCities / len(self.g)

    def get_continents_list(self):
        # go through list of airports and add them to the appropriate list
        northAmerica = []
        southAmerica = []
        europe = []
        africa = []
        asia = []
        australia = []
        for city in self.g:
            if self.g[city]["info"]["continent"] == "North America":
                northAmerica.append(self.g[city]["info"]["code"])
            elif self.g[city]["info"]["continent"] == "South America":
                southAmerica.append(self.g[city]["info"]["code"])
            elif self.g[city]["info"]["continent"] == "Europe":
                europe.append(self.g[city]["info"]["code"])
            elif self.g[city]["info"]["continent"] == "Africa":
                africa.append(self.g[city]["info"]["code"])
            elif self.g[city]["info"]["continent"] == "Asia":
                asia.append(self.g[city]["info"]["code"])
            elif self.g[city]["info"]["continent"] == "Australia":
                australia.append(self.g[city]["info"]["code"])
        return ("North America: " + ', '.join(northAmerica) +
                "\nSouth America: " + ', '.join(southAmerica) +
                "\nEurope: " + ', '.join(europe) +
                "\nAfrica: " + ', '.join(africa) +
                "\nAsia: " + ', '.join(asia) +
                "\nAustralia: " + ', '.join(australia))

    def list_cities(self):
        for key in self.g:
            print(key)

    def get_map(self):
        print("http://www.gcmap.com/mapui?P=", end="")
        for city in self.g:
            for dest in self.g[city]["destinations"]:
                print(city + "-" + dest + ",", end="")
        print('\n')

    # I define a hub city as a city with 5 or more destinations
    def get_hub_cities(self):
        hubCities = ""
        for city in self.g:
            if len(self.g[city]["destinations"]) > 4:
                hubCities = hubCities + " " + city
        return hubCities

    # this function needs to go through all routes and delete any refences to the selected city
    def remove_city(self):
        city = input("Enter City Code to Remove: ")
        if city in self.g:
            del self.g[city]
            # remove routes containing 'city'
            for source in self.g:
                if city in self.g[source]["destinations"]:
                    self.numRoutes -= len(self.g[source]["destinations"])
                    del self.g[source]["destinations"][city]
                    # recheck all the shortest/longest/biggest/smallest/etc
        self.recalculate_net_info()

    # recalculates network information
    def recalculate_net_info(self):
        shortest_route = 0
        longest_route = sys.maxsize
        shortest_source = ""
        shortest_dest = ""
        longest_source = ""
        longest_dest = ""
        num_routes = 0
        for city in self.g:
            for dest in self.g[city]["destinations"]:
                num_routes += 1
                if self.g[city]["destinations"][dest] < shortest_route:
                    shortest_route = self.g[city]["destinations"][dest]
                    shortest_source = city
                    shortest_dest = dest
                elif self.g[city]["destinations"][dest] > longest_route:
                    longest_route = self.g[city]["destinations"][dest]
                    longest_source = city
                    longest_dest = dest
        self.shortestFlight = shortest_route
        self.shortestFlightSource = shortest_source
        self.shortestFlightDest = shortest_dest
        self.longestFlight = longest_route
        self.longestFlightSource = longest_source
        self.longestFlightDest = longest_dest

    def add_city(self):
        city = input("Enter new city code: ")
        if city in self.g:
            print("City already exists.")
            return
        self.add_vertex(city)
        # prompt for remaining info
        self.g[city]["info"]["code"] = city
        self.g[city]["info"]["name"] = input("Enter full name of city: ")
        self.g[city]["info"]["country"] = input("Enter country code: ")
        self.g[city]["info"]["continent"] = input("Enter name of continent: ")
        self.g[city]["info"]["timezone"] = int(input("Enter timezone: "))
        lat = input("Latitude N or S?: ")
        lat_num = input("Latitude degree: ")
        while int(lat_num) < 0:
            print("invalid")
            lat_num = input("Latitude degree: ")
        long = input("Longitude E or W?: ")
        long_num = input("Longitude degree: ")
        while int(long_num) < 0:
            print("invalid")
            long_num = input("Longitude degree: ")
        coords = {}
        coords[lat] = lat_num
        coords[long] = long_num
        pop = int(input("Population: "))
        while int(pop) < 0:
            print("invalid")
            pop = int(input("Population: "))
        region = int(input("Region: "))
        while int(region) < 0:
            print("invalid")
            region = int(input("Region: "))
        self.g[city]["info"]["coordinates"] = coords
        self.g[city]["info"]["population"] = pop
        self.g[city]["info"]["region"] = region

    def add_route(self):
        source = input("Source city: ")
        dest = input("Destination city: ")
        distance = input("Distance: ")
        while int(distance) < 0:
            print("invalid")
            distance = input("Distance: ")
        self.add_edge(source, dest, int(distance))

    def edit_name(self, city):
        name = input("Enter new name: ")
        self.g[city]["info"]["name"] = name

    def edit_country(self, city):
        country = input("Enter new country: ")
        self.g[city]["info"]["country"] = country

    def edit_continent(self, city):
        continent = input("Enter new continent: ")
        self.g[city]["info"]["continent"] = continent

    def edit_timezone(self, city):
        timezone = int(input("Enter new timezone: "))
        self.g[city]["info"]["timezone"] = timezone

    def edit_coordinates(self, city):
        lat = input("N or S: ")
        if lat == "N" or lat == "S":
            lat_val = int(input("Latitude degree: "))
            if (lat_val.isdigit()):
                long = input("E or W: ")
                if lat == "E" or lat == "W":
                    long_val = int(input("Longitude degree: "))
                    if long_val.isdigit():
                        del self.g[city]["info"]["coordinates"]
                        self.g[city]["info"]["coordinates"] = {}
                        self.g[city]["info"]["coordinates"][lat] = lat_val
                        self.g[city]["info"]["coordinates"][long] = long_val
                        return

        print("invalid")

    def edit_population(self, city):
        pop = int(input("Enter new population: "))
        if pop.isdigit():
            self.g[city]["info"]["population"] = pop
            return
        print("invalid")

    def edit_region(self, city):
        region = int(input("Enter new region: "))
        if region.isdigit():
            self.g[city]["info"]["region"] = region
            return
        print("invalid")

    def remove_route(self):
        source = input("Enter source city code: ")
        if source in self.g:
            dest = input("Enter destination to remove: ")
            if dest in self.g[source]["destinations"]:
                self.delete_route(source, dest)
        print("invalid")

    def delete_route(self, source, dest):
        if dest in self.g[source]["destinations"]:
            del self.g[source]["destinations"][dest]
            self.numRoutes -= 1
            return
        print("invalid")

    # http://geekly-yours.blogspot.com/2014/03/dijkstra-algorithm-python-example-source-code-shortest-path.html
    def dijkstra(self, graph, src, dest, visited=[], distances={}, predecessors={}):
        try:
            """ calculates a shortest path tree routed in src
            """
            # a few sanity checks
            if src not in graph:
                raise TypeError('the root of the shortest path tree cannot be found in the graph')
            if dest not in graph:
                raise TypeError('the target of the shortest path cannot be found in the graph')
            # ending condition
            if src == dest:
                # We build the shortest path and display it
                path = []
                pred = dest
                while pred != None:
                    path.append(pred)
                    pred = predecessors.get(pred, None)
                print('shortest path: ' + str(path) + " cost=" + str(distances[dest]))
            else:
                # if it is the initial  run, initializes the cost
                if not visited:
                    distances[src] = 0
                # visit the neighbors
                for neighbor in graph[src]["destinations"]:
                    if neighbor not in visited:
                        new_distance = distances[src] + graph[src]["destinations"][neighbor]
                        if new_distance < distances.get(neighbor, float('inf')):
                            distances[neighbor] = new_distance
                            predecessors[neighbor] = src
                # mark as visited
                visited.append(src)
                # now that all neighbors have been visited: recurse
                # select the non visited node with lowest distance 'x'
                # run Dijskstra with src='x'
                unvisited = {}
                for k in graph:
                    if k not in visited:
                        unvisited[k] = distances.get(k, float('inf'))
                x = min(unvisited, key=unvisited.get)
                self.dijkstra(graph, x, dest, visited, distances, predecessors)
        except:
            print("impossible route")
            return

    def shortest_path(self):
        start = input("Enter start: ")
        target = input("Enter target: ")
        self.dijkstra(self.g, start, target)

    def route_info(self):
        route = []
        total_distance = 0
        total_price = 0
        price_per_km = 0.35
        total_time = 0
        layover_time = 2.0
        TOP_SPEED = 750

        while True:
            city = input("Enter City, (F)inish or (Q)uit: ")
            if city == "Q":
                return None
            elif city == "F":
                break
            else:
                if city in self.g:
                    if route:  # if route is not empty
                        if city in self.g[route[-1]]["destinations"]:
                            route.append(city)
                        else:
                            print("Invalid Route")
                            return None
                    else:
                        route.append(city)
                else:
                    print("Invalid city code")

        # get total distance
        for city in range(0, len(route) - 1):
            total_distance += self.get_distance(route[city], route[city + 1])
            total_price += (self.get_distance(route[city], route[city + 1]) * price_per_km)
            if price_per_km > 0.0:
                price_per_km -= .05
                # calculate time
                # using the formula t = (Vi + Vf) / (2*distance) for first and last part of flight
            if self.get_distance(route[city], route[city + 1]) >= 400:
                # accell and decel time
                total_time += 2 * (TOP_SPEED / (2 * 200))
                # constant speed time
                total_time += TOP_SPEED / self.get_distance(route[city], route[city + 1])
            else:
                total_time += 2 * (TOP_SPEED / (self.get_distance(route[city], route[city + 1])))
            total_time += layover_time - (.16666666 * len(self.g[route[city]]["destinations"]))
        format(total_time, '.2f')
        # print the info
        return str("Total Distance: " + str(total_distance) + " km" +
                   "\nTotal Cost:    $" + str(total_price) +
                   "\nTotal Time:     " + str('{:.2f}'.format(total_time)) + " hours")
