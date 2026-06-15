class ReadOnlySerializerMixin:
    def create(self, validated_data):
        raise NotImplementedError("This serializer is read-only")

    def patch(self, instance, validated_data):
        raise NotImplementedError("This serializer is read-only")
