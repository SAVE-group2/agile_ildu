from django.http import JsonResponse	
from rest_framework.decorators import api_view	
from api.models.models import Model	
from .models import Dataset, DatasetTask	
	
	
@api_view(['GET', 'POST', 'DELETE'])	
def dataset_list(request):	
    	
	if request.method == 'GET':	
        return _dataset_list_get(request)	
	
def _dataset_list_get(request):	
	
    filter_dict = {'deleted': False}	
	
    if request.query_params.get('status'):	
        filter_dict['status'] = request.query_params.get('status')	
	
    if request.query_params.get('model_id'):	
        model_id = request.query_params.get('model_id')	
        model = Model.objects.get(id=model_id)	
        	
		filter_dict['schema__columns__contains'] = model.schema['columns']	
        filter_dict['status__in'] = [	
            Dataset.COMPLETE,	
            Dataset.UPLOADED,	
            Dataset.READY_TO_PROCESS	
        ]	
	
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
	
    return JsonResponse(datasets)
