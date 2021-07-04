from rest_framework import serializers

from ratings.models import Rating

class RatingAddSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Rating
        fields = ("id", "rating", "doctor")

    def validate(self, attrs):
        request = self.context.get('request')
        if attrs['rating'] >= 6:
            raise serializers.ValidationError("Вы не можете ставить оценку выше 5")
        if Rating.objects.filter(
                author=request.user).exists():
            raise serializers.ValidationError("Вы не можете оценивать больше чем 1 один раз")
        return attrs
    
    def create(self, validated_data):
        request = self.context.get('request')
        rating = Rating.objects.create(author=request.user, **validated_data)
        return rating

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['rating'] = instance.rating
        return representation