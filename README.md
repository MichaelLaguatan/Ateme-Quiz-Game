# Ateme-Quiz-Game

Here is the Ateme Quiz Game to be used at the NAB trade show

## Start Up

1. Open a powershell terminal and navigate to the 'Ateme-Quiz-Game' folder
2. To activate the Python virtual environment, enter the following command:

    `.\.venv\Scripts\Activate.ps1`

3. Once inside the virtual environment, you can start the flask application (the host parameter is necessary for the application to be reachable by other devices):

    `flask run --host 0.0.0.0`

4. Any changes should cause the application to restart automatically, but you can restart it by pressing `Ctrl + C` and then re-entering the command to start the flask application    


## Editing The Questions

Questions are imported into the database based on which of the `questions_*.csv` files they are in. Questions in `questions_1.csv` are put into the pool of questions for `OTT`, `questions_2.csv` is for `DAI`, and `questions_3.csv` is for `Encoding`. Inside the questions files, each row is a question and is formatted as:

`question,option1,option2,option3,option4,correct_answer`

Once the files are updated with the questions, go to this route while the application is running: 

`localhost:5000/read_csv`

Which should read the questions from each file and place them into the database. This also deletes any of the questions that are already in the database so any questions you want to use should be in one of three questions files.

To edit the amount of questions used for each quiz, there is the variable `QUESTION_AMOUNT` on line 11 of `app\routes.py` that tells the application how many questions to choose for each quiz.

## Clearing the Database

The route `localhost:5000/clear_db` clears the entirety of the database (users and questions) which effectively resets the application. This route is only usuable through `POST` requests which can be sent through Postman. For the app to work properly, the questions will have to be read from the csv and imported into the database again.

## Contacts Route

The route `localhost:5000/contacts` returns all the users stored in the database in a JSON format. It's first sorted by the quiz type/category, then by day taken in descending order, then by score in descending order, and lastly the time they took to take the quiz in ascending order.