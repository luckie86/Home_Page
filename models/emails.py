from google.appengine.ext import ndb


class Email(ndb.Model):
    name = ndb.StringProperty()
    email = ndb.StringProperty()
    phone_number = ndb.StringProperty()
    message = ndb.TextProperty()
    sent = ndb.DateTimeProperty(auto_now_add=True)
    deleted = ndb.BooleanProperty(default=False)
