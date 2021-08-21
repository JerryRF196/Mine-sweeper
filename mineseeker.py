# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import pygame, sys, random
pygame.init()

# =============================================================================
# Objetos
# =============================================================================

class Cell():
    def __init__(self, pos_x, pos_y):
        self.size = 35
        self.x = pos_x + 5
        self.y = pos_y + 5
        self.pressed = False
        self.bomb = False
        self.flag = False
        self.activated = False
        self.number = None
        self.drawn = True

    
    def draw(self):
        pygame.draw.rect(screen, self.colour, (self.x , self.y , self.size, self.size))
        if self.flag:
            Draw_flag(self.x, self.y + 2)
        if self.activated:
            if self.bomb:
                Draw_bomb(black, self.x + 2, self.y + 2)
            elif self.number:
                Draw_text(screen, str(self.number), 40, colour_list[self.number], self.x + self.size/2, self.y - 5)

    def update(self, mouse):
        if self.activated:
            self.colour = (220,220,220)
        else:
            if (mouse[0] in range(int(self.x), int(self.x + self.size))
            and (mouse[1] in range (int(self.y), int(self.y + self.size)))):
                self.colour = colour2
            else:
                self.colour = colour1
            
        

class Button():
    def __init__(self, x, y, button_width, button_height, text, size_text):
        self.color = button_color1
        self.x = x
        self.y = y
        self.y_init = y
        self.width = button_width
        self.height = button_height
        self.text = text
        self.size_text = size_text
        self.pressed = False
        
    def draw(self):
        pygame.draw.rect(screen, (50,50,50), [self.x, self.y_init + 5, self.width, self.height],0 ,50)
        pygame.draw.rect(screen, self.color, [self.x, self.y + 5*self.pressed, self.width, self.height],0 ,50)
        Draw_text(screen, self.text, self.size_text, black,self.x + self.width/2,self.y + 10 +5*self.pressed)
        
    def inButton(self, mouse):
        if (mouse[0] in range(int(self.x), int(self.x + self.width+1))
        and mouse[1] in range(int(self.y), int(self.y + self.height+1))):
            self.color = button_color2

        else:
            self.color = button_color1

class Text():
    def __init__(self, text, size, x, y):
        self.text = text
        self.size = size
        self.x = x
        self.y = y

    def draw(self):
        Draw_text(screen, self.text, self.size, black, self.x, self.y)

class Box():
    def __init__(self, size, x, y):
        self.activated = False
        self.text = ""
        self.size = size
        self.x = x
        self.y = y
        self.width = 150
        self.height = 40
        self.colour = button_color2

    def draw(self):
        pygame.draw.rect(screen, self.colour, (self.x, self.y, self.width, self.height))
        Draw_text(screen, self.text, self.size, black, self.x + 25, self.y + 5)

    def inBox(self, mouse):
        if (mouse[0] in range(int(self.x), int(self.x + self.width+1))
        and mouse[1] in range(int(self.y), int(self.y + self.height+1))):
            self.colour = button_color1
            self.activated = True
        else:
            self.colour = button_color2
            self.activated = False
# =============================================================================
# Funciones
# =============================================================================
def Draw_text(surface, text, size, color, x, y):
    font = pygame.font.SysFont("serif", size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x,y)
    surface.blit(text_surface, text_rect)

def Draw_bomb(colour, pos_x, pos_y):
    points = [[0,15], [5,10], [5,5], [10,5], [15,0], [20,5], [25,5], [25,10], [30,15], [25,20], [25,25], [20,25], [15,30], [10,25], [5,25], [5,20]]
    for i in range(len(points)):
        points[i][0] += pos_x
        points[i][1] += pos_y
    pygame.draw.polygon(screen, colour, points)
    
  
def Draw_flag(pos_x, pos_y):
    pygame.draw.line(screen, black, (pos_x + 6, pos_y + 29), (pos_x + 26, pos_y + 29), 2)
    pygame.draw.line(screen, black, (pos_x + 11, pos_y + 27), (pos_x + 21, pos_y + 27), 2)
    pygame.draw.line(screen, black, (pos_x + 15, pos_y + 10), (pos_x + 15, pos_y + 30), 2)
    points = [[15,0], [30,6], [15,12]]
    for i in range(len(points)):
        points[i][0] += pos_x
        points[i][1] += pos_y
    pygame.draw.polygon(screen, red, points)

