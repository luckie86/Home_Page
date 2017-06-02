#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import jinja2
import webapp2

from google.appengine.api import mail
from models.emails import Email


template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), autoescape=False)


class BaseHandler(webapp2.RequestHandler):

    def write(self, *a, **kw):
        return self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        return self.write(self.render_str(template, **kw))

    def render_template(self, view_filename, params=None):
        if not params:
            params = {}
        template = jinja_env.get_template(view_filename)
        return self.response.out.write(template.render(params))


class MainHandler(BaseHandler):
    def get(self):
        return self.render_template("index.html")

    def post(self):
        name = self.request.get("name")
        email = self.request.get("email")
        phone_number = self.request.get("phone_number")
        message = self.request.get("message")

        save_email = Email(name=name, email=email, phone_number=phone_number, message=message)
        save_email.put()

        mail.send_mail(sender="luckie.luke@gmail.com",
                       to="luckie.luke@gmail.com",
                       subject="New web inquiry",
                       body=u"""
Your have new inquiry from {0} 
with email {1} 
phone number: {2} 
at: {3} 
with following message: 
{4}.""".format (name, email, phone_number, save_email.sent, message, ))

        return self.render_template("index.html")

app = webapp2.WSGIApplication([
    webapp2.Route('/', MainHandler),
], debug=True)
