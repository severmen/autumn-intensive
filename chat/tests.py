from django.test import TestCase
from project.settings import mongoDB_services
import redis
class SystemTest(TestCase):
    def test_mongoDB_emptiness(self):
        self.assertEqual(mongoDB_services.count_documents({}), 0)
    def test_mongoDB_add_and_delete(self):
        mongoDB_services.insert_one({"test_key": "test"})
        self.assertEqual(mongoDB_services.count_documents({"test_key": "test"}), 1)
        mongoDB_services.delete_one({"test_key": "test"})
        self.assertEqual(mongoDB_services.count_documents({}), 0)
    def test_redis_coonnect(self):
        r = redis.StrictRedis(host='host.docker.internal', port=6379, db=1)
        r.set('test', "test_text")
        self.assertEqual(r.get('test').decode("utf-8") , "test_text")


