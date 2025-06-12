#create virtual environment
python3 -m venv p
source p/bin/activate

#install requirements

pip install --upgrade pip

pip install -r requirements.txt

 
#### navigaye  puzzles
cd puzzles/
# migrateions
python manage.py makemigrations
python manage.py migrate
# navigate to base directory
cd ..

# train word2vec model
./p/bin/python puzzles/wordsearch/model_training.py
#### navigaye  puzzles
cd puzzles/
# run server
python manage.py runserver