def Set_positions():
    global x_bomb, y_bomb, x_flag, y_flag, drawings
    drawings = True
    x_bomb = []
    y_bomb = []
    x_flag = []
    y_flag = []
    for _ in range(3):
        x_bomb.append(random.randint(0, width-30))
        y_bomb.append(random.randint(0, height-30))

        x_flag.append(random.randint(0, width-30))
        y_flag.append(random.randint(0, height-30))


def Create_Map(all_mapp, n_bombs, all_cells, spot_chosen = None):
    if spot_chosen:
        all_mapp.remove(spot_chosen)
    for i in range(n_bombs):
        spot = random.choice(all_mapp)
        all_mapp.remove(spot)
        all_cells[spot[0]][spot[1]].bomb = True
        
    # Empezamos con la construcción del mapa
    # Celdas interiores
    for x in range(table_size[0]):
        for y in range(table_size[1]):
            cell = all_cells[x][y]
            if not cell.bomb:
                count = 0
                for i in range(x-1, x+2):
                    for j in range(y-1, y+2):
                        if i in range(table_size[0]) and j in range(table_size[1]):
                            if all_cells[i][j].bomb:
                                count += 1
                cell.number = count
    # Bordes
    
    # Esquinas
    
    return all_cells
        

def reveal_cell(x,y):
    global n_activated, alive 
    cell = all_cells[x][y]
    if not cell.flag and not cell.activated:
        cell.activated = True
        if cell.bomb:
            alive = False
        else:
            n_activated += 1
            if cell.number == 0:
                for i in range(x-1, x+2):
                    for j in range (y-1, y+2):
                        if i in range(table_size[0]) and j in range(table_size[1]):
                                reveal_cell(i,j)

    

