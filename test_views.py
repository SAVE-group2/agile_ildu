"""Tests for Dataset view functions."""
from django.test import TestCase
from django.http import HttpRequest
from api.datasets.models import Dataset
from api.datasets.views import _dataset_list_get

NAME = 'name'
DESCRIPTION = 'description'
STATUS = 'status'
FILESIZE = 'filesize'
ROW_COUNT = 'row_count'
COL_COUNT = 'col_count'
CREATED_AT = 'created_at'
UPDATED_AT = 'updated_at'

DATASET_MAP = {
	NAME: 'test01',
	DESCRIPTION: 'this is a test',
	STATUS: 'complete',
	FILESIZE: '27334',
	ROW_COUNT: '3428347',
	COL_COUNT: '15',
	CREATED_AT: '20140514',
	UPDATED_AT: '20140608'
}

class DatasetUpdateViewTestCase(TestCase):
    """Tests for Dataset views."""

    def setUp(self):
        """
        Set up tests.

        self.dataset is a Dataset object. 
        """
        self.dataset = [Dataset.objects.create(
            'name': NAME,	
            'description': DESCRIPTION,	
            'status': COMPLETE,	
            'filesize': FILESIZE,	
            'row_count': ROW_COUNT,	
            'col_count': COL_COUNT,	
            'created_at': CREATED_AT,	
            'updated_at': UPDATED_AT
		)]

	def test_get_dataset_list(self):
		"""Test GET dataset list."""
		self.request = HttpRequest()	
		self.request.method = 'GET'
		response = views._dataset_list_get(self.request)
		self.assertJSONEqual(
			str(response.content, encoding='utf8'), 
			self.dataset
		)
