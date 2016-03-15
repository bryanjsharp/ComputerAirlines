from unittest import TestCase
from graph import Graph
import parse
import os.path
import json


class TestGraph(TestCase):
    def test_init_empty(self):
        test = Graph()
        return test

    def test_init_full(self):
        test = Graph()
        parse.load_json(test, "data.json")
        return test

    def load_json_init(self):
        graph = Graph()
        if os.path.isfile('../data.json'):
            with open('../data.json') as data_file:
                data = json.load(data_file)
                parse.parse_routes(data, graph)
                parse.parse_info(data, graph)
        return graph

    def test_add_vertex(self):
        test = self.test_init_empty()
        test.add_vertex("A")
        self.assertEquals({'destinations': {}, 'info': {}}, test.g["A"])

    def test_add_edge(self):
        test = self.test_init_empty()
        test.add_edge("A", "B", 5)
        self.assertEquals({"B": 5}, test.g["A"]["destinations"])

    def test_get_distance(self):
        test = self.test_init_empty()
        test.add_edge("A", "B", 5)
        self.assertEqual(5, test.get_distance("A", "B"))

    def test_get_name(self):
        test = self.load_json_init()
        self.assertEqual("Chicago", test.get_name("CHI"))

    def test_get_country(self):
        test = self.load_json_init()
        self.assertEqual("US", test.get_country("CHI"))

    def test_get_continent(self):
        test = self.load_json_init()
        self.assertEqual("North America", test.get_continent("CHI"))

    def test_get_timezone(self):
        test = self.load_json_init()
        self.assertEqual("-6", test.get_timezone("CHI"))

    def test_get_coordinates(self):
        test = self.load_json_init()
        self.assertEqual("N: 42 W: 88", test.get_coordinates("CHI"))

    def test_get_population(self):
        test = self.load_json_init()
        self.assertEqual(9850000, test.get_population("CHI"))

    def test_get_region(self):
        test = self.load_json_init()
        self.assertEqual(3, test.get_region("CHI"))

    def test_add_info(self):
        # add info is called by load_json_init
        test = self.load_json_init()
        self.assertEqual("Chicago", test.get_name("CHI"))

    def test_get_longest_flight(self):
        test = self.load_json_init()
        self.assertEqual("SYD -> LAX: 12051", test.get_longest_flight())

    def test_get_shortest_flight(self):
        test = self.load_json_init()
        self.assertEqual("WAS -> NYC: 334", test.get_shortest_flight())

    def test_get_average_distance(self):
        test = self.load_json_init()
        self.assertEqual(2300.276595744681, test.get_average_distance())

    def test_get_biggest_city(self):
        test = self.load_json_init()
        self.assertEqual("Tokyo: 34000000", test.get_biggest_city())

    def test_get_smallest_city(self):
        test = self.load_json_init()
        self.assertEqual("Essen: 589900", test.get_smallest_city())

    def test_get_average_city_size(self):
        test = self.load_json_init()
        self.assertEqual(11796143.75, test.get_average_city_size())

    def test_recalculate_net_info(self):
        test = self.load_json_init()

    def test_delete_route(self):
        test = self.load_json_init()
        test.delete_route("SCL", "LIM")
        self.assertEqual(False, "LIM" in test.g["SCL"]["destinations"])
