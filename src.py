import math
try:
    import pygame
except ImportError:
    print("Make sure you have python3 and pygame installed")

from parser import PythonParser


# Initialize the game engine
pygame.init()

display_width, display_height = 1000, 800
frames_per_second = 30

# Define some colors
white = (255, 255, 255)
red = (255, 0, 0)
blue = (0, 0, 255)
green = (0, 255, 0)
black = (0, 0, 0)

# Make the game window and update caption
game_display = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption("Code Flow Graph")

clock = pygame.time.Clock()


def render_text(text, x, y, size=15, color=black):
    font = pygame.font.Font('freesansbold.ttf', size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.center = (x, y)
    game_display.blit(text_surface, text_rect)


def drawGraph(graph_obj):
    height_diff = 90

    # Draw the nodes as circles and label them
    for node in graph_obj.nodes:
        pygame.draw.circle(
            game_display, green,
            (display_width//2, height_diff*(node+1)), 20
        )
        render_text(str(node), display_width//2, height_diff*(node+1), size=20)

    # Draw the edges, the two lines are for arrows (trial and error)
    # Straight edge if edge[1] - edge[0] == 1
    for edge in graph_obj.edges:
        if edge[1] < edge[0]:
            x = edge[0] - edge[1]
            pygame.draw.arc(
                game_display, black, [
                    display_width//2 - 30*x, height_diff*(edge[1]+1),
                    60*x, height_diff*x
                ],
                3/2*math.pi + 0.2,
                1/2*math.pi - (0.5875 - 0.282*x + 0.0395*x*x),
                2
            )
            pygame.draw.line(
                game_display, black,
                (display_width//2+19, height_diff*(edge[1]+1)+3),
                (display_width//2+25, height_diff*(edge[1]+1)+20-2*x),
                2
            )
            pygame.draw.line(
                game_display, black,
                (display_width//2+19, height_diff*(edge[1]+1)+2),
                (display_width//2+34, height_diff*(edge[1]+1)-3*x),
                2
            )
        else:
            x = edge[1] - edge[0]
            if x == 1:
                pygame.draw.line(
                    game_display, blue,
                    (display_width//2, height_diff*(edge[0]+1) + 15),
                    (display_width//2, height_diff*(edge[1]+1) - 20),
                    2
                )
                pygame.draw.line(
                    game_display, black,
                    (display_width//2, height_diff*(edge[1]+1)-20),
                    (display_width//2-10, height_diff*(edge[1]+1)-35),
                    2
                )
                pygame.draw.line(
                    game_display, black,
                    (display_width//2, height_diff*(edge[1]+1)-20),
                    (display_width//2+10, height_diff*(edge[1]+1)-35),
                    2
                )
            else:
                pygame.draw.arc(
                    game_display, red, [
                        display_width//2 - 30*x, height_diff*(edge[0]+1),
                        60*x, height_diff*x
                    ],
                    1/2*math.pi + 0.2,
                    3/2*math.pi - (0.5875 - 0.282*x + 0.0395*x*x),
                    2
                )
                pygame.draw.line(
                    game_display, black,
                    (display_width//2-19, height_diff*(edge[1]+1)-8),
                    (display_width//2-34, height_diff*(edge[1]+1)+3*x),
                    2
                )
                pygame.draw.line(
                    game_display, black,
                    (display_width//2-19, height_diff*(edge[1]+1)-2),
                    (display_width//2-25-x, height_diff*(edge[1]+1)-20+2*x),
                    2
                )
            # Labelling the edges when there are more than one edge
            if sum(graph_obj.adj_matrix[edge[0]-1]) > 1:
                if edge[1]-1 == graph_obj.adj_matrix[edge[0]-1].index(1):
                    # 'T' label is always going to be next of a straight line
                    render_text(
                        'T', display_width//2 - 10,
                        height_diff*(edge[0]+1)+50*x
                    )
                else:
                    render_text(
                        'F', display_width//2 - 30*x - 10,
                        height_diff*(edge[0]+1)+45*x
                    )


def main():

    closed = False
    graph_obj = PythonParser('test.py').construct_graph()
    graph_obj.print()

    while not closed:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                closed = True

        # graph_obj.print()
        game_display.fill(white)
        drawGraph(graph_obj)

        pygame.display.update()
        clock.tick(60)

    pygame.quit()
    quit()


if __name__ == '__main__':
    main()
