import json
import pygame
from threading import Thread

class SimpleGui:
    def __init__(self, topology_file, network_graph, window_height, window_width):
        with open(topology_file) as f:
            self.topology =json.load(f)
        self.network_graph = network_graph
        pygame.init()
        self.screen = pygame.display.set_mode((window_width, window_height))
        self.background = pygame.Surface(self.screen.get_size())
        self.background.fill((255,255,255))
        self.router = pygame.image.load('resources/icons/router.jpg').convert_alpha()
        self.router = pygame.transform.scale(self.router, (40,40))
        self.font = pygame.font.SysFont('Courier New', 24)

    def draw(self):
        self.screen.blit(self.background, (0,0))
        for edge in self.topology['edges']:
            for node in self.topology['nodes']:
                for vertex in node['vertices']:
                    if edge['source']['node'] == node['id'] and edge['source']['vertex'] == vertex['id']:
                        start_pos = vertex['position']['x'],vertex['position']['y']
                    elif edge['destination']['node'] == node['id'] and edge['destination']['vertex'] == vertex['id']:
                        end_pos = vertex['position']['x'],vertex['position']['y']
            pygame.draw.line(self.screen, (0,0,0), start_pos, end_pos)
        for node in self.topology['nodes']:
            if node['type'] == 'router':
                self.screen.blit(self.router, (node['position']['x'] - 20,node['position']['y'] - 20))
                for vertex in node['vertices']:
                    rect = pygame.Rect(vertex['position']['x'] - 5, vertex['position']['y'] - 5, 10, 10)
                    try:
                        interface = self.network_graph[node['id']][vertex['id']]
                        pygame.draw.rect(self.screen, (0,255,0) if interface['status'] == 'Normal' else (255,0,0), rect)
                        if rect.collidepoint(pygame.mouse.get_pos()):
                            print(node['id'], vertex['id'], interface)
                    except:
                        pygame.draw.rect(self.screen, (255,0,0), rect)
        pygame.display.update()
