
from django.db.models import Max
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics, viewsets
from rest_framework.pagination import (LimitOffsetPagination,
                                       PageNumberPagination)
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from api.filter import InStockFilterBackend, OrderFilter, ProductFilter
from api.models import *
from api.serializers import (OrderSerializer, ProducInfoSerializer,UserSerializer,
                             ProductSerializer , OrderCreateSerializer)
from rest_framework.decorators import action

class ProductListCreateAPIView(generics.ListCreateAPIView):
  queryset = Product.objects.order_by('pk')
  serializer_class = ProductSerializer
  filterset_class = ProductFilter
  filter_backends = [
    DjangoFilterBackend,
    filters.SearchFilter,
    filters.OrderingFilter,
    InStockFilterBackend,
  ]
  search_fields = ['name' , 'description']
  ordering_fields = ['name' , 'price', 'stock']
  pagination_class = LimitOffsetPagination
  # pagination_class.page_size = 2
  # pagination_class.page_query_param = 'pagenum'
  # pagination_class.page_size_query_param = 'size'
  # max_page_size = 4

  def get_permissions(self):
    self.get_permissions_classes = [AllowAny]
    if self.request.method == 'POST':
      self.permission_classes = [IsAdminUser]
    return super().get_permissions()

# @api_view(['GET'])
# def product_list(request)s:
#   products = Product.objects.all()
#   serializer = ProductSerializer(products , many = True)
#   return Response(serializer.data)


class ProductDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
  queryset = Product.objects.filter(stock__gt=0)
  serializer_class = ProductSerializer
  lookup_url_kwarg = 'product_id'

  def get_permissions(self):
    self.get_permissions_classes = [AllowAny]
    if self.request.method == ['POST' , 'PUT' , 'PATCH', 'DELETE']:
      self.permission_classes = [IsAdminUser]
    return super().get_permissions()
  
# @api_view(['GET'])
# def product_detail(request , pk):
#   product = get_object_or_404(Product , pk = pk)
#   serializer = ProductSerializer(product)
#   return Response(serializer.data)

class OrderViewSet(viewsets.ModelViewSet):
  queryset = Order.objects.prefetch_related('items__product')
  serializer_class = OrderSerializer
  permission_classes = [IsAuthenticated]
  
  filter_backends = [DjangoFilterBackend] 
  filterset_class = OrderFilter

  def perform_create(self, serializer):
    serializer.save(self.request.user)

  def get_serializer(self):
    if self.action == 'create' or self.action == 'update':
      return OrderCreateSerializer
    return super().get_serializer()

  def get_queryset(self):
    qs = super().get_queryset()
    if not self.request.user.is_staff:
      qs = qs.filter(user = self.request.user)
    return qs
  

  
# class OrderListAPIView(generics.ListAPIView):
#   queryset = Order.objects.prefetch_related('items__product')
#   serializer_class = OrderSerializer


# class UserOrderListAPIView(generics.ListAPIView):
#   queryset = Order.objects.prefetch_related('items__product')
#   serializer_class = OrderSerializer
#   permission_classes = [IsAuthenticated]

#   def get_queryset(self):  
#     qs = super().get_queryset()
#     return qs.filter(user = self.request.user)

# @api_view(['GET'])
# def order_list(request):
#   orders = Order.objects.prefetch_related('items__product')
#   serializer = OrderSerializer(orders , many = True)
#   return Response(serializer.data)

# @api_view(["GET"])
# def product_info(request):
#   products = Product.objects.all()
#   serializer = ProducInfoSerializer({
#     'products': products,
#     'count': len(products),
#     'max_price': products.aggregate( max_price = Max('price'))['max_price']})
#   return Response(serializer.data)

class ProductInfoAPIView(APIView):
  def get(self , request):
    products = Product.objects.all()
    serializer = ProducInfoSerializer({
      'products': products,
      'count': len(products),
      'max_price': products.aggregate( max_price = Max('price'))['max_price']})
    return Response(serializer.data)
  
class UserListView(generics.ListAPIView):
  queryset = User.objects.all()
  serializer = UserSerializer
  pagination_class = None


  

