from unittest import TestCase
from graph import Graph
import parse
import os
import json


class TestParse(TestCase):
    def test_load_json(self):
        g = Graph()
        parse.load_json(g, "data.json")
        self.assertEquals("Chicago", g.g["CHI"]["info"]["name"])

    def test_parse_routes(self):
        g = Graph()
        with open('data.json') as data_file:
            data = json.load(data_file)
            parse.parse_routes(data, g)

        self.assertEqual(958, g.g["CHI"]["destinations"]["ATL"])

    def test_parse_info(self):
        g = Graph()
        with open('data.json') as data_file:
            data = json.load(data_file)
            parse.parse_routes(data, g)
            parse.parse_info(data, g)

        self.assertEqual("Chicago", g.g["CHI"]["info"]["name"])

    def test_export_json(self):
        g = Graph()
        test_graph = Graph()
        parse.load_json(g, "data.json")

        parse.export_json(g, "../output.json")
        parse.load_json(test_graph, "../output.json")
        self.assertEqual("Chicago", test_graph.g["CHI"]["info"]["name"])



