#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import jinja2
import datetime
import os
import webapp2
import logging
from google.appengine.ext import ndb

jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))

class CurrentUser(ndb.Model):
    current_username = ndb.StringProperty()
    accessed = ndb.DateTimeProperty()

class User(ndb.Model):
    username = ndb.StringProperty()
    password = ndb.StringProperty()
    e_mail = ndb.StringProperty()
    scores = ndb.IntegerProperty(repeated=True)
    high_score = ndb.IntegerProperty()
    character = ndb.StringProperty()

class MainHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template('templates/homepage.html')
        self.response.out.write(template.render())

class SignInHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template('templates/sign_in.html')
        self.response.out.write(template.render())

class PlayHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template('templates/game.html')
        self.response.out.write(template.render())

class CreateUserHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template('templates/create_user.html')
        self.response.out.write(template.render())

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/sign-in', SignInHandler),
    ('/play', PlayHandler),
    ('/create-user', CreateUserHandler)
], debug=True)
