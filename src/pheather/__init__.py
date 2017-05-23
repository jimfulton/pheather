from __future__ import print_function

import feather
import os
import persistent
import tempfile
import time
import ZODB.blob

def connection(dsn, blob_dir=None, **kw):
    td = None
    if blob_dir is None:
        if dsn.startswith('postgresql://'):
            td = tempfile.TemporaryDirectory('blobs')
            blob_dir = td.name
        else:
            blob_dir = dsn + '.blobs'

    if dsn.startswith('postgresql://'):
        import newt.db
        conn = newt.db.connection(
            dsn, blob_dir=blob_dir, shared_blob_dir=False, keep_history=True,
            **kw)
    else:
        import ZODB
        conn = ZODB.connection(dsn, blob_dir=blob_dir)

    conn._td = td # hold on till garbage
    return conn

class Pheather(persistent.Persistent):

    def __init__(self, **attrs):
        self.__dict__.update(attrs)
        self.__data = ZODB.blob.Blob()

    def write(self, df):
        fd, path = tempfile.mkstemp(
            dir=self._p_jar.db().storage.fshelper.temp_dir)
        os.close(fd)
        feather.write_dataframe(df, path)
        self.__data.consumeFile(path)

    def save(self, df=None, note=None):
        if note:
            self._p_jar.transaction_manager.get().note(note)

        if df is not None:
            self.write(df)

        self._p_jar.transaction_manager.commit()

    def read(self):
        self.__data.open().close()
        return feather.read_dataframe(self.__data.committed())

    def history(self, size=9):
        for h in self._p_jar.db().history(self.__data._p_oid, size):
            yield h

    def log(self, size=9):
        for h in self.history(size):
            print(time.ctime(h['time']), h['description'])

