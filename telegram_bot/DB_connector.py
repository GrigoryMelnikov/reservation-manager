import pandas as pd
import psycopg2
from pandas import DataFrame

from config import postgres_db_params


def connect_postgres():
    try:
        conn = psycopg2.connect(**postgres_db_params)
        return conn
    except psycopg2.Error as e:
        print(f"Error connecting to the database: {e}")
        return None


def postgres_exe(query, DML=False) -> DataFrame | bool:
    conn = connect_postgres()
    if conn is not None:
        try:
            with conn.cursor() as cur:
                cur.execute(query)
                if not DML:
                    columns_names = [desc[0] for desc in cur.description]
                    df = pd.DataFrame(cur.fetchall(), columns=columns_names)
                    response = df
                else:
                    conn.commit()
                    response = True
        except (Exception, psycopg2.DatabaseError) as e:
            print('Ran this query {}\nGot this Error:{}'.format(query, e))
            response = False
        finally:
            conn.close()
            return response
