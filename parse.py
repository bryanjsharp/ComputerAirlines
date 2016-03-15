from graph import Graph
import json
import os.path


def load_json(graph, filename):
    if os.path.isfile(filename):
        with open(filename) as data_file:
            data = json.load(data_file)
            parse_routes(data, graph)
            parse_info(data, graph)


def parse_routes(data, graph):
    length = len(data["routes"])
    for i in range(0, length):
        # add the cities in the routes
        graph.add_vertex(data["routes"][i]["ports"][0])
        graph.add_vertex(data["routes"][i]["ports"][1])
        # Add destinations and distances to routes
        graph.add_edge(data["routes"][i]["ports"][0], data["routes"][i]["ports"][1],
                       data["routes"][i]["distance"])


def parse_info(data, graph):
    length = len(data["metros"])
    for i in range(0, length):
        graph.add_info(data["metros"][i])


def export_json(graph, filename):
    output = {}
    output["metros"] = []
    output["routes"] = []
    for city in graph.g:
        output["metros"].append(graph.g[city]["info"])
        for dest in graph.g[city]["destinations"]:
            output["routes"].append({"ports": [city, dest],
                                     "distance": graph.g[city]["destinations"][dest]})
    # export output to json
    if os.path.isfile(filename):
        with open(filename, "w+") as data_file:
            json.dump(output, data_file)
