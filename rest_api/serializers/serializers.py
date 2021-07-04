from rest_framework import serializers
from comments.models import Comments
from django.utils import timezone
from doctorsUser.models import Reception, Reserve
from rest_framework import response, status

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comments
        fields = ('__all__')

class CommentsAddSerializers(serializers.ModelSerializer):
    class Meta:
        model = Comments
        fields = ("id", "doctor", "message")

    def create(self, validated_data):
        request = self.context.get("request")
        comment = Comments.objects.create(sent_at=timezone.now, author=request.user, **validated_data)
        return comment

class ReceptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reception
        fields = ("__all__")

class ReceptionAddSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reception
        fields = ('id', 'doctor', "date", 'time')

    def create(self, validated_data):
        reception = Reception.objects.create(**validated_data)
        return reception

class ReservedSerializers(serializers.ModelSerializer):
    class Meta:
        model = Reserve
        fields = ('id', 'who', 'doctor', "date", 'time')

class MakeReserverSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reserve
        fields = ('id', 'who', 'doctor', "date", 'time')

    def create(self, validated_data):
        request = self.context.get("request")
        date, time, doctor = validated_data['date'], validated_data['time'], validated_data['doctor']
        if Reception.objects.filter(doctor=doctor, date=date, time=time).exists():
            reserve = Reserve.objects.create(who=request.user, **validated_data)
            return reserve
        elif Reserve.objects.filter(doctor=doctor, date=date, time=time).exists():
            raise serializers.ValidationError("Время занято!")
        else:
            raise serializers.ValidationError("Указонного времени нет!")
            
