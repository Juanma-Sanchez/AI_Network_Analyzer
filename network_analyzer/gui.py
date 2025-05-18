import json
import pygame
from pygame.locals import *
from threading import Thread

class SimpleGui:
    def __init__(self, topology_file, network_status, window_height, window_width):
        with open(topology_file) as f:
            self.topology =json.load(f)
        self.network_status = network_status
        self.window_height = window_height
        self.window_width = window_width
        self.keep_drawing = True

    def blit_text(self, surface, text, pos, font, color=pygame.Color('black')):
        words = [word.split(' ') for word in text.splitlines()]  # 2D array where each row is a list of words.
        space = font.size(' ')[0]  # The width of a space.
        max_width, max_height = surface.get_size()
        x, y = pos
        for line in words:
            for word in line:
                word_surface = font.render(word, True, color)
                word_width, word_height = word_surface.get_size()
                if x + word_width >= max_width:
                    x = pos[0]  # Reset the x.
                    y += word_height  # Start on new row.
                surface.blit(word_surface, (x, y))
                x += word_width + space
            x = pos[0]  # Reset the x.
            y += word_height  # Start on new row

    def draw(self):
        pygame.init()
        self.screen = pygame.display.set_mode((self.window_width, self.window_height))
        self.background = pygame.Surface(self.screen.get_size())
        self.background.fill((255,255,255,255))
        self.router = pygame.image.load('resources/icons/router.jpg').convert_alpha()
        self.router = pygame.transform.scale(self.router, (60,60))
        self.font = pygame.font.SysFont('Courier New', 16)
        clock = pygame.time.Clock()
        while self.keep_drawing:
            pygame.event.get()
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
                    self.screen.blit(self.router, (node['position']['x'] - 30, node['position']['y'] - 30))
                    for vertex in node['vertices']:
                        rect = pygame.Rect(vertex['position']['x'] - 5, vertex['position']['y'] - 5, 10, 10)
                        try:
                            interface = self.network_status[node['id']][vertex['id']]
                            pygame.draw.rect(self.screen, (0,255,0) if interface['status'] == 'Normal' else (255,0,0), rect)
                            if rect.collidepoint(pygame.mouse.get_pos()):
                                self.screen.blit(
                                    self.font.render(f'Device: {node['id']}', True, (0,0,0)),
                                    (5, self.window_height - 160)
                                )
                                self.screen.blit(
                                    self.font.render(f'Interface: {vertex['id']}', True, (0,0,0)),
                                    (5, self.window_height - 140)
                                )
                                self.screen.blit(
                                    self.font.render(f'{interface['status']} since {interface['last_change']}', True, (0,0,0)),
                                    (5, self.window_height - 120)
                                )
                                self.screen.blit(
                                    self.font.render(f'Last input bandwidth: {interface['last_bandwidth_in']:.2f} bps', True, (0,0,0)),
                                    (5, self.window_height - 100)
                                )
                                self.screen.blit(
                                    self.font.render(f'Last output bandwidth: {interface['last_bandwidth_out']:.2f} bps', True, (0,0,0)),
                                    (5, self.window_height - 80)
                                )
                                self.blit_text(self.screen, interface['message'], (5, self.window_height - 60), self.font)
                        except:
                            pygame.draw.rect(self.screen, (255,0,0), rect)
            pygame.display.update()
            clock.tick(12)

    def launch(self):
        t = Thread(target=self.draw)
        t.start()
