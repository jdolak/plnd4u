#!/usr/bin/env python3

import unittest
import sys
import requests
from time import sleep

sys.path.append('./src')
from func_adv import *

class basic_func_tests(unittest.TestCase):
    def test_class_search(self):
        results = db_search_past_classes('Database Concepts',(1,1,1,1,1,1,1,1,1))

        self.assertEqual(len(results), 1, "Too many results")
        self.assertEqual(results, [('CSE 30246', 'Database Concepts')], "Results do not match")

    def test_create_user(self):
        self.assertEqual(db_register_student('test', 'test test', 'CSE', '2025'), 0, "User registration Failed")
        self.assertEqual(db_create_login('test','test'), 0, "User password creation failed")

    def test_web_requests(self):

        user = "test"
        password = "test"

        s = requests.Session() 

        url = "http://localhost/login"
        json={'netid':user ,'pw': password}
        self.assertEqual(str(s.post(url, json=json)), "<Response [200]>", "Failed login")

        url = "http://localhost/classes"
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

        url = "http://localhost/plan"
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