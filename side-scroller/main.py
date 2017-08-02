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
import imp
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
        proper_display = {
        "login": False
        }
        current_users = CurrentUser.query().order(-CurrentUser.accessed).fetch(limit = 1)
        for current_user in current_users:
            if current_user.current_username == "no one":
                proper_display["login"] = False
            else:
                proper_display["login"] = True
        template = jinja_environment.get_template('templates/homepage.html')
        self.response.out.write(template.render(proper_display))

class SignInHandler(webapp2.RequestHandler):
    def get(self):
        if CurrentUser.query().order(-CurrentUser.accessed).fetch(limit = 1) == "":
            people_here = CurrentUser.query().order(-CurrentUser.accessed).fetch(limit = 1)
            for person_here in people_here:
                if person_here.current_username == "no one" or person_here.current_username == "":
                    template = jinja_environment.get_template('templates/sign_in.html')
                    self.response.out.write(template.render())
                else:
                    template = jinja_environment.get_template('templates/homepage.html')
                    self.response.out.write(template.render())
                    self.response.out.write("<br> You're already logged in why don't you play the game?")
        else:
            template = jinja_environment.get_template('templates/sign_in.html')
            self.response.out.write(template.render())
    def post(self):
        user = self.request.get("user_id")
        passw = self.request.get("pass_value")
        results = User.query(User.username == user).fetch()
        one_true_password = ""
        yes = {
            "Correct": ""
        }
        for result in results:
            if result.password == passw:
                one_true_password = result.password
        if one_true_password == passw:
            new_session = CurrentUser(current_username = user, accessed = datetime.datetime.now())
            new_session.put()
            template = jinja_environment.get_template('Erkhes-Stuff/game.html')
            self.response.write(template.render())
        else:
            yes["Correct"]="That's wrong."
            self.response.write(template.render(yes))

class LogOutHandler(webapp2.RequestHandler):
    def get(self):
        current_users = CurrentUser.query().order(CurrentUser.accessed).fetch(limit = 1)
        for current_user in current_users:
            if current_user.current_username != "" and current_user.current_username != "no one":
                end_session = CurrentUser(current_username = "no one", accessed = datetime.datetime.now())
                end_session.put()
                sel.response.write("You've successfully logged out.")
            else:
                self.response.out.write("You might want to log in before logging out.")

class ScoreboardHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template('templates/scoreboard.html')
        self.response.out.write(template.render())
        leaders = []
        testers = User.query().order(-User.high_score).fetch(limit = 10)
        for tester in testers:
            if tester.high_score != 0:
                leaders.append(tester)
        for leader in leaders:
            self.response.out.write("%s scored a high score of %d <br>" % (leader.username, leader.high_score))
        length = len(leaders)
        if length < 10:
            leftovers = 10 - length
            while leftovers != 0:
                self.response.out.write("????? scored a high score of ????? <br>")
                leftovers -= 1
        users_own = CurrentUser.query().order(-CurrentUser.accessed).fetch(limit = 1)
        for user_own in users_own:
            users_high = User.query(User.username == user_own.current_username).fetch(limit = 1)
            for user_high in users_high:
                self.response.write("Personal High Score: %d" % user_high.high_score)

class PlayHandler(webapp2.RequestHandler):
    def get(self):
        this_username = CurrentUser.query().order(-CurrentUser.accessed).fetch(limit = 1)
        for current_man in this_username:
            if current_man.current_username != "no one" and current_man.current_username != "":
                self.response.write(current_man.current_username)
                user_scores = User.query(User.username == current_man.current_username).fetch()
                for user_score in user_scores:
                    user_score.scores.append(45)
                    user_score.high_score = 20
        # game.html = imp.load_source('game.html', '../Erkhes-Stuff/game.html')
        # print game.html.read()
        template = jinja_environment.get_template('Erkhes-Stuff/game.html')
        self.response.out.write(template.render())

class CreateUserHandler(webapp2.RequestHandler):
    def get(self):
        if CurrentUser.query().order(-CurrentUser.accessed).fetch(limit = 1) == "":
            people_here = CurrentUser.query().order(-CurrentUser.accessed).fetch(limit = 1)
            for person_here in people_here:
                if person_here.current_username == "no one" or person_here.current_username == "":
                    template = jinja_environment.get_template('templates/create_user.html')
                    self.response.write(template.render())
                else:
                    template = jinja_environment.get_template('templates/homepage.html')
                    self.response.out.write(template.render())
                    self.response.out.write("<br> You're already logged in why don't you play the game?")
        else:
            template = jinja_environment.get_template('templates/create_user.html')
            self.response.write(template.render())
    def post(self):
        request_user = self.request.get("new_user")
        request_password = self.request.get("password_c1")
        request_check = self.request.get("password_c2")
        request_character = self.request.get("character_type")
        if request_password == request_check:
            character_info = {
                "user1": request_user,
                "password1": request_password,
                "character1": request_character
            }
            new_guy = User(username = request_user, password = request_password, character = request_character, high_score = 0, scores = [])
            new_guy.put()
            first_session = CurrentUser(current_username = request_user, accessed = datetime.datetime.now())
            first_session.put()
            template = jinja_environment.get_template('templates/homepage.html')
            # template = jinja_environment.get_template('Erkhes-Stuff/game.html')
            self.response.write(template.render())
        else:
            template = jinja_environment.get_template('templates/create_user.html')
            self.response.out.write("Error: Confirm your password correctly.")
            self.response.out.write(template.render())

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/sign-in', SignInHandler),
    ('/play', PlayHandler),
    ('/create-user', CreateUserHandler),
    ('/leaderboard', ScoreboardHandler)
], debug=True)
