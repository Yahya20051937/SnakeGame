import pygame


def check_limits(func):
    """
    This function is used to keep the snake always on the screen
    :param func:
    :return:
    """

    def wrapper(node, windows):

        if node.rect.x > windows.get_width():
            node.out_of_screen = True
            node.rect.x = 0
        elif node.rect.x < 0:
            node.rect.x = windows.get_width()
            node.out_of_screen = True
        elif node.rect.y > windows.get_height():
            node.rect.y = 0
            node.out_of_screen = True
        elif node.rect.y < 0:
            node.rect.y = windows.get_height()
            node.out_of_screen = True
        else:
            func(node, windows)

    return wrapper


def change_direction(node):
    node.direction = node.parent.direction
    node.last_change_direction_x_coordinate = node.rect.x
    node.last_change_direction_y_coordinate = node.rect.y


def fix_position(node):

    if node.direction == node.parent.direction:
        if node.direction == 'right':
            node.rect.x = node.parent.rect.x - node.WIDTH
            node.rect.y = node.parent.rect.y
        elif node.direction == 'left':
            node.rect.x = node.parent.rect.x + node.WIDTH
            node.rect.y = node.parent.rect.y
        elif node.direction == 'down':
            node.rect.y = node.parent.rect.y - node.HEIGHT
            node.rect.x = node.parent.rect.x
        elif node.direction == 'up':
            node.rect.y = node.parent.rect.y + node.HEIGHT
            node.rect.x = node.parent.rect.x


def check_if_snake_died(snake):
    head = snake.head

    if head.direction == 'right':
        for node in snake.nodes[1:]:
            if head.rect.x + head.rect.width == node.rect.x and node.rect.y <= head.rect.y <= node.rect.y + node.rect.height:  # the coordinate of the top right corner of the head should be equal to the top left corner of  the node, and both y coordinates should be equal
                return True
    elif head.direction == 'left':
        for node in snake.nodes[1:]:
            if head.rect.x == node.rect.x + node.rect.width and node.rect.y <= head.rect.y <= node.rect.y + node.rect.height:  # the coordinate of the top left corner must be equal to the coordinate of the top right corner of the node, and the y coordinate should be equal
                return True
    elif head.direction == 'down':
        for node in snake.nodes[1:]:
            if head.rect.y + head.rect.height == node.rect.y and node.rect.x <= head.rect.x <= node.rect.x + node.rect.width:  # the bottom left corner of  the head should be equal to the top left corner of the node, and both x coordinates should be equal
                return True
    elif head.direction == 'up':
        for node in snake.nodes[1:]:
            if head.rect.y == node.rect.y + node.rect.height and node.rect.x <= head.rect.x <= node.rect.x + node.rect.width:  # the top left corner of  the head should be equal to the bottom left corner of the node, and both x coordinates should be equal
                return True
    return False


def stop_snake(snake):
    for node in snake.nodes:
        node.right[1] = 0
        node.left[1] = 0
        node.up[1] = 0
        node.down[1] = 0




