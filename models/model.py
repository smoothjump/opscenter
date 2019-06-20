#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from models.orm import Model, IntegerField, StringField


class Users(Model):
    id = IntegerField(primary_key=True)
    name = StringField()
    email = StringField()


class DInstances(Model):
    id = IntegerField(primary_key=True)
    name = StringField()
    ipAddr = StringField()
    db_type = StringField(default="MySQL")
    db_version = StringField(default="5.6")


