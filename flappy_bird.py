# flappy_bird.py
import pygame
import neat
import time
import os
import bird
import pipe
import base

WINDOW_WIDTH, WINDOW_HEIGHT = 550, 800
BG_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bg.png")))
PIPE_GAP = 550
BASE_Y = 730

pygame.font.init()
STAT_FONT = pygame.font.SysFont("comicsans", 50)


def draw_window(window, birds, pipes, ground, score):
    window.blit(BG_IMG, (0, 0))
    for p in pipes:
        p.draw(window)

    text = STAT_FONT.render("Score: " + str(score), 1, (255, 255, 255))
    window.blit(text, (WINDOW_WIDTH - 10 - text.get_width(), 10))
    ground.draw(window)
    for fbird in birds:
        fbird.draw(window)
    pygame.display.update()


def main(genomes, config):
    nets = []
    ge = []
    birds = []

    for _, g in genomes:
        net = neat.nn.FeedForwardNetwork.create(g, config)
        nets.append(net)
        birds.append(bird.Bird(230, 350))
        g.fitness = 0
        ge.append(g)

    window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    ground = base.Base(BASE_Y)
    pipes = [pipe.Pipe(PIPE_GAP)]
    running = True
    clock = pygame.time.Clock()

    score = 0

    while running:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                quit()

        pipe_ind = 0
        if len(birds) > 0:
            if len(pipes) > 1 and birds[0].x > pipes[0].x + pipes[0].PIPE_TOP.get_width():
                pipe_ind = 1
        else:
            running = False
            break

        for i, fbird in enumerate(birds):
            fbird.move()
            ge[i].fitness += 0.1
            output = nets[i].activate(
                (fbird.y, abs(fbird.y - pipes[pipe_ind].height), abs(fbird.y - pipes[pipe_ind].bottom)))

            if output[0] > 0.5:
                fbird.jump()

        remove = []
        add_pipe = False
        for p in pipes:
            for i, fbird in enumerate(birds):
                if p.collide(fbird):
                    ge[i].fitness -= 1
                    birds.pop(i)
                    nets.pop(i)
                    ge.pop(i)

                if not p.passed and p.x < fbird.x:
                    p.passed = True
                    add_pipe = True

            if p.x + p.PIPE_TOP.get_width() < 0:
                remove.append(p)

            p.move()

        if add_pipe:
            score += 1
            for g in ge:
                g.fitness += 5
            pipes.append(pipe.Pipe(PIPE_GAP))

        for p in remove:
            pipes.remove(p)

        for i, fbird in enumerate(birds):
            if fbird.y + fbird.img.get_height() >= BASE_Y or fbird.y < 0:
                birds.pop(i)
                nets.pop(i)
                ge.pop(i)

        ground.move()
        draw_window(window, birds, pipes, ground, score)



def run(config_file):
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                                neat.DefaultSpeciesSet, neat.DefaultStagnation,
                                config_file)
    p = neat.Population(config)
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    winner = p.run(main, 50)


if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config-feedforward.txt")
    run(config_path)
