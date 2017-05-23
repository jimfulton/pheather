=====================================
Store Pandas data frame as ZODB blobs
=====================================

Currently experimental.

Usage, assuming you have a ZODB connection already::


  import pandas, pheather, transaction

  conn.root.iris = Pheather()
  transaction.commit()

  iris = pandas.read_csv('iris.csv')

  conn.root.iris.save(iris)

Then, later in a separate session::

  import pheather

  iris = conn.root.iris.read()

For folks who are new to ZODB, there's a helper function for
connecting to (and creating) a ZODB file-based or Postgres-based database::

  import pheather

  # Local files:
  conn = pheather.connection('data.fs')

  # Postgres database using URL-based connection strings:
  conn = pheather.connection('postgresql://localhost/mydb')
