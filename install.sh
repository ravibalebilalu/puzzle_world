#create virtual environment
python3 -m venv p
source p/bin/activate

#install requirements

pip install --upgrade pip

pip install -r requieremets.txt

# train word2vec model
./p/bin/python puzzles/wordsearch/model_training.py
cd puzzles

# run server
python manage.py runserver

