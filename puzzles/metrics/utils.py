from wordsearch.models import Puzzle as WordSearchPuzzle
from sudokuapp.models import Puzzle as SudokuPuzzle
from django.contrib.auth import get_user_model
from django.utils import timezone
import pandas as pd
User = get_user_model()

                
    

def user_metrics():
    puzzle_name,user_name,played_date,time_taken = [],[],[],[]
    wordsearch_puzzles =  WordSearchPuzzle.objects.all()
    sudoku_puzzle = SudokuPuzzle.objects.all()
    for game in [wordsearch_puzzles,sudoku_puzzle]:
        if game:
            for puzzle in game:
                if puzzle.initial_time and puzzle.finished_time:
                    i = timezone.make_aware(puzzle.initial_time) if timezone.is_naive(puzzle.initial_time) else puzzle.initial_time
                    f = timezone.make_aware(puzzle.finished_time) if timezone.is_naive(puzzle.finished_time) else puzzle.finished_time

    

                    user_name.append(puzzle.user.username)
                    played_date.append(puzzle.initial_time.strftime("%d/%b/%Y"))
                    time_taken.append(round((f - i).total_seconds() / 60, 2))
                    puzzle_name.append(puzzle.name)
                    raw_data = list(zip(puzzle_name,user_name,played_date,time_taken))
                    df = pd.DataFrame(raw_data,columns=["puzzle_name","user_name","played_date","time_taken"])
    return df



def calculations(df,user):
    # time taken average : sudoku
    user_df = df[df["user_name"] == user.username]
    time_av = user_df.groupby("puzzle_name")["time_taken"].mean().reset_index()
    time_av["time_taken"] = time_av["time_taken"].apply(lambda x: round(x,3))
    
    return time_av
     
     
     
    
    
     

    
    

 
     

  
             
         
            
     
    


                 

             
