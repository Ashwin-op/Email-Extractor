import mysql.connector


# DON'T CHANGE THESE IF YOU DON'T KNOW WHAT YOU'RE DOING!
########################################################################################################################

def csv_to_mysql(load_sql, host, user, password):
    try:
        con = mysql.connector.connect(host=host,
                                      user=user,
                                      password=password,
                                      autocommit=True)
        print('Connected to DB: {}'.format(host))
        # Create cursor and execute Load SQL
        cursor = con.cursor()
        cursor.execute(load_sql)
        print('Successfully loaded the table from csv')
        con.close()

    except Exception as e:
        print('Error: {}'.format(str(e)))


########################################################################################################################

# FILL ALL THE INFORMATION HERE

# Fill the necessary details like "name of the file", "schema name (There should be three attributes/columns in it
# namely, 'Id', 'Email', 'Link')", "table name", "host IP", "username", "password"
load_sql = "LOAD DATA LOCAL INFILE 'college.csv' INTO TABLE test.emailId FIELDS TERMINATED BY ',';"
host = ''
user = ''
password = ''

########################################################################################################################


csv_to_mysql(load_sql, host, user, password)
