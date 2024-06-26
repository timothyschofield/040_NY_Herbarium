"""
    Creates a local database for testing the sql


"""

from mysql.connector import connect, Error

try:

    # you could also pass in database="online_movie_rating" here
    with connect(host="localhost", user="root", password="password") as connection:
        print(connection)
        create_db_query = "CREATE DATABASE IF NOT EXISTS ny_herbarium"
        with connection.cursor() as cursor:
            cursor.execute(create_db_query)


        show_db_query = "SHOW DATABASES"
        with connection.cursor() as cursor:
            cursor.execute(show_db_query)
            for db in cursor:
                print(db)

        use_db_query = "USE ny_herbarium"
        with connection.cursor() as cursor:
            cursor.execute(use_db_query)  


        specimenCards = """
                                    CREATE TABLE IF NOT EXISTS specimenCards(
                                    id INT AUTO_INCREMENT PRIMARY KEY,
                                    darCatalogNumber INTEGER(10),
                                    darCollector VARCHAR(255),
                                    AI_darCollector VARCHAR(255),
                                    collectionTeam LONGTEXT,
                                    AI_collectionTeam LONGTEXT,
                                    collectionNumberPreffix VARCHAR(255),
                                    AI_collectionNumberPrefix VARCHAR(255),
                                    collectionNumber INTEGER(10),
                                    AI_collectionNumber INTEGER(10),
                                    collectionNumberSuffix VARCHAR(255),
                                    AI_collectionNumberSuffix VARCHAR(255),
                                    collectionNumberText VARCHAR(255),
                                    AI_collectionNumberText VARCHAR(255)
                                    )
                                    """

        with connection.cursor() as cursor:
            cursor.execute(specimenCards)
            connection.commit()











except Error as e:
    print(f"TIM ERROR: {e}")
    exit()



