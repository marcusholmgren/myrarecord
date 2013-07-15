#!/usr/bin/env python
__author__ = 'Marcus Holmgren'

from google.appengine.ext import db


class Customer(db.Model):
    first_name = db.StringProperty(required=True)
    last_name = db.StringProperty(required=True)
    email = db.EmailProperty(required=True)
    created_date = db.DateTimeProperty(auto_now_add=True)
    last_modified = db.DateTimeProperty(auto_now=True)

    def __str__(self):
        return "%s %s (%s)" % (self.first_name, self.last_name, self.email)

    def __unicode__(self):
        return unicode("%s %s (%s)" % (self.first_name, self.last_name, self.email))


class Order(db.Model):
    record = db.StringProperty(required=True, choices=["CD2008-02", "CD2004-05", "BothCD"])
    customer = db.ReferenceProperty(reference_class=Customer, collection_name="orders")
    address = db.StringProperty(required=True)
    postal_code = db.PostalAddressProperty(required=True)
    city = db.StringProperty(required=True)
    phone = db.PhoneNumberProperty(required=True)
    message = db.StringProperty(required=False)
    created_date = db.DateTimeProperty(auto_now_add=True)
    last_modified = db.DateTimeProperty(auto_now=True)

    def __str__(self):
        return "%s to %s %s" % (self.record, self.postal_code, self.city)

    def __unicode__(self):
        return unicode("%s to %s %s" % (self.record, self.postal_code, self.city))


#musik:CD2008-02
#firstname:
#lastname:
#adress:
#postnummer:
#ort:
#email:
#email_validate:
#Telefon:
#meddelande:
