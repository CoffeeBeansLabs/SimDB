import sqlite3
from sqlite3 import Error

class ContentVectorsDB():

  def __init__(self,db_file):
    self.conn = self._create_connection(db_file)

  def initialize_db(self):
    self._define_schema()
    self._define_indexes()

  def _create_connection(self, db_file):
    """ create a database connection to the SQLite database
        specified by the db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
      conn = sqlite3.connect(db_file)
    except Error as e:
      print(e)

    return conn

  def _define_schema(self):
    ddl_string = """
    CREATE TABLE IF NOT EXISTS content_vector (
      content_id int primary key,
      index_id int,
      title text,
      content text,
      vector blob
    );
    """
    self._run_sql(ddl_string)

  def _define_indexes(self):
    ddl_string = """
    CREATE INDEX idx_index_id on content_vector (index_id);
    """
    title_idx = """
    CREATE INDEX idx_title on content_vector (title);
    """
    self._run_sql(ddl_string)
    self._run_sql(title_idx)

  def _run_sql(self,sql):
    cur = self.conn.cursor()
    cur.execute(sql)
    self.conn.commit()

  def add_content_vectors(self,content_vectors):
    insert_values = """
    insert into content_vectors values (?,?,?,?,?);
    """
    cur = self.conn.cursor()
    cur.executemany(insert_values,content_vectors)
    self.conn.commit()


