from Yahtzeegamecode import Game, Player, EasyAI, EZBoard, HardAI
## UI code ##

import random, math, PySimpleGUI as psg, time, os, sys , re, sqlite3, statistics, tkinter, threading

# Get the absolute path of the script directory
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# Terminal UI

class Terminal:
    


        # initialise game
        def __init__(self):

            self.game = Game()

            

        # run game
            
        def run(self):
            
            
            while True:
                # get and validate number of players
                try:
                    self.playernum = int(input("Enter the number of players: "))
                    self.AIplayers = int(input("Enter the number of AI players: "))
                    break
                except ValueError:
                    print("Invalid number of players")
                    continue



            
                    

                
            # add players to game
            for player in range(self.playernum):
                self.game.players.append(Player())

            # get player names
            for player in self.game.players:
                player.name = input("Enter your name: ")
            
            # add AI players to game
            for player in range(self.AIplayers):
                self.game.players.append(EasyAI())

            
            
            # play game
            while self.game.roundnum < 13:
                self.tround()

            print('Game Over!')
            
            # end sequence
            for player in self.game.players:
                print(player.name + "'s score is: " + str(player.scorecard.count_score()))
            print('the winner is '+ self.game.get_winner().name + ' with a score of ' + str(self.game.get_winner().scorecard.count_score()))

            

        # get and validate user input for rerolls

        ###############################
        # USE OF RECURSIVE VALIDATION #
        ###############################
                
        def __get_reroll_choice(self):
            try:
                reroll_list = (input("Enter the dice indexes you want to reroll, seperated by a comma: ")).split(',')
                if reroll_list == ['']:
                    return []
                for dice in reroll_list:
                    if int(dice) not in range(1, 6):
                        print("Invalid choice- must be between 1 and 5")
                        reroll_list = self.__get_reroll_choice()
            except ValueError or TypeError:
                print("Invalid choice")
                reroll_list = self.__get_reroll_choice()
            
            return reroll_list
            
        # get and validate user input for category choice

        def __get_category_choice(self,player):
            try:
                choice = (int(input("Enter your choice: ")))
            
            # check if choice is valid
            except ValueError or TypeError:
                print("Invalid choice")
                choice = self.__get_category_choice(player)

            if choice not in range(1, 14):
                print("Invalid choice- must be between 1 and 13")
                choice = self.__get_category_choice(player)
            

            
            if player.get_scorecard().scorecard[player.scorecard.keylist[choice-1]] != None:
                print("Category already scored")
                choice = self.__get_category_choice(player)
            

            return choice  

        # play round
           
        def tround(self):

            self.game.roundnum += 1

            print("Round " + str(self.game.roundnum))
            for player in self.game.players:
                if isinstance(player, EasyAI) or isinstance(player, HardAI):
                    self.__ai_turn(player)
                else:
                    self.turn(player)

        # play user turn
                        
        def turn(self,player):

            
            print(player.name + "'s turn")
            self.game.dice.roll()
            print("Your dice are: " + str(self.game.dice.get_dice()))
            while self.game.rerolls < self.game.REROLLS:
                self.game.rerolls += 1
                self.game.dice.reroll(self.__get_reroll_choice())
                print("Your dice are: " + str(self.game.dice.get_dice()))
            self.game.rerolls = 0
            player.scorecard.show_scorecard()
            choice = self.__get_category_choice(player)
            player.scorecard.score_roll(self.game.dice, choice)
            player.scorecard.show_scorecard()

        # play AI turn
            
        def __ai_turn(self,player):
                
                print(player.name + "'s turn")
                self.game.dice.roll()
                print("Your dice are: " + str(self.game.dice.get_dice()))
                self.game.rerolls = 0
                player.scorecard.show_scorecard()
                player.play()
                player.scorecard.show_scorecard()




# GUI 
                
