import time

import pygame

pygame.font.init()

FPS = 60
WIDTH, HEIGHT = 400, 400
WHITE = (255, 255, 255)

WINDOWS = pygame.display.set_mode((WIDTH, HEIGHT))


def update_image(snake, check_point, lost_label=None):
    WINDOWS.fill(WHITE)
    for node in snake.nodes:
        node.update(WINDOWS)
    WINDOWS.blit(check_point.image, check_point.rect)
    if lost_label is not None:
        lost_label.draw(WINDOWS)
    pygame.display.update()


def handle_movement(snake, keys):
    from functions import change_direction, fix_position
    keys_directions = {
        pygame.K_UP: "up",
        pygame.K_DOWN: "down",
        pygame.K_LEFT: "left",
        pygame.K_RIGHT: "right"
    }

    for node in snake.nodes:

        if node.is_head:
            for key in keys_directions.keys():
                if keys[key]:
                    if ((node.direction == 'left' or node.direction == 'right') and (
                            keys_directions[key] == 'up' or keys_directions[key] == 'down')) or (
                            (node.direction == 'down' or node.direction == 'up') and (
                            keys_directions[key] == 'left' or keys_directions[key] == 'right')):
                        if node.direction != keys_directions[key]:
                            node.last_change_direction_x_coordinate = node.rect.x
                            node.last_change_direction_y_coordinate = node.rect.y

                            node.direction = keys_directions[key]

        else:
            # fix the position so as every node is attached to its parent
            if node.direction != node.parent.direction:
                if node.direction == 'right':
                    if node.rect.x >= node.parent.last_change_direction_x_coordinate:
                        change_direction(node)
                elif node.direction == 'left':
                    if node.rect.x <= node.parent.last_change_direction_x_coordinate:
                        change_direction(node)
                elif node.direction == 'up':
                    if node.rect.y <= node.parent.last_change_direction_y_coordinate:
                        change_direction(node)
                elif node.direction == 'down':
                    if node.rect.y >= node.parent.last_change_direction_y_coordinate:
                        change_direction(node)
            else:
                pass

        node.move(WINDOWS)


def game():
    """
    Function to run the game loop and handle game logic.

    Returns:
        None
    """

    # Import necessary modules and classes
    from objects import Snake, Node, CheckPoint, BigCheckPoint, Label
    from functions import check_if_snake_died, fix_position, stop_snake

    clock = pygame.time.Clock()
    run = True

    # Create initial nodes and snake
    head = Node()
    snake = Snake(head=head)
    node1 = Node(parent=head)
    node2 = Node(parent=node1)

    snake.nodes.append(node1)
    snake.nodes.append(node2)
    fix_position(node1)
    fix_position(node2)

    # Create label for "You lost" message
    lost_label = Label(x=WINDOWS.get_width() / 2 - 25, y=WINDOWS.get_height() / 2 - 12.5, width=50, height=25,
                       color=(255, 0, 0), text='You lost')

    # Add additional nodes to the snake
    for i in range(15):
        new_node = Node(parent=snake.nodes[-1])
        snake.nodes.append(new_node)
        fix_position(new_node)

    j = 0
    start = time.time()
    check_point = CheckPoint()
    draw_lost_label = False
    score = 0

    while run:
        j += 1
        clock.tick(FPS)

        # Check if the snake died
        if not draw_lost_label:
            if check_if_snake_died(snake):
                stop_snake(snake)
                start = time.time()
                draw_lost_label = True

        # Check if the current checkpoint is a BigCheckPoint and time elapsed since start > 3 seconds
        if check_point.__class__ == BigCheckPoint and time.time() - start > 3:
            check_point = CheckPoint()
            start = time.time()

        # Handle Pygame events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

        # Get the pressed keys
        keys = pygame.key.get_pressed()

        # Check if the snake head collides with the checkpoint
        if snake.head.rect.colliderect(check_point.rect):
            score += 1

            # If the checkpoint is a BigCheckPoint, add 4 new nodes to the snake
            if check_point.__class__ == BigCheckPoint:
                for i in range(4):
                    new_node = Node(parent=snake.nodes[-1])
                    new_node.direction = new_node.parent.direction
                    snake.nodes.append(new_node)
                    fix_position(new_node)

            # If the checkpoint is a regular CheckPoint, add 1 new node to the snake
            else:
                new_node = Node(parent=snake.nodes[-1])
                new_node.direction = new_node.parent.direction
                snake.nodes.append(new_node)
                fix_position(new_node)

            # Generate a new checkpoint
            if score % 5 != 0:
                check_point = CheckPoint()
            else:
                check_point = BigCheckPoint()
                start = time.time()

        # Handle snake movement based on pressed keys
        handle_movement(snake, keys)

        # Check if the "You lost" label is being displayed
        if draw_lost_label:
            if time.time() - start < 3:
                update_image(snake, check_point, lost_label)
            else:
                main()

        # Update the game display
        else:
            update_image(snake, check_point)


def main():
    from objects import Label, Button
    buttons = []
    label1 = Label(x=WINDOWS.get_width() / 2 - 100, y=10, width=200, height=50, text='Snake Game', color=(255, 0, 0))
    button1 = Button(x=WINDOWS.get_width() / 2 - 25, y=30 + label1.rect.height, width=50, height=30, text='Play',
                     color=(0, 0, 255), func=game)
    buttons.append(button1)
    background_image = pygame.image.load('snake.jpg')
    pygame.transform.scale(background_image, (WINDOWS.get_width(), WINDOWS.get_height()))

    run = True
    clock = pygame.time.Clock()
    while run:
        clock.tick(FPS)
        WINDOWS.fill(WHITE)
        label1.draw(WINDOWS)
        for button in buttons:
            button.draw(WINDOWS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            else:
                for button in buttons:
                    if button.handle_event(event):
                        run = False

        WINDOWS.blit(background_image,
                     (WINDOWS.get_width() / 2 - background_image.get_width() / 2, WINDOWS.get_height() / 2 - 50))
        pygame.display.update()


main()
