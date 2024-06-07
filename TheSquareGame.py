import pygame as pg
import os

def load_sound(file):
    """Load a sound file from the given path."""
    full_path = os.path.join(os.path.dirname(__file__), file)
    if os.path.exists(full_path):
        return pg.mixer.Sound(full_path)
    else:
        print(f"Warning: Sound file '{file}' not found.")
        return None

programIcon = pg.image.load('tsqIcon.png')

pg.display.set_icon(programIcon)

def game_loop():
    """Main game loop."""
    global best_time

    pg.init()

    display_info = pg.display.Info()
    SCREEN_WIDTH = display_info.current_w - 100
    SCREEN_HEIGHT = display_info.current_h - 100

    screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pg.display.set_caption("The Square Game")

    player = pg.Rect(300, 250, 50, 50)
    enemy = pg.Rect(600, 250, 50, 50)

    clock = pg.time.Clock()
    start_time = pg.time.get_ticks()

    tick_rate = 60  # Initial tick rate
    tick_increase_interval = 10  # seconds
    tick_increase_amount = 50  # Increase the tick rate by 50 each time

    power_up_sound = load_sound('powerUp.wav')
    explosion_sound = load_sound('explosion.wav')
    music = load_sound('music.wav')

    # Play the music once here, before the game loop starts
    if not pg.mixer.music.get_busy():  # Check if music is already playing
        music.play(-1)  # The -1 means the music will loop indefinitely

    last_tick_increase_time = 0  # Keep track of the last time we increased the tick rate

    run = True
    while run:
        current_time = (pg.time.get_ticks() - start_time) / 1000  # Convert to seconds

        # Check if it's time to increase the tick rate
        if current_time - last_tick_increase_time >= tick_increase_interval:
            tick_rate += tick_increase_amount
            last_tick_increase_time = current_time
            if power_up_sound:
                power_up_sound.play()

        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False

        screen.fill((0, 0, 0))

        pg.draw.rect(screen, (0, 0, 255), player)
        pg.draw.rect(screen, (255, 0, 0), enemy)

        if player.colliderect(enemy):
            if explosion_sound:
                explosion_sound.play()
            run = False

        key = pg.key.get_pressed()
        if key[pg.K_a]:
            player.move_ip(-1, 0)
        if key[pg.K_d]:
            player.move_ip(1, 0)
        if key[pg.K_w]:
            player.move_ip(0, -1)
        if key[pg.K_s]:
            player.move_ip(0, 1)

        if key[pg.K_LEFT]:
            player.move_ip(-1, 0)
        if key[pg.K_RIGHT]:
            player.move_ip(1, 0)
        if key[pg.K_UP]:
            player.move_ip(0, -1)
        if key[pg.K_DOWN]:
            player.move_ip(0, 1)

        if player.left < 0:
            player.left = 0
        if player.right > SCREEN_WIDTH:
            player.right = SCREEN_WIDTH
        if player.top < 0:
            player.top = 0
        if player.bottom > SCREEN_HEIGHT:
            player.bottom = SCREEN_HEIGHT

        if pg.time.get_ticks() % 1000 < 500:
            if player.centerx > enemy.centerx:
                enemy.move_ip(1, 0)
            if player.centerx < enemy.centerx:
                enemy.move_ip(-1, 0)
            if player.centery > enemy.centery:
                enemy.move_ip(0, 1)
            if player.centery < enemy.centery:
                enemy.move_ip(0, -1)

        pg.display.flip()
        clock.tick(tick_rate)

    time_survived = current_time

    if time_survived > best_time:
        best_time = time_survived

    print(f"Time survived: {time_survived:.2f} seconds")
    print(f"Best time survived: {best_time:.2f} seconds")

    pg.quit()

best_time = 0
while True:
    game_loop()
    try_again = input("Do you want to try again? (yes/no): ")
    if try_again.lower() != "yes":
        break
