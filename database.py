import mysql.connector
from mysql.connector import Error

# Connect to MySQL server first (without specifying the database)
mydb = mysql.connector.connect(
    host="localhost",
    port=3306,
    user="root",
    password="Raj@9104"
)


def connect():
    try:
        # Create a cursor object to interact with the MySQL database
        mycursor = mydb.cursor()

        # Create the database if it doesn't exist
        mycursor.execute("CREATE DATABASE IF NOT EXISTS voting_system")

        # Switch to the 'voting_system' database
        mydb.database = "voting_system"

        # Create the tables if they don't exist
        mycursor.execute("""
            CREATE TABLE IF NOT EXISTS admin (
                id INT AUTO_INCREMENT PRIMARY KEY,
                registration_id VARCHAR(20) NOT NULL UNIQUE,
                name VARCHAR(50) NOT NULL,
                aadhar VARCHAR(12) NOT NULL UNIQUE,
                phone VARCHAR(10) NOT NULL UNIQUE,
                gender VARCHAR(7) NOT NULL
            )
        """)

        mycursor.execute("""
            CREATE TABLE IF NOT EXISTS vote (
                id INT AUTO_INCREMENT PRIMARY KEY,
                voter_id VARCHAR(20) NOT NULL UNIQUE,
                poll VARCHAR(50) NOT NULL,
                district VARCHAR(50) NOT NULL
            )
        """)

        mycursor.execute("""
            CREATE TABLE IF NOT EXISTS voters (
                id INT AUTO_INCREMENT PRIMARY KEY,
                voter_id VARCHAR(20) NOT NULL UNIQUE,
                name VARCHAR(50) NOT NULL,
                aadhar VARCHAR(12) NOT NULL UNIQUE,
                phone VARCHAR(10) NOT NULL UNIQUE,
                gender VARCHAR(7) NOT NULL
            )
        """)

        print("[DONE]   DATABASE & TABLES CREATED SUCCESSFULLY!!")
        print("--------------------------------------------------")

    except Error as e:
        print(f"[ERROR]   Error during database/table creation: {e}")

    finally:
        # Close the cursor
        mycursor.close()


# Call the connect function to create the database and tables
connect()


# Function Definitions

def findByAadhar(aadhar):
    try:
        mycursor = mydb.cursor()
        sql = "SELECT * FROM voters WHERE aadhar = %s"
        mycursor.execute(sql, (aadhar,))
        result = mycursor.fetchone()
        return result
    except Error as e:
        print(f"[WARN]   Failed to find user by aadhar: {e}")
    finally:
        mycursor.close()


def findByVoterId(voterId):
    try:
        mycursor = mydb.cursor()
        sql = "SELECT * FROM voters WHERE voter_id = %s"
        mycursor.execute(sql, (voterId,))
        result = mycursor.fetchone()
        return result
    except Error as e:
        print(f"[WARN]   Failed to find user by Voter ID: {e}")
    finally:
        mycursor.close()


def addVoter(voterId, name, aadhar, phone, gender):
    try:
        mycursor = mydb.cursor()
        sql = """INSERT INTO voters (voter_id, name, aadhar, phone, gender) 
                 VALUES (%s, %s, %s, %s, %s)"""
        mycursor.execute(sql, (voterId, name, aadhar, phone, gender))
        mydb.commit()
        return True
    except Error as e:
        print(f"[WARN]   User Record failed to register: {e}")
        return False
    finally:
        mycursor.close()


def submitVote(voterId, poll, district):
    try:
        mycursor = mydb.cursor()
        sql = """INSERT INTO vote (voter_id, poll, district) 
                 VALUES (%s, %s, %s)"""
        mycursor.execute(sql, (voterId, poll, district))
        mydb.commit()
        return True
    except Error as e:
        print(f"[WARN]   Unable to submit Vote: {e}")
        return False
    finally:
        mycursor.close()


def findByVoterIdinVote(voterId):
    try:
        mycursor = mydb.cursor()
        sql = "SELECT * FROM vote WHERE voter_id = %s"
        mycursor.execute(sql, (voterId,))
        result = mycursor.fetchone()
        return result
    except Error as e:
        print(f"[WARN]   Error during finding voter from vote entity: {e}")
    finally:
        mycursor.close()


