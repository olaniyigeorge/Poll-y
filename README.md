# Poll-y
On my journey of learning Django web framework, I'm building the Poll app described in the Django documentation and adding some little functionalities to it.

This is...
> # A poll app with some of the functionalities of a social media app built with the Django web framework.

My goal is to build a poll app that allows users to create and participate in polls on a variety of topics. The app would also include some social media features, such as the ability to follow other users, like and comment on polls, and receive notifications about new polls or activity from followed users.

## Features:

- ***User authentication***: Users should be able to create an account and login to the app.
- ***Poll creation***: Users should be able to create a new poll by entering a question and multiple answer choices. Users can also set the duration of the poll, and choose to make it public or private.
- ***Poll participation***: Users should be able to browse and participate in polls created by other users. They can vote for their preferred answer and see the results of the poll in real-time.
- ***Social media features***: Users should be able to follow other users to see their polls and activity on a feed. Users should also be able to like and comment on polls, and receive notifications about new polls or activity from followed users.
- ***Analytics and insights***: Users should be able to view detailed analytics and insights about their own polls, including the number of votes, demographics of voters, and other engagement metrics.


-- Interested individuals are welcome to contribute to this project
## How to run locally/contribute

1. Clone the repo using `git clone https://github.com/olaniyigeorge/Poll-y.git`
2. Create a virtual environment in the cloned repo directory with `python -m venv env`
3. Activate the virtual environment `env\Scripts\activate`
4. Install the dependencies `pip install -r requirements.txt`
5. Run `python manage.py migrate` to setup the database
6. Run the server from the command line(in the project directory) with `python manage.py runserver`
7. Lastly, navigate to `http://127.0.0.1:8000/` in your web browser 



### Some Intented UIs
![Poll-y  auth page](https://github.com/olaniyigeorge/Poll-y/assets/27226623/261e0cb5-2b16-4110-be67-b943fbf1348d)
![Poll-y auth'd feed](https://github.com/olaniyigeorge/Poll-y/assets/27226623/2e264b49-af6d-4e45-bcd1-46027489979a)
![Poll-y poll page](https://github.com/olaniyigeorge/Poll-y/assets/27226623/5b570256-4e6a-4922-ab15-c8d10c36782e)
