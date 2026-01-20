from database.DB_connect import DBConnect
from model.artist import Artist

class DAO:


    @staticmethod
    def get_all_artists():

        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = """
                SELECT *
                FROM artist a
                """
        cursor.execute(query)
        for row in cursor:
            artist = Artist(id=row['id'], name=row['name'],n_albums=0)
            result.append(artist)
        cursor.close()
        conn.close()
        return result

    @staticmethod
    def get_all_min_artists(n_alb):

        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = """
                select ar.id, ar.name , COUNT(*) as n
                from album a , artist ar 
                where  a.artist_id = ar.id 
                group by ar.id
                having COUNT(*) >= %s
                """
        cursor.execute(query, (n_alb,))
        for row in cursor:
            artist = Artist(id=row['id'], name=row['name'], n_albums=row['n'])
            result.append(artist)
        cursor.close()
        conn.close()
        return result


    @staticmethod
    def get_connections(artist):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """ 
          select a1.artist_id as a1 , a2.artist_id as a2 
        from track t1, track t2, album a1, album a2
where t1.genre_id = t2.genre_id and a1.artist_id  > a2.artist_id 
and a1.id = t1.album_id and a2.id = t2.album_id 
group by a1.artist_id , a2.artist_id 
                 """

        cursor.execute(query)

        for row in cursor:
            if row['a1'] in artist and row['a2'] in artist:
                result.append((row['a1'], row['a2']))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def get_genere(artist_id):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """ 
  select t.genre_id as t
from album a , track t
where a.id = t.album_id and a.artist_id = %s
group by t.genre_id 


         """

        cursor.execute(query,(artist_id,))

        for row in cursor:
            result.append(row["t"])

        cursor.close()
        conn.close()
        return result

