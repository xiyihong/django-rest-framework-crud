from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from utils.viewsets import ModelViewSet
from rest_framework import status
from rest_framework.response import Response

from order.models import Order
from .serializers import OrderSerializer
from rest_framework.decorators import action


class OrderViewSet(ModelViewSet):
    serializer_class = OrderSerializer
    queryset = Order.objects.filter(valid=True)
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['key']
    search_fields = ['$key', '$buyer', '$receiver_addr', '$title', '$shop_name']
    ordering = ['key']

    @classmethod
    def get_by_id(cls, id):
        res = Order.objects.filter(id=id, valid=True)
        ser = OrderSerializer(res)
        return ser

    def get(self, request):
        res = Order.objects.filter(valid=True)
        ser = OrderSerializer(res)
        return ser

    # @action(['delete'], False, "delete")
    # def delete(self, request, *args, **kwargs):
    #     if not self.request.data:
    #         raise RuntimeError("删除参数为空")
    #     ids = request.data.get("ids", None)
    #     if ids and isinstance(ids, list):
    #         for id in ids:
    #             instances = Order.objects.filter(id = id)
    #             if not instances[0]:
    #                 continue
    #             instances[0].valid = 0
    #             instances[0].save
    #     return Response(
    #         data=[],
    #         code=200,
    #         msg="批量删除成功"
    #     )
    # @action(methods=['post'], detail=False, url_path="delete")
    # def delete(self, request):
    #     ids = request.data.get("ids", None)
    #     if ids and isinstance(ids, list):
    #         for id in ids:
    #             instances = Order.objects.filter(id = id)
    #             if not instances[0]:
    #                 continue
    #             instances[0].valid = 0
    #             instances[0].save
    #     return Response(status=status.HTTP_204_NO_CONTENT)
    #
    #
    #
    def destroy(self, request):
        import pdb
        pdb.set_trace()
        instance = self.get_object()
        instance.valid = False
        instance.save()
        return Response(
            data=[],
            code=204,
            msg="批量删除成功",
            status=status.HTTP_204_NO_CONTENT
        )