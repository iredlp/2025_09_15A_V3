from database.DB_connect import DBConnect
from model.piloti import Piloti


class DAO():

    @staticmethod
    def getAllYears():
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = "SELECT distinct year FROM seasons s  ORDER BY year"

        cursor.execute(query)

        for row in cursor:
            results.append(row["year"])

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getAllNodes(anno1, anno2):
        conn = DBConnect.get_connection()
        results = []

        cursor = conn.cursor(dictionary=True)
        query = """ select distinct d.*
                from drivers d , results r , races ra 
                where d.driverId =r.driverId 
                and ra.raceId =r.raceId 
                and ra.`year` between %s and %s
                and r.`position` is not null ; """

        cursor.execute(query, (anno1, anno2))

        for row in cursor:
            results.append(Piloti(**row))

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getSquadrePerPilota(idPilota, anno1, anno2):
        conn = DBConnect.get_connection()
        results = []

        cursor = conn.cursor(dictionary=True)
        query = """ select  r.raceId as raceId, c.constructorId as constructorId
from constructors c , results r, races ra , drivers d 
where d.driverId =r.driverId  and d.driverId =%s
and ra.raceId =r.raceId    and r.constructorId =c.constructorId 
and ra.`year` between %s and %s
and r.`position` is not null 
                     """

        cursor.execute(query, (idPilota, anno1, anno2))

        for row in cursor:
            results.append((row["raceId"],row["constructorId"]))

        cursor.close()
        conn.close()
        return results

