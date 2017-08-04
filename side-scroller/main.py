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
# import imp
from google.appengine.ext import ndb
from google.appengine.api import app_identity
from google.appengine.api import mail
# import smtplib
# import socket
import sys
# import getpass
# from email.mime.text import MIMEText
# from email.mime.multipart import MIMEMultipart

jinja_environment = jinja2.Environment(loader=
    jinja2.FileSystemLoader(os.path.dirname(__file__)))

class CurrentUser(ndb.Model):
    current_username = ndb.StringProperty()
    accessed = ndb.DateTimeProperty()

class User(ndb.Model):
    username = ndb.StringProperty()
    password = ndb.StringProperty()
    e_mail = ndb.StringProperty()
    deaths = ndb.IntegerProperty()
    wins = ndb.IntegerProperty()
    # scores = ndb.IntegerProperty()
    #(repeated=True)
    high_score = ndb.IntegerProperty()
    # character = ndb.StringProperty()

class MainHandler(webapp2.RequestHandler):
    def get(self):
        proper_display = {
        "login": False
        }
        current_users = CurrentUser.query().order(-CurrentUser.accessed).fetch(limit = 1)
        for current_user in current_users:
            if current_user.current_username == "guest":
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
                if person_here.current_username == "guest" or person_here.current_username == "":
                    template = jinja_environment.get_template('templates/sign_in.html')
                    self.response.out.write(template.render())
                else:
                    template = jinja_environment.get_template('templates/error.html')
                    self.response.out.write(template.render())
        else:
            template = jinja_environment.get_template('templates/sign_in.html')
            self.response.out.write(template.render())
    def post(self):
        user = self.request.get("user_id")
        passw = self.request.get("pass_value")
        results = User.query(User.username == user).fetch()
        one_true_password = ""
        yes = {
            "Correct": True
        }
        for result in results:
            if result.password == passw:
                one_true_password = result.password
        if one_true_password == passw:
            new_session = CurrentUser(current_username = user, accessed = datetime.datetime.now())
            new_session.put()
            # template = jinja_environment.get_template('templates/stats.html')
            # self.response.write(template.render())
            self.redirect("/stats")
        else:
            template = jinja_environment.get_template('templates/sign_in.html')
            yes["Correct"]=False
            self.response.write(template.render(yes))

class ForgotPasswordHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template('templates/forgot_password.html')
        self.response.out.write(template.render())
        mail.send_mail(sender="noreply@side-scroller.appspot.com",
                   to="Albert Johnson <dmwe1fs.tv2@gmail.com>",
                   subject="Your account has been approved",
                   body="""Dear Albert:

                   Your example.com account has been approved.  You can now visit
                   http://www.example.com/ and sign in using your Google Account to
                   access new features.

                   Please let us know if you have any questions.

                   The example.com Team
                   """)

        # server = smtplib.SMTP_SSL('smtp.googlemail.com', 587)
        # server.ehlo()
        # server.starttls()
        # server.ehlo()
        # username = 'dmwe1fs.tv2@gmail.com'
        # password = ''
        # server.login(username, password)
        # msg = "Please work right."
        # server.sendmail(username, username, msg)
        # # fromaddr = 'dmwe1fs.tv2@gmail.com'
        # # toaddrs = 'dmwe1fs.tv2@gmail.com'
        # # msg = MIMEMultipart('alternative')
        # # msg['Subject'] = "Trial"
        # # msg['From'] = "good morning" #like name
        # # msg['To'] = "GGGGGG"
        # # body = MIMEText("example email body")
        # # msg.attach(body)
        # # username = 'dmwe1fs.tv2@gmail.com'
        # # password = ''
        # # server = smtplib.SMTP_SSL('smtp.googlemail.com', 465)
        # # server.login(username, password)
        # # server.quit()


class LogOutHandler(webapp2.RequestHandler):
    def get(self):
        current_users = CurrentUser.query().order(-CurrentUser.accessed).fetch(limit = 1)
        for current_user in current_users:
            if current_user.current_username != "" and current_user.current_username != "guest":
                end_session = CurrentUser(current_username = "guest", accessed = datetime.datetime.now())
                end_session.put()
                self.response.write("You've successfully logged out.")
            else:
                template = jinja_environment.get_template('templates/error.html')
                self.response.out.write(template.render())