def Menu():
    global drawings, table_size, menu
    timer = 100
    drawings = False
    
    ##Botones
    #Case = 0
    button_Start = Button(width/2 - 125, height/2, 250, 75, "Start Game" , 40)
    button_Difficult = Button(width/2 - 100, height/2 + 100, 200, 50, "Select level", 30)
    button_Back = Button(50, 675, 150, 50, "Back", 30)
    all_buttons = [button_Start, button_Difficult]
    
    #Case = 1
    button_Easy = Button(width/2 - 100, height/2 + 0, 200, 50, "Easy", 30)
    button_Medium = Button(width/2 - 100, height/2 + 75, 200, 50, "Medium", 30)
    button_Hard = Button(width/2 - 100, height/2 + 150, 200, 50, "Hard", 30)
    button_Customize = Button (width/2 - 100, height/2 + 225, 200, 50 , "Customize", 30)
    list_buttons = [button_Easy, button_Medium, button_Hard, button_Customize,  button_Back]

    switch_buttons = {
                        button_Easy : easy_level,
                        button_Medium : medium_level,
                        button_Hard : hard_level
                      }


    #Case = 2
    button_Accept = Button(width/2 - 100, height/2 + 275, 250, 75, "Accept", 40)
    edit_buttons = [button_Accept, button_Back]



    timer_error = 0 # 120fps = 2s
    error_active = False
    text_error = ""
    text_width_error = Text("Please, choose another value for the width", 40, 450, height/2 + 225)
    text_height_error = Text("Please, choose another value for the height", 40, 450, height/2 + 225)
    text_nbombs_error = Text("There are so many bombs", 40, 450, height/2 + 225)
    text_void = Text("Missing data to fill in", 40, 450, height/2 + 225)
    text_width_begin = Text("Width: ", 40, 300, height/2 + 0)
    text_height_begin = Text("Height: ", 40, 300, height/2 + 75)
    text_nbombs_begin = Text("Bombs: " , 40, 300, height/2 + 150)
    text_width_end = Text("(max: 15)", 20, 600, height/2 + 10)
    text_height_end = Text("(max: 19)", 20, 600, height/2 + 85)
    all_text = [text_width_begin, text_height_begin, text_nbombs_begin, text_width_end, text_height_end]
    

    box_width = Box(30, 370, height/2)
    box_height = Box(30, 370, height/2 + 75)
    box_nbombs = Box(30, 370, height/2 + 150)
    all_boxs = [box_width, box_height, box_nbombs]

    
    alpha = 0
    alpha_dir = 1
    
    case = 0  # 0 = Main Menu, 1 = Difficult Menu, 2 = Customize level
    active_buttons = all_buttons
    active_text = None
    active_box = None

    while menu:
        if case == 0:
            active_buttons = all_buttons
            active_text = None
            active_box = None
        elif case == 1:
            active_buttons = list_buttons
            active_text = None
            active_box = None
        elif case == 2:
            active_buttons = edit_buttons
            active_text = all_text
            active_box = all_boxs

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            for button in active_buttons:
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and button.color == button_color2:
                    button.pressed = True
                if event.type == pygame.MOUSEBUTTONUP and button.pressed:
                    button.pressed = False
                    if button.color == button_color2:
                        if button == button_Start:
                            menu = False
                        elif button == button_Difficult:
                            case = 1
                        elif button == button_Customize:
                            case = 2
                        elif button == button_Back:
                            case-= 1
                        elif button == button_Accept:
                            if box_width.text == "" or box_height.text == "" or box_nbombs.text == "":
                                error_active = True
                                text_error = text_void
                            elif int(box_width.text) > 15:
                                error_active = True
                                text_error = text_width_error
                            elif int(box_height.text) > 19:
                                error_active = True
                                text_error = text_height_error
                            elif int(box_nbombs.text) > int(box_width.text) * int(box_height.text) - 5:
                                error_active = True
                                text_error = text_nbombs_error
                            else:
                                case = 0
                                table_size = (int(box_width.text), int(box_height.text), int(box_nbombs.text))
                        else:
                            case = 0
                            table_size = switch_buttons[button]

            if active_box:
                for box in active_box:
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        box.inBox(mouse_pos)

                    elif event.type == pygame.KEYDOWN and box.activated:
                        if event.key == pygame.K_BACKSPACE:
                            box.text = box.text[:-1]
                        elif event.unicode.isnumeric() and len(box.text) < 2:
                            box.text += event.unicode




        # Lógica del menú
        mouse_pos = pygame.mouse.get_pos()
        for button in active_buttons:
            button.inButton(mouse_pos)
        
        if timer > 150:
            Set_positions()
            
            timer = 0
        else:
            timer += 1
        

        if error_active:
            timer_error += 1
            if timer_error > 120:
                timer_error = 0
                error_active = False


        # Dibujar pantalla
        screen.fill(screen_color)
        if drawings:    
            for i in range(3):
                Draw_bomb(black, x_bomb[i], y_bomb[i])
                Draw_flag(x_flag[i], y_flag[i])
                
        for button in active_buttons:
            button.draw()
        
        if active_text:
            for text in active_text:
                text.draw()

        if active_box:
            for box in all_boxs:
                box.draw()

        if error_active:
            text_error.draw()
                

        alpha += alpha_dir
        if alpha == 255 or alpha == 0:
            alpha_dir *= -1
        Draw_text(screen, "Minesweeper", 100, (alpha, alpha, alpha), width/2, height/4)  
        
        pygame.display.update()
        clock.tick(fps)   


