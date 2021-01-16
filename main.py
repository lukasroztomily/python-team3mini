import pygame
import math
import random


# init
pygame.init()
w = 600
sidebar = 200
grid_length = 12
grid_from_settings = 12 # 8 / 12 / 20
grid_length = grid_from_settings
num_of_bombs = 34
flags = []
num_of_flags = 0
bomb_squares = []
discovered_squares = []
corner_squares = []
win = False
start_time = 0
ticking = 0
clock = pygame.time.Clock()
screen = pygame.display.set_mode((w + sidebar, w))
pygame.display.set_caption("minesweeper")
pygame.display.set_icon(pygame.image.load('bombicon.png'))
clicked = False #||
counter = 0 #||

# basic parameters
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GREY = (128, 128, 128)
YELLOW = (204, 204, 0)
PURPLE = (102, 0, 102)
BROWN = (102, 51, 0)
DARK_BLUE = (0, 0, 153)
MAROON = (102, 0, 0)
flag_img = pygame.image.load('flag.png')
bomb_img = pygame.image.load('bomb.png')
num_font = pygame.font.Font('freesansbold.ttf', 24)
text_font = pygame.font.Font('freesansbold.ttf', 16)
colour_number = {
    1: RED, 2: BLUE, 3: GREEN, 4: YELLOW, 5: PURPLE, 6: BROWN, 7: DARK_BLUE, 8: MAROON
}

# create grid
num_of_squares = int(math.pow(grid_length, 2))
spaces_remaining = num_of_squares - num_of_bombs
grid = [
    ['', '', '', '', '', '', '', '', '', '', '', ''],
    ['', '', '', '', '', '', '', '', '', '', '', ''],
    ['', '', '', '', '', '', '', '', '', '', '', ''],
    ['', '', '', '', '', '', '', '', '', '', '', ''],
    ['', '', '', '', '', '', '', '', '', '', '', ''],
    ['', '', '', '', '', '', '', '', '', '', '', ''],
    ['', '', '', '', '', '', '', '', '', '', '', ''],
    ['', '', '', '', '', '', '', '', '', '', '', ''],
    ['', '', '', '', '', '', '', '', '', '', '', ''],
    ['', '', '', '', '', '', '', '', '', '', '', ''],
    ['', '', '', '', '', '', '', '', '', '', '', ''],
    ['', '', '', '', '', '', '', '', '', '', '', '']
]


def load_bombs(avoid):
    remaining = num_of_bombs
    x = 0
    y = 0
    remaining_squares = num_of_squares - 1
    while remaining > 0:
        xy = x, y
        chance = random.randint(0, remaining_squares)
        if chance <= remaining and xy != avoid:
            grid[x][y] = "!"
            bomb_squares.append(xy)
            remaining -= 1
        remaining_squares -= 1
        if x < grid_length - 1:
            x += 1
        else:
            x = 0
            y += 1


def draw_grid_lines():
    for line in range(grid_length - 1):
        line_start = round((w / grid_length) * (line + 1))
        pygame.draw.line(screen, BLACK, (line_start, 0), (line_start, w), 6)
        pygame.draw.line(screen, BLACK, (0, line_start), (w, line_start), 6)

    # 4 Cary okolo okna
    pygame.draw.line(screen, BLACK, (0, 0), (0, w), 6)
    pygame.draw.line(screen, BLACK, (0, 0), (w, 0), 6)
    pygame.draw.line(screen, BLACK, (w, 0), (w, w), 6)
    pygame.draw.line(screen, BLACK, (0, w), (w, w), 6)


def draw_side_text():
    global ticking, capture
    text = "minesweeper"
    draw_text = text_font.render(text, True, MAROON)
    screen.blit(draw_text, (w + 30, 20))
    text = f"{grid_length} x {grid_length}"
    draw_text = text_font.render(text, True, MAROON)
    screen.blit(draw_text, (w + 30, 40))
    text = f"{spaces_remaining} spaces remaining"
    draw_text = text_font.render(text, True, BLACK)
    screen.blit(draw_text, (w + 20, 80))
    text = f"{num_of_bombs} bombs to avoid"
    draw_text = text_font.render(text, True, BLACK)
    screen.blit(draw_text, (w + 20, 110))
    ticking = str(round((pygame.time.get_ticks() - start_time) / 1000))
    if bombs_loaded and playing:
        text = ticking
    elif not playing:
        text = capture
    else:
        text = "0"
    draw_text = text_font.render(text, True, BLACK)
    screen.blit(draw_text, (w + 80, 150))
    text = "space bar to reset"
    draw_text = text_font.render(text, True, BLACK)
    screen.blit(draw_text, (w + 30, 560))
    text = "Basil Eagle 27/08/20"
    text = "Team 03"
    draw_text = text_font.render(text, True, BLACK)
    screen.blit(draw_text, (w + 30, 580))
    if num_of_flags > 0 and playing:
        text = f"{num_of_flags} flag(s) used"
        draw_text = text_font.render(text, True, BLACK)
        screen.blit(draw_text, (w + 20, 190))
        text = f"{num_of_bombs - num_of_flags} bomb(s) missing"
        draw_text = text_font.render(text, True, BLACK)
        screen.blit(draw_text, (w + 20, 220))
    if not playing:
        if win:
            text = "YOU WIN!"
            text_colour = GREEN
        else:
            text = "YOU LOSE!"
            text_colour = MAROON
        draw_text = text_font.render(text, True, text_colour)
        screen.blit(draw_text, (w + 30, 250))


