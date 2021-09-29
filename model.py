import datetime
from sqlalchemy import Table, Column, Integer, DateTime, Sequence, String, ForeignKey, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker, Session
from flask_login import UserMixin


engine = create_engine(
    'postgresql://oom_note:oom_note@localhost:5432/oom_note')
base = declarative_base()
Session = sessionmaker(bind=engine)
# s = Session()
# s.query(User).filter_by(username='ahunt').first()


class User(base):
    __tablename__ = 'users'
    id = Column(Integer, Sequence('users_id_seq'), primary_key=True)
    username = Column(String)
    password = Column(String)
    email = Column(String)
    first_name = Column(String)
    last_name = Column(String)
    last_login = Column(DateTime, default=datetime.datetime.utcnow)

    def __repr__(self):
        return "<User(id={}, username={})".format(self.id, self.username)

    @property
    def is_active(self):
        return True

    @property
    def is_authenticated(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return self.username


class Note(base):
    __tablename__ = 'notes'
    id = Column(Integer, Sequence('notes_id_seq'), primary_key=True)
    title = Column(String)
    content = Column(String)
    userid = Column(Integer, ForeignKey('users.id'))
    last_updated = Column(DateTime, default=datetime.datetime.utcnow)

    def __repr__(self):
        return "<Note(id={}, title={})".format(self.id, self.title)