def Game():
    # TODO study optimization for global variables
    global table_size, menu, mapp, all_cells, all_mapp, n_activated, alive
    first_click = True

    width_table = 40 * table_size[0] +5
    height_table = 40 * table_size[1] +5
    pos_x_table = width/2 - width_table/2 + 100
    pos_y_table = height/2- height_table/2
    n_bombs = table_size[2]
    n_flag = 0
    n_activated = 0
    
    alive=True
    restart = False
    winner = False
    
    frames = 0
    seconds = 0
    minutes = 0
    
    
    all_mapp = []
    all_cells = []
    
    
    button_restart = Button(50, 600, 150, 50, "Restart", 30)
    button_back = Button(50, 675, 150, 50, "Back", 30)
    all_buttons = [button_restart, button_back]
        
    
    for i in range(table_size[0]):
        row =[]
        for j in range(table_size[1]):
            cell = Cell((pos_x_table) + 40*i,  (pos_y_table) + 40*j)
            row.append(cell)
            
            all_mapp.append([i,j])
        all_cells.append(row)
        
    # Draw just once
    screen.fill(screen_color)
    pygame.draw.rect(screen, table_color, (pos_x_table, pos_y_table, width_table, height_table))

        
    while not restart and not menu:
        for event in pygame.event.get():
    
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            for button in all_buttons:    
                if event.type == pygame.MOUSEBUTTONDOWN and button.color == button_color2:
                    button.pressed = True
                if event.type == pygame.MOUSEBUTTONUP and button.pressed:
                    button.pressed = False
                    if button.color == button_color2:
                        if button is button_restart:
                            restart = True
                        elif button is button_back:
                            menu = True
            
            if alive:

                for i in range(table_size[0]):
                    for j in range(table_size[1]):
                        cell = all_cells[i][j]
                        if not cell.activated:
                            if event.type == pygame.MOUSEBUTTONDOWN and cell.colour == colour2:
                                cell.pressed = True
                            if event.type == pygame.MOUSEBUTTONUP and cell.pressed:
                                cell.pressed = False
                                if cell.colour == colour2:
                                    if first_click and (event.button == 1 or event.button == 3):
                                        Create_Map(all_mapp, n_bombs, all_cells, [i,j])
                                        first_click = False
                                    if event.button == 1:
                                        reveal_cell(i,j)
                                        if n_activated == table_size[0] * table_size[1]- n_bombs:
                                            winner = True
                                            pygame.time.delay(500)
                                    elif event.button == 3:
                                        cell.flag = not cell.flag
                                        n_flag += 2 * cell.flag - 1 
                                            

        # Lógica
        mouse_pos = pygame.mouse.get_pos()
        
        for button in all_buttons:
            button.inButton(mouse_pos)
        
        if alive and not winner:
            for row in all_cells:
                for cell in row:
                    cell.update(mouse_pos)
        
        
        
        # Drawing

        pygame.draw.rect(screen, table_color, (5, 430, 250, 120))
        
        if alive and not winner:
            frames += 1
            if frames == 60:
                frames = 0
                seconds += 1
                if seconds == 60:
                    minutes += 1
                    seconds = 0
    
        for row in all_cells:
            for cell in row:
                if cell.drawn:
                    cell.draw()
                    if cell.activated:
                        cell.drawn = False
        
        Draw_text(screen,"Mines: {}".format(n_bombs - n_flag), 50, black, 125, 500)
        
        Draw_text(screen,"Time: " + str(minutes) +":"+ str(seconds).zfill(2), 50, black, 125, 430)
        
        if winner:
             Draw_text(screen,"You Won!", 100, black, 201, 50)
        
        button_restart.draw()
        button_back.draw()
        pygame.display.update()
        clock.tick(fps)
        
# =============================================================================
# Definicion de valores
# =============================================================================
# Colores
white = (255,255,255)
black = (0,0,0)
blue = (0,0,255)
green = (0,255,0)
red = (255,0,0)
dark_blue = (0,0,128)
dark_red = (128,0,0)
dark_green = (0,128,0)
orange = (255,165,0)
brown = (139,69,19)

colour_list = [None, blue, green, red, dark_blue, dark_green, dark_red, orange, brown]

screen_color = (165,238,160)
button_color1 = (230, 230, 230)
button_color2 = (180, 180, 180)
table_color = (200,200,200)
colour1 = (80,80,150)
colour2 = (125,125,200)


# Niveles
easy_level = (6,8,10)
medium_level = (10,14,30)
hard_level = (15,19,50)

# Reloj
fps = 60
clock = pygame.time.Clock()

# Pantalla
width = 900
height = 800
screen = pygame.display.set_mode((width,height))
pygame.display.set_caption("Mine Seeker")



# Ejecuta el juego
global menu, table_size
menu = True
table_size = easy_level
while True:
    if menu:
        Menu()
    else:
        Game()