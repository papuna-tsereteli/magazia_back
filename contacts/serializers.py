from rest_framework import serializers
from .models import Submission

class SubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Submission
        fields = [
            'id',
            'name',
            'email',
            'phone',
            'message',
            'submission_type',
            'product'
        ]
