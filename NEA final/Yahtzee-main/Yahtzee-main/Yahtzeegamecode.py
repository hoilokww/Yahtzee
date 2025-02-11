## Yahtzee game code ##

import random, math, PySimpleGUI as sg, re, numpy as np



class Player:           # Player class
    def __init__(self):
        
        self.name = None
        self.scorecard = Scorecard() # players have a scorecard object

    def get_name(self):
        return self.name
    
    def get_scorecard(self):
        return self.scorecard   
    
    def get_score(self):
        return self.scorecard.score
    
    def get_bonus(self):
        return self.scorecard.bonus
    
    def get_upper_score(self):
        return self.scorecard.upper_score
    
    def get_lower_score(self):
        return self.scorecard.lower_score


    def get_total_score(self):
        return self.scorecard.total_score
 


class Scorecard:        # Scorecard class - built in scoring methods
    def __init__(self):
        self.scorecard = {
            "1.ones": None,
            "2.twos": None,
            "3.threes": None,
            "4.fours": None,
            "5.fives": None,
            "6.sixes": None,
            "7.three of a kind": None,
            "8.four of a kind": None,
            "9.full house": None,
            "10.small straight": None,
            "11.large straight": None,
            "12.yahtzee": None,
            "13.chance": None
        }
        self.score = 0
        self.bonus = 0
        self.upper_score = 0
        self.lower_score = 0
        self.total_score = 0
        self.yahtzee_bonus = 0  # Track additional Yahtzees
        self.keylist = [key for key in self.scorecard.keys()]

    
    def show_scorecard(self):
        print("Scorecard")
        for key, value in self.scorecard.items():
            print(f"{key}: {value}")

    def score_roll(self, dice, choice):
        # Check for Yahtzee bonus first
        dice_values = dice.get_dice()
        first_die = dice_values[0]
        is_yahtzee = all(die == first_die for die in dice_values)
        
        if is_yahtzee and self.scorecard["12.yahtzee"] == 50:  # If this is a subsequent Yahtzee
            self.yahtzee_bonus += 50  # Add bonus points
        
        # Now proceed with normal scoring
        if choice == 1:
            self.scorecard["1.ones"] = self.score_ones(dice)
        elif choice == 2:
            self.scorecard["2.twos"] = self.score_twos(dice)
        elif choice == 3:
            self.scorecard["3.threes"] = self.score_threes(dice)
        elif choice == 4:
            self.scorecard["4.fours"] = self.score_fours(dice)
        elif choice == 5:
            self.scorecard["5.fives"] = self.score_fives(dice)
        elif choice == 6:
            self.scorecard["6.sixes"] = self.score_sixes(dice)
        elif choice == 7:
            self.scorecard["7.three of a kind"] = self.score_three_of_a_kind(dice)
        elif choice == 8:
            self.scorecard["8.four of a kind"] = self.score_four_of_a_kind(dice)
        elif choice == 9:
            self.scorecard["9.full house"] = self.score_full_house(dice)
        elif choice == 10:
            self.scorecard["10.small straight"] = self.score_small_straight(dice)
        elif choice == 11:
            self.scorecard["11.large straight"] = self.score_large_straight(dice)
        elif choice == 12:
            self.scorecard["12.yahtzee"] = self.score_yahtzee(dice)
        elif choice == 13:
            self.scorecard["13.chance"] = self.score_chance(dice)
        else:
            print("Invalid choice")

    def score_ones(self, dice):
        return dice.count(1)
    
    def score_twos(self, dice):
        return dice.count(2) * 2
    
    def score_threes(self, dice):
        return dice.count(3) * 3
    
    def score_fours(self, dice):
        return dice.count(4) * 4
    
    def score_fives(self, dice):
        return dice.count(5) * 5
    
    def score_sixes(self, dice):
        return dice.count(6) * 6
    
    def score_three_of_a_kind(self, dice):
        for die in dice.get_dice():
            if dice.count(die) >= 3:
                return sum(dice.get_dice())
            
        return 0
    
    
    def score_four_of_a_kind(self, dice):
        for die in dice.get_dice():
            if dice.count(die) >= 4:
                return sum(dice.get_dice())
        
        return 0
       
    def score_full_house(self, dice):
        countlist = []
        for die in dice.get_dice():
            countlist.append(dice.count(die))
        if 3 in countlist and 2 in countlist:
            return 25
        else:
            return 0
        
        
    # use regex to check for small straight
    def score_small_straight(self, dice):
        match = re.search(r'1234|2345|3456|12345|23456', ''.join(str(die) for die in sorted(list(set(dice.get_dice())))))
        if match:
            return 30
        else:
            return 0

    def score_large_straight(self, dice):
        if sorted(dice.get_dice()) == [2, 3, 4, 5, 6] or sorted(dice.get_dice()) == [1, 2, 3, 4, 5]:
            return 40
        else:
            return 0
    
    def score_yahtzee(self, dice):
        for die in dice.get_dice():
            if dice.count(die) == 5:
                return 50
            else:
                return 0

    def score_chance(self, dice):
        return sum(dice.get_dice())
    
    def count_score(self):
        # Reset scores before counting
        self.upper_score = 0
        self.lower_score = 0
        
        for key, value in self.scorecard.items():
            if value == None:
                    value = 0
            if key in ["1.ones", "2.twos", "3.threes", "4.fours", "5.fives", "6.sixes"]:
                self.upper_score += value
            else:
                self.lower_score += value
                
        # add bonus if applicable
        if self.upper_score >= 63:
            self.bonus = 35
        else:
            self.bonus = 0
            
        # Add Yahtzee bonus to lower score
        self.lower_score += self.yahtzee_bonus
            
        self.score = self.upper_score + self.lower_score + self.bonus
        return self.score
    
    def get_scorecard(self):
        return self.scorecard
    
    def get_score(self):
        return self.score
    
    def get_upper_score(self):
        return sum([self.scorecard[key] for key, value in self.scorecard.items() if (key in ["1.ones", "2.twos", "3.threes", "4.fours", "5.fives", "6.sixes"] and value != None)])
    
    # turns scorecard to list of tuples
    def genlist(self):
        dictlist = []
        for key, value in self.scorecard.items():
            dictlist.append([key,value])
        return dictlist
    
    def bonus_calc(self):
        if self.get_upper_score() >= 63:
            return '35'
        else:
            return f'0, ({self.get_upper_score() - 63})'
            

        
