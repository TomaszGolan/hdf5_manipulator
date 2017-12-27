#!/usr/bin/env python
"""
"""
from six.moves import range

from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, Float
from sqlalchemy import UniqueConstraint
from sqlalchemy import MetaData
from sqlalchemy import select
from sqlalchemy import and_


class MnvCategoricalSQLiteReader:
    """
    record segments or planecodes in a sqlite db
    """
    def __init__(self, n_classes, db_base_name, db_prob_column_format='prob%03d'):
        self.n_classes = n_classes
        self.db_name = db_base_name + '.db'
        self._db_prob_columns_format = db_prob_column_format
        self._configure_db()

    def read_data(self, limit=1):
        """ test reader - careful calling this on anything but tiny dbs! """
        s = select([self.table])
        s = s.limit(limit)
        rp = self.connection.execute(s)
        results = rp.fetchall()
        return results

    def read_record(self, run, subrun, gate, evt):
        """
        result structure
        r[0][0] == id
        r[0][1:5] == (run, sub, gate, evt)
        r[0][5] == segment prediction
        r[0][6:] == individual segment probabilities
        """
        s = select([self.table]).where(
            and_(
                self.table.c.run == run,
                self.table.c.subrun == subrun,
                self.table.c.gate == gate,
                self.table.c.phys_evt == evt
            )
        )
        rp = self.connection.execute(s)
        results = rp.fetchall()
        return results

    def read_record_by_id(self, id):
        """ by id """
        s = select([self.table]).where(
            self.table.c.id == id
        )
        rp = self.connection.execute(s)
        results = rp.fetchall()
        return results

    def get_argmax_prediction(self, run, subrun, gate, evt):
        """ get the segment / planecode """
        s = select([self.table]).where(
            and_(
                self.table.c.run == run,
                self.table.c.subrun == subrun,
                self.table.c.gate == gate,
                self.table.c.phys_evt == evt
            )
        )
        rp = self.connection.execute(s)
        results = rp.fetchall()
        return results[0][5]

    def _setup_prediction_table(self):
        self.table = Table('zsegment_prediction', self.metadata,
                           Column('id', Integer(), primary_key=True),
                           Column('run', Integer()),
                           Column('subrun', Integer()),
                           Column('gate', Integer()),
                           Column('phys_evt', Integer()),
                           Column('segment', Integer()),
                           UniqueConstraint(
                               'run', 'subrun', 'gate', 'phys_evt'
                           ))
        for i in range(self.n_classes):
            name = self._db_prob_columns_format % i
            col = Column(name, Float())
            self.table.append_column(col)

    def _configure_db(self):
        db = 'sqlite:///' + self.db_name
        self.metadata = MetaData()
        self.engine = create_engine(db)
        self.connection = self.engine.connect()
        self._setup_prediction_table()
        self.metadata.create_all(self.engine)
