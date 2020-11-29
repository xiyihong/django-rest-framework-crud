from order.models import Order
from rest_framework.serializers import ModelSerializer

class OrderSerializer(ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'

    def create(self, validated_data):
        # print()
        key = validated_data.get('key')
        existed = Order.objects.filter(key=key)
        if existed:
            print('existed!!!')
            pass
        else:
            print('created!!!')
            existed = Order.objects.create(**validated_data)
            existed.save()
        return existed