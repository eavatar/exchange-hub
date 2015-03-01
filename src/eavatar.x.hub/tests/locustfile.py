# -*- coding: utf-8 -*-
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)


from locust import HttpLocust, TaskSet, task


class UserBehavior(TaskSet):
    @task(2)
    def index(self):
        self.client.get("/")

    @task(2)
    def status(self):
        self.client.get("/.status")


class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    min_wait=5000
    max_wait=9000