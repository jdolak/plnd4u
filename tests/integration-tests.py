#!/usr/bin/env python3

import unittest
import sys
import requests
import os
from time import sleep

sys.path.append('./src')
from func_adv import *

USER = "test"
PASS = "test"

HOST_PORT = os.getenv('HOST_PORT')

class basic_func_tests(unittest.TestCase):

    def test_create_user(self):
        self.assertEqual(db_register_student(USER, 'test test', 'cse', '2025'), 0, "User registration Failed")
        self.assertEqual(db_create_login(USER,PASS), 0, "User password creation failed")

    def test_class_search(self):
        results = db_search_past_classes(USER, 'Database Concepts',(1,1,1,1,1,1,0,0,0))

        self.assertEqual(len(results), 1, "Too many results")
        self.assertEqual(results, [('CSE 30246', 'Database Concepts')], "Results do not match")

    def test_web_requests(self):

        user = USER
        password = PASS

        s = requests.Session() 

        url = f"http://localhost:{HOST_PORT}/login"
        json={'netid':user ,'pw': password}
        self.assertEqual(str(s.post(url, json=json)), "<Response [200]>", "Failed login")

        url = f"http://localhost:{HOST_PORT}/classes"
        json = {'action': 'add_to_plan', 'year': 'Freshman', 'semester': 'Fall', 'course': 'CSE 20311', 'class_name': 'Fundamentals of Computing', 'global_netid': ''}
        self.assertEqual(str(s.post(url, json=json)), "<Response [200]>", "Failed adding course to Freshman Year")

        json = {'action': 'add', 'course_name': 'test', 'course_code': 'test', 'global_netid': ''}
        self.assertEqual(str(s.post(url, json=json)), "<Response [200]>", "Failed adding unlisted course")

        fr_classes = db_show_student_enrollments(user,'FRFA')
        un_classes = db_show_student_enrollments(user,'UNLT')

        self.assertEqual(len(fr_classes), 1, "Number of classes for freshman year not 1")
        self.assertEqual(len(un_classes), 1, "Number of classes for unlisted courses not 1")

        self.assertEqual(fr_classes[0][1], "CSE 20311", "Class enrolled not CSE 20311")
        self.assertEqual(un_classes[0][3], "test", "Unlisted test class not enrolled")

        url = f"http://localhost:{HOST_PORT}/plan"
        json={'global_netid': '', 'course_code': 'CSE 20311', 'semester': 'FRFA', 'course_name': 'Fundamentals of C...'}
        self.assertEqual(str(s.post(url, json=json)), "<Response [200]>", "Error removing freshman year class")
        json={'global_netid': '', 'course_code': 'test', 'semester': 'UNLT', 'course_name': 'test'}
        self.assertEqual(str(s.post(url, json=json)), "<Response [200]>", "Error removing unlisted class")


        #fr_classes = db_show_student_enrollments(user,'FRFA')
        #un_classes = db_show_student_enrollments(user,'UNLT')

        #self.assertEqual(len(fr_classes), 0, "Still classes remaining")
        #self.assertEqual(len(un_classes), 0, "Still classes remaining") 

if __name__ == '__main__':
    unittest.main()