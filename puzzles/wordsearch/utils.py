import random
import string
from wordsearch.models import Puzzle, Word, Char
from datetime import datetime
import os
from gensim.models import Word2Vec
from puzzles.logger import logging



     



def generate_grids(puzzle, word_list):
    row_len = puzzle.row_length
    col_len = puzzle.col_length

    # Prepare empty grid
    grid = [["" for _ in range(col_len)] for _ in range(row_len)]
    char_objs = [[None for _ in range(col_len)] for _ in range(row_len)]
    directions = [(0, 1), (1, 0), (1, 1), (-1, 1)]

    # Place words
    for word_text in word_list:
        word_obj = Word.objects.create(puzzle=puzzle, word=word_text)
        placed = False
        attempts = 0

        while not placed and attempts < 100:
            attempts += 1
            for dx, dy in random.sample(directions, len(directions)):
                x = random.randint(0, row_len - 1)
                y = random.randint(0, col_len - 1)
                end_x = x + dx * (len(word_text) - 1)
                end_y = y + dy * (len(word_text) - 1)

                if 0 <= end_x < row_len and 0 <= end_y < col_len:
                    can_place = True
                    for i in range(len(word_text)):
                        nx = x + dx * i
                        ny = y + dy * i
                        if grid[nx][ny] not in ("", word_text[i]):
                            can_place = False
                            break

                    if can_place:
                        for i in range(len(word_text)):
                            nx = x + dx * i
                            ny = y + dy * i
                            grid[nx][ny] = word_text[i]
                            char_objs[nx][ny] = {'char': word_text[i], 'word': word_obj}
                        placed = True
                        break

    # Now fill grid row-by-row, creating Char objects in order
    for i in range(row_len):
        for j in range(col_len):
            if not grid[i][j]:
                grid[i][j] = random.choice(string.ascii_lowercase)
                char_objs[i][j] = {'char': grid[i][j], 'word': None}

            index = i * col_len + j
            Char.objects.create(
                character=char_objs[i][j]['char'],
                index=index,
                puzzle=puzzle,
                word=char_objs[i][j]['word']
            )

    return grid,word_list

def build_puzzle():
     
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    BASE_DIR = "/".join(BASE_DIR.split("/")[:-1])

     
    model_path = os.path.join( BASE_DIR,"artifacts","words.model")
    model = Word2Vec.load(model_path)
    words = model.wv.index_to_key
    choice = random.sample(words,10)
    puzzle = Puzzle(row_length=12, col_length=12)
    puzzle.save()
    logging.info("New puzzle created")
    grid, placed_words = generate_grids(puzzle, choice)

     

def process_form_data(form_data):
    char_list,index_list = [],[]
    for i in form_data:
        char_list.append(i[0])
        index_list.append(int(i[1:].strip()))
         
    return [char_list,index_list]
def select_color(puzzle):
    COLORS = [
    '#4682B4',  # Soft Blue
    '#CD5C5C',  # Warm Red
    '#228B22',  # Forest Green
    '#DAA520',  # Golden Yellow
    '#6A5ACD',  # Deep Purple
    '#FF6F61',  # Coral Pink
    '#008080',  # Teal
    '#9370DB',  # Lavender
    '#CC5500',  # Burnt Orange
    '#708090',  # Slate Gray
    ]
    words= puzzle.words.all()
    assigned_colors = [word.word_color for word in words if word.word_color]
    available_colors = [color for color in COLORS if color not in assigned_colors]
    if available_colors:
        return random.choice(available_colors)
    return  "#faf"

     

def check_word(char_list,words,puzzle,chars):
    
    word = "".join(char_list)
    word_bank = [w.word for w in words]
    for w in words:
        if w.word == word or w.word == word[::-1]:
            w.word_checked = True
            selected_color = select_color(puzzle)
            w.word_color = selected_color
            w.save()
            
            w.chars.update(char_checked = True)
            w.chars.update(char_color =selected_color )
            break
        
            
def check_puzzle_copmleated(puzzle,words):
    # check each word
    for word in words:
        if not  word.word_checked:
            puzzle.grid_checked = False
            puzzle.save()
             
            return False
     
    puzzle.finished_time = datetime.now()
    puzzle.inProgress = False
    puzzle.grid_checked = True
    puzzle.save()
   
     
         
        

    return True

 

def initialize_puzzle(puzzle):
     
    puzzle.initial_time = datetime.now()
    puzzle.inProgress = True
    logging.info(f"{puzzle.user} started a puzzle")
    puzzle.save()

 


     
     
     
