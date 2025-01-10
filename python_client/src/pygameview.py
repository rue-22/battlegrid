from enum import StrEnum
from classes import GameState, Location, Piece, PieceKind, Side, Action, GameVerdict, piece_mappings
from view import ActionObserver, NewGameObserver
from sprites import datasprites, boardtextures
import pygame

#CONSTANTS
TILESET_PATH = "src/assets/assets.png"
TILE_SIZE = 32 


class ScreenState(StrEnum):
    GAME = 'GAME'
    MENU = 'MENU'
    
# Colors
GRAY = (169, 169, 169)
HOVER_COLOR = (200, 200, 200)


class Button:
    def __init__(self, x: int, y: int, width: int, height: int, text: str):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = GRAY

    def draw(self, screen: pygame.Surface):
        button_font = pygame.font.Font("src/assets/kongtext.ttf", 16)
        pygame.draw.rect(screen, self.color, self.rect, border_radius=5)
        text_surf = button_font.render(self.text, True, "black")
        screen.blit(text_surf, (self.rect.x + (self.rect.width - text_surf.get_width()) // 2, 
                               self.rect.y + (self.rect.height - text_surf.get_height()) // 2))

    def is_hovered(self, mouse_pos: tuple[int, int]):
        return self.rect.collidepoint(mouse_pos)


class GameView:
    def __init__(self, state: GameState):
        self.pygame_init()
        self.assets: pygame.Surface = pygame.image.load(TILESET_PATH).convert_alpha()
        self.select_mode: Action | None = None
        self.selected_piece_to_move: Piece | None = None
        self.selected_piece_to_drop: tuple[PieceKind, Side] | None = None
        self.sprite_click_areas: dict[tuple[PieceKind,Side],pygame.Rect] = {}
        
        self.menu_buttons: dict[str, Button] = {}
        self.screen_state: ScreenState = ScreenState.MENU   

        self.on_state_change(state)
        
        #initialize observers here
        self._action_observers: list[ActionObserver] = []  
        self._new_game_obseervers: list[NewGameObserver] = []
    
    def on_state_change(self, state: GameState): #protocol
        self.current_player = state.curr_player
        self.board = state.board
        self.moves_made = state.moves_made
        self.red_dict = state.red_player.stored_pieces
        self.blue_dict = state.blue_player.stored_pieces
        self.verdict = state.game_verdict

        #Network state:
        self.nid = state.network_id
        self.P2_connected = state.is_P2_connected
        self.P1_chosen_variant = state.P1board_variant
    
    @property
    def assigned_player_side(self):
        if self.nid == 1:
            return Side.BLUE
        else:
            return Side.RED

    @property
    def selected_piece_possible_moves(self) -> list[Location]:
        locations = []
        if self.selected_piece_to_move:
            locations = self.board.get_valid_moves(self.selected_piece_to_move)
        return locations
    
    @property
    def valid_drop_locations(self) -> list[Location]:
        if self.selected_piece_to_drop:
            piecekind, side = self.selected_piece_to_drop
        
            match side:
                case Side.RED:
                    if len(self.red_dict[piecekind]) == 0:
                        return []
                case Side.BLUE:
                    if len(self.blue_dict[piecekind]) == 0:
                        return []
            return self.board.get_valid_drops()
        else: return []

    # Calculate tile size dynamically based on the zoom factor and screen dimensions
    @property
    def tile_size(self) -> int:
        # Determine the maximum tile size that fits within both screen dimensions
        tile_size_width = self.VIEWPORT_WIDTH // self.board.cols
        tile_size_height = self.VIEWPORT_HEIGHT // self.board.rows
        base_tile_size = min(tile_size_width, tile_size_height)
        return int(base_tile_size)
    
       
    def pygame_init(self):
        pygame.init()

        global SCREEN_WIDTH, SCREEN_HEIGHT
        screen_info = pygame.display.Info()
        FULLSCREEN_W, FULLSCREEN_H = screen_info.current_w, screen_info.current_h
        SCREEN_WIDTH, SCREEN_HEIGHT = FULLSCREEN_W//2 - 20, FULLSCREEN_H - 200
        
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Battlegrid")
        self.VIEWPORT_X = 0      # X offset of the viewport
        self.VIEWPORT_Y = 105     # Y offset of the viewport
        self.VIEWPORT_WIDTH = SCREEN_WIDTH                    # Width of the viewport
        self.VIEWPORT_HEIGHT = SCREEN_HEIGHT - self.VIEWPORT_Y * 2 # Height of the viewport
        
    def get_sprite(self, x: int, y:int, tile_size: int = TILE_SIZE, opacity: int = 255) -> pygame.Surface:
        rect = pygame.Rect(x * tile_size, y * tile_size, tile_size, tile_size)
        sprite = self.assets.subsurface(rect)  
        sprite.set_alpha(opacity)  
        return sprite

    def get_tile_texture(self, row: int, col: int) -> str:
        variant = boardtextures[self.board.variant] # change depending how variants is initialized
        return variant[row][col] 
        
    def get_piece_texture(self, piece: Piece) -> str:
        match piece.side:
            case Side.BLUE:
                side = 'blue'
            case Side.RED:
                side = 'red'
        match piece.piece_kind:
            case PieceKind.SWORDSMAN:
                kind = 'swordsman'
            case PieceKind.MAGE:
                kind = 'mage'
            case PieceKind.ARCHER:
                kind = 'archer'
            case PieceKind.GUARD:
                kind = 'guard'
            case PieceKind.LONGSWORD:
                kind = 'longsword'
            case PieceKind.CRYSTAL:
                kind = 'crystal'

        texture = side + '_' + kind
        return texture

    def get_highlight_texture(self, location: Location) -> str:        
        color = ""
        match self.select_mode:
            case Action.MOVE:
                if self.selected_piece_to_move:
                    if self.selected_piece_to_move.location == location:
                        color = "yellow"
                
                if location in self.selected_piece_possible_moves:
                    if self.board.get_piece(location):
                        color = "red"
                    else:
                        color ="blue"
            case Action.DROP:
                if location in self.valid_drop_locations:
                    color = "blue"
            case None:
                pass
        return color
    
    def draw_turns_left(self):
        fontface = "src/assets/kongtext.ttf"
        font = pygame.font.Font(fontface, 10)
        
        num_moves = "Turns Left: " + str(3 - (self.moves_made))

        if self.nid == 1:
            if self.current_player.side == Side.RED:
                num_moves = "Red Turn"
            indicator = "YOU'RE BLUE - - - " + num_moves
            color = "#305CDE"
            text_y = SCREEN_HEIGHT - 30
        else:
            if self.current_player.side == Side.BLUE:
                num_moves = "Blue Turn"
            indicator = "YOU'RE RED - - - " + str(num_moves)
            color = "#EE4B2B"
            text_y = 10
       
        text_surface = font.render(indicator, True, color)
        text_x = SCREEN_WIDTH//2 - text_surface.get_width()//2
    
        self.screen.blit(text_surface, (text_x, text_y))

    def draw_player_interface(self):
        fontface = "src/assets/kongtext.ttf"
        font = pygame.font.Font(fontface, 17)
        
        box = 55
        rad = 8 
        self.draw_turns_left()

        red_rect_x = SCREEN_WIDTH // 2 - ((box * 5) // 2)
        red_rect_y = 30 + 10 + rad      # Place near the bottom
        blue_rect_x = SCREEN_WIDTH // 2 - ((box * 5) // 2)  # Centered horizontally
        blue_rect_y = SCREEN_HEIGHT - box - (30 + 10 + 10)  # Place near the bottom
        rect_width = int(box * 1)    # Width of each box
        rect_height = box
        
        # Red 
        for piecekind, lst in self.red_dict.items():
            rect_color = "black"
            pygame.draw.rect(self.screen, rect_color, (red_rect_x, red_rect_y, rect_width, rect_height))
            sprite = self.get_sprite(*datasprites["red_" + piecekind.value.lower()])
            sprite_size = int(box * 1)
            scaled_sprite = pygame.transform.scale(sprite, (sprite_size, sprite_size))

            # sprite
            sprite_x = red_rect_x + (rect_width - sprite_size) // 2
            sprite_y = red_rect_y + (rect_height - sprite_size) // 2
            # Selected sprite
            if self.selected_piece_to_drop == (piecekind,Side.RED):
                highlight_sprite = self.get_sprite(*datasprites["white"])
                highlight_sprite.set_alpha(128)
                self.screen.blit(pygame.transform.scale(highlight_sprite, (sprite_size, sprite_size)), (sprite_x,sprite_y))
            self.screen.blit(scaled_sprite, (sprite_x, sprite_y))

            # text
            text_surface = font.render(str(len(lst)), True, "white")
            text_x = red_rect_x + (rect_width - text_surface.get_width()) // 2
            text_y = 10 + rad*2 + 5
            self.screen.blit(text_surface, (text_x, text_y))

            # Add the rectangle as a clickable area
            self.sprite_click_areas[(piecekind, Side.RED)] = pygame.Rect(red_rect_x, red_rect_y, rect_width, rect_height)
            red_rect_x += rect_width  # Add spacing between
        
        # Blue
        for piecekind, lst in self.blue_dict.items():
            rect_color = "black"
            pygame.draw.rect(self.screen, rect_color, (blue_rect_x, blue_rect_y, rect_width, rect_height))
            sprite = self.get_sprite(*datasprites["blue_" + piecekind.value.lower()])
            sprite_size = int(box * 1)
            scaled_sprite = pygame.transform.scale(sprite, (sprite_size, sprite_size))

            # sprite
            sprite_x = blue_rect_x + (rect_width - sprite_size) // 2
            sprite_y = blue_rect_y + (rect_height - sprite_size) // 2
            # Selected sprite
            if self.selected_piece_to_drop == (piecekind,Side.BLUE):
                highlight_sprite = self.get_sprite(*datasprites["white"])
                highlight_sprite.set_alpha(128)
                self.screen.blit(pygame.transform.scale(highlight_sprite, (sprite_size, sprite_size)), (sprite_x,sprite_y))
            self.screen.blit(scaled_sprite, (sprite_x, sprite_y))

            # text
            text_surface = font.render(str(len(lst)), True, "white")
            text_x = blue_rect_x + (rect_width - text_surface.get_width()) // 2
            text_y = SCREEN_HEIGHT - (10 + rad + 35)
            self.screen.blit(text_surface, (text_x, text_y))

            # Add the rectangle as a clickable area
            self.sprite_click_areas[(piecekind, Side.BLUE)] = pygame.Rect(blue_rect_x, blue_rect_y, rect_width, rect_height)
            blue_rect_x += rect_width  # Add spacing between

    def draw_board(self):
        board = self.board

        VIEWPORT_WIDTH = self.VIEWPORT_WIDTH # Width of the viewport
        VIEWPORT_HEIGHT = self.VIEWPORT_HEIGHT
        
        tile_size = self.tile_size
        board_width = tile_size * board.cols
        board_height = tile_size * board.rows
        x_offset = (VIEWPORT_WIDTH - board_width) // 2
        y_offset = (VIEWPORT_HEIGHT - board_height) // 2
        
        # Create a surface for the viewport
        viewport = pygame.Surface((VIEWPORT_WIDTH, VIEWPORT_HEIGHT))
        viewport.fill("black")  

        # Note: order of rendering matters
        for row in range(board.rows):
            for col in range(board.cols):
                x = col * tile_size + x_offset
                y = row * tile_size + y_offset
                    
                # Render Tile Texture
                name = self.get_tile_texture(row,col) 
                tile_sprite = self.get_sprite(*datasprites[name])
                viewport.blit(pygame.transform.scale(tile_sprite, (tile_size, tile_size)), (x,y))

                # Render Highlight Texture
                opacity = 128 
                match self.select_mode:
                    # MOVE: Render all possible moves of a selected piece 
                    case Action.MOVE:
                        highlight_color = self.get_highlight_texture(Location(row,col))
                        if highlight_color:
                            highlight_sprite = self.get_sprite(*datasprites[highlight_color])
                            highlight_sprite.set_alpha(opacity)
                            viewport.blit(pygame.transform.scale(highlight_sprite, (tile_size, tile_size)), (x,y))
                    
                    case Action.DROP:
                    # DROP: Render all possible moves of a selected sprite
                        highlight_color = self.get_highlight_texture(Location(row,col))
                        if highlight_color:
                            highlight_sprite = self.get_sprite(*datasprites[highlight_color])
                            highlight_sprite.set_alpha(opacity)
                            viewport.blit(pygame.transform.scale(highlight_sprite, (tile_size, tile_size)), (x,y))
                    case None:
                        pass

                # Render Piece Texture
                piece = board.get_piece(Location(row,col))
                if piece:
                    piece_name = self.get_piece_texture(piece)
                    piece_sprite = self.get_sprite(*datasprites[piece_name])
                    viewport.blit(pygame.transform.scale(piece_sprite, (tile_size, tile_size)), (x,y))
        
        self.screen.blit(viewport, (self.VIEWPORT_X, self.VIEWPORT_Y))
                
    def draw_game_result(self):
        content = ""
        match self.verdict:
            case GameVerdict.CONTINUE:
                return
            case GameVerdict.BLUE_WINNER:
                content = "BLUE WINS"
            case GameVerdict.RED_WINNER:
                content = "RED WINS"
            case GameVerdict.DRAW:
                content = "DRAW, NO ONE WINS"
    
        width = SCREEN_WIDTH
        height = SCREEN_HEIGHT

        rect_surface = pygame.Surface((width,  height), pygame.SRCALPHA)
        rect_surface.fill((255, 255, 255, 200))  # RGBA: Black with 50% opacity (128/255)
        self.screen.blit(rect_surface, (0, SCREEN_HEIGHT // 2 - rect_surface.get_height() // 2))

        font = pygame.font.Font("src/assets/meow.ttf", 50)
        text_surface = font.render(str(content), True, "black")
        text_width = text_surface.get_width()
        text_height = text_surface.get_height()
        text_x = width//2
        text_y = height//2
        self.screen.blit(text_surface, (text_x-text_width//2, text_y-text_height//2))

    def draw(self):
        self.screen.fill("black")
        
        if self.screen_state == ScreenState.MENU:
            self.draw_main_menu()

        elif self.screen_state == ScreenState.GAME:
            self.draw_board()
            self.draw_player_interface()
            self.draw_game_result()

        pygame.display.flip()
    
    def draw_main_menu(self):
        self.screen.fill("white")

        # Draw the menu text
        font = pygame.font.Font("src/assets/meow.ttf", 70) 
        title_text = font.render("Battlegrid", True, "black")
        self.screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 50))

        # Draw main buttons
        if self.nid == 1:
            if self.P2_connected:
                button_width, button_height = 300, 70 
                self.menu_buttons["4"] = Button(SCREEN_WIDTH // 2 - button_width//2, SCREEN_HEIGHT // 2 - 100, button_width, button_height, "Classic")
                self.menu_buttons["1"] = Button(SCREEN_WIDTH // 2 - button_width//2, SCREEN_HEIGHT // 2 - 0, button_width, button_height, "Rush")
                self.menu_buttons["2"] = Button(SCREEN_WIDTH // 2 - button_width//2, SCREEN_HEIGHT // 2 + 100, button_width, button_height, "War")
                self.menu_buttons["3"] = Button(SCREEN_WIDTH // 2 - button_width//2, SCREEN_HEIGHT // 2 + 200, button_width, button_height, "Prime")
                for key in self.menu_buttons:
                    self.menu_buttons[key].draw(self.screen)
            else:
                font = pygame.font.Font("src/assets/meow.ttf", 20) 
                title_text = font.render("waiting for P2 to connect...", True, "black")
                self.screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, SCREEN_HEIGHT // 2))
        
        elif self.nid == 2:
            if self.P1_chosen_variant != 0:
                self.screen_state = ScreenState.GAME
                self._on_new_game(self.P1_chosen_variant)
            else:
                font = pygame.font.Font("src/assets/meow.ttf", 20) 
                title_text = font.render("waiting for P1 to choose board...", True, "black")
                self.screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, SCREEN_HEIGHT // 2 ))

    def run(self):
        clock = pygame.time.Clock()
        fps = 60
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.screen_state == ScreenState.MENU and self.P2_connected:
                        mouse_pos = pygame.mouse.get_pos()
                        if self.menu_buttons["1"].is_hovered(mouse_pos):
                            self.screen_state = ScreenState.GAME
                            self._on_new_game(1)
                        elif self.menu_buttons["2"].is_hovered(mouse_pos):
                            self.screen_state = ScreenState.GAME
                            self._on_new_game(2)
                        elif self.menu_buttons["3"].is_hovered(mouse_pos):
                            self.screen_state = ScreenState.GAME
                            self._on_new_game(3)
                        elif self.menu_buttons["4"].is_hovered(mouse_pos):
                            self.screen_state = ScreenState.GAME
                            self._on_new_game(4)
                    elif self.screen_state == ScreenState.GAME:
                        self.on_click()
            self.draw()
            clock.tick(fps)
        pygame.quit()
    
    def get_grid_position(self, mouse_x: int, mouse_y: int) -> Location | None:
        x = mouse_x - self.VIEWPORT_X
        y = mouse_y - self.VIEWPORT_Y
        tile_size = self.tile_size
        x_offset = (self.VIEWPORT_WIDTH - (tile_size * self.board.cols)) // 2       # Calculate horizontal offset
        y_offset = (self.VIEWPORT_HEIGHT - (tile_size * self.board.rows)) // 2     # Calculate vertical offset
        # Calculate column and row indices
        col = (x - x_offset) // tile_size
        row = (y - y_offset) // tile_size
        if 0 <= col < self.board.cols and 0 <= row < self.board.rows:
            return Location(row, col) 
        return None
    
    # Cheks if the sprite menu is clicked
    def check_sprite_click(self, x: int, y: int): #optimize later
        for (piecekind, side), rect in self.sprite_click_areas.items():
            if rect.collidepoint((x,y)):
                # deselect current sprite to move by clicking itself
                if self.selected_piece_to_drop == (piecekind, side):
                    self.select_mode = None
                    self.selected_piece_to_drop = None
                # select a sprite -- ensures current player picks own 
                elif side == self.current_player.side and side == self.assigned_player_side:
                    self.select_mode = Action.DROP
                    self.selected_piece_to_drop = (piecekind, side)
                    self.selected_piece_to_move = None

    # Checks if part of a board is clicked
    def check_board_click(self, mouse_x: int, mouse_y: int):
        grid_coordinates = self.get_grid_position(mouse_x, mouse_y)
        if grid_coordinates and self.verdict == GameVerdict.CONTINUE:
            piece = self.board.get_piece(grid_coordinates)
            # deselect current piece to move by clicking itself
            if self.selected_piece_to_move == self.board.get_piece(grid_coordinates) and self.select_mode == Action.MOVE:
                self.select_mode = None
                self.selected_piece_to_move = None
            # perform move, tap a highlighted area when a piece is highlighted/selected
            elif grid_coordinates in self.selected_piece_possible_moves and self.selected_piece_to_move:
                temp = self.selected_piece_to_move
                self.selected_piece_to_move = None
                self._on_action(Action.MOVE, temp, grid_coordinates)
            # perform drop, tap a highlighted area to drop piece
            elif grid_coordinates in self.valid_drop_locations and self.selected_piece_to_drop is not None:
                piecekind, side = self.selected_piece_to_drop
                piece = Piece(piece_mappings[piecekind],Location(-1,-1),side)
                self.selected_piece_to_drop = None
                self._on_action(Action.DROP, piece, grid_coordinates)
            # select a piece -- ensures current player picks own pieces
            elif piece and piece.side == self.current_player.side and piece.side == self.assigned_player_side:
                self.select_mode = Action.MOVE
                self.selected_piece_to_move = piece
                self.selected_piece_to_drop = None

    def on_click(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        # When Screen is game, fix later
        self.check_sprite_click(mouse_x, mouse_y)
        self.check_board_click(mouse_x, mouse_y)

    def _on_action(self, action: Action, piece: Piece, to: Location):
        for observer in self._action_observers:
            observer.on_action(action, piece, to)
        
    def _on_new_game(self, variant: int):
        for observer in self._new_game_obseervers:
            observer.on_new_game(variant)

    def register_action_observer(self, observer: ActionObserver):
        self._action_observers.append(observer)
    
    def register_new_game_observer(self, observer: NewGameObserver):
        self._new_game_obseervers.append(observer)

