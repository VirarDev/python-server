import psycopg2

try:
    # Connect to your PostgreSQL database by providing the necessary connection details
    connection = psycopg2.connect(
        user="jay",
        password="1234",
        host="ec2-43-204-101-69.ap-south-1.compute.amazonaws.com",
        port="5432",  # default PostgreSQL port is 5432
        database="talentov"
    )

    # Create a cursor object using the cursor() method
    cursor = connection.cursor()

    # Execute a SQL query
    cursor.execute("SELECT version();")

    # Fetch the result
    record = cursor.fetchone()
    print("You are connected to - ", record, "\n")

except (Exception, psycopg2.Error) as error:
    print("Error while connecting to PostgreSQL", error)

finally:
    # Close the database connection
    if connection:
        cursor.close()
        connection.close()
        print("PostgreSQL connection is closed")
