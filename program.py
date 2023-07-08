
#importing the required libraries
import matplotlib.pyplot as plt
import mysql.connector as c
import numpy as np

#setting up the connection with mysql
con = c.connect(host = 'localhost',user = 'root', password = 'mysql#7',database = 'world')

#creating a cursor object
cur = con.cursor()

#using the database sports
cur.execute("use sports")

def function1():
    '''
    Function for choice 1: Bar Graph showing number of gold, silver, bronze and total medals won over years
    void, no return type function
    '''

    #executing command and fetching data
    cur.execute("select distinct year(date) from medals")
    year = cur.fetchall()

    # Creating values for x axis according to our required groups
    X_axis = np.arange(len(year))
    # print(X_axis)

    year_list = []

    # Creating List having years as string
    for x in year:
        year_list.append(str(x[0]))
    # print(year_list)

    gold,silver,bronze,totalMedals=[],[],[],[]
    num_years = len(year_list)

    #extracting and storing data for y axis for number of gold, silver, bronze, total medals in each year
    for i in range(num_years):
        cur.execute("select sum(gold_medals),sum(silver_medals), sum(bronze_medals), sum(total_medals) from medals where year(date) = " + str(year_list[i]) )
        y=cur.fetchall()
        for j in y:
            #print(j)
            #creating list to hold number of gold, silver, bronze, total medals in years
            gold.append(int(j[0]))
            silver.append(int(j[1]))
            bronze.append(int(j[2]))
            totalMedals.append(int(j[3]))

    #print(gold)
    #print(silver)
    #print(bronze)
    #print(totalMedals)

    width = 0.15  # Width of each bar
    # Creating bar graph for gold, silver, bronze and total medals with x axis having the years
    bar1 = plt.bar(X_axis, gold, width, color='y')
    bar2 = plt.bar(X_axis + width, silver, width, color='silver')
    bar3 = plt.bar(X_axis + width * 2, bronze, width, color='brown')
    bar4 = plt.bar(X_axis + width * 3, totalMedals, width, color='green')

    # Add counts above the bar graphs
    for rect in bar1 + bar2 + bar3 + bar4:
        height = rect.get_height()
        plt.text(rect.get_x() + rect.get_width() / 2.0, height, f'{height:.0f}', ha='center', va='bottom')

    # Adding labels, title, legend
    plt.xlabel("Years")
    plt.ylabel('number of medals')
    plt.title("Medals over years")
    plt.xticks(X_axis+width,year_list)
    plt.legend( (bar1, bar2, bar3, bar4), ('Gold', 'Silver', 'Bronze', 'Total Medals') )
    plt.show()

def function2():
    '''
    Function for choice 2: Bar Graph showing total number of medals won in each sport over years
    void, no return type function
    '''

    cur.execute("select distinct year(date) from medals")
    year = cur.fetchall()
    year_list = []

    # Creating List having years
    for x in range(len(year)):
        # print(year[x])
        year_list.append(year[x][0])

    distinct_sports = []

    # Creating list having all the sports
    cur.execute("select distinct sports from medals")
    fetch = cur.fetchall()
    for a in fetch:
        distinct_sports.append(str(a[0]))

    # Creating values for x axis according to our required groups
    x_axis = np.arange(len(distinct_sports))

    # Creating a 2D array for storing the data of number of total medals won
    rows = len(year_list)   # Row represent a year
    cols = len(distinct_sports) # Column represent a sport
    array_2d = [[0 for j in range(cols)] for i in range(rows)]  #initializing the 2D array with zeros

    # Inserting data into 2D array
    for p in range(len(year_list)):
        for q in range(len(distinct_sports)):
            cur.execute(
                "select total_medals from medals where sports = '" + distinct_sports[q] + "'" + " and year(date) = " + str(year_list[p]) )
            f = cur.fetchall()
            # print(f)
            array_2d[p][q] = f[0][0]
    # print(array_2d)

    width = 0.17    # Width of each bar
    # Creating bar graph of number of total medals won in a year with x axis as sport
    bar1 = plt.bar(x_axis, array_2d[0], width, color='y')
    bar2 = plt.bar(x_axis + width, array_2d[1], width, color='red')
    bar3 = plt.bar(x_axis + width * 2, array_2d[2], width, color='green')

    # Add counts above the two bar graphs
    for rect in bar1 + bar2 + bar3:
        height = rect.get_height()
        plt.text(rect.get_x() + rect.get_width() / 2.0, height, f'{height:.0f}', ha='center', va='bottom')

    # Adding labels, title, legend
    plt.xlabel("Sports")
    plt.ylabel('Number of Total Medals')
    plt.title("Medals of individual sports over years")
    plt.xticks(x_axis + width, distinct_sports)
    plt.legend((bar1, bar2, bar3), ('2017', '2018', '2019'))
    plt.show()


def function3():
    '''
    Function for choice 3: Pie Chart showing distribution of sports items ordered in a year
    void, no return type function
    '''

    cur.execute("select distinct year(date) from items_ordered")
    year = cur.fetchall()

    year_list = []

    # Creating List having years
    for x in range(len(year)):
        year_list.append(year[x][0])
    #print(year_list)

    for x in year_list:
        #print(x)
        quantity_list = []
        cur.execute("select quantity from items_ordered where year(date)=  " + str(x))
        quantity = cur.fetchall()

        # Creating list having the quantity of sports item ordered in a given year
        for i in quantity:
            quantity_list.append(i[0])
        #print(quantity_list)

        cur.execute("select item from items_ordered where year(date)= " + str(x))
        item = cur.fetchall()

        l = []
        # Creating list having the name of the sports item ordered
        for y in item:
            l.append(str(y[0]))
        # print(l)

        # Creating the pie chart
        plt.pie(quantity_list, labels=l, autopct="%1.2f%%")
        plt.title("items ordered in " + str(x))
        plt.axis = 'equal'
        plt.show()


def function4():
    '''
    Function for choice 4: Line Plot showing Total number of sports items ordered over years
    void, no return type function
    '''

    cur.execute("select year(date), sum(quantity) from items_ordered group by year(date)")
    result = cur.fetchall()

    y = []
    x = []

    # Creating data for x axis(years) and y axis(number of items ordered)
    for i in result:
        x.append(int(i[0]))
        y.append(i[1])

    # Plotting the line
    plt.plot(x, y)
    plt.title("Sports Items ordered over years ")
    plt.xlabel("Years")
    plt.ylabel("Total number of sports item ordered")
    plt.show()


print("WELCOME\n")

# Showing the choices user want to explore
while True:
    print("1. Bar Graph showing number of gold, silver, bronze and total medals won over years")
    print("2. Bar Graph showing total number of medals won in each sport over years")
    print("3. Pie Chart showing distribution of sports items ordered in a year ")
    print("4. Line Plot showing Total number of sports items ordered over years")
    print("5. Exit \n ")

    choice = input ("Enter your choice(from 1 - 5): ")

    # Checking if user input is a number, if yes converting it to integer data type
    if choice.isdigit():
        choice = int (choice)

    # Ensuring user input is in our range
    if choice not in [1,2,3,4,5]:
        print("INVALID CHOICE !\nTRY AGAIN\n")
        continue

    if choice == 5:
        print("THANK YOU")
        break

    if choice == 1:
        function1()

    if choice == 2:
        function2()

    if choice == 3:
        function3()

    if choice == 4:
        function4()
