import math, enum
from constants import ONLY_LEFT
from classes.Map import Direction

avalible_dir = {
    Direction.TOP: [Direction.TOP, Direction.RIGHT],
    Direction.RIGHT: [Direction.RIGHT, Direction.BOTTOM],
    Direction.BOTTOM: [Direction.BOTTOM, Direction.LEFT],
    Direction.LEFT: [Direction.LEFT, Direction.TOP]
}


class Node:
    def __init__(self, **kwargs):
        self.parent = kwargs["parent"] if "parent" in kwargs else None
        self.pos = kwargs["pos"]
        self.branch = kwargs["branch"] if "branch" in kwargs else 1
        self.direction = kwargs["direction"] if "direction" in kwargs else None
        self.index = kwargs["index"] if "index" in kwargs else 0
        self.surrounded = [None] * 4
        self.children = [None] * 4

    def cost(self, car, dump):
        return math.floor((self.get_distance(dump)/2 + self.index) * 10) # self.get_distance(car)

    def get_distance(self, pos):
        return math.hypot(self.pos[0]-pos[0], self.pos[1]-pos[1])

    def get_surrounded(self, map):
        return map.get_surrounded(self.pos)

    def expand(self, index, car):
        new_node = Node(pos=self.get_surrounded(car.map)[index], parent=self, index=self.index+1, direction=[x for x in Direction][index], branch=self.branch + len([x for x in self.children if x]))
        self.children[index] = new_node
        car.all_nodes.append(self.children[index])
        car.nodes_to_render.append(self.children[index])
        if new_node.can_expand(car):
            car.expandable.append(new_node)
        if not self.can_expand(car) and self in car.expandable:
            car.expandable.remove(self)

    def can_expand(self, car):
        if self.parent:
            for i, x in enumerate(self.get_surrounded(car.map)):
                if self.can_expand_to(i, car):
                    return True
        return False

    def can_expand_to(self, index, car):
        dir = self.get_surrounded(car.map)[index]
        if len(dir) > 0:
            if dir != self.parent.pos and not self.children[index]:
                if [x for x in Direction][index] in avalible_dir[self.direction] or not ONLY_LEFT:
                    same_pos = [x for x in car.all_nodes if x.pos == self.pos and x != self]
                    if len(same_pos) > 0:
                        if same_pos[0].children[index] or same_pos[0].parent.pos == self.get_surrounded(car.map)[index]:
                            return False
                    return True

        return False
