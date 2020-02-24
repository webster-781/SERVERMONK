OUR HACKATHON PROJECT!
The required modules to be installed are in the requirements.txt
On a separate note, the following are the ones in the requirements.txt which you absolutely have to install:
1.Flask==0.12.2  (flask)
2.Flask-Bcrypt==0.7.1 (flask_bcrypt)
3.Flask-Login==0.5.0 (flask_login)
4.Flask-SQLAlchemy==2.4.1 (flask_sqlalchemy)
5.Flask-WTF==0.14.3 (flask_wtf)
You have to be in HACKATHON/hackathon directory and run Untitled with Flask as follows:
You then have to open your terminal and open "../HACKATHON/hackathon/" directory using cd command
1.Then you have to type the following command into the terminal window:
        export FLASK_APP=Untitled.py
That should run without any errors ideally
2.Then you have to type the following command into the terminal window:
        flask run
The should output some sqlalchemy code followed by a localhost link.Click on it.
That should open a browser window within five seconds.
The website would be up and running.
FEATURES OF THE WEBSITE:
1.)Firstly we have a Home Page. On the home page you can Register to our Web App, log in to your personalised dashboard, or contact us at facebook/instagram.
2.)On the register page, enter your email and password to become a registered user with us.
3.)You will be redirected to the homepage. Use your email and password to login. 
4.)This will open you dashboard where you can view the personalized track of your weekly and daily food and water input. Certain characterstics include a pie graph showing percentage of carbs, protiens and fats in your food. You can also track your calorie and water input. Also there will be a bar graph showing past 4 days nutrient inputs.
5.)You have to add the food you eat using the add food form. Please note that the units of food is generalized and is treated as 1 unit = 100gm. So please keep that in mind :) 
6.)You can also view all your entries by clicking on the ALL ENTRIES button on the nav-bar.
7.)Finally, you can log out and will be redirected to the home page.