class GUI:

    #dice image initialisation
    
    
    #GUI initialisation
    def __init__(self):
        self.game = Game()
        self.__theme = "DarkGrey1"
        self.__rules = os.path.join(SCRIPT_DIR, 'Rules.txt')
        self.__aidifficulty = 'Easy'
        self.EZboardopt = False
        self.main_window = None
        self.mute_sounds = False  # Add mute sounds setting
        
        # Initialize pygame mixer and sound paths
        import pygame
        pygame.mixer.init()
        self.sounds_dir = os.path.join(SCRIPT_DIR, 'sounds')
        self.dice_roll_sound = os.path.join(self.sounds_dir, 'dice roll.mp3')
        self.game_over_sound = os.path.join(self.sounds_dir, 'Game Over.mp3')
        self.point_sound = os.path.join(self.sounds_dir, 'Point.mp3')
        self.yahtzee_sound = os.path.join(self.sounds_dir, 'Yahtzee.mp3')
        self.hover_sound = os.path.join(self.sounds_dir, 'hover.mp3')
        self.select_sound = os.path.join(self.sounds_dir, 'select.mp3')

        # Color themes
        self.color_themes = {
            'Midnight': {
                'background': '#1A1B26',
                'primary': '#7AA2F7',
                'secondary': '#24283B',
                'text': '#C0CAF5',
                'accent': '#BB9AF7'
            },
            'Sakura': {
                'background': '#2D2D44',
                'primary': '#FF7EB6',
                'secondary': '#1F1F33',
                'text': '#FFDEDE',
                'accent': '#FF9ECE'
            },
            'Emerald': {
                'background': '#1B2023',
                'primary': '#00B894',
                'secondary': '#2D3436',
                'text': '#DFE6E9',
                'accent': '#55EFC4'
            },
            'Sunset': {
                'background': '#2D142C',
                'primary': '#FF6B6B',
                'secondary': '#1F0F1E',
                'text': '#FFE3E3',
                'accent': '#FFA502'
            }
        }
        self.current_theme = 'Midnight'  # Set Midnight as default theme

        # Initialize animations
        self.animation_settings = {
            'button_hover_alpha': 0.8,
            'button_click_alpha': 0.6,
            'animation_steps': 1,  # Reduced to 1 for instant response
            'animation_delay': 0.001,  # Minimal delay for smoother animation
            'fade_steps': 10,
            'hover_scale': 1.03  # Reduced scale for subtler effect
        }

        # Button styles
        self.button_styles = {
            'normal': {
                'font': ("Comic Sans MS", 12, 'bold'),
                'border_width': 0,
                'pad': (10, 10)
            },
            'large': {
                'font': ("Comic Sans MS", 16, 'bold'),
                'border_width': 0,
                'pad': (15, 15)
            },
            'title': {
                'font': ("Comic Sans MS", 40, 'bold'),
                'pad': (20, 20)
            },
            'subtitle': {
                'font': ("Comic Sans MS", 24, 'bold'),
                'pad': (10, 10)
            },
            'button': {
                'small': (12, 2),
                'medium': (20, 2),
                'large': (30, 3)
            }
        }

        # Unicode dice characters with custom styling
        self.dice_symbols = {
            1: "⚀",
            2: "⚁",
            3: "⚂",
            4: "⚃",
            5: "⚄",
            6: "⚅"
        }

    def smooth_button_animation(self, window, button_key, is_hover):
        """Perform smooth button animation"""
        try:
            button = window[button_key]
            if not button:
                return
                
            # Get base size based on button type
            if button_key == 'Start new Game':
                base_size = (30, 3)  # Main PLAY button
            elif button_key in ['Start', 'Cancel', 'Apply', 'Play Again', 'Exit', 'Back_btn', 'Reset_btn', 'Start_Game', 'Next turn']:
                base_size = (12, 2)  # Small buttons
            else:
                base_size = (25, 2)  # Regular menu buttons
            
            # Calculate target size with hover effect
            hover_scale = 1.1 if is_hover else 1.0  # Increase size by 10% on hover
            target_size = [
                int(base_size[0] * hover_scale),
                int(base_size[1] * hover_scale)
            ]
            
            # Update button size
            button.set_size(target_size)
            window.refresh()
            
        except Exception as e:
            pass  

    def run(self):
        # Get current theme colors
        theme = self.color_themes[self.current_theme]
        BACKGROUND_COLOR = theme['background']
        PRIMARY_COLOR = theme['primary']
        SECONDARY_COLOR = theme['secondary']
        TEXT_COLOR = theme['text']
        ACCENT_COLOR = theme['accent']
        
        # set theme
        psg.theme(self.__theme)
        
        # Get best score from leaderboard
        best_score = 0
        if os.path.isfile('leaderboard.db'):
            conn = sqlite3.connect('leaderboard.db')
            c = conn.cursor()
            c.execute("SELECT MAX(score) FROM leaderboard")
            result = c.fetchone()
            if result[0] is not None:
                best_score = result[0]
            conn.close()

        # Create animated gradient title
        title_elements = []
        for i, char in enumerate("YAHTZEE"):
            color = self.interpolate_color(PRIMARY_COLOR, ACCENT_COLOR, i / len("YAHTZEE"))
            title_elements.append(
                psg.Text(char,
                        font=("Segoe UI", 60, 'bold'),
                        text_color=color,
                        background_color=BACKGROUND_COLOR,
                        pad=(1, 1),
                        key=f'title_{i}')
            )

        subtitle_elements = []
        for i, char in enumerate("DICE GAME"):
            color = self.interpolate_color(ACCENT_COLOR, PRIMARY_COLOR, i / len("DICE GAME"))
            subtitle_elements.append(
                psg.Text(char,
                        font=("Segoe UI", 30, 'bold'),
                        text_color=color,
                        background_color=BACKGROUND_COLOR,
                        pad=(1, 1),
                        key=f'subtitle_{i}')
            )

        # Create animated dice with pulsing effect
        dice_style = {
            'font': ("Segoe UI", 80),
            'text_color': PRIMARY_COLOR,
            'background_color': BACKGROUND_COLOR,
            'pad': (20, 20)
        }
        
        dice1 = [[psg.Text(self.dice_symbols[5], **dice_style, key='dice1')]]
        dice2 = [[psg.Text(self.dice_symbols[6], **dice_style, key='dice2')]]

        # Create buttons with enhanced hover effects
        def create_menu_button(text, size, color, key, is_main=False):
            # Increased default button sizes
            main_size = (30, 3)  # Larger size for main PLAY button
            regular_size = (25, 2)  # Larger size for other buttons
            
            button = psg.Button(text,
                            size=main_size if is_main else regular_size,
                            font=self.button_styles['large' if is_main else 'normal']['font'],
                            button_color=(TEXT_COLOR, color),
                            border_width=0,
                            key=key,
                            mouseover_colors=(TEXT_COLOR, ACCENT_COLOR),
                            pad=(0, 10 if is_main else 5))
            return button

        # Main menu layout
        layout = [
            [psg.Column(dice1, background_color=BACKGROUND_COLOR, element_justification='left', key='dice_col1'), 
             psg.Column([[psg.Column([title_elements], background_color=BACKGROUND_COLOR, element_justification='center')],
                        [psg.Column([subtitle_elements], background_color=BACKGROUND_COLOR, element_justification='center')]], 
                       background_color=BACKGROUND_COLOR,
                       element_justification='center'),
             psg.Column(dice2, background_color=BACKGROUND_COLOR, element_justification='right', key='dice_col2')],
            
            [psg.Text(f"Best Score: {best_score}",
                     font=self.button_styles['subtitle']['font'],
                     text_color=ACCENT_COLOR,
                     background_color=BACKGROUND_COLOR,
                     pad=(0, 30),
                     key='score_text')],
            
            [psg.VPush()],
            
            [create_menu_button("▶ PLAY", None, PRIMARY_COLOR, 'Start new Game', True)],
            
            [psg.VPush()],
            
            [create_menu_button("🏆 Leaderboard", None, SECONDARY_COLOR, 'Leaderboard')],
            [create_menu_button("📖 Rules", None, SECONDARY_COLOR, 'Rules')],
            [create_menu_button("⚙️ Settings", None, SECONDARY_COLOR, 'Settings')],
            
            [psg.VPush()],
            
            [create_menu_button("Exit", None, '#FF5252', 'Exit')]
        ]
                  
        window = psg.Window("Yahtzee",
                          layout,
                          size=(800, 800),
                          element_justification='c',
                          background_color=BACKGROUND_COLOR,
                          margins=(50, 50),
                          finalize=True)
        
        window.maximize()

        # Bind hover events for all buttons
        for key in ['Start new Game', 'Leaderboard', 'Rules', 'Settings', 'Exit']:
            window[key].bind('<Enter>', '+HOVER')
            window[key].bind('<Leave>', '+UNHOVER')

        # Animation variables
        pulse_direction = 1
        pulse_alpha = 1.0
        title_offset = 0
        hover_scale = 1.0
        hover_direction = 1

        try:
            while True:
                event, values = window.read(timeout=50)
                
                if event == psg.WIN_CLOSED:
                    window.close()
                    sys.exit()
                
                # Handle button hover effects with scale animation
                if event and '+HOVER' in event:
                    btn_key = event.split('+')[0]
                    self.play_hover_sound()
                    self.smooth_button_animation(window, btn_key, True)
                elif event and '+UNHOVER' in event:
                    btn_key = event.split('+')[0]
                    self.smooth_button_animation(window, btn_key, False)
                
                # Handle main events
                if event == "Start new Game":
                    self.play_select_sound()
                    window.close()
                    self.newgame()
                    break
                elif event == "Leaderboard":
                    self.play_select_sound()
                    self.leaderboard()
                elif event == "Rules":
                    self.play_select_sound()
                    self.rules()
                elif event == "Settings":
                    self.play_select_sound()
                    window.close()
                    self.settings()
                    return
                elif event == "Exit":
                    self.play_select_sound()
                    window.close()
                    sys.exit()
                
                # Animate title with smooth color transitions
                title_offset = (title_offset + 0.1) % (2 * 3.14159)
                for i, char in enumerate("YAHTZEE"):
                    color = self.interpolate_color(
                        PRIMARY_COLOR, 
                        ACCENT_COLOR,
                        (math.sin(title_offset + i * 0.5) + 1) / 2
                    )
                    window[f'title_{i}'].update(text_color=color)

                # Pulse effect for dice
                pulse_alpha += 0.05 * pulse_direction
                if pulse_alpha >= 1.0:
                    pulse_direction = -1
                    pulse_alpha = 1.0
                elif pulse_alpha <= 0.5:
                    pulse_direction = 1
                    pulse_alpha = 0.5

                dice_color = self.apply_alpha(PRIMARY_COLOR, pulse_alpha)
                window['dice1'].update(text_color=dice_color)
                window['dice2'].update(text_color=dice_color)

        except Exception as e:
            if 'window' in locals():
                window.close()
            return

    # load leaderoard from database, display in table
        
    def leaderboard(self):
        # Get current theme colors
        theme = self.color_themes[self.current_theme]
        BACKGROUND_COLOR = theme['background']
        PRIMARY_COLOR = theme['primary']
        SECONDARY_COLOR = theme['secondary']
        TEXT_COLOR = theme['text']
        ACCENT_COLOR = theme['accent']
        
        try:
            # Create buttons with consistent styling
            back_button = psg.Button(
                "Back",
                size=self.button_styles['button']['small'],
                font=self.button_styles['normal']['font'],
                button_color=(TEXT_COLOR, PRIMARY_COLOR),
                border_width=0,
                pad=(10, 20),
                key='Back_btn'
            )

            reset_button = psg.Button(
                "Reset Leaderboard",
                size=self.button_styles['button']['small'],
                font=self.button_styles['normal']['font'],
                button_color=(TEXT_COLOR, '#FF5252'),
                border_width=0,
                pad=(10, 20),
                key='Reset_btn'
            )

            # check if leaderboard exists
            if not os.path.isfile('leaderboard.db'):
                psg.popup("No leaderboard found",
                         font=self.button_styles['normal']['font'],
                         background_color=BACKGROUND_COLOR,
                         text_color=TEXT_COLOR)
                return
            
            def refresh_leaderboard():
                conn = sqlite3.connect('leaderboard.db')
                c = conn.cursor()
                c.execute("SELECT player_name, score FROM leaderboard ORDER BY score DESC")
                leaderboard_data = c.fetchall()
                conn.close()
                return leaderboard_data
            
            leaderboard = refresh_leaderboard()

            # Create gradient title with animation
            title_elements = []
            for i, char in enumerate("🏆 Leaderboard"):
                color = self.interpolate_color(PRIMARY_COLOR, ACCENT_COLOR, i / len("🏆 Leaderboard"))
                title_elements.append(
                    psg.Text(char,
                            font=self.button_styles['title']['font'],
                            text_color=color,
                            background_color=BACKGROUND_COLOR,
                            pad=(1, 1))
                )

            # Create a frame with rounded corners effect
            def create_rounded_frame(content):
                return psg.Column([
                    [psg.Frame("", content,
                              background_color=BACKGROUND_COLOR,
                              relief=psg.RELIEF_SOLID,
                              border_width=0)]
                ], background_color=BACKGROUND_COLOR, pad=(10, 10))

            # Enhanced table style
            table_style = {
                'values': leaderboard,
                'headings': ["Player", "Score"],
                'num_rows': min(len(leaderboard), 10),
                'auto_size_columns': True,
                'justification': 'center',
                'font': self.button_styles['normal']['font'],
                'background_color': SECONDARY_COLOR,
                'text_color': TEXT_COLOR,
                'header_background_color': PRIMARY_COLOR,
                'header_text_color': TEXT_COLOR,
                'selected_row_colors': (TEXT_COLOR, ACCENT_COLOR),
                'key': 'leaderboard_table',
                'row_height': 35,
                'header_font': self.button_styles['subtitle']['font']
            }

            layout = [
                [psg.Column([title_elements],
                           background_color=BACKGROUND_COLOR,
                           element_justification='center',
                           pad=(0, 20))],
                
                [create_rounded_frame([[psg.Table(**table_style)]])],
                
                [psg.Column([
                    [back_button, reset_button]
                ], background_color=BACKGROUND_COLOR,
                   element_justification='center',
                   pad=(0, 20))]
            ]
            
            window = psg.Window("Leaderboard",
                              layout,
                              background_color=BACKGROUND_COLOR,
                              element_justification='center',
                              modal=True,
                              finalize=True,
                              alpha_channel=1.0,
                              margins=(20, 20))
            
            window.maximize()
            
            # Bind hover events
            window['Back_btn'].bind('<Enter>', '+HOVER')
            window['Back_btn'].bind('<Leave>', '+UNHOVER')
            window['Reset_btn'].bind('<Enter>', '+HOVER')
            window['Reset_btn'].bind('<Leave>', '+UNHOVER')
        
            while True:
                event, values = window.read()
                
                # Handle hover events with consistent behavior
                if event and ('+HOVER' in event or '+UNHOVER' in event):
                    self.handle_button_hover(window, event)
                
                if event in ("Back", "Back_btn", psg.WIN_CLOSED):
                    self.play_select_sound()
                    break
                elif event in ("Reset Leaderboard", "Reset_btn"):
                    self.play_select_sound()
                    confirm = psg.popup_yes_no(
                        "Are you sure you want to reset the leaderboard?\nThis action cannot be undone.",
                        title="Confirm Reset",
                        background_color=BACKGROUND_COLOR,
                        text_color=TEXT_COLOR,
                        button_color=(TEXT_COLOR, PRIMARY_COLOR),
                        font=self.button_styles['normal']['font']
                    )
                    if confirm == "Yes":
                        conn = sqlite3.connect('leaderboard.db')
                        c = conn.cursor()
                        c.execute("DELETE FROM leaderboard")
                        conn.commit()
                        conn.close()
                        
                        leaderboard = refresh_leaderboard()
                        window['leaderboard_table'].update(values=leaderboard)
            
            window.close()
            self.run()
            return

        except Exception as e:
            if 'window' in locals():
                window.close()
            return

    # add player to leaderboard database
    def addtoleaderboard(self, player):
        
        conn = sqlite3.connect('leaderboard.db')
        c = conn.cursor()
        c.execute('''
                  CREATE TABLE IF NOT EXISTS leaderboard (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    player_name TEXT,
                    score INTEGER
                    )
                    ''')

        c.execute("INSERT INTO leaderboard (player_name, score) VALUES (?, ?)", (player.name, player.scorecard.get_score()))
        conn.commit()
        conn.close()


    # rules page
    def rules(self):
        # Get current theme colors
        theme = self.color_themes[self.current_theme]
        BACKGROUND_COLOR = theme['background']
        PRIMARY_COLOR = theme['primary']
        SECONDARY_COLOR = theme['secondary']
        TEXT_COLOR = theme['text']
        ACCENT_COLOR = theme['accent']
        
        with open(self.__rules, 'r') as f:
            rules = f.read()

        # Create gradient title
        title_elements = self.create_gradient_text(
            "📖 Game Rules",
            PRIMARY_COLOR,
            ACCENT_COLOR,
            self.button_styles['title']['font']
        )

        layout = [
            [psg.Column([title_elements], 
                       background_color=BACKGROUND_COLOR,
                       element_justification='center',
                       pad=(0, 20))],
            
            [psg.Frame("", [
                [psg.Column([[psg.Text(rules, 
                                     font=self.button_styles['normal']['font'],
                                     text_color=TEXT_COLOR,
                                     background_color=BACKGROUND_COLOR)]], 
                          scrollable=True,
                          vertical_scroll_only=True,
                          size=(1100, 500),
                          background_color=BACKGROUND_COLOR)]
            ], background_color=BACKGROUND_COLOR,
               relief=psg.RELIEF_SOLID,
               border_width=0)],
            
            [psg.Button("Back",
                       size=(25, 2),
                       font=self.button_styles['normal']['font'],
                       button_color=(TEXT_COLOR, PRIMARY_COLOR),
                       mouseover_colors=(TEXT_COLOR, self.apply_alpha(PRIMARY_COLOR, self.animation_settings['button_hover_alpha'])),
                       border_width=0,
                       pad=(0, 20))]
        ]
        
        window = psg.Window("Rules",
                          layout,
                          background_color=BACKGROUND_COLOR,
                          element_justification='center',
                          modal=True,
                          resizable=True,
                          finalize=True,
                          alpha_channel=1.0)
        
        window.maximize()

        while True:
            event, values = window.read()
            if event in ("Back", psg.WIN_CLOSED):
                break
        
        window.close()

    
    # starts a new game      
    def newgame(self):
        # Get current theme colors
        theme = self.color_themes[self.current_theme]
        BACKGROUND_COLOR = theme['background']
        PRIMARY_COLOR = theme['primary']
        SECONDARY_COLOR = theme['secondary']
        TEXT_COLOR = theme['text']
        ACCENT_COLOR = theme['accent']

        # Player selection layout
        layout = [
            [psg.VPush()],
            [psg.Text("✨ New Game Setup", 
                     font=("Comic Sans MS", 50, 'bold'),
                     text_color=TEXT_COLOR,
                     background_color=BACKGROUND_COLOR,
                     pad=(0, 40))],
            [psg.VPush()],
            [psg.Frame("", [
                [psg.Column([
                    [psg.Text("👥 Number of Players", 
                             font=("Comic Sans MS", 24),
                             text_color=TEXT_COLOR,
                             background_color=BACKGROUND_COLOR,
                             pad=(0, 20))],
                    [psg.Column([[
                        psg.Frame("", [
                            [psg.Column([[
                                psg.Spin(values=[i for i in range(1, 6)],
                                        initial_value=1,
                                        key='players',
                                        size=(3, 1),
                                        font=("Comic Sans MS", 20),
                                        text_color=TEXT_COLOR,
                                        background_color=SECONDARY_COLOR)
                            ]], background_color=SECONDARY_COLOR, pad=(10, 10))]], 
                            background_color=SECONDARY_COLOR,
                            relief=psg.RELIEF_SOLID,
                            border_width=0)
                    ]], background_color=BACKGROUND_COLOR, pad=(0, 20), element_justification='center')],
                    [psg.Text("🤖 Number of AI Players", 
                             font=("Comic Sans MS", 24),
                             text_color=TEXT_COLOR,
                             background_color=BACKGROUND_COLOR,
                             pad=(0, 20))],
                    [psg.Column([[
                        psg.Frame("", [
                            [psg.Column([[
                                psg.Spin(values=[i for i in range(0, 6)],
                                        initial_value=0,
                                        key='ai_players',
                                        size=(3, 1),
                                        font=("Comic Sans MS", 20),
                                        text_color=TEXT_COLOR,
                                        background_color=SECONDARY_COLOR)
                            ]], background_color=SECONDARY_COLOR, pad=(10, 10))]], 
                            background_color=SECONDARY_COLOR,
                            relief=psg.RELIEF_SOLID,
                            border_width=0)
                    ]], background_color=BACKGROUND_COLOR, pad=(0, 20), element_justification='center')]
                ], background_color=BACKGROUND_COLOR, element_justification='center', pad=(40, 20))]
            ], background_color=BACKGROUND_COLOR, relief=psg.RELIEF_SOLID, border_width=0)],
            [psg.VPush()],
            [psg.Column([
                [psg.Button("▶ Start", 
                           button_color=(TEXT_COLOR, PRIMARY_COLOR),
                           font=("Comic Sans MS", 20, 'bold'),
                           size=self.button_styles['button']['small'],
                           border_width=0,
                           mouseover_colors=(TEXT_COLOR, ACCENT_COLOR),
                           pad=(10, 0),
                           key='Start'),
                 psg.Button("✖ Cancel", 
                           button_color=(TEXT_COLOR, '#FF5252'),
                           font=("Comic Sans MS", 20, 'bold'),
                           size=self.button_styles['button']['small'],
                           border_width=0,
                           mouseover_colors=(TEXT_COLOR, '#FF1744'),
                           pad=(10, 0),
                           key='Cancel')]
            ], background_color=BACKGROUND_COLOR, pad=(0, 20))],
            [psg.VPush()]
        ]

        window = psg.Window("New Game",
                          layout,
                          background_color=BACKGROUND_COLOR,
                          element_justification='c',
                          modal=True,
                          resizable=True,
                          finalize=True,
                          margins=(100, 50))
        
        window.maximize()

        # Bind hover events for Start and Cancel buttons
        self.bind_button_events(window, ['Start', 'Cancel'])

        while True:
            event, values = window.read()
            
            if event and ('+HOVER' in event or '+UNHOVER' in event):
                self.handle_button_hover(window, event)
            
            if event in (None, 'Cancel', psg.WIN_CLOSED):
                self.play_select_sound()
                window.close()
                self.run()
                return
            
            if event == 'Start':
                self.play_select_sound()
                playernum = int(values['players'])
                ai_players = int(values['ai_players'])
                
                if playernum < 1 or ai_players < 0 or ai_players > 5:
                    psg.popup("Invalid number of players: must be at least 1 human player and no more than 5 AI players",
                             font=("Comic Sans MS", 12),
                             background_color=BACKGROUND_COLOR,
                             text_color=TEXT_COLOR)
                    continue
                
                window.close()
                break

        self.game = Game()
        
        # Get player names
        name_layout = [
            [psg.VPush()],
            [psg.Text("Enter Player Names", 
                     font=("Comic Sans MS", 50),
                     text_color=TEXT_COLOR,
                     background_color=BACKGROUND_COLOR,
                     pad=(0, 40))],
            [psg.VPush()],
            [psg.Column([
                *sum([[
                    [psg.Text(f"Player {i+1}:", 
                             font=("Comic Sans MS", 24),
                             text_color=TEXT_COLOR,
                             background_color=BACKGROUND_COLOR,
                             pad=(0, 10))],
                    [psg.Input(key=f'name_{i}', 
                             size=(30, 1), 
                             font=("Comic Sans MS", 20),
                             background_color=SECONDARY_COLOR,
                             text_color=TEXT_COLOR,
                             pad=(0, 20))]
                ] for i in range(playernum)], [])
            ], background_color=BACKGROUND_COLOR, pad=(0, 20))],
            [psg.VPush()],
            [psg.Button("Start Game", 
                       button_color=(TEXT_COLOR, PRIMARY_COLOR), 
                       font=("Comic Sans MS", 20),
                       size=(20, 2),
                       border_width=0,
                       mouseover_colors=(TEXT_COLOR, ACCENT_COLOR),
                       pad=(0, 20),
                       key='Start_Game')],
            [psg.VPush()]
        ]

        window = psg.Window("Player Names",
                          name_layout,
                          background_color=BACKGROUND_COLOR,
                          element_justification='c',
                          modal=True,
                          resizable=True,
                          finalize=True)
        
        window.maximize()

        # Bind hover events for the Start Game button
        window['Start_Game'].bind('<Enter>', '+HOVER')
        window['Start_Game'].bind('<Leave>', '+UNHOVER')

        while True:
            event, values = window.read()
            
            if event and ('+HOVER' in event or '+UNHOVER' in event):
                self.handle_button_hover(window, event)
            
            if event == 'Start_Game':
                self.play_select_sound()
                break
            elif event in (None, psg.WIN_CLOSED):
                self.play_select_sound()
                window.close()
                self.run()
                return

        # Only proceed with game setup if window wasn't closed
        for i in range(playernum):
            player = Player()
            player.name = values[f'name_{i}'] if values[f'name_{i}'] else f"Player {i+1}"
            self.game.players.append(player)

        # Add AI players
        for i in range(ai_players):
            if self.__aidifficulty == 'Easy':
                ai = EasyAI()
            else:
                ai = HardAI()
            ai.name = f"AI {i+1}"
            self.game.players.append(ai)

        # Start the game
        while self.game.roundnum < self.game.NUM_ROUNDS:
            self.roundgui()

        # Show end game screen
        self.show_end_game()

    # round sequence
    def roundgui(self):
        self.game.roundnum += 1
    
        # Get current theme colors
        theme = self.color_themes[self.current_theme]
        BACKGROUND_COLOR = theme['background']
        PRIMARY_COLOR = theme['primary']
        SECONDARY_COLOR = theme['secondary']
        TEXT_COLOR = theme['text']
        ACCENT_COLOR = theme['accent']
        
        # Create a smooth round transition screen
        layout = [
            [psg.VPush()],
            [psg.Text(f"Round {self.game.roundnum}", 
                     font=("Comic Sans MS", 80, 'bold'),
                     text_color=TEXT_COLOR,
                     background_color=BACKGROUND_COLOR,
                     pad=(0, 30))],
            [psg.Text("🏆 Current Standings", 
                     font=("Comic Sans MS", 36, 'bold'),
                     text_color=ACCENT_COLOR,
                     background_color=BACKGROUND_COLOR,
                     pad=(0, 20))],
            [psg.Frame("", [
                [psg.Column([
                    # Header row
                    [psg.Column([
                        [psg.Text("Rank", 
                                font=("Comic Sans MS", 20, 'bold'),
                                text_color=ACCENT_COLOR,
                                background_color=SECONDARY_COLOR,
                                pad=(20, 10),
                                size=(8, 1),
                                justification='center')],
                    ], background_color=SECONDARY_COLOR),
                    psg.Column([
                        [psg.Text("Player", 
                                font=("Comic Sans MS", 20, 'bold'),
                                text_color=ACCENT_COLOR,
                                background_color=SECONDARY_COLOR,
                                pad=(20, 10),
                                size=(15, 1),
                                justification='center')],
                    ], background_color=SECONDARY_COLOR),
                    psg.Column([
                        [psg.Text("Score", 
                                font=("Comic Sans MS", 20, 'bold'),
                                text_color=ACCENT_COLOR,
                                background_color=SECONDARY_COLOR,
                                pad=(20, 10),
                                size=(8, 1),
                                justification='center')],
                    ], background_color=SECONDARY_COLOR)],
                    # Player rows
                    *[[psg.Column([
                        [psg.Text(f"#{i+1}", 
                                font=("Comic Sans MS", 20, 'bold'),
                                text_color=ACCENT_COLOR if i == 0 else TEXT_COLOR,
                                background_color=SECONDARY_COLOR,
                                pad=(20, 10),
                                size=(8, 1),
                                justification='center')],
                    ], background_color=SECONDARY_COLOR),
                    psg.Column([
                        [psg.Text(f"{player.name}", 
                                font=("Comic Sans MS", 20),
                                text_color=TEXT_COLOR,
                                background_color=SECONDARY_COLOR,
                                pad=(20, 10),
                                size=(15, 1),
                                justification='center')],
                    ], background_color=SECONDARY_COLOR),
                    psg.Column([
                        [psg.Text(f"{player.scorecard.count_score()}", 
                                font=("Comic Sans MS", 20, 'bold'),
                                text_color=ACCENT_COLOR,
                                background_color=SECONDARY_COLOR,
                                pad=(20, 10),
                                size=(8, 1),
                                justification='center')],
                    ], background_color=SECONDARY_COLOR)]
                    for i, player in enumerate(sorted(self.game.players, 
                                                    key=lambda x: x.scorecard.count_score(), 
                                                    reverse=True))]
                ], background_color=SECONDARY_COLOR,
                   element_justification='center',
                   pad=(20, 20))]], 
                background_color=SECONDARY_COLOR,
                relief=psg.RELIEF_SOLID,
                border_width=0)],
            [psg.VPush()],
            [psg.Button("▶ Start Round",
                       size=(30, 2),
                       font=("Comic Sans MS", 24, 'bold'),
                       button_color=(TEXT_COLOR, PRIMARY_COLOR),
                       mouseover_colors=(TEXT_COLOR, ACCENT_COLOR),
                       border_width=0,
                       pad=(0, 30))]
        ]
        
        window = psg.Window(f"Round {self.game.roundnum}",
                          layout,
                          background_color=BACKGROUND_COLOR,
                          element_justification='c',
                          no_titlebar=True,
                          modal=True,
                          resizable=True,
                          finalize=True)
        
        window.maximize()
        
        # Bind hover event for Start Round button
        window['▶ Start Round'].bind('<Enter>', '+HOVER')
        window['▶ Start Round'].bind('<Leave>', '+UNHOVER')

        while True:
            event, values = window.read()
            
            if event and ('+HOVER' in event or '+UNHOVER' in event):
                self.handle_button_hover(window, event)
            
            if event == '▶ Start Round':
                self.play_select_sound()
                break

        # Add a fade-out effect
        for alpha in range(255, 0, -15):
            window.set_alpha(alpha)
            time.sleep(0.01)
        
        window.close()
        
        # Play the round
        for player in self.game.players:
            if isinstance(player, EasyAI) or isinstance(player, HardAI):
                self.ai_turn_gui(player)
            else:
                self.turngui(player)

    # turn sequence
    def turngui(self, player):
        # Get current theme colors
        theme = self.color_themes[self.current_theme]
        BACKGROUND_COLOR = theme['background']
        PRIMARY_COLOR = theme['primary']
        SECONDARY_COLOR = theme['secondary']
        TEXT_COLOR = theme['text']
        ACCENT_COLOR = theme['accent']
        
        self.game.rerolls = 0
        # Don't roll dice immediately - wait for first roll button

        # Create scoring buttons with clearer format
        scoring_buttons = []
        for idx, key in enumerate(player.scorecard.keylist, 1):
            if player.scorecard.scorecard[key] is not None:
                # Already scored categories
                display_text = f"{idx}. {key}: {player.scorecard.scorecard[key]} ✓"
                scoring_buttons.append(
                    [psg.Text(display_text,
                              size=(40, 1),
                              font=("Comic Sans MS", 14),
                            text_color=ACCENT_COLOR,
                            background_color=BACKGROUND_COLOR)]
                )
            else:
                display_text = f"{idx}. {key}"
                scoring_buttons.append(
                    [psg.Button(display_text,
                            size=(40, 1),
                              key=f'score_{idx}',
                            font=("Comic Sans MS", 14),
                              button_color=(TEXT_COLOR, SECONDARY_COLOR),
                              mouseover_colors=(TEXT_COLOR, PRIMARY_COLOR),
                              disabled=True,  # Disable scoring until first roll
                              border_width=1)]
                )

        # Create initial dice section with hidden dice
        dice_section = [
            [psg.Frame("Available Dice", [
                [psg.Column([[psg.Button("?",
                                    font=("Arial", 60),
                                    size=(2, 1),
                                    key=f'dice_{idx}',
                                    button_color=(TEXT_COLOR, SECONDARY_COLOR),
                                    mouseover_colors=(ACCENT_COLOR, PRIMARY_COLOR),
                                    visible=False,
                                    border_width=1)
                            for idx in range(5)]], 
                        background_color=BACKGROUND_COLOR,
                        pad=(10, 10),
                        element_justification='center')]
            ], font=("Comic Sans MS", 20, 'bold'), title_color=TEXT_COLOR, background_color=BACKGROUND_COLOR, relief=psg.RELIEF_RIDGE)],
            [psg.Frame("Kept Dice", [
                [psg.Column([[psg.Button("",
                                    font=("Arial", 60),
                                    size=(2, 1),
                                    key=f'kept_{i}',
                                    button_color=(TEXT_COLOR, SECONDARY_COLOR),
                                    mouseover_colors=(ACCENT_COLOR, PRIMARY_COLOR),
                                    border_width=1,
                                    visible=True)
                            for i in range(5)]], 
                        background_color=BACKGROUND_COLOR,
                        key='kept_dice',
                        pad=(10, 10),
                        element_justification='center')]
            ], font=("Comic Sans MS", 20, 'bold'), title_color=TEXT_COLOR, background_color=BACKGROUND_COLOR, relief=psg.RELIEF_RIDGE)],
            [psg.VPush()],
            [psg.Button("🎲 Roll Dice 🎲", key='first_roll',  # First roll button
                       font=("Comic Sans MS", 24, 'bold'),
                       size=(20, 2),
                       button_color=(TEXT_COLOR, PRIMARY_COLOR),
                       mouseover_colors=(TEXT_COLOR, ACCENT_COLOR),
                       border_width=3,
                       pad=(0, 20)),
             psg.Button("🎲 Roll Again 🎲", key='reroll',  # Reroll button (initially disabled)
                       font=("Comic Sans MS", 24, 'bold'),
                       size=(20, 2),
                       button_color=(TEXT_COLOR, PRIMARY_COLOR),
                       mouseover_colors=(TEXT_COLOR, ACCENT_COLOR),
                       disabled=True,
                       border_width=3,
                       pad=(0, 20))]
        ]

        # Create a scrollable column for scoring buttons with increased size
        scoring_frame = psg.Frame("📋 Scorecard", [
            [psg.Column(scoring_buttons, 
                       scrollable=False,
                       background_color=BACKGROUND_COLOR,
                       element_justification='center',
                       pad=(5, 5))]
        ], font=("Comic Sans MS", 20, 'bold'), title_color=TEXT_COLOR, background_color=BACKGROUND_COLOR, relief=psg.RELIEF_RIDGE)

        left_column = [
            [psg.Frame("🎮 Game Info", [
                [psg.Column([
                    [psg.Text(f"Round {self.game.roundnum} - {player.name}'s turn", 
                             font=("Comic Sans MS", 32, 'bold'),
                             text_color=TEXT_COLOR,
                             background_color=BACKGROUND_COLOR,
                             justification='center')],
                    [psg.Text(f"Rerolls remaining: {self.game.REROLLS - self.game.rerolls}", 
                             key='rerolls',
                             font=("Comic Sans MS", 20),
                             text_color=ACCENT_COLOR,
                             background_color=BACKGROUND_COLOR,
                             justification='center')]
                ], background_color=BACKGROUND_COLOR, element_justification='center')]
            ], font=("Comic Sans MS", 20, 'bold'), title_color=TEXT_COLOR, background_color=BACKGROUND_COLOR, relief=psg.RELIEF_RIDGE)],
            [psg.Column(dice_section, 
                       background_color=BACKGROUND_COLOR,
                       pad=(20, 20),
                       element_justification='center')]
        ]

        right_column = [
            [scoring_frame],
            [psg.Frame("🌟 Bonus", [
                [psg.Text(f"Current Bonus: {player.scorecard.bonus_calc()}", 
                         font=("Comic Sans MS", 20, 'bold'),
                         text_color=ACCENT_COLOR,
                         background_color=BACKGROUND_COLOR,
                         justification='center')]
            ], font=("Comic Sans MS", 15, 'bold'), title_color=TEXT_COLOR, background_color=BACKGROUND_COLOR, relief=psg.RELIEF_RIDGE)]
        ]

        if self.EZboardopt:
            EZboard = EZBoard(player)
            EZboardtable = psg.Table(values=[], 
                                   headings=["Category", "Expected Score"],
                                   num_rows=14,
                                   auto_size_columns=True,
                                   justification='c',
                                   font=("Comic Sans MS", 14),
                                   background_color=SECONDARY_COLOR,
                                   text_color=TEXT_COLOR,
                                   header_background_color=PRIMARY_COLOR,
                                   header_text_color=TEXT_COLOR)
            right_column.insert(1, [psg.Frame("🎯 Expected Scores", [
                [psg.Column([[EZboardtable]], 
                           background_color=BACKGROUND_COLOR,
                           scrollable=True,
                           vertical_scroll_only=True,
                           size=(400, 300),
                           element_justification='center')]
            ], font=("Comic Sans MS", 20, 'bold'), title_color=TEXT_COLOR, background_color=BACKGROUND_COLOR, relief=psg.RELIEF_RIDGE)])

        layout = [
            [psg.Column(left_column, background_color=BACKGROUND_COLOR, pad=(20, 20), element_justification='center'),
                         psg.VerticalSeparator(),
                         psg.Column(right_column, background_color=BACKGROUND_COLOR, pad=(20, 20), element_justification='center')]
        ]

        window = psg.Window("🎲 Yahtzee", 
                          layout,
                          background_color=BACKGROUND_COLOR,
                          element_justification='c',
                          resizable=True,
                          finalize=True)
        
        window.maximize()
        kept_indices = []
        kept_values = []
        first_roll_done = False

        while True:
            event, values = window.read()
            
            if event == psg.WIN_CLOSED:
                sys.exit()
                
            # Handle first roll
            elif event == 'first_roll':
                self.play_sound(self.dice_roll_sound)  # Play dice roll sound
                self.game.dice.roll()
                first_roll_done = True
                
                # Animate dice roll
                for _ in range(10):
                    for i in range(5):
                        random_face = random.randint(1, 6)
                        window[f'dice_{i}'].update(text=self.dice_symbols[random_face], visible=True)
                    window.refresh()
                    time.sleep(0.05)
                
                # Show final dice values
                for i, dice in enumerate(self.game.dice.get_dice()):
                    window[f'dice_{i}'].update(text=self.dice_symbols[dice], visible=True)
                
                # Enable reroll button and scoring buttons
                window['reroll'].update(disabled=False)
                window['first_roll'].update(disabled=True)
                
                # Enable scoring buttons
                for idx in range(1, 14):
                    if player.scorecard.scorecard[player.scorecard.keylist[idx-1]] is None:
                        window[f'score_{idx}'].update(disabled=False)
                
                # Update EZBoard if enabled
                if self.EZboardopt:
                    EZboard.update_scorecard(self.game.dice)
                    EZboardtable.update(EZboard.genlist())
                
                # Update potential scores if EZboard is enabled
                for idx, key in enumerate(player.scorecard.keylist, 1):
                    if player.scorecard.scorecard[key] is None:
                        potential_score = player.scorecard.score_roll(self.game.dice, idx)
                        player.scorecard.scorecard[key] = None
                        
                        if self.EZboardopt:
                            display_text = f"{idx}. {key} → {potential_score} points"
                            window[f'score_{idx}'].update(text=display_text)
                
            # Rest of the event handling remains the same...
            elif event.startswith('dice_'):
                if first_roll_done and self.game.rerolls < self.game.REROLLS:
                    idx = int(event.split('_')[1])
                    if idx not in kept_indices:
                        kept_indices.append(idx)
                        dice_value = self.game.dice.get_dice()[idx]
                        kept_values.append(dice_value)
                        window[f'kept_{len(kept_indices)-1}'].update(text=self.dice_symbols[dice_value])
                        window[event].update(visible=False)
            
            elif event.startswith('kept_'):
                kept_idx = int(event.split('_')[1])
                if kept_idx < len(kept_indices):
                    orig_idx = kept_indices[kept_idx]
                    dice_value = kept_values[kept_idx]
                    kept_indices.pop(kept_idx)
                    kept_values.pop(kept_idx)
                    window[f'dice_{orig_idx}'].update(text=self.dice_symbols[dice_value], visible=True)
                    for i in range(5):
                        if i < len(kept_values):
                            window[f'kept_{i}'].update(text=self.dice_symbols[kept_values[i]])
                        else:
                            window[f'kept_{i}'].update(text="")
            
            elif event == 'reroll':
                reroll_indices = [i+1 for i in range(5) if i not in kept_indices]
                
                if self.game.rerolls < self.game.REROLLS:
                    self.play_sound(self.dice_roll_sound)  # Play dice roll sound
                    self.game.rerolls += 1
                    self.game.dice.reroll(reroll_indices)
                    
                    for _ in range(10):
                        for i in range(5):
                            if i not in kept_indices:
                                random_face = random.randint(1, 6)
                                window[f'dice_{i}'].update(text=self.dice_symbols[random_face])
                        window.refresh()
                        time.sleep(0.05)
                    
                    for i, dice in enumerate(self.game.dice.get_dice()):
                        if i not in kept_indices:
                            window[f'dice_{i}'].update(text=self.dice_symbols[dice], visible=True)
                    
                    window['rerolls'].update(f"Rerolls remaining: {self.game.REROLLS - self.game.rerolls}")
                    
                    if self.EZboardopt:
                        EZboard.update_scorecard(self.game.dice)
                        EZboardtable.update(EZboard.genlist())
                    
                    for idx, key in enumerate(player.scorecard.keylist, 1):
                        if player.scorecard.scorecard[key] is None:
                            potential_score = player.scorecard.score_roll(self.game.dice, idx)
                            player.scorecard.scorecard[key] = None
                            
                            if self.EZboardopt:
                                display_text = f"{idx}. {key} → {potential_score} points"
                            else:
                                display_text = f"{idx}. {key}"
                            
                            window[f'score_{idx}'].update(text=display_text)
                    
                    if self.game.rerolls == self.game.REROLLS:
                        window['reroll'].update(disabled=True)
            
            elif event.startswith('score_'):
                category_idx = int(event.split('_')[1])
                category_name = player.scorecard.keylist[category_idx-1]
                
                # Get the score before applying it
                if category_name == "12.yahtzee":
                    actual_score = player.scorecard.score_yahtzee(self.game.dice)
                    player.scorecard.scorecard[category_name] = None
                    if actual_score == 50:  # If it's a valid Yahtzee
                        self.play_sound(self.yahtzee_sound)
                    elif actual_score > 0:  # If points were scored
                        self.play_sound(self.point_sound)
                else:
                    # Handle other scoring categories
                    if category_name == "1.ones":
                        actual_score = player.scorecard.score_ones(self.game.dice)
                    elif category_name == "2.twos":
                        actual_score = player.scorecard.score_twos(self.game.dice)
                    elif category_name == "3.threes":
                        actual_score = player.scorecard.score_threes(self.game.dice)
                    elif category_name == "4.fours":
                        actual_score = player.scorecard.score_fours(self.game.dice)
                    elif category_name == "5.fives":
                        actual_score = player.scorecard.score_fives(self.game.dice)
                    elif category_name == "6.sixes":
                        actual_score = player.scorecard.score_sixes(self.game.dice)
                    elif category_name == "7.three of a kind":
                        actual_score = player.scorecard.score_three_of_a_kind(self.game.dice)
                    elif category_name == "8.four of a kind":
                        actual_score = player.scorecard.score_four_of_a_kind(self.game.dice)
                    elif category_name == "9.full house":
                        actual_score = player.scorecard.score_full_house(self.game.dice)
                    elif category_name == "10.small straight":
                        actual_score = player.scorecard.score_small_straight(self.game.dice)
                    elif category_name == "11.large straight":
                        actual_score = player.scorecard.score_large_straight(self.game.dice)
                    elif category_name == "13.chance":
                        actual_score = player.scorecard.score_chance(self.game.dice)
                    
                    # Play point sound if points were scored
                    if actual_score > 0:
                        self.play_sound(self.point_sound)
                
                # Set the score directly in the scorecard
                player.scorecard.scorecard[category_name] = actual_score
                
                score_layout = [
                    [psg.Text("🎯 Category Scored!", 
                             font=("Comic Sans MS", 24, 'bold'),
                             text_color=TEXT_COLOR,
                             background_color=BACKGROUND_COLOR,
                             justification='center')],
                    [psg.Text(f"{category_name}", 
                             font=("Comic Sans MS", 20),
                             text_color=ACCENT_COLOR,
                             background_color=BACKGROUND_COLOR,
                             justification='center')],
                    [psg.Text(f"+{actual_score}", 
                             font=("Comic Sans MS", 36, 'bold'),
                             text_color=PRIMARY_COLOR,
                             background_color=BACKGROUND_COLOR,
                             justification='center')],
                    [psg.Text("points", 
                             font=("Comic Sans MS", 16),
                             text_color=TEXT_COLOR,
                             background_color=BACKGROUND_COLOR,
                             justification='center')]
                ]
                
                score_window = psg.Window("Score",
                                        [[psg.Column(score_layout, 
                                                   background_color=BACKGROUND_COLOR,
                                                   element_justification='center',
                                                   pad=(20, 20))]],
                                        background_color=BACKGROUND_COLOR,
                                        no_titlebar=True,
                                        keep_on_top=True,
                                        element_justification='center',
                                        finalize=True)
                
                score_window.set_min_size((300, 200))
                
                for alpha in range(0, 255, 15):
                    score_window.set_alpha(alpha)
                    time.sleep(0.01)
                
                time.sleep(1.5)
                
                for alpha in range(255, 0, -15):
                    score_window.set_alpha(alpha)
                    time.sleep(0.01)
                
                score_window.close()
                break

        for alpha in range(255, 0, -15):
            window.set_alpha(alpha)
            time.sleep(0.01)
        
        window.close()

    # play AI turn in GUI
    def ai_turn_gui(self, player):
        try:
            # Get current theme colors
            theme = self.color_themes[self.current_theme]
            BACKGROUND_COLOR = theme['background']
            PRIMARY_COLOR = theme['primary']
            SECONDARY_COLOR = theme['secondary']
            TEXT_COLOR = theme['text']
            ACCENT_COLOR = theme['accent']

            # Play dice roll sound for AI's roll
            self.play_sound(self.dice_roll_sound)
            
            # Execute AI turn
            player.play()
            
            # Get current dice and score
            current_dice = player.dice.get_dice()
            dice_display = ' '.join([self.dice_symbols[d] for d in current_dice])
            
            # Create scoreboard
            scorecardlist = []
            for key in player.scorecard.keylist:
                scorecardlist.append([key, player.scorecard.scorecard[key]])

            # Create the table first
            score_table = psg.Table(
                values=scorecardlist,
                headings=["Category", "Score"],
                auto_size_columns=True,
                num_rows=min(len(scorecardlist), 13),
                font=("Comic Sans MS", 12),
                text_color=TEXT_COLOR,
                background_color=SECONDARY_COLOR,
                header_background_color=PRIMARY_COLOR,
                header_text_color=TEXT_COLOR,
                justification='center',
                pad=(20, 20)
            )

            # Create layout
            layout = [
                [psg.Text(f"Round {self.game.roundnum}", 
                         font=("Comic Sans MS", 24, 'bold'),
                         text_color=TEXT_COLOR,
                         background_color=BACKGROUND_COLOR,
                         pad=(0, 20))],
                         
                [psg.Text(f"{player.name}'s turn", 
                         font=("Comic Sans MS", 20),
                         text_color=ACCENT_COLOR,
                         background_color=BACKGROUND_COLOR,
                         pad=(0, 20))],
                         
                [psg.Text(dice_display, 
                         font=("Arial", 60),
                         text_color=PRIMARY_COLOR,
                         background_color=BACKGROUND_COLOR,
                         pad=(0, 30))],
                         
                [score_table],
                          
                [psg.Button("Next turn",
                           font=("Comic Sans MS", 16),
                           button_color=(TEXT_COLOR, PRIMARY_COLOR),
                           size=(12, 2),
                           border_width=0,
                           pad=(0, 20))]
            ]

            window = psg.Window(f"{player.name}'s Turn",
                              layout,
                              background_color=BACKGROUND_COLOR,
                              element_justification='c',
                              modal=True,
                              finalize=True)
            
            window.maximize()

            # Bind hover event
            window['Next turn'].bind('<Enter>', '+HOVER')
            window['Next turn'].bind('<Leave>', '+UNHOVER')

            # Event loop
            while True:
                event, values = window.read(timeout=100)  # Add timeout to keep window responsive
                
                if event == psg.WIN_CLOSED:
                    break
                    
                if event == 'Next turn':
                    self.play_select_sound()
                    break
                    
                if event and ('+HOVER' in event or '+UNHOVER' in event):
                    self.handle_button_hover(window, event)

            window.close()
            
        except Exception as e:
            print(f"[ERROR] Error in AI turn GUI: {str(e)}")
            # If there's an error, still need to close the window properly
            if 'window' in locals():
                window.close()

    
    # settings page
    def settings(self):
        # Get current theme colors
        theme = self.color_themes[self.current_theme]
        BACKGROUND_COLOR = theme['background']
        PRIMARY_COLOR = theme['primary']
        SECONDARY_COLOR = theme['secondary']
        TEXT_COLOR = theme['text']
        ACCENT_COLOR = theme['accent']
        
        try:
            # Create a scrollable column for the settings content
            settings_column = [
                [psg.Text("⚙️ Settings", 
                         font=("Comic Sans MS", 24, 'bold'), 
                         text_color=TEXT_COLOR,
                         background_color=BACKGROUND_COLOR,
                         pad=(0, 20))],
                
                [psg.Frame("Appearance", [
                    [psg.Text("Color Theme", 
                             font=("Comic Sans MS", 12),
                             text_color=TEXT_COLOR,
                             background_color=BACKGROUND_COLOR)],
                    [psg.Combo(list(self.color_themes.keys()), 
                              default_value=self.current_theme, 
                              key='color_theme', 
                              readonly=True,
                              font=("Comic Sans MS", 12),
                              size=(20, 1),
                              text_color=TEXT_COLOR,
                              background_color=BACKGROUND_COLOR,
                              button_background_color=PRIMARY_COLOR)]
                ], font=("Comic Sans MS", 12), title_color=TEXT_COLOR, 
                   background_color=BACKGROUND_COLOR,
                   pad=(10, 10))],
                
                [psg.Frame("Sound", [
                    [psg.Checkbox('🔇 Mute Sounds', 
                                default=self.mute_sounds,
                                key='mute_sounds',
                                text_color=TEXT_COLOR,
                                background_color=BACKGROUND_COLOR,
                                font=("Comic Sans MS", 12),
                                pad=(0, 10))]
                ], font=("Comic Sans MS", 12), title_color=TEXT_COLOR,
                   background_color=BACKGROUND_COLOR,
                   pad=(10, 10))],
                
                [psg.Frame("Gameplay", [
                    [psg.Text("AI Difficulty", 
                             font=("Comic Sans MS", 12),
                             text_color=TEXT_COLOR,
                             background_color=BACKGROUND_COLOR)],
                    [psg.Combo(['Easy', 'Hard'], 
                              default_value=self.__aidifficulty, 
                              key='aidifficulty', 
                              readonly=True,
                              font=("Comic Sans MS", 12),
                              size=(20, 1),
                              text_color=TEXT_COLOR,
                              background_color=BACKGROUND_COLOR,
                              button_background_color=PRIMARY_COLOR)],
                    [psg.Checkbox('Enable EZboard', 
                                default=self.EZboardopt, 
                                key='EZboard', 
                                text_color=TEXT_COLOR,
                                background_color=BACKGROUND_COLOR,
                                font=("Comic Sans MS", 12),
                                pad=(0, 10))]
                ], font=("Comic Sans MS", 12), title_color=TEXT_COLOR,
                   background_color=BACKGROUND_COLOR,
                   pad=(10, 10))]
            ]

            # Create buttons with consistent styling
            apply_button = psg.Button(
                "Apply",
                size=self.button_styles['button']['small'],
                font=self.button_styles['normal']['font'],
                button_color=(TEXT_COLOR, PRIMARY_COLOR),
                border_width=0,
                pad=(10, 10),
                key='Apply'
            )

            cancel_button = psg.Button(
                "Cancel",
                size=self.button_styles['button']['small'],
                font=self.button_styles['normal']['font'],
                button_color=(TEXT_COLOR, '#FF5252'),
                border_width=0,
                pad=(10, 10),
                key='Cancel'
            )

            # Update layout to use consistent buttons
            layout = [
                [psg.Column(settings_column,
                           scrollable=True,
                           vertical_scroll_only=True,
                           background_color=BACKGROUND_COLOR,
                           size=(400, 400))],
                [psg.Column([[apply_button, cancel_button]],
                          background_color=BACKGROUND_COLOR,
                          pad=(0, 10),
                          element_justification='center')]
            ]

            window = psg.Window("Settings", 
                              layout,
                              background_color=BACKGROUND_COLOR,
                              element_justification='c',
                              modal=True,
                              size=(450, 550),
                              finalize=True,
                              resizable=False)
            
            # Center the window on screen
            window.move(
                (window.get_screen_dimensions()[0] - 450) // 2,
                (window.get_screen_dimensions()[1] - 550) // 2
            )

            # Bind hover events for buttons
            window['Apply'].bind('<Enter>', '+HOVER')
            window['Apply'].bind('<Leave>', '+UNHOVER')
            window['Cancel'].bind('<Enter>', '+HOVER')
            window['Cancel'].bind('<Leave>', '+UNHOVER')

            while True:
                event, values = window.read()
                
                # Handle hover effects with scale animation
                if event and ('+HOVER' in event or '+UNHOVER' in event):
                    self.handle_button_hover(window, event)
                
                if event == "Apply":
                    self.current_theme = values['color_theme']
                    self.__aidifficulty = values['aidifficulty']
                    self.EZboardopt = values['EZboard']
                    self.mute_sounds = values['mute_sounds']
                    self.play_select_sound()
                    window.close()
                    self.run()
                    return
                elif event in (psg.WIN_CLOSED, "Cancel"):
                    self.play_select_sound()
                    window.close()
                    self.run()
                    return

        except Exception as e:
            if 'window' in locals():
                window.close()
            self.run()
            return

    def play_hover_sound(self):
        """Play hover sound effect"""
        if not self.mute_sounds:
            try:
                import pygame
                sound = pygame.mixer.Sound(self.hover_sound)
                sound.set_volume(0.3)  # Lower volume for hover sound
                sound.play()
            except Exception as e:
                pass

    def play_select_sound(self):
        """Play select sound effect"""
        if not self.mute_sounds:
            try:
                import pygame
                sound = pygame.mixer.Sound(self.select_sound)
                sound.play()
            except Exception as e:
                pass

    def smooth_button_animation(self, window, button_key, is_hover):
        """Perform smooth button animation"""
        try:
            button = window[button_key]
            if not button:
                return
                
            # Get base size based on button type
            if button_key == 'Start new Game':
                base_size = (30, 3)  # Main PLAY button
            elif button_key in ['Start', 'Cancel', 'Apply', 'Play Again', 'Exit', 'Back_btn', 'Reset_btn', 'Start_Game', 'Next turn']:
                base_size = (12, 2)  # Small buttons
            else:
                base_size = (25, 2)  # Regular menu buttons
            
            # Calculate target size with hover effect
            hover_scale = 1.1 if is_hover else 1.0  # Increase size by 10% on hover
            target_size = [
                int(base_size[0] * hover_scale),
                int(base_size[1] * hover_scale)
            ]
            
            # Update button size
            button.set_size(target_size)
            window.refresh()
            
        except Exception as e:
            pass  # Silently handle any hover errors

    def play_sound(self, sound_file):
        """Play a sound file"""
        if not self.mute_sounds:  # Only play sound if not muted
            try:
                import pygame
                sound = pygame.mixer.Sound(sound_file)
                sound.play()
                pygame.time.wait(50)  # Small wait to ensure sound starts playing
            except Exception as e:
                pass  # Silently handle any sound errors to not interrupt gameplay

    def show_end_game(self):
        # Play game over sound
        self.play_sound(self.game_over_sound)
        
        # Get current theme colors
        theme = self.color_themes[self.current_theme]
        BACKGROUND_COLOR = theme['background']
        PRIMARY_COLOR = theme['primary']
        TEXT_COLOR = theme['text']
        ACCENT_COLOR = theme['accent']

        # Calculate final scores and determine winner
        final_scores = []
        winner = None
        highest_score = -1
        
        for player in self.game.players:
            score = player.scorecard.count_score()
            final_scores.append([player.name, score])
            if score > highest_score:
                highest_score = score
                winner = player
            # Add player to leaderboard if they're not an AI
            if not isinstance(player, EasyAI) and not isinstance(player, HardAI):
                self.addtoleaderboard(player)

        # Sort scores in descending order
        final_scores.sort(key=lambda x: x[1], reverse=True)

        # Create layout for end game screen
        layout = [
            [psg.Text("🎮 Game Over! 🎮", 
                     font=("Comic Sans MS", 40, 'bold'),
                     text_color=TEXT_COLOR,
                     background_color=BACKGROUND_COLOR,
                     pad=(0, 20))],
            
            [psg.Text(f"🏆 Winner: {winner.name}", 
                     font=("Comic Sans MS", 30),
                     text_color=ACCENT_COLOR,
                     background_color=BACKGROUND_COLOR,
                     pad=(0, 20))],
            
            [psg.Text(f"Score: {highest_score}", 
                     font=("Comic Sans MS", 24),
                     text_color=TEXT_COLOR,
                     background_color=BACKGROUND_COLOR,
                     pad=(0, 20))],
            
            [psg.Frame("Final Standings", [
                [psg.Table(values=final_scores,
                          headings=["Player", "Score"],
                          auto_size_columns=True,
                          justification='center',
                          font=("Comic Sans MS", 12),
                          background_color=BACKGROUND_COLOR,
                          text_color=TEXT_COLOR,
                          header_background_color=PRIMARY_COLOR,
                          header_text_color=TEXT_COLOR,
                          num_rows=min(len(final_scores), 10))]
            ], font=("Comic Sans MS", 16),
               title_color=TEXT_COLOR,
               background_color=BACKGROUND_COLOR,
               pad=(10, 10))],
            
            [psg.Button("Play Again",
                       button_color=(TEXT_COLOR, PRIMARY_COLOR),
                       font=("Comic Sans MS", 14, 'bold'),
                       size=(15, 1),
                       pad=(5, 20)),
             psg.Button("Exit",
                       button_color=(TEXT_COLOR, '#FF5252'),
                       font=("Comic Sans MS", 14, 'bold'),
                       size=(15, 1),
                       pad=(5, 20))]
        ]

        window = psg.Window("Game Over",
                           layout,
                           background_color=BACKGROUND_COLOR,
                           element_justification='c',
                           modal=True,
                           finalize=True)
        
        # Bind hover events for Play Again and Exit buttons
        window['Play Again'].bind('<Enter>', '+HOVER')
        window['Play Again'].bind('<Leave>', '+UNHOVER')
        window['Exit'].bind('<Enter>', '+HOVER')
        window['Exit'].bind('<Leave>', '+UNHOVER')

        while True:
            event, values = window.read()
            
            if event and ('+HOVER' in event or '+UNHOVER' in event):
                self.handle_button_hover(window, event)
            
            if event == "Play Again":
                self.play_select_sound()
                window.close()
                self.run()
                return
            elif event in (psg.WIN_CLOSED, "Exit"):
                self.play_select_sound()
                window.close()
                sys.exit()

    def interpolate_color(self, color1, color2, t):
        """Interpolate between two hex colors."""
        # Convert hex to RGB
        def hex_to_rgb(hex_color):
            hex_color = hex_color.lstrip('#')
            return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        
        # Convert RGB to hex
        def rgb_to_hex(rgb):
            return '#{:02x}{:02x}{:02x}'.format(int(rgb[0]), int(rgb[1]), int(rgb[2]))
        
        # Get RGB values
        rgb1 = hex_to_rgb(color1)
        rgb2 = hex_to_rgb(color2)
        
        # Interpolate
        rgb = tuple(int(rgb1[i] + (rgb2[i] - rgb1[i]) * t) for i in range(3))
        return rgb_to_hex(rgb)

    def apply_alpha(self, hex_color, alpha):
        """Apply alpha value to a hex color."""
        rgb = self.hex_to_rgb(hex_color)
        return '#{:02x}{:02x}{:02x}'.format(
            int(rgb[0] * alpha),
            int(rgb[1] * alpha),
            int(rgb[2] * alpha)
        )

    def hex_to_rgb(self, hex_color):
        """Convert hex color to RGB tuple."""
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

    def create_gradient_text(self, text, color1, color2, font):
        """Create gradient text elements."""
        elements = []
        for i, char in enumerate(text):
            color = self.interpolate_color(color1, color2, i / len(text))
            elements.append(
                psg.Text(char,
                        font=font,
                        text_color=color,
                        background_color=self.color_themes[self.current_theme]['background'],
                        pad=(1, 1)))
        return elements

    def bind_button_events(self, window, button_keys):
        """Bind hover events to multiple buttons."""
        for key in button_keys:
            if key in window.key_dict:
                window[key].bind('<Enter>', '+HOVER')
                window[key].bind('<Leave>', '+UNHOVER')

    def handle_button_hover(self, window, event):
        """Handle button hover events with improved consistency"""
        try:
            btn_key = event.split('+')[0]
            is_hover = '+HOVER' in event
            
            if is_hover:
                self.play_hover_sound()
                
            # Get button colors based on button type
            theme = self.color_themes[self.current_theme]
            if btn_key in ['Exit', 'Reset_btn', 'Cancel']:
                base_color = '#FF5252'
                hover_color = '#FF1744'
            else:
                base_color = theme['primary']
                hover_color = theme['accent']
            
            # Update button color and size
            if btn_key in window.key_dict:
                button = window[btn_key]
                # Update color
                button.update(button_color=(theme['text'], hover_color if is_hover else base_color))
                # Update size with animation
                self.smooth_button_animation(window, btn_key, is_hover)
                
        except Exception as e:
            pass  # Silently handle any hover errors

###############################
# USE OF RECURSIVE VALIDATION #
###############################

# gets game mode from user input          
def __get_game_mode():
    game_mode = input("Play in terminal or GUI? (t/g): ")
    if game_mode == "t":
        game = Terminal()
        game.run()
    elif game_mode == "g":
        game = GUI()
        game.run()
    else:
        print("Invalid game mode")
        __get_game_mode()

# main function
if __name__ == "__main__":    
    __get_game_mode()