# find what square the mouse is in
def find_grid_coords(x, y):
    found = False
    gridX = 0
    gridY = 0
    y_max = round(w / grid_length)
    y_min = 0
    while not found:
        x_max = round(w / grid_length)
        x_min = 0
        for space in range(grid_length):
            if x_max >= x >= x_min and y_max >= y >= y_min:
                return gridX, gridY
            else:
                x_min += round(w / grid_length)
                x_max += round(w / grid_length)
                gridX += 1
        gridX = 0
        y_max += round(w / grid_length)
        y_min += round(w / grid_length)
        gridY += 1


def update_grid():
    global flags, num_of_flags
    for x in range(grid_length):
        for y in range(grid_length):
            xy = x, y
            if xy in discovered_squares and xy not in bomb_squares:
                grid[x][y] = "O"
                if xy in flags:
                    flags.remove(xy)
                    num_of_flags -= 1
    remaining = 0
    for row in grid:
        for item in row:
            if item == '':
                remaining += 1
    return remaining


def get_flag(xy):
    global flags, num_of_flags
    if xy in flags:
        flags.remove(xy)
        num_of_flags -= 1
    else:
        flags.append(xy)
        num_of_flags += 1


# how many neighbours
def corner_number(x, y):
    bomb_neighbours = 0
    neighbours = [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1), (x + 1, y + 1), (x + 1, y - 1), (x - 1, y - 1),
                  (x - 1, y + 1)]
    for neighbour in neighbours:
        if neighbour in bomb_squares:
            bomb_neighbours += 1
    colour = colour_number.get(bomb_neighbours)
    return bomb_neighbours, colour


# draw graphics
def draw_graphics():
    size = round((w / grid_length) - 6)
    for xy in discovered_squares:
        x = xy[0]
        y = xy[1]
        draw_x = round((w / grid_length) * x) + 3
        draw_y = round((w / grid_length) * y) + 3
        pygame.draw.rect(screen, WHITE, (draw_x, draw_y, size, size))
    for xy in corner_squares:
        x = xy[0]
        y = xy[1]
        draw_x = round(((w / grid_length) * x) + 4)
        draw_y = round(((w / grid_length) * y) + 4)
        number, colour = corner_number(x, y)
        draw_number = num_font.render(str(number), True, colour)
        screen.blit(draw_number, (draw_x, draw_y))
    if playing:
        for xy in flags:
            x = xy[0]
            y = xy[1]
            draw_x = round(((w / grid_length) * x) + 8)
            draw_y = round(((w / grid_length) * y) + 8)
            screen.blit(flag_img, (draw_x, draw_y))
    else:
        for xy in bomb_squares:
            x = xy[0]
            y = xy[1]
            draw_x = round(((w / grid_length) * x) + 5)
            draw_y = round(((w / grid_length) * y) + 5)
            screen.blit(bomb_img, (draw_x, draw_y))


# find neighbouring empty squares
def uncover_squares(x, y):
    xy = x, y
    neighbours = [(x - 1, y), (x, y + 1), (x + 1, y), (x, y - 1), (x + 1, y + 1), (x + 1, y - 1), (x - 1, y - 1),
                  (x - 1, y + 1)]
    for neighbour in neighbours:
        if grid_length > neighbour[0] >= 0 and grid_length > neighbour[1] >= 0:
            if neighbour in bomb_squares and xy not in corner_squares:
                corner_squares.append(xy)
                break
            elif neighbour not in discovered_squares and neighbour not in bomb_squares:
                discovered_squares.append(neighbour)
                uncover_squares(neighbour[0], neighbour[1])


def reset():
    global start_time, playing, bombs_loaded, num_of_flags, spaces_remaining, win
    start_time = 0 
    playing = True
    bombs_loaded = False
    corner_squares.clear()
    discovered_squares.clear()
    bomb_squares.clear()
    flags.clear()
    num_of_flags = 0
    spaces_remaining = num_of_squares - num_of_bombs
    win = False
    for x in range(grid_length):
        for y in range(grid_length):
            grid[x][y] = ''


