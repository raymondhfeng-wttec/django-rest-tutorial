from django_filters import rest_framework as filters
from snippets.models import Snippet 

class SnippetFilter(filters.FilterSet):
	min_id = filters.NumberFilter(field_name='id', lookup_expr='gte')
	max_id = filters.NumberFilter(field_name='id', lookup_expr='lte')
	min_date = filters.DateFilter(field_name='created', lookup_expr='gte')
	max_date = filters.DateFilter(field_name='created', lookup_expr='lte')

	class Meta:
		model = Snippet
		fields = ['created', 'id', 'title', 'code', 'linenos', 'language', 'style', 
		'owner', 'min_id', 'max_id', 'min_date', 'max_date']