########################
# COMPLEX USE OF OOP #
########################
        
class EZBoard(Scorecard): # player assistance board
    def __init__(self, player):
        super().__init__()
        self.scorecard = {    # take out later as not needed?
            "1.ones": None,
            "2.twos": None,
            "3.threes": None,
            "4.fours": None,
            "5.fives": None,
            "6.sixes": None,
            "7.three of a kind": None,
            "8.four of a kind": None,
            "9.full house": None,
            "10.small straight": None,
            "11.large straight": None,
            "12.yahtzee": None,
            "13.chance": None
        }
        self.player = player

    def update_scorecard(self, dice):
        #calculate expected value for each category
        for key in self.scorecard:
            
                if key == "1.ones":
                    self.scorecard[key] = self.score_ones(dice)
                elif key == "2.twos":
                    self.scorecard[key] = self.score_twos(dice)
                elif key == "3.threes":
                    self.scorecard[key] = self.score_threes(dice)
                elif key == "4.fours":
                    self.scorecard[key] = self.score_fours(dice)
                elif key == "5.fives":
                    self.scorecard[key] = self.score_fives(dice)
                elif key == "6.sixes":
                    self.scorecard[key] = self.score_sixes(dice)
                elif key == "7.three of a kind":
                    self.scorecard[key] = self.score_three_of_a_kind(dice)
                elif key == "8.four of a kind":
                    self.scorecard[key] = self.score_four_of_a_kind(dice)
                elif key == "9.full house":
                    self.scorecard[key] = self.score_full_house(dice)
                elif key == "10.small straight":
                    self.scorecard[key] = self.score_small_straight(dice)
                elif key == "11.large straight":
                    self.scorecard[key] = self.score_large_straight(dice)
                elif key == "12.yahtzee":
                    self.scorecard[key] = self.score_yahtzee(dice)
                elif key == "13.chance":
                    self.scorecard[key] = self.score_chance(dice)
                else:
                    raise NotImplementedError

            
          
            
        return self.scorecard
    
    
    
    
        

    

    
class Dice:         # Dice class
    def __init__(self):
        self.dice = [0 for i in range(Game.DICE)]
        

   

    def get_dice(self):
        return self.dice

   
    
    def roll(self):
        for index in range(len(self.dice)):
            self.dice[index] = random.randint(1, 6)
        return self.dice


    
                   
    def reroll(self, rerollchoice):
        for choice in rerollchoice:
            self.dice[int(choice)-1] = random.randint(1, 6)

       
    
    #counts the instances of a given number in the dice list
    def count(self, number):
        return self.dice.count(number)
    
        
    


