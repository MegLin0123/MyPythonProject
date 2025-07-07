"""
stanCode Breakout Project
Adapted from Eric Roberts's Breakout by
Sonja Johnson-Yu, Kylie Jue, Nick Bowman, 
and Jerry Liao.

Provide a template of The Breakout Game including bricks, ball and paddle.
"""
from campy.graphics.gwindow import GWindow
from campy.graphics.gobjects import GOval, GRect, GLabel
from campy.gui.events.mouse import onmouseclicked, onmousemoved
import random

BRICK_SPACING = 5      # Space between bricks (in pixels). This space is used for horizontal and vertical spacing
BRICK_WIDTH = 40       # Width of a brick (in pixels)
BRICK_HEIGHT = 15      # Height of a brick (in pixels)
BRICK_ROWS = 10        # Number of rows of bricks
BRICK_COLS = 10        # Number of columns of bricks
BRICK_OFFSET = 50      # Vertical offset of the topmost brick from the window top (in pixels)
BALL_RADIUS = 10       # Radius of the ball (in pixels)
PADDLE_WIDTH = 75      # Width of the paddle (in pixels)
PADDLE_HEIGHT = 15     # Height of the paddle (in pixels)
PADDLE_OFFSET = 50     # Vertical offset of the paddle from the window bottom (in pixels)
INITIAL_Y_SPEED = 7    # Initial vertical speed for the ball
MAX_X_SPEED = 5        # Maximum initial horizontal speed for the ball


class BreakoutGraphics:

    def __init__(self, ball_radius=BALL_RADIUS, paddle_width=PADDLE_WIDTH, paddle_height=PADDLE_HEIGHT,
                 paddle_offset=PADDLE_OFFSET, brick_rows=BRICK_ROWS, brick_cols=BRICK_COLS, brick_width=BRICK_WIDTH,
                 brick_height=BRICK_HEIGHT, brick_offset=BRICK_OFFSET, brick_spacing=BRICK_SPACING, title='Breakout'):

        # Create a graphical window, with some extra space
        window_width = brick_cols * (brick_width + brick_spacing) - brick_spacing
        window_height = brick_offset + 3 * (brick_rows * (brick_height + brick_spacing) - brick_spacing)
        self.window = GWindow(width=window_width, height=window_height, title=title)

        # Create a paddle
        self.paddle = GRect(paddle_width, paddle_height, x=(window_width-paddle_width)/2, y=window_height-paddle_offset-paddle_height)
        self.paddle.filled = True
        self.window.add(self.paddle)

        # Center a filled ball in the graphical window
        self.ball = GOval(ball_radius*2, ball_radius*2, x=(window_width-ball_radius*2)/2, y=(window_height-ball_radius*2)/2)
        self.ball.filled = True
        self.window.add(self.ball)
        self._bw = ball_radius*2
        self._bh = ball_radius*2

        # Default initial velocity for the ball
        self.__dx = 0
        self.__dy = 0
        self.is_moving = False
        self._count = 1                # The count of the ball going back to the original position
        self._lives = 0
        self.remove_brick_count = 0   # The count of removing bricks

        # Initialize our mouse listeners
        onmouseclicked(self.set_ball_velocity)

        onmousemoved(self.change_position)
        self._pw = paddle_width
        self._ph = paddle_height
        self._ww = window_width
        self._wh = window_height
        self._po = paddle_offset

        # Draw bricks
        self._br = brick_rows
        self._bc = brick_cols
        self._bw = brick_width
        self._bh = brick_height
        self._bs = brick_spacing
        self._bo = brick_offset
        self.brick = GRect(brick_width, brick_height)
        self.set_bricks()

    def set_bricks(self):
        for i in range(self._br):
            for j in range(self._bc):
                self.brick = GRect(self._bw, self._bh, x=(self._bw+self._bs)*j, y=self._bo+(self._bh+self._bs)*i)
                self.brick.filled = True
                if i < 2:
                    self.brick.fill_color = 'red'
                    self.brick.color = 'red'
                elif 2 <= i < 4:
                    self.brick.fill_color = 'orange'
                    self.brick.color = 'orange'
                elif 4 <= i < 6:
                    self.brick.fill_color = 'yellow'
                    self.brick.color = 'yellow'
                elif 6 <= i < 8:
                    self.brick.fill_color = 'green'
                    self.brick.color = 'green'
                else:
                    self.brick.fill_color = 'blue'
                    self.brick.color = 'blue'
                self.window.add(self.brick)

    def change_position(self, event):         # The position of the paddle
        self.paddle.y = self._wh - self._po - self._ph
        if event.x < self._pw/2:
            self.paddle.x = 0
        elif event.x > self._ww - self._pw/2:
            self.paddle.x = self._ww - self._pw
        else:
            self.paddle.x = event.x - self._pw/2

    def set_ball_velocity(self, event):        # The velocity of the ball
        if not self.is_moving and self._count <= self._lives:
            self.is_moving = True
            self.__dy = INITIAL_Y_SPEED
            self.__dx = random.randint(1, MAX_X_SPEED)
            if random.random() > 0.5:
                self.__dx = -self.__dx

    def get_dx(self):
        return self.__dx

    def get_dy(self):
        return self.__dy

    def set_vx(self, vx):
        self.__dx = vx

    def set_vy(self, vy):
        self.__dy = vy

    def set_lives(self, lives):
        self._lives = lives

    def get_brick_rows(self):
        return self._br

    def get_brick_cols(self):
        return self._bc

    def collision(self):
        ball_top_left = self.window.get_object_at(self.ball.x, self.ball.y)
        ball_top_right = self.window.get_object_at(self.ball.x+self.ball.width, self.ball.y)
        ball_bottom_left = self.window.get_object_at(self.ball.x, self.ball.y+self.ball.height)
        ball_bottom_right = self.window.get_object_at(self.ball.x+self.ball.width, self.ball.y + self.ball.height)

        if ball_top_left is not None and ball_top_left is not self.paddle:
            self.window.remove(ball_top_left)
            self.remove_brick_count += 1
            self.__dy = -self.__dy
        elif ball_top_right is not None and ball_top_right is not self.paddle:
            self.window.remove(ball_top_right)
            self.remove_brick_count += 1
            self.__dy = -self.__dy
        elif ball_bottom_left is not None and ball_bottom_left is not self.paddle:
            self.window.remove(ball_bottom_left)
            self.remove_brick_count += 1
            self.__dy = -self.__dy
        elif ball_bottom_right is not None and ball_bottom_right is not self.paddle:
            self.window.remove(ball_bottom_right)
            self.remove_brick_count += 1
            self.__dy = -self.__dy
        elif ball_bottom_left is self.paddle or ball_bottom_right is self.paddle:
            self.__dy = -self.__dy
            if self.__dy > 0:
                self.__dy = -self.__dy

    def reset_ball(self):        # Reset the ball to the original position
        self.ball.x = (self._ww-self._bw)/2
        self.ball.y = (self._wh-self._bh)/2
        self.__dx = 0
        self.__dy = 0
        self.is_moving = False
        self._count += 1
        self.window.add(self.ball)
