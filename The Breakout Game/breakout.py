"""
stanCode Breakout Project
Adapted from Eric Roberts's Breakout by
Sonja Johnson-Yu, Kylie Jue, Nick Bowman,
and Jerry Liao.

File: breakout.py
Name: Meg
---------------------------
This program plays a game called
"The Breakout Game" in which players
using the paddle which can bounce back the ball
to clear the bricks
on screen to gain scores
"""

from campy.gui.events.timer import pause
from breakoutgraphics import BreakoutGraphics


FRAME_RATE = 10         # 100 frames per second
NUM_LIVES = 3			# Number of attempts


def main():
    graphics = BreakoutGraphics()
    vx = graphics.get_dx()
    vy = graphics.get_dy()
    lives = graphics.set_lives(NUM_LIVES)
    brick_rows = graphics.get_brick_rows()
    brick_cols = graphics.get_brick_cols()
    reset_count = 0

    # Add the animation loop here!
    while True:
        vx = graphics.get_dx()
        vy = graphics.get_dy()
        graphics.ball.move(vx, vy)
        if graphics.ball.x <= 0 or graphics.ball.x+graphics.ball.width >= graphics.window.width:
            vx = graphics.set_vx(-vx)
        if graphics.ball.y <= 0:
            vy = graphics.set_vy(-vy)
        if graphics.ball.y >= graphics.window.height:
            graphics.reset_ball()                                    # Reset the ball to the original position
            reset_count += 1
        pause(FRAME_RATE)
        graphics.collision()
        if graphics.remove_brick_count == brick_rows*brick_cols or reset_count == NUM_LIVES:
            break                                                                        # Remove all bricks or no lives
    if graphics.remove_brick_count == brick_rows*brick_cols:
        print('Win!')
    else:
        print('Game over!')


if __name__ == '__main__':
    main()
