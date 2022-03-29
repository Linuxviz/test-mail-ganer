# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from django.template.loader import render_to_string


# Create your tests here.

class Test(TestCase):
    def test_a(self):
        html_content = render_to_string('email_example.html', {'content': 'contentgogo'})
        print(html_content)
