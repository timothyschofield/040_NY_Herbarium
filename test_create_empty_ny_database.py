"""
    Creates a local database for testing the sql
"""

from mysql.connector import connect, Error

from test_ny_cols import ny_db_cols

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

        specimenCards = f"CREATE TABLE IF NOT EXISTS specimenCards(id INT AUTO_INCREMENT PRIMARY KEY,\n"

        for col_name, col_type in ny_db_cols:
            specimenCards = f"{specimenCards}{col_name} {col_type},\n"

        specimenCards = f"{specimenCards[:-2]})" # get rid of final comma and add closing bracket
        print(specimenCards)




        """
        specimenCards =             
                                    CREATE TABLE IF NOT EXISTS specimenCards(
                                    id INT AUTO_INCREMENT PRIMARY KEY,
                                    
                                    irn INTEGER(10),
                                    darGlobalUniqueIdentifier VARCHAR(100),
                                    darInstitutionCode VARCHAR(50),
                                    darCatalogNumber INTEGER(10),
                                    darRelatedInformation VARCHAR(200),
                                    darImageURL VARCHAR(200),
                                    darImageURL_a VARCHAR(200),
                                    darImageURL_b VARCHAR(200),
                                    darKingdom VARCHAR(100),
                                    darPhylum VARCHAR(100),
                                    darFamily VARCHAR(100),
                                    darScientificName VARCHAR(100),
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
                                    AI_collectionNumberText VARCHAR(2),
                                    collectionDD VARCHAR(2),
                                    collectionMM VARCHAR(2),
                                    collectionYYYY VARCHAR(4),
                                    AI_collectionDD VARCHAR(2),
                                    AI_collectionMM VARCHAR(2),
                                    AI_collectionYYYY VARCHAR(4),    
                                    collectionDD2 VARCHAR(2),
                                    collectionMM2 VARCHAR(2),
                                    collectionYYYY2 VARCHAR(4),
                                    AI_collectionDD2 VARCHAR(2),
                                    AI_collectionMM2 VARCHAR(2),
                                    AI_collectionYYYY2 VARCHAR(4),                                  
                                    colVerbatimDate VARCHAR(255),
                                    AI_colVerbatimDate VARCHAR(255),
                                    darCollectionNotes LONGTEXT,
                                    AI_darCollectionNotes LONGTEXT,
                                    darContinent VARCHAR(255),
                                    AI_darContinent VARCHAR(255),
                                    darCountry VARCHAR(255),
                                    AI_darCountry VARCHAR(255), 
                                    darStateProvince VARCHAR(255),
                                    AI_darStateProvince VARCHAR(255), 
                                    darCounty VARCHAR(255),
                                    AI_darCounty VARCHAR(255), 
                                    darCountyId INTEGER(10),
                                    AI_darCountyId INTEGER(10),
                                    darLocality LONGTEXT,
                                    AI_darLocality LONGTEXT, 
                                    township_tab VARCHAR(255),
                                    AI_township_tab VARCHAR(255), 
                                    range_tab VARCHAR(255),
                                    AI_range_tab VARCHAR(255), 
                                    section_tab VARCHAR(255),
                                    AI_section_tab VARCHAR(255), 
                                    darMinimumElevationMeters FLOAT(10),
                                    AI_darMinimumElevationMeters FLOAT(10), 
                                    darMaximumElevationMeters FLOAT(10),
                                    AI_darMaximumElevationMeters FLOAT(10),  
                                    darMinimumElevationFeet FLOAT(10),
                                    AI_darMinimumElevationFeet FLOAT(10),  
                                    darMaximumElevationFeet FLOAT(10),
                                    AI_darMaximumElevationFeet FLOAT(10),  
                                    darLatitudeDecimal FLOAT(10),
                                    AI_darLatitudeDecimal FLOAT(10),  
                                    darLongitudeDecimal FLOAT(10),
                                    AI_darLongitudeDecimal FLOAT(10),  
                                    latitudeDMS VARCHAR(255),
                                    AI_latitudeDMS VARCHAR(255),  
                                    longitudeDMS VARCHAR(255),
                                    AI_longitudeDMS VARCHAR(255),  
                                    darGeodeticDatum VARCHAR(255),
                                    AI_darGeodeticDatum VARCHAR(255), 
                                    darGeorefMethod VARCHAR(255),
                                    AI_darGeorefMethod VARCHAR(255),  
                                    darCoordinateUncertaintyInMeter FLOAT(10),
                                    AI_darCoordinateUncertaintyInMeter FLOAT(10), 
                                    colLocationNotes LONGTEXT,
                                    AI_colLocationNotes LONGTEXT, 
                                    feaCultivated LONGTEXT,
                                    AI_feaCultivated LONGTEXT, 
                                    feaPlantFungDescription LONGTEXT,
                                    AI_feaPlantFungDescription LONGTEXT, 
                                    feaFrequency LONGTEXT,
                                    AI_feaFrequency LONGTEXT,
                                    habHabitat LONGTEXT,
                                    AI_habHabitat LONGTEXT, 
                                    habVegetation LONGTEXT,
                                    AI_habVegetation LONGTEXT,
                                    habSubstrate LONGTEXT,
                                    AI_habSubstrate LONGTEXT, 
                                    speOtherSpecimenNumbers_tab LONGTEXT, 
                                    AI_speOtherSpecimenNumbers_tab LONGTEXT,
                                    ocrText LONGTEXT,
                                    AI_ocrText LONGTEXT)
                                    
        """
        
        
        with connection.cursor() as cursor:
            cursor.execute(specimenCards)
            connection.commit()

except Error as e:
    print(f"TIM ERROR: {e}")
    exit()



