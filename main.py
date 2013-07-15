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
import webapp2
import os
import logging
from models import Customer, Order
from google.appengine.ext import db
from google.appengine.ext.webapp import template
from webapp2_extras import json

#os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
#from google.appengine.dist import use_library
#use_library('django', '1.2')


class MainHandler(webapp2.RequestHandler):
    def get_2(self):
        #self.response.write('Hello world!')
        filepath = os.path.dirname(__file__)
        template_path = os.path.join(filepath, "views/index.html")
        dic = {}
        html = template.render(template_path, dic)
        self.response.headers['Content-Type'] = 'text/html'
        self.response.out.write(html)

    def get(self):
        self.response.content_type = 'application/json'
        c = Customer.all().get()
        obj = {
            'name': "%s %s" % (c.first_name, c.last_name),
            'email': c.email,
            'orders': []
        }
        for o in c.orders:
            obj['orders'].append(o.record)
        self.response.write(json.encode(obj))


class OrderHandler(webapp2.RequestHandler):
    def post(self):
        email = self.get_string("email")
        c = Customer.all().filter("email =", email).get()
        if not c:
            logging.info("Create customer %s", email)
            c = Customer(first_name=self.get_string("firstname"),
                        last_name=self.get_string("lastname"),
                        email=db.Email(email))
            db.put(c)
        logging.info("Customer: %s is saved? %s, no of orders? %s", str(c), c.is_saved(), c.orders)


        o = Order(customer=c,
                record = self.get_string("musik"),
                address = self.get_string("adress"),
                postal_code = db.PostalAddress(self.request.get("postnummer")),
                city = self.get_string("ort"),
                phone = db.PhoneNumber(self.request.get("telefon")),
                message = db.Text(self.request.get("meddelande")))
        logging.info("Musik: %s", str(o))
        db.put(o)

        self.response.out.write("Det gick bra! %s, %s" % (str(c), str(o)))

    def get_string(self, parameter_name):
        value = unicode(self.request.get(parameter_name))
        if value:
            return value.strip()
        else:
            return value


app = webapp2.WSGIApplication([
    ('/api/order', OrderHandler),
    ('/', MainHandler)
], debug=True)
