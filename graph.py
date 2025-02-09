from collections import defaultdict, deque
from typing import List, Set, Dict, Tuple
import graphviz

class GridAnalyzer:
    def __init__(self, grid: List[List[str]], warehouse_ids: Set[str]):
        self.grid = grid
        self.height = len(grid)
        self.width = len(grid[0])
        self.warehouse_ids = warehouse_ids
        self.nodes = {}  # Armazena os nós do grafo
        self.node_types = {}  # Armazena o tipo de cada nó
        self.edges = []  # Armazena as arestas do grafo
        
    def is_valid_position(self, x: int, y: int) -> bool:
        return 0 <= x < self.width and 0 <= y < self.height
    
    def is_road(self, x: int, y: int) -> bool:
        return self.grid[y][x] == 'R'
    
    def is_building(self, x: int, y: int) -> bool:
        return self.grid[y][x].isdigit()
    
    def get_building_id(self, x: int, y: int) -> str:
        return self.grid[y][x] if self.is_building(x, y) else None
    
    def get_road_width(self, x: int, y: int) -> int:
        if not self.is_road(x, y):
            return 0
            
        width = 1
        temp_x = x + 1
        while temp_x < self.width and self.is_road(temp_x, y):
            width += 1
            temp_x += 1
            
        height = 1
        temp_y = y + 1
        while temp_y < self.height and self.is_road(x, temp_y):
            height += 1
            temp_y += 1
            
        return max(width, height)
    
    def find_buildings(self):
        """Identifica todos os prédios e suas entradas."""
        directions = [(0, -1), (1, 0), (0, 1), (-1, 0)]
        
        # Encontra todos os prédios únicos
        buildings = set()
        for y in range(self.height):
            for x in range(self.width):
                if self.is_building(x, y):
                    buildings.add((x, y, self.get_building_id(x, y)))
        
        # Para cada prédio, encontra o ponto de conexão com a estrada
        for x, y, building_id in buildings:
            # Procura uma estrada adjacente
            for dx, dy in directions:
                new_x, new_y = x + dx, y + dy
                if self.is_valid_position(new_x, new_y) and self.is_road(new_x, new_y):
                    node_id = f"building_{building_id}"
                    self.nodes[(new_x, new_y)] = node_id
                    self.node_types[node_id] = {
                        'type': 'building',
                        'id': building_id,
                        'is_warehouse': building_id in self.warehouse_ids
                    }
                    break
    
    def find_road_nodes(self):
        """Identifica todos os nós do grafo relacionados a estradas."""
        directions = [(0, -1), (1, 0), (0, 1), (-1, 0)]
        
        for y in range(self.height):
            for x in range(self.width):
                if not self.is_road(x, y):
                    continue
                    
                road_neighbors = 0
                for dx, dy in directions:
                    new_x, new_y = x + dx, y + dy
                    if self.is_valid_position(new_x, new_y) and self.is_road(new_x, new_y):
                        road_neighbors += 1
                
                current_width = self.get_road_width(x, y)
                node_type = None
                
                # Determina o tipo do nó
                if road_neighbors == 1:
                    node_type = 'end'
                elif road_neighbors in [3, 4]:
                    node_type = 'intersection'
                elif road_neighbors == 2:
                    # Verifica mudança de largura
                    for dx, dy in directions:
                        new_x, new_y = x + dx, y + dy
                        if self.is_valid_position(new_x, new_y) and self.is_road(new_x, new_y):
                            if self.get_road_width(new_x, new_y) != current_width:
                                node_type = 'width_change'
                                break
                
                if node_type:
                    node_id = f"node_{x}_{y}"
                    self.nodes[(x, y)] = node_id
                    self.node_types[node_id] = {
                        'type': node_type,
                        'width': current_width
                    }
    
    def connect_nodes(self):
        """Conecta os nós do grafo com arestas."""
        for node_pos in self.nodes:
            visited = set()
            queue = deque([(node_pos, 0)])
            
            while queue:
                current_pos, distance = queue.popleft()
                if current_pos in visited:
                    continue
                    
                visited.add(current_pos)
                x, y = current_pos
                
                if current_pos != node_pos and current_pos in self.nodes:
                    width = self.get_road_width(x, y)
                    self.edges.append((
                        self.nodes[node_pos],
                        self.nodes[current_pos],
                        width,
                        distance
                    ))
                    continue
                
                for dx, dy in [(0, -1), (1, 0), (0, 1), (-1, 0)]:
                    new_x, new_y = x + dx, y + dy
                    if (self.is_valid_position(new_x, new_y) and 
                        self.is_road(new_x, new_y) and 
                        (new_x, new_y) not in visited):
                        queue.append(((new_x, new_y), distance + 1))
    
    def generate_graphviz(self) -> str:
        """Gera a representação do grafo em formato Graphviz."""
        dot = graphviz.Graph(comment='Grid Graph')
        
        # Define estilos para diferentes tipos de nós
        dot.attr('node', shape='circle')  # estilo padrão
        
        # Adiciona nós com diferentes estilos baseados no tipo
        for pos, node_id in self.nodes.items():
            node_info = self.node_types[node_id]
            label = f"({pos[0]}, {pos[1]})"
            attrs = {}
            
            if node_info['type'] == 'building':
                attrs['shape'] = 'box'
                label = f"Building {node_info['id']}"
                if node_info['is_warehouse']:
                    attrs['style'] = 'filled'
                    attrs['fillcolor'] = 'lightblue'
                    label += "\n(Warehouse)"
            elif node_info['type'] == 'intersection':
                attrs['style'] = 'filled'
                attrs['fillcolor'] = 'yellow'
                label += "\nIntersection"
            elif node_info['type'] == 'width_change':
                attrs['style'] = 'filled'
                attrs['fillcolor'] = 'lightgreen'
                label += f"\nWidth: {node_info['width']}"
            elif node_info['type'] == 'end':
                attrs['style'] = 'filled'
                attrs['fillcolor'] = 'pink'
                label += "\nEnd"
            
            dot.node(node_id, label, **attrs)
        
        # Adiciona arestas
        for start, end, width, distance in self.edges:
            dot.edge(start, end, label=f"W:{width}, D:{distance}")
        
        return dot.source
    
    def analyze(self) -> str:
        """Executa a análise completa da grade."""
        self.find_buildings()
        self.find_road_nodes()
        self.connect_nodes()
        return self.generate_graphviz()

