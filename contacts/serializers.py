from rest_framework import serializers
from .models import Submission


class SubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Submission
        fields = ['name', 'phone', 'address', 'quantity', 'comment', 'submission_type', 'product']

    def validate(self, data):
        # Ensure required fields are present for product submissions
        if data.get('submission_type') == 'PRODUCT':
            required_fields = ['name', 'phone', 'address', 'quantity']
            for field in required_fields:
                if not data.get(field):
                    raise serializers.ValidationError(f'{field} is required for product submissions.')

        # Validate quantity is positive
        if data.get('quantity') and data.get('quantity') <= 0:
            raise serializers.ValidationError('Quantity must be greater than 0.')

        return data