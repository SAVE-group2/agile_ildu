from django.http import JsonResponse	
from rest_framework.decorators import api_view	
from api.models.models import Model	
from .models import Dataset, DatasetTask
import unittest
	
STATUS_KEY = 'status'
MODEL_ID_KEY = 'model_id'

# designate API method	
@api_view(['GET', 'POST', 'DELETE'])	
def dataset_list(request):	
    """
    Handle operations on a collection of datasets.

    Invokes a function appropriate for the HTTP method.
    Accepts GET, POST, and DELETE requests.

    """	
	if request.method == 'GET':	
        return _dataset_list_get(request)	
	
def _dataset_list_get(request):	

    filter_dict = {'deleted': False}	
	
    # it is requested when browsing datasets in a model.
    if request.query_params.get(STATUS_KEY):	
        filter_dict['status'] = request.query_params.get(STATUS_KEY)	

    try:	
        # it is requested when browsing datasets in a prediction.
        if request.query_params.get(MODEL_ID_KEY):	
            model_id = request.query_params.get(MODEL_ID_KEY)	
            model = Model.objects.get(id=model_id)		
            """
            Filter only datasets that
               1. contain the columns of the model schema.
               2. are inspected or preprocessed.
            """
            filter_dict['schema__columns__contains'] = model.schema['columns']	
            filter_dict['status__in'] = [	
                Dataset.COMPLETE,	
                Dataset.UPLOADED,	
                Dataset.READY_TO_PROCESS	
            ]
    except TypeError:
        return JsonResponse({'error':'model_id must be integer'})
	
    # make a json to return
    datasets = {	
        'datasets': [{	
            'id': dataset.id,	
            'name': dataset.name,	
            'description': dataset.description,	
            'status': dataset.status,	
            'filesize': dataset.filesize,	
            'row_count': dataset.shape_count('rows'),	
            'col_count': dataset.shape_count('cols'),	
            'created_at': str(dataset.created_at),	
            'updated_at': str(dataset.updated_at)	
        } for dataset in Dataset.objects.filter(**filter_dict)]	
    }	
	
    # return the json
    return JsonResponse(datasets)
