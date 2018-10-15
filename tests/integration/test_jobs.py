import time

from endpoints.jobs import JobEndpoints
from tests.integration.entity import EntityIntegrationTest


class JobEndpointsIntegrationTest(EntityIntegrationTest):
    """
    Job endpoints integration tests.
    """

    def __init__(self, *args, **kwargs):
        super(JobEndpointsIntegrationTest, self).__init__(*args, **kwargs)
        self.endpoints = JobEndpoints(**self.endpoint_kwargs)

    def get_default_config(self):
        """
        Returns the default entity config.
        Override upon inheritance.
        """
        return {"name": "TEST JOB"}

    def get_compute_params(self, nodes=1, notify='n', ppn=1, queue='D', time_limit='00:05:00'):
        return {
            "cluster": {"fqdn": "master-vagrant-cluster-001.exabyte.io"},
            "nodes": nodes,
            "notify": notify,
            "ppn": ppn,
            "queue": queue,
            "timeLimit": time_limit
        }

    def test_list_jobs(self):
        self.list_entities_test()

    def test_get_job_by_id(self):
        self.get_entity_by_id_test()

    def test_create_job(self):
        self.create_entity_test()

    def test_delete_job(self):
        self.delete_entity_test()

    def test_update_job(self):
        self.update_entity_test()

    def _wait_for_job_to_finish(self, id_, timeout=300):
        end = time.time() + timeout
        while time.time() < end:
            job = self.endpoints.get(id_)
            if job["status"] == "finished": return
            time.sleep(5)
        raise BaseException("job with ID {} did not finish within {} seconds".format(id_, timeout))

    def test_submit_job(self):
        job = self.create_entity()
        self.endpoints.submit(job['_id'])
        self.assertEqual('submitted', self.endpoints.get(job['_id'])['status'])
        self._wait_for_job_to_finish(job["_id"])

    def test_create_job_timeLimit(self):
        time_limit = "00:10:00"
        job = self.create_entity({"compute": self.get_compute_params(time_limit=time_limit)})
        self.assertEqual(self.endpoints.get(job['_id'])['_id'], job['_id'])
        self.assertEqual(self.endpoints.get(job['_id'])['compute']['timeLimit'], time_limit)

    def test_create_job_notify(self):
        job = self.create_entity({"compute": self.get_compute_params(notify='abe')})
        self.assertEqual(self.endpoints.get(job['_id'])['_id'], job['_id'])
        self.assertEqual(self.endpoints.get(job['_id'])['compute']['notify'], 'abe')