class StatsHandler(webapp2.RequestHandler):
    def get(self):
        current_users = CurrentUser.query().order(-CurrentUser.accessed).fetch(limit = 1)
        for current_user in current_users:
            if current_user.current_username != "" and current_user.current_username != "guest":
                persons = User.query(User.username == current_user.current_username).fetch(limit = 1)
                for person in persons:
                    template = jinja_environment.get_template('templates/stats.html')
                    user_stats = {
                        "user" : person.username,
                        "user_high_score" : person.high_score,
                        "user_wins" : person.wins,
                        "user_deaths" : person.deaths
                        }
                self.response.out.write(template.render(user_stats))
            else:
                template = jinja_environment.get_template('templates/error.html')
                self.response.out.write(template.render())

class InstructionsHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template('templates/instructions.html')
        self.response.out.write(template.render())

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
        # if CurrentUser.query().order(-CurrentUser.accessed).fetch(limit = 1) != "":
        #     this_username = CurrentUser.query().order(-CurrentUser.accessed).fetch(limit = 1)
        #     for current_man in this_username:
        #         if current_man.current_username != "guest" and current_man.current_username != "":
        #             template = jinja_environment.get_template('templates/stats.html')
        #         # user_stats = {
        #         #     "user" : person.username,
        #         #     "user_high_score" : person.high_score,
        #         #     "user_wins" : person.wins,
        #         #     "user_deaths" : person.deaths
        #         #     }
        #             self.response.out.write(template.render())
        #             user_scores = User.query(User.username == current_man.current_username).fetch()
        #             for user_score in user_scores:
        #                 if user_score.scores > user_score.high_score:
        #                     user_score.high_score = user_score.scores
        #                     user_score.put()
        # # game.html = imp.load_source('game.html', '../Erkhes-Stuff/game.html')
        # # print game.html.read()
        #         else:
        #             template = jinja_environment.get_template('Erkhes-Stuff/game.html')
        #             self.response.out.write(template.render())
        # else:
        #     template = jinja_environment.get_template('Erkhes-Stuff/game.html')
        #     self.response.out.write(template.render())
    # def post(self):
        template = jinja_environment.get_template('Erkhes-Stuff/game.html')
        self.response.out.write(template.render())

class CreateUserHandler(webapp2.RequestHandler):
    def get(self):
        if CurrentUser.query().order(-CurrentUser.accessed).fetch(limit = 1) == "":
            people_here = CurrentUser.query().order(-CurrentUser.accessed).fetch(limit = 1)
            for person_here in people_here:
                if person_here.current_username == "guest" or person_here.current_username == "":
                    template = jinja_environment.get_template('templates/create_user.html')
                    self.response.out.write(template.render())
                else:
                    template = jinja_environment.get_template('templates/error.html')
                    self.response.out.write(template.render())
        else:
            template = jinja_environment.get_template('templates/create_user.html')
            self.response.out.write(template.render())
    def post(self):
        request_user = self.request.get("new_user")
        request_password = self.request.get("password_c1")
        request_check = self.request.get("password_c2")
        request_e_mail = self.request.get("e_mail")
        copy_users = User.query().fetch()
        # taken = {
        #     "yes": ""
        # }
        # help_me = {
        #     "person" : False
        #     }
        for copy_user in copy_users:
            if request_user == copy_user.username or request_user == "" or len(request_user) < 4 or request_user == "guest":
                # taken["yes"] = "It is"
                template = jinja_environment.get_template('templates/create_user.html')
                self.response.out.write(template.render())
                # self.response.write(template.render(taken))
                return
        if request_password == request_check and len(request_password) > 3:
            character_info = {
                "user1": request_user,
                "password1": request_password,
                "e_mail1": request_e_mail
            }
            new_guy = User(username = request_user, password = request_password, e_mail = request_e_mail, deaths = 0, wins = 0, high_score = 0)
            new_guy.put()
            first_session = CurrentUser(current_username = request_user, accessed = datetime.datetime.now())
            first_session.put()
            # help_me["person"] = True
            template = jinja_environment.get_template('templates/create_user.html')
            # self.response.write(template.render(help_me))
            # template = jinja_environment.get_template('templates/stats.html')
            self.response.write(template.render())
        else:
            # taken["yes"] = "It is"
            template = jinja_environment.get_template('templates/create_user.html')
            # self.response.write(template.render(taken))
            self.response.out.write(template.render())


app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/sign-in', SignInHandler),
    ('/play', PlayHandler),
    ('/create-user', CreateUserHandler),
    ('/leaderboard', ScoreboardHandler),
    ('/instructions', InstructionsHandler),
    ('/log-out', LogOutHandler),
    ('/forgot-password', ForgotPasswordHandler),
    ('/stats', StatsHandler)
], debug=True)
