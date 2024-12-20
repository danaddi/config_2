import os
import subprocess

import yaml
import sys
from debian.debfile import DebFile


def extract_dependencies_from_deb(deb_file):
    """Извлекает зависимости из .deb файла."""
    if not os.path.exists(deb_file):
        raise FileNotFoundError(f"Файл {deb_file} не найден.")

    try:
        deb = DebFile(deb_file)
        control = deb.control
        if "Depends" in control:
            depends_str = control["Depends"]
            dependencies = [dep.split()[0] for dep in depends_str.split(", ")]
            return dependencies
        else:
            return []
    except Exception as e:
        raise RuntimeError(f"Ошибка извлечения зависимостей из {deb_file}: {e}")


def parse_yaml_config(config_path):
    """Чтение конфигурационного файла."""
    with open(config_path, "r") as file:
        config = yaml.safe_load(file)
    if "graph_visualizer" not in config or "package_file" not in config:
        raise ValueError("Конфигурационный файл должен содержать 'graph_visualizer' и 'package_file'.")
    return config


def generate_plantuml_graph(dependencies, package_name, output_file):
    """Создание графа зависимостей в формате PlantUML."""
    try:
        with open(output_file, "w") as file:
            file.write("@startuml\n")
            for dep in dependencies:
                file.write(f'"{package_name}" --> "{dep}"\n')
            file.write("@enduml\n")
        print(f"PlantUML файл создан: {output_file}")
    except Exception as e:
        raise RuntimeError(f"Ошибка создания PlantUML графа: {e}")


def visualize_graph(graph_visualizer, plantuml_file):
    """Визуализация графа с использованием PlantUML."""
    try:
        subprocess.run(["java", "-jar", graph_visualizer, plantuml_file], check=True)
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Ошибка при визуализации графа: {e}")


def main(config_path):
    """Основная функция."""
    try:
        # Чтение конфигурационного файла
        config = parse_yaml_config(config_path)
        package_file = config["package_file"]
        graph_visualizer = config["graph_visualizer"]

        # Проверка наличия PlantUML
        if not os.path.exists(graph_visualizer):
            raise FileNotFoundError(f"PlantUML не найден по пути: {graph_visualizer}")

        # Извлечение зависимостей
        print(f"Извлечение зависимостей из: {package_file}")
        dependencies = extract_dependencies_from_deb(package_file)

        # Генерация PlantUML графа
        package_name = os.path.basename(package_file)
        plantuml_file = "dependencies.puml"
        generate_plantuml_graph(dependencies, package_name, plantuml_file)

        # Визуализация графа
        print("Визуализация графа зависимостей...")
        visualize_graph(graph_visualizer, plantuml_file)

        print("Граф зависимостей успешно создан и визуализирован.")
    except Exception as e:
        print(f"Ошибка: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Использование: python dependency_visualizer.py <путь_к_конфигу_yaml>")
        sys.exit(1)
    main(sys.argv[1])
