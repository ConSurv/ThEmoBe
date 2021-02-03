from unittest import TestCase
import cv2
from unittest.mock import Mock
from flask import request, jsonify


class TestDemo(TestCase):

    def setUp(self):
        self.video = cv2.VideoCapture("file/demo.mp4")
        self.dummy_id = 123
        self.DEFAULT_EXPIRES_IN = 900  # In sec
        self.DEFAULT_POLLING_INTERVAL = 2
        self.persistent_status = True
        self.emo = True
        self.behav = True
        self.threat = True
        self.form = {"emo":self.emo, "behav":self.behav, "threat":self.threat, "persistent_status":self.persistent_status,
                     "expires_in":self.DEFAULT_POLLING_INTERVAL}
        self.files = {"video":self.video, "filename":"demo.mp4"}
        self.request = Mock()
        self.request.form = self.form
        self.request.files = self.files

    # 1
    def test_annotate_errorFile(self):
        from Demo import annotate
        self.files = {"video":self.video, "filename":"demo.avi"}
        self.request.files = self.files
        response = {"error_id": "Bad Request", "error_message": "video file missing"}
        out = annotate(self.request)
        self.assertEqual(out, response)

    # 2
    def test_annotate_errorEmo(self):
        from Demo import annotate
        self.form = {"behav":self.behav, "threat":self.threat}
        self.request.form = self.form
        response = {"error_id": "Bad Request", "error_message": "parameters missing : 'emo' "}
        out = annotate(self.request)
        self.assertEqual(out, response)

    # 3
    def test_annotate_errorBehav(self):
        from Demo import annotate
        self.form = {"emo":self.emo, "threat":self.threat}
        self.request.form = self.form
        response = {"error_id": "Bad Request", "error_message": "parameters missing : 'behav' "}
        out = annotate(self.request)
        self.assertEqual(out, response)

    # 4
    def test_annotate_errorThreat(self):
        from Demo import annotate
        self.form = {"behav":self.behav, "emo":self.emo}
        self.request.form = self.form
        response = {"error_id": "Bad Request", "error_message": "parameters missing : 'threat' "}
        out = annotate(self.request)
        self.assertEqual(out, response)

    # 5
    def test_Annotate_error_Persist_Expires(self):
        from Demo import annotate
        self.form = {"behav": self.behav, "emo": self.emo, "threat":self.threat}
        self.request.form = self.form
        response = {"themobe_id": 123, "video": "demo.mp4", "video_status": "processing", "expires_in": self.DEFAULT_EXPIRES_IN,
                    "interval": self.DEFAULT_POLLING_INTERVAL}
        out = annotate(self.request)
        self.assertEqual(out, response)

    # 6
    def test_Annotate_error_Expires(self):
        from Demo import annotate
        self.form = {"behav": self.behav, "emo": self.emo, "threat":self.threat, "persistent_status":self.persistent_status}
        self.request.form = self.form
        response = {"themobe_id": 123, "video": "demo.mp4", "video_status": "processing", "expires_in": self.DEFAULT_EXPIRES_IN,
                    "interval": self.DEFAULT_POLLING_INTERVAL}
        out = annotate(self.request)
        self.assertEqual(out, response)

    # 7
    def test_Annotate_error_Expires_100(self):
        from Demo import annotate
        self.form['expires_in'] = 100
        self.request.form = self.form
        response = {"themobe_id": 123, "video": "demo.mp4", "video_status": "processing", "expires_in": 100,
                    "interval": self.DEFAULT_POLLING_INTERVAL}
        out = annotate(self.request)
        self.assertEqual(out, response)

    # 8
    def test_Annotate_error_Expires_1000(self):
        from Demo import annotate
        self.form['expires_in'] = 1000
        self.request.form = self.form
        response = {"themobe_id": 123, "video": "demo.mp4", "video_status": "processing", "expires_in": self.DEFAULT_EXPIRES_IN,
                    "interval": self.DEFAULT_POLLING_INTERVAL}
        out = annotate(self.request)
        self.assertEqual(out, response)

    # 9
    def test_Annotate_errorPersist_Expires_100(self):
        from Demo import annotate
        self.form = {"behav": self.behav, "emo": self.emo, "threat": self.threat, "expires_in":100}
        self.request.form = self.form
        response = {"themobe_id": 123, "video": "demo.mp4", "video_status": "processing", "expires_in": 100,
                    "interval": self.DEFAULT_POLLING_INTERVAL}
        out = annotate(self.request)
        self.assertEqual(out, response)

    # 10
    def test_Annotate_error_Expires_1000(self):
        from Demo import annotate
        self.form = {"behav": self.behav, "emo": self.emo, "threat": self.threat, "expires_in":1000}
        self.request.form = self.form
        response = {"themobe_id": 123, "video": "demo.mp4", "video_status": "processing", "expires_in": self.DEFAULT_EXPIRES_IN,
                    "interval": self.DEFAULT_POLLING_INTERVAL}
        out = annotate(self.request)
        self.assertEqual(out, response)
