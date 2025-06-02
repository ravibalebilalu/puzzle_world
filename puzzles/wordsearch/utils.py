import random
import string
from wordsearch.models import Puzzle, Word, Char

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

def process_form_data(form_data):
    char_list,index_list = [],[]
    for i in form_data:
        char_list.append(i[0])
        index_list.append(int(i[1:].strip()))
         
    return [char_list,index_list]


def check_word(char_list,words,puzzle,chars):
    word = "".join(char_list)
    word_bank = [w.word for w in words]
    for w in words:
        if w.word == word or w.word == word[::-1]:
            w.word_checked = True
            w.save()
            w.chars.update(char_checked = True)
            break
        
            
def check_puzzle_copmleated(puzzle,words):
    for word in words:
        if not  word.word_checked:
            puzzle.grid_checked = False
            puzzle.save()
            return ""
    puzzle.grid_checked = True
    puzzle.save()
     
    
         
     


     
     
     
