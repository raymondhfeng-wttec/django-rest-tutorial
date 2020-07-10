from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from snippets.models import Snippet
from snippets.serializers import SnippetSerializer

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from django.http import Http404
from rest_framework.views import APIView

from rest_framework import mixins
from rest_framework import generics

from django.contrib.auth.models import User
from snippets.serializers import UserSerializer

from rest_framework import permissions

from snippets.permissions import IsOwnerOrReadOnly
from snippets.models import Snippet

from rest_framework import renderers
from rest_framework import viewsets
from rest_framework.decorators import action

from rest_framework.reverse import reverse

from django_filters.rest_framework import DjangoFilterBackend

from snippets.filters import SnippetFilter

class SnippetViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.

    Additionally we also provide an extra `highlight` action.
    """
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_class = SnippetFilter

    @action(detail=True, renderer_classes=[renderers.StaticHTMLRenderer])
    def highlight(self, request, *args, **kwargs):
        snippet = self.get_object()
        return Response(snippet.highlighted)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        owner = self.request.query_params.get("owner", None)
        if owner is None:
            return super().get_queryset()
        else:
            return Snippet.objects.filter(owner__username=owner)

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This viewset automatically provides `list` and `detail` actions.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer