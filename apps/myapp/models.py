from __future__ import unicode_literals
from datetime import date
from django.db import models

import re
import bcrypt

NAME_REGEX = re.compile(r'^[A-Za-z]\w+$')
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')
PASSWORD_REGEX = re.compile(r'^[0-9a-zA-Z!@#$%]{8,40}$')

class UserManager(models.Manager):
    def validate_reg(self, postData):
        errors = []

        if len(postData['name']) < 2:
            errors.append("Name fields must be at least 3 characters")
        if len(postData['alias']) < 2:
            errors.append("Alias name must be at least 3 characters")
        if not re.match(NAME_REGEX, postData['alias']):
            errors.append("Alias name must be letters only")
        if not re.match(EMAIL_REGEX, postData['email']):
            errors.append("Invalid Email")
        if not re.match(PASSWORD_REGEX, postData['password']):
            errors.append("Password needs 8 or more (letters and numbers, and or symbol)")
        if postData["password"] != postData["confirm"]:
            errors.append("Password Confirmation doesn't match")

        if not errors:
            hashed = bcrypt.hashpw((postData['password'].encode()), bcrypt.gensalt(14))
            new_user = self.create(
                
                name = postData['name'],
                alias = postData['alias'],
                email = postData['email'],
                birth_date = postData['birth_date'],
                password = hashed
            )
            return new_user
                    
        return errors
            


    def login_val(self, postData):
        errors = []
        
        if len(self.filter(email=postData['email'])) > 0:
            user = self.filter(email=postData['email'])[0]
            if not bcrypt.checkpw(postData['password'].encode(), user.password.encode()):
                errors.append('email/password incorrect')
        else:
            errors.append('email/password incorrect')

        if errors:
            return errors
        return user



class User(models.Model):
    
    name = models.CharField(max_length=100)
    alias = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    birth_date = models.DateField(max_length=8)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()
    
    def __str__(self):
         return "<User object: {}>".format(self.name)



class Friendship(models.Model):
    from_friend = models.ForeignKey(
    User, related_name='friend_set')
    to_friend = models.ForeignKey(
    User, related_name='to_friend_set'
    )
    def __unicode__(self):
        return u'%s, %s' % (
            self.from_friend.username,
            self.to_friend.username
            )
    class Meta:
        unique_together = (('to_friend', 'from_friend'), )
