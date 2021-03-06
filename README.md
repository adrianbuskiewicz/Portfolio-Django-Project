# Portfolio

Portfolio is an web app alowing users to calculate Minimal Volatility Portfolio and Optimal Risky Portfolio with their own companies stocks, and monitor their prices after theoretical purchase.

## Technologies
* Python 3.x
* Django 3.2.7
* Bootstrap 5.0
* Pandas
* Numpy
* yfinance


## Installation

Clone the github repository to your directory.

```bash
git clone https://github.com/adrianbuskiewicz/Portfolio-Django-Project.git
```

Create and activate virtual environment.

```bash
py -m venv env
env\Scripts\activate
```

Install needed packages.

```bash
(env) cd your_project_directory_name
(env) pip install -r requirements.txt
```

Migrate models to the database.

```bash
(env) py manage.py makemigrations
(env) py manage.py migrate
```

Create admin (superuser).

```bash
(env) py manage.py createsuperuser
```

Run server.

```bash
(env) py manage.py runserver
```

## Usage

### Companies
User can add own companies and calculate for them rate of returns and volatility in given period of time (start date and end date). Also correlation matrix is presented which might be a good source of data for choosing companies needed in MVP and ORP.

### Portfolios
Based on companies stats calculated in companies view, app will calculate predicted MVP and ORP using simulation of 10 000 portfolios. User may then decide about investing in MVP or ORP with given amount of budget.

### Bought Portfolios
In this view are presented all portfolios user decided to use in investment. App shows plenty of statistics like owned capital based on actual price and difference between capital in purchase day and today (total return).

### Bought Portfolio Detail
Every bought portfolios has it's dedicated view, where are presented detailed statistics like actual prices of stocks and individual return on every stocks. 