def findByRegId(regId):
    try:
        mycursor = mydb.cursor()
        sql = "SELECT * FROM admin WHERE registration_id = %s"
        mycursor.execute(sql, (regId,))
        result = mycursor.fetchone()
        return result
    except Error as e:
        print(f"[WARN]   Failed to find admin using Registered ID: {e}")
    finally:
        mycursor.close()


def findByAadharinAdmin(aadhar):
    try:
        mycursor = mydb.cursor()
        sql = "SELECT * FROM admin WHERE aadhar = %s"
        mycursor.execute(sql, (aadhar,))
        result = mycursor.fetchone()
        return result
    except Error as e:
        print(f"[WARN]   Failed to find admin using Aadhar No.: {e}")
    finally:
        mycursor.close()


def addAdmin(regId, name, aadhar, phone, gender):
    try:
        mycursor = mydb.cursor()
        sql = """INSERT INTO admin (registration_id, name, aadhar, phone, gender) 
                 VALUES (%s, %s, %s, %s, %s)"""
        mycursor.execute(sql, (regId, name, aadhar, phone, gender))
        mydb.commit()
        return True
    except Error as e:
        print(f"[WARN]   Unable to register admin: {e}")
        return False
    finally:
        mycursor.close()


def getTotalCount():
    try:
        mycursor = mydb.cursor()
        sql = "SELECT COUNT(*) FROM vote"
        mycursor.execute(sql)
        result = mycursor.fetchone()
        return result[0]
    except Error as e:
        print(f"[WARN]   Error while fetching total vote count: {e}")
    finally:
        mycursor.close()


def getTotalUserCount():
    try:
        mycursor = mydb.cursor()
        sql = "SELECT COUNT(*) FROM voters"
        mycursor.execute(sql)
        result = mycursor.fetchone()
        return result[0]
    except Error as e:
        print(f"[WARN]   Error while fetching total user count: {e}")
    finally:
        mycursor.close()


def getPartyCount(party):
    try:
        mycursor = mydb.cursor()
        sql = "SELECT COUNT(*) FROM vote WHERE poll LIKE %s"
        mycursor.execute(sql, ('%' + party + '%',))
        result = mycursor.fetchone()
        return result[0]
    except Error as e:
        print(f"[WARN]   Error while fetching party count: {e}")
    finally:
        mycursor.close()


def getallVoters():
    try:
        mycursor = mydb.cursor()
        sql = """SELECT voters.name, voters.phone, voters.gender, vote.district
                 FROM voters
                 LEFT JOIN vote ON voters.voter_id = vote.voter_id"""
        mycursor.execute(sql)
        result = mycursor.fetchall()
        return result
    except Error as e:
        print(f"[WARN]   Failed to fetch all Voters record: {e}")
    finally:
        mycursor.close()


def getUserByAadhar(aadhar):
    try:
        mycursor = mydb.cursor()
        sql = """SELECT voters.name, voters.phone, voters.gender, vote.district
                 FROM voters
                 LEFT JOIN vote ON voters.voter_id = vote.voter_id
                 WHERE aadhar = %s"""
        mycursor.execute(sql, (aadhar,))
        result = mycursor.fetchone()
        return result
    except Error as e:
        print(f"[WARN]   Failed to fetch user by aadhar: {e}")
    finally:
        mycursor.close()


def updateUserByAadhar(name, phone, gender, aadhar):
    try:
        mycursor = mydb.cursor()
        sql = """UPDATE voters SET name = %s, phone = %s, gender = %s 
                 WHERE aadhar = %s"""
        mycursor.execute(sql, (name, phone, gender, aadhar))
        mydb.commit()
        return True
    except Error as e:
        print(f"[WARN]   Failed to update user record: {e}")
        return False
    finally:
        mycursor.close()


def deleteUserByAadhar(aadhar):
    try:
        mycursor = mydb.cursor()
        sql = """DELETE FROM voters WHERE aadhar = %s"""
        mycursor.execute(sql, (aadhar,))
        mydb.commit()
        return True
    except Error as e:
        print(f"[WARN]   Failed to delete user: {e}")
        return False
    finally:
        mycursor.close()