#||
def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)




class button():
		
	#colours for button and text
	button_col = (255, 0, 0)
	hover_col = (75, 225, 255)
	click_col = (50, 150, 255)
	text_col = BLACK
	button_width = 180
	button_height = 70

	def __init__(self, x, y, text):
		self.x = x
		self.y = y
		self.text = text

	def draw_button(self):

		global clicked
		action = False

		#get mouse position
		pos = pygame.mouse.get_pos()

		#create pygame Rect object for the button
		button_rect = pygame.Rect(self.x, self.y, self.button_width, self.button_height)
		
		#check mouseover and clicked conditions
		if button_rect.collidepoint(pos):
			if pygame.mouse.get_pressed()[0] == 1:
				clicked = True
				pygame.draw.rect(screen, self.click_col, button_rect)
			elif pygame.mouse.get_pressed()[0] == 0 and clicked == True:
				clicked = False
				action = True
			else:
				pygame.draw.rect(screen, self.hover_col, button_rect)
		else:
			pygame.draw.rect(screen, self.button_col, button_rect)
		
		#add shading to button
		pygame.draw.line(screen, WHITE, (self.x, self.y), (self.x + self.button_width, self.y), 2)
		pygame.draw.line(screen, WHITE, (self.x, self.y), (self.x, self.y + self.button_height), 2)
		pygame.draw.line(screen, BLACK, (self.x, self.y + self.button_height), (self.x + self.button_width, self.y + self.button_height), 2)
		pygame.draw.line(screen, BLACK, (self.x + self.button_width, self.y), (self.x + self.button_width, self.y + self.button_height), 2)

		#add text to button
		text_img = text_font.render(self.text, True, self.text_col)
		text_len = text_img.get_width()
		screen.blit(text_img, (self.x + int(self.button_width / 2) - int(text_len / 2), self.y + 25))
		return action






# ||
def game():
    global running, playing, bombs_loaded, capture

    # game loop
    running = True
    playing = True
    bombs_loaded = False

    while running:
        screen.fill(GREY)

        draw_grid_lines()
        draw_side_text()
        draw_graphics()
        
        mouseX, mouseY = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit() # Needed for cross button to quit correctly
                exit() 

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    reset()
            if event.type == pygame.MOUSEBUTTONDOWN and playing:
                if mouseX < w and pygame.mouse.get_pressed() == (1, 0, 0):
                    gridX, gridY = find_grid_coords(mouseX, mouseY)
                    gridXY = gridX, gridY
                    if not bombs_loaded:
                        load_bombs(gridXY)
                        bombs_loaded = True
                        start_time = pygame.time.get_ticks()
                    if gridXY not in discovered_squares:
                        if gridXY in bomb_squares:
                            win = False
                            playing = False
                            capture = ticking
                        else:
                            discovered_squares.append(gridXY)
                            uncover_squares(gridX, gridY)
                            spaces_remaining = update_grid()
                            if spaces_remaining < 1:
                                win = True
                                playing = False
                                capture = ticking

                elif mouseX < w and pygame.mouse.get_pressed() == (0, 0, 1):
                    gridX, gridY = find_grid_coords(mouseX, mouseY)
                    gridXY = gridX, gridY
                    if gridXY not in discovered_squares:
                        get_flag(gridXY)

        pygame.display.update()
        clock.tick(60)




#||
def main_menu():
    global w

    # Creating Buttons
    play_button = button(w/2, w/2-100, 'Play')
    options_button = button(w/2, w/2, 'Options')
    quit_button = button(w/2, w/2+100, 'Quit')


    while True:
        
        screen.fill((0,0,0))
        draw_text('Main Menu', text_font, (255, 255, 255), screen, 20, 20)


        if play_button.draw_button():
            game()
        if options_button.draw_button():
            options()
        if quit_button.draw_button():
            pygame.quit()
            exit()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    exit()

        pygame.display.update()
        clock.tick(60)



def options():
    global grid_from_settings

    # Creating Buttons
    small = button(w/2, w/2-100, 'Small')
    medium = button(w/2, w/2, 'Medium')
    high = button(w/2, w/2+100, 'High')


    running = True
    while running:

        screen.fill((0,0,0))

        # Text Options
        draw_text('Options', text_font, (255, 255, 255), screen, 20, 20)

        # Actions when button is clicked
        if small.draw_button():
            grid_from_settings = 8
            game()
        if medium.draw_button():
            grid_from_settings = 12
            game()
        if high.draw_button():
            grid_from_settings = 20
            game()



        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit() # Needed for cross button to quit correctly
                exit() 
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
        
        pygame.display.update()
        clock.tick(60)


if __name__ == '__main__':
    main_menu()