import unittest

from main import *


class TestDependencyVisualizer(unittest.TestCase):

    def test_parse_yaml_config(self):
        config_content = """
        graph_visualizer: "/path/to/plantuml.jar"
        package_name: "test_package"
        """
        with open("test_config.yaml", "w") as file:
            file.write(config_content)
        config = parse_yaml_config("test_config.yaml")
        self.assertEqual(config["graph_visualizer"], "/path/to/plantuml.jar")
        self.assertEqual(config["package_name"], "test_package")

    def test_generate_plantuml_graph(self):
        dependencies = {"pkg1": {"pkg2": {}, "pkg3": {}}, "pkg4": {}}
        plantuml_content = generate_plantuml_graph(dependencies)
        self.assertIn("pkg1 --> pkg2", plantuml_content)
        self.assertIn("pkg1 --> pkg3", plantuml_content)
        self.assertIn("pkg4", plantuml_content)

    def test_get_package_dependencies(self):
        dependencies = get_package_dependencies("nonexistent_package")
        self.assertEqual(dependencies, {})