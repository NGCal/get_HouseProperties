from rest_framework import serializers
from .models import Provider,Fields

class ProviderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Provider
        fields = "__all__"

class FieldsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fields
        fields = "__all__"

class ResponseFormatter():
    data = {
        "success":None,
        "message":None,
        "request":None,
        "response":None
    }

    def __init__(self,data):
        try:
            self.data["success"] = data["success"]
            self.data["message"] = data["message"]
            self.data["request"] = data["request"]

            if "response" in data:
                self.data["response"] = data["response"]
        except:
            pass
    def __dict__(self):
        return self.data