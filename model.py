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
    # def __init__(self):
    #     self.__is_authenticated = False
    #     self.__is_active = False
    #     self.__is_anonymous = False
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

    # # flask-login
    # __is_authenticated = True
    # __is_active = True
    # __is_anonymous = False
    #
    # def get_is_authenticated(self):
    #     return self.__is_authenticated
    # def set_is_authenticated(self, is_authenticated):
    #     self.__is_authenticated = is_authenticated
    # is_authenticated = property(get_is_authenticated, set_is_authenticated)
    #
    # def get_is_active(self):
    #      return self.__is_active
    # def set_is_active(self, is_active):
    #     self.__is_active = is_active
    # is_active = property(get_is_active, set_is_active)
    #
    # def get_is_anonymous(self):
    #     return self.__is_anonymous
    # def set_is_anonymous(self, is_anonymous):
    #     self.__is_anonymous = is_anonymous
    # is_anonymous = property(get_is_anonymous, set_is_anonymous)
    #
    # def get_id(self):
    #     return self.username

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
