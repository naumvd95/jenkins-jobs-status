from unittest import TestCase
from unittest import skip
import jenkins

import report
import os

__author__ = 'rkhozinov'
__project__ = 'jenkins-python-parse-jobs'


class TestReporter(TestCase):
    def setUp(self):
        self.host = os.getenv('JENKINS_HOST')
        self.port = os.getenv('JENKINS_PORT', '8080')
        self.user = os.getenv('JENKINS_USER')
        self.password = os.getenv('JENKINS_PASSWORD')
        self.server = jenkins.Jenkins('http://{0}:{1}'.format(self.host, self.port),
                                      username=self.user, password=self.password)
        self.test_job_name = 'test_job'

    def test_connection_noauth(self):
        server = report.connect(self.host, self.port)
        self.assertIsInstance(server.get_version(), str)

    def test_connection_auth(self):
        server = report.connect(self.host, self.port, self.user, self.password)
        self.assertIsInstance(server.get_version(), str)

    def test_get_jobs(self):
        original_job_list = [job['name'] for job in self.server.get_jobs()]
        method_jobs_list = report.get_jobs(self.server)
        self.assertListEqual(original_job_list, method_jobs_list, method_jobs_list)

    def test_get_specific_jobs(self):
        original_jobs = [job['name'] for job in self.server.get_jobs()]
        name_filter = original_jobs[1]

        original_filtered_jobs = [name for name in original_jobs if name_filter in name]
        method_filtered_jobs = report.get_jobs(self.server, name_filter=name_filter)

        self.assertListEqual(original_filtered_jobs, method_filtered_jobs)

    def test_get_latest_result(self):
        jobs = self.server.get_jobs()
        job_name = jobs[69]['name']
        job_last_build_number = self.server.get_job_info(job_name)['lastCompletedBuild']['number']
        original_job_result = self.server.get_build_info(job_name, job_last_build_number)['result']
        method_job_result = report.get_latest_result(self.server, job_name)
        self.assertEqual(original_job_result, method_job_result)

    def test_get_latest_build_number_count(self):
        original_jobs = [job['name'] for job in self.server.get_jobs()]
        jobs_count = len(original_jobs)

        builds_numbers = []
        for job in original_jobs:
            print job
            builds_numbers.append(report.get_latest_build_number(self.server, job))

        self.assertListEqual(jobs_count, len(builds_numbers))

    def test_jobs_without_builds(self):
        original_jobs = [job['name'] for job in self.server.get_jobs()]
        jobs_without_builds = []
        build_numbers = []
        for job in original_jobs:
            if self.server.get_job_info(job)['lastCompletedBuild']:
                print job

        self.assertIn(0, jobs_without_builds)

    def test_null_jobs(self):
        jobs = [job['name'] for job in self.server.get_jobs()]
        jobs2 = [job['name'] for job in self.server.get_jobs() if job['name']]
        self.assertEqual(len(jobs), len(jobs2))

    def test_null_builds(self):
        jobs = [job['name'] for job in self.server.get_jobs()]
        for job in jobs:
            self.assertIsNotNone(self.server.get_job_info(job)['lastCompletedBuild'], job)

    def test_get_latest_build_number(self):
        jobs = [job['name'] for job in self.server.get_jobs()]
        for job_name in jobs:
            if job_name:
                origin_build_number = self.server.get_job_info(job_name)['lastCompletedBuild']['number']
                method_build_number = report.get_latest_build_number(self.server, job_name)
                self.assertEqual(origin_build_number, method_build_number)

    def test_get_failed_jobs(self):
        original_jobs = [job['name'] for job in self.server.get_jobs()]
        original_failed_jobs = []

        for job in original_jobs:
            job_last_build_number = self.server.get_job_info(job)['lastCompletedBuild']['number']
            if 'FAILED' in self.server.get_build_info(job, job_last_build_number)['result']:
                original_failed_jobs.append(job)

        method_failed_jobs = report.get_failed_jobs(self.server)
        self.assertListEqual(original_failed_jobs, method_failed_jobs)


def tearDown(self):
    try:
        self.server.delete_job(self.test_job_name)
    except:
        pass