def create_example_grid():
    """Cria uma grade de exemplo para demonstração."""
    grid = [
        ['R', 'R', '1', '1', 'R'],
        ['R', 'R', '1', '1', 'R'],
        ['R', 'R', 'R', 'R', 'R'],
        ['2', '2', 'R', '3', '3'],
        ['2', '2', 'R', '3', '3']
    ]
    warehouse_ids = {'1', '3'}
    return grid, warehouse_ids

def visualize_grid(grid):
    """Função auxiliar para visualizar a grade no terminal."""
    for row in grid:
        print(' '.join(row))

def main():
    # Cria grade de exemplo
    grid, warehouse_ids = create_example_grid()
    
    # Mostra a grade no terminal
    print("Grade gerada:")
    visualize_grid(grid)
    
    # Cria o analisador
    analyzer = GridAnalyzer(grid, warehouse_ids)
    
    # Gera o código Graphviz
    graphviz_code = analyzer.analyze()
    
    # Cria um objeto Graphviz
    dot = graphviz.Source(graphviz_code)
    
    # Renderiza e salva o grafo
    dot.render("grid_graph", format="pdf", cleanup=True)
    dot.render("grid_graph", format="png", cleanup=True)
    
    print("\nGrafo gerado! Verifique os arquivos 'grid_graph.pdf' e 'grid_graph.png'")

if __name__ == "__main__":
    main()
