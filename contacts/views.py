from rest_framework import generics
from .models import Submission
from .serializers import SubmissionSerializer

# This view is for creating new submissions only (POST requests)
class SubmissionCreateView(generics.CreateAPIView):
    queryset = Submission.objects.all()
    serializer_class = SubmissionSerializer