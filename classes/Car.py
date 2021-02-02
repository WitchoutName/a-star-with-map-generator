from classes.Node import Node
from classes.Map import *
from constants import *
from pygame import locals
import math, pygame, time, sys

sign_of_dir = {
    Direction.TOP: "▲",
    Direction.RIGHT: "►",
    Direction.BOTTOM: "▼",
    Direction.LEFT: "◄",
    None: "none"
}

class Car:
    def __init__(self, map, window):
        self.map = map
        self.window = window
        self.path = None
        self.all_nodes = []
        self.expandable = []
        self.end = None
        self.nodes_to_render = []
        self.render_green = []
        pygame.font.init()
        self.font = pygame.font.SysFont('Arial', round(WINDOW_SIZE[0] / self.map.matrix.shape[0] / 2))
        self.finding = True
        self.image = pygame.transform.scale(self.map.display, WINDOW_SIZE)

    def get_lowest_node(self):
        temp_path = [*self.expandable]
        if len(temp_path) > 0:
            temp_path.sort(key=lambda x: x.cost(self.map.car, self.map.dump))
            return temp_path[0]
        else:
            return None

    def find_dump(self):
        self.path = Node(pos=self.map.car)
        self.all_nodes.append(self.path)
        [self.path.expand(i, self) for i, x in enumerate(self.path.get_surrounded(self.map)) if len(x) > 0]

        start_time = time.time()
        while self.finding:
            pygame.event.get()
            self.perform_turn()
            self.render_finding_state()

        if not self.map.solvable:
            print("Maze not solvable")
            return False
        else:
            print(f"steps: {self.end.index}, time: {round((time.time() - start_time) * 100) / 100}")
            node_list = self.get_path_nodes()
            start_time = time.time()
            index, increment, running = 0, True, True
            while running:
                for e in pygame.event.get():
                    if e.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if e.type == pygame.KEYDOWN:
                        if e.key == locals.K_SPACE:
                            running = False
                if time.time() - start_time > 1 / PLAY_BACK_SPEED:
                    start_time = time.time()
                    if increment:
                        index += 1
                        if index > len(node_list) - 1:
                            index -= 1
                            increment = False
                surf = pygame.transform.scale(self.map.display, WINDOW_SIZE)
                m = WINDOW_SIZE[0] / self.map.matrix.shape[0]
                for x in range(index+1):
                    color = color_of_object["%" if x == index else "/"]
                    pygame.draw.rect(surf, color, (node_list[x].pos[1] * m, node_list[x].pos[0] * m, m, m))
                    sign_surface = self.font.render(f"{node_list[x].index} {sign_of_dir[node_list[x].direction]}", False, (0, 0, 0))
                    surf.blit(sign_surface, (node_list[x].pos[1] * m, node_list[x].pos[0] * m + m/2, m, m))
                self.window.blit(surf, (0, 0))
                pygame.display.flip()
            return True

    def perform_turn(self):
        finding = True
        lowest = self.get_lowest_node()
        if lowest:
            for i, x in enumerate(lowest.get_surrounded(self.map)):
                if len(x) > 0 and lowest.can_expand_to(i, self):
                    lowest.expand(i, self)
                    if lowest.children[i].pos == self.map.dump:
                        finding = False
                        self.end = lowest.children[i]
        else:
            temp_path = [*self.all_nodes]
            temp_path.sort(key=lambda x: x.cost(self.map.car, self.map.dump))
            self.end = temp_path[0]
            finding = False
            self.map.solvable = False

        [self.expandable.remove(x) for x in self.expandable if not x.can_expand(self)]
        self.finding = finding

    def render_finding_state(self):
        #for node in self.render_green:
        #    self.render_node(node, "/")
        #    self.render_green.remove(node)

        for node in self.nodes_to_render:
            self.render_node(node, "/") #"%" if node.can_expand(self) else "/")
            self.nodes_to_render.remove(node)
            self.render_green.append(node)

        self.window.blit(self.image, (0, 0))
        pygame.display.flip()

    def render_node(self, node, sign):
        m = WINDOW_SIZE[0] / self.map.matrix.shape[0]
        color = color_of_object[sign]
        pygame.draw.rect(self.image, color, (node.pos[1] * m, node.pos[0] * m, m, m))
        if RENDER_DATA:
            text_surface = self.font.render(f"{math.floor(node.get_distance(self.map.dump) * 10) / 10} {node.index}",
                                        False, (0, 0, 0))
            sign_surface = self.font.render(f"{node.branch} {sign_of_dir[node.direction]}", False, (0, 0, 0))
            self.image.blit(text_surface, (node.pos[1] * m, node.pos[0] * m))
            self.image.blit(sign_surface, (node.pos[1] * m, node.pos[0] * m + m / 2))

    def get_path_nodes(self):
        final_list = [self.end]
        while final_list[0].parent:
            final_list.insert(0, final_list[0].parent)
        return final_list


