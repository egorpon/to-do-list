class ReadOnlySerializerMixin:
    def create(self, validated_data):
        raise NotImplementedError("This serializer is read-only")

    def update(self, instance, validated_data):
        raise NotImplementedError("This serializer is read-only")


class CreateOnlySerializerMixin:
    def create(self, validated_data):
        raise NotImplementedError("This serializer is create-only")


class UpdateOnlySerializerMixin:
    def update(self, instance, validated_data):
        raise NotImplementedError("This serializer is update-only")