class Game:             # Game class


    #initialise constants
    REROLLS = 2
    DICE = 5
    NUM_ROUNDS = 13
    

    def __init__(self):
        
        self.AIplayers = 0
        self.dice = Dice()
        self.scorecard = Scorecard()
        self.roundnum = 0
        self.rerolls = 0        
        #allow multiple players
        self.players = []
        self.winner = None
        self.takennames = []
        
    # find winner
    def get_winner(self):
        
        current_score = 0
    
        for player in self.players:
            score = player.get_scorecard().count_score()
            if score >= current_score:
                current_score = score
                self.winner = player
            
        return self.winner   
    
    
      

# Easy AI class
class EasyAI(Player):
    def __init__(self):
        super().__init__()
        self.name = "Easy AI"
        self.scorecard = Scorecard()
        self.rerolls = 2
        self.dice = Dice()

    def play(self):
        try:
            self.dice.roll()
            category = self.__get_best_category()
            
            if category is None:
                for i in range(1, 14):
                    key = self.scorecard.keylist[i-1]
                    if self.scorecard.scorecard[key] is None:
                        category = i
                        break
            
            if category:
                self.scorecard.score_roll(self.dice, category)
                
        except Exception:
            for i in range(1, 14):
                key = self.scorecard.keylist[i-1]
                if self.scorecard.scorecard[key] is None:
                    self.scorecard.score_roll(self.dice, i)
                    break
    
    def __get_best_category(self):
        try:
            first_available = None
            for category in range(1, 14):
                category_key = self.scorecard.keylist[category-1]
                if self.scorecard.scorecard[category_key] is None:
                    first_available = category
                    break
            
            if first_available is None:
                return None
            
            best_score = -1
            best_category = first_available
            current_dice = self.dice.get_dice()
            
            for category in range(1, 14):
                category_key = self.scorecard.keylist[category-1]
                if self.scorecard.scorecard[category_key] is None:
                    score = 0
                    if category <= 6:  # Upper section
                        score = sum(d for d in current_dice if d == category)
                    elif category == 7:  # Three of a kind
                        score = self.scorecard.score_three_of_a_kind(self.dice)
                    elif category == 8:  # Four of a kind
                        score = self.scorecard.score_four_of_a_kind(self.dice)
                    elif category == 9:  # Full house
                        score = self.scorecard.score_full_house(self.dice)
                    elif category == 10:  # Small straight
                        score = self.scorecard.score_small_straight(self.dice)
                    elif category == 11:  # Large straight
                        score = self.scorecard.score_large_straight(self.dice)
                    elif category == 12:  # Yahtzee
                        score = self.scorecard.score_yahtzee(self.dice)
                    else:  # Chance
                        score = sum(current_dice)
                    
                    if score > best_score:
                        best_score = score
                        best_category = category
            
            return best_category
            
        except Exception:
            return first_available

# count how many of each dice there are

    def FindDiceState(self,dice_list):
        # Initialize a dictionary to store the count of each dice value
        dice_count = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0}

        # Iterate through the dice_list and update the counts
        for value in dice_list:
            # Check if the value is a valid dice value
            if value in dice_count:
                # Increment the count for the respective dice value
                dice_count[value] += 1
            else:
                print(f"Illegal dice value: {value}")

        return dice_count
        
    
    # choose category function
    def __choosecategory(self, dice):
        
        
        # make dictionary of scorable categories
        scored = []
        scoreablecategories = self.scorecard.get_scorecard().copy()
        for key, value in scoreablecategories.items():
            if value != None:
                scored.append(key)
        for key in scored:
            scoreablecategories.pop(key, None)

        predicted_scores = {}

        for key, value in scoreablecategories.items():
            if key == "1.ones":
                predicted_scores[1] = self.scorecard.score_ones(dice)
            elif key == "2.twos":
                predicted_scores[2] = self.scorecard.score_twos(dice)
            elif key == "3.threes":
                predicted_scores[3] = self.scorecard.score_threes(dice)
            elif key == "4.fours":
                predicted_scores[4] = self.scorecard.score_fours(dice)
            elif key == "5.fives":
                predicted_scores[5] = self.scorecard.score_fives(dice)
            elif key == "6.sixes":
                predicted_scores[6] = self.scorecard.score_sixes(dice)
            elif key == "7.three of a kind":
                predicted_scores[7] = self.scorecard.score_three_of_a_kind(dice)
            elif key == "8.four of a kind":
                predicted_scores[8] = self.scorecard.score_four_of_a_kind(dice)
            elif key == "9.full house":
                predicted_scores[9] = self.scorecard.score_full_house(dice)
            elif key == "10.small straight":
                predicted_scores[10] = self.scorecard.score_small_straight(dice)
            elif key == "11.large straight":
                predicted_scores[11] = self.scorecard.score_large_straight(dice)
            elif key == "12.yahtzee":
                predicted_scores[12] = self.scorecard.score_yahtzee(dice)
            elif key == "13.chance":
                predicted_scores[13] = self.scorecard.score_chance(dice)
            else:
                raise NotImplementedError
            
        # sort the dictionary by value
        
        sorted_scores = self.__merge_sort(list(predicted_scores.items()))
        category = sorted_scores.pop()
        chosen_category = category[0]
        expscore = category[1]

        # check if exp score is zero, and if there are rerolls left then reroll all dice
        if expscore == 0 and self.rerolls > 0:
            self.dice.roll()
            self.rerolls -= 1
            return self.__choosecategory(self.dice)


        
        else:
            self.rerolls = 2
            return chosen_category
        
