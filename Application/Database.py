# This Python file uses the following encoding: utf-8

# NOTE: this is just a dump of all the SQLite database code that was removed from the main project, for reference...

import sqlite3
import os.path
from contextlib import closing

databaseFileName = './Camera.db'


def addImageToDatabase(fileName, timestamp):
    print("Add image to DB:", fileName, timestamp)

    with closing(sqlite3.connect(databaseFileName)) as connection:
        with closing(connection.cursor()) as cursor:
            sql = "INSERT INTO images(name,timestamp) VALUES(?,?)"
            cursor.execute(sql, (fileName, timestamp))

            connection.commit()


def imageInDatabase(fileName):
    with closing(sqlite3.connect(databaseFileName)) as connection:
        with closing(connection.cursor()) as cursor:
            sql = "SELECT * FROM images WHERE name = ?"
            cursor = connection.execute(sql, (fileName,))

            for row in cursor:
                # print(row)
                return True

    return False


self.initDatabase()

self.readFoldersFromDatabase()
self.readCamerasFromDatabase()

def initDatabase(self):
    if not os.path.exists(databaseFileName):
        print("Create database")

        with closing(sqlite3.connect(databaseFileName)) as connection:
            with closing(connection.cursor()) as cursor:
                sql = '''CREATE TABLE IF NOT EXISTS images (
                                                    name text NOT NULL PRIMARY KEY,
                                                    timestamp text
                                                    );'''
                cursor.execute(sql)

                sql = '''CREATE TABLE IF NOT EXISTS cameras (
                                                    url text NOT NULL PRIMARY KEY,
                                                    name text NOT NULL
                                                    );'''
                cursor.execute(sql)

                sql = '''CREATE TABLE IF NOT EXISTS folders (
                                                    url text NOT NULL PRIMARY KEY,
                                                    name text NOT NULL
                                                    );'''
                cursor.execute(sql)

                def addFolderToDatabase(self, url, name):
                    print("Add folder to DB:", url, name)

                    with closing(sqlite3.connect(databaseFileName)) as connection:
                        with closing(connection.cursor()) as cursor:
                            sql = "INSERT INTO folders(url,name) VALUES(?,?)"
                            cursor.execute(sql, (url, name))

                            connection.commit()


                def removeFolderFromDatabase(self, url):
                    print("Remove folder from DB:", url)

                    with closing(sqlite3.connect(databaseFileName)) as connection:
                        with closing(connection.cursor()) as cursor:
                            sql = "DELETE FROM folders WHERE url = ?"
                            cursor.execute(sql, (url,))

                            connection.commit()


                def addCameraToDatabase(self, url, name):
                    print("Add folder to DB:", url, name)

                    with closing(sqlite3.connect(databaseFileName)) as connection:
                        with closing(connection.cursor()) as cursor:
                            sql = "INSERT INTO cameras(url,name) VALUES(?,?)"
                            cursor.execute(sql, (url, name))

                            connection.commit()


                def removeCameraFromDatabase(self, url):
                    print("Remove camera from DB:", url)

                    with closing(sqlite3.connect(databaseFileName)) as connection:
                        with closing(connection.cursor()) as cursor:
                            sql = "DELETE FROM cameras WHERE url = ?"
                            cursor.execute(sql, (url,))

                            connection.commit()


                def readFoldersFromDatabase(self):
                    with closing(sqlite3.connect(databaseFileName)) as connection:
                        with closing(connection.cursor()) as cursor:
                            sql = "SELECT url FROM folders"
                            cursor = connection.execute(sql)

                            for row in cursor:
                                self.folderList.append(row[0])
                                # print(row)


                def readCamerasFromDatabase(self):
                    with closing(sqlite3.connect(databaseFileName)) as connection:
                        with closing(connection.cursor()) as cursor:
                            sql = "SELECT url FROM cameras"
                            cursor = connection.execute(sql)

                            for row in cursor:
                                self.cameraList.append(row[0])
                                # print(row[0])