#####################
# COMPLEX USE OF OOP #
#####################
        
class HardAI(Player):
    def __init__(self):
        super().__init__()
        self.name = "Hard AI"
        self.scorecard = Scorecard()
        self.rerolls = 2
        self.dice = Dice()
    
    def play(self):
        try:
            self.dice.roll()
            current_dice = self.dice.get_dice()
            
            # First reroll
            if self.rerolls > 0:
                reroll_indices = self.__get_reroll_indices(current_dice)
                if reroll_indices:
                    self.dice.reroll(reroll_indices)
                    self.rerolls -= 1
                    current_dice = self.dice.get_dice()
            
            # Second reroll
            if self.rerolls > 0:
                reroll_indices = self.__get_reroll_indices(current_dice)
                if reroll_indices:
                    self.dice.reroll(reroll_indices)
                    self.rerolls -= 1
                    current_dice = self.dice.get_dice()
            
            category = self.__get_best_category()
            
            if category is None:
                for i in range(1, 14):
                    key = self.scorecard.keylist[i-1]
                    if self.scorecard.scorecard[key] is None:
                        category = i
                        break
            
            if category:
                self.scorecard.score_roll(self.dice, category)
                
        except Exception:
            for i in range(1, 14):
                key = self.scorecard.keylist[i-1]
                if self.scorecard.scorecard[key] is None:
                    self.scorecard.score_roll(self.dice, i)
                    break
    
    def __get_reroll_indices(self, current_dice):
        try:
            counts = {1:0, 2:0, 3:0, 4:0, 5:0, 6:0}
            for die in current_dice:
                counts[die] += 1
            
            max_count = max(counts.values())
            max_value = max(counts.items(), key=lambda x: (x[1], x[0]))[0]
            
            if max_count == 5:  # Yahtzee
                return []
            
            sorted_dice = sorted(current_dice)
            if sorted_dice in ([1,2,3,4,5], [2,3,4,5,6]):  # Large Straight
                return []
            
            reroll = []
            for i, die in enumerate(current_dice):
                if die != max_value:
                    reroll.append(i + 1)
            
            return reroll
            
        except Exception:
            return []
    
    def __get_best_category(self):
        try:
            first_available = None
            for category in range(1, 14):
                category_key = self.scorecard.keylist[category-1]
                if self.scorecard.scorecard[category_key] is None:
                    first_available = category
                break
        
            if first_available is None:
                return None
            
            best_score = -1
            best_category = first_available
            current_dice = self.dice.get_dice()
            
            for category in range(1, 14):
                category_key = self.scorecard.keylist[category-1]
                if self.scorecard.scorecard[category_key] is None:
                    score = 0
                    if category <= 6:  # Upper section
                        score = sum(d for d in current_dice if d == category)
                    elif category == 7:  # Three of a kind
                        score = self.scorecard.score_three_of_a_kind(self.dice)
                    elif category == 8:  # Four of a kind
                        score = self.scorecard.score_four_of_a_kind(self.dice)
                    elif category == 9:  # Full house
                        score = self.scorecard.score_full_house(self.dice)
                    elif category == 10:  # Small straight
                        score = self.scorecard.score_small_straight(self.dice)
                    elif category == 11:  # Large straight
                        score = self.scorecard.score_large_straight(self.dice)
                    elif category == 12:  # Yahtzee
                        score = self.scorecard.score_yahtzee(self.dice)
                    else:  # Chance
                        score = sum(current_dice)
                    
                    if score > best_score:
                        best_score = score
                        best_category = category
            
            return best_category
            
        except Exception:
            return first_available





        

