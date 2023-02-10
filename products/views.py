from django.shortcuts import render
from rest_framework import generics, mixins, permissions
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404
from .models import Product
from .serializers import ProductSerializers
# Create your views here.
# CreateAPIView >> make views in data 
class ProductListCreateAPIView(generics.ListCreateAPIView):
   queryset = Product.objects.all()
   serializer_class = ProductSerializers
   #permission_classes = [permissions.IsAuthenticated]
   #IsAuthenticatedOrReadOnly

   def perform_create(self, serializer):
      #print(serializer.validated_data)
      title = serializer.validated_data.get('title')
      content = serializer.validated_data.get('content')
      if content is None:
         content = title
      serializer.save(content=content)

product_list_create_view = ProductListCreateAPIView.as_view()

class ProductDetailAPIView(generics.RetrieveAPIView):
   # queryset and serializer_class is important value
   queryset = Product.objects.all()
   serializer_class = ProductSerializers
   # lookup_field = 'pk'
product_detail_view = ProductDetailAPIView.as_view()


class ProductUpdateAPIView(generics.UpdateAPIView):
   # queryset and serializer_class is important value
   queryset = Product.objects.all()
   serializer_class = ProductSerializers
   lookup_field = 'pk'

   def perform_update(self, serializer):
      instance = serializer.save()
      if not instance.content:
         instance.content = instance.title

product_update_view = ProductUpdateAPIView.as_view()


class ProductDestroyAPIView(generics.DestroyAPIView):
   # queryset and serializer_class is important value
   queryset = Product.objects.all()
   serializer_class = ProductSerializers
   lookup_field = 'pk'

   def perform_destroy(self, instance):
      super().perform_destroy(instance)

product_destroy_view = ProductDestroyAPIView.as_view()


class ProductMixinView(
   mixins.CreateModelMixin,
   mixins.ListModelMixin,
   mixins.RetrieveModelMixin,
   generics.GenericAPIView
   ):
  
   queryset = Product.objects.all()
   serializer_class = ProductSerializers
   lookup_field = 'pk'

   def get(self, request, *args, **kwargs): #Http ->> get
      pk = kwargs.get("pk")
      if pk is not None:
         return self.retrieve(request, *args, **kwargs)
      return self.list(request, *args, **kwargs)
   def post(self, request, *args, **kwargs): #Http ->> post
      return self.create(request, *args, **kwargs)
   def perform_create(self, serializer):
      #print(serializer.validated_data)
      title = serializer.validated_data.get('title')
      content = serializer.validated_data.get('content')
      if content is None:
         content = title
      serializer.save(content=content)
product_mixin_view = ProductMixinView.as_view()

"""
class ProductListAPIView(generics.ListAPIView):
   # queryset and serializer_class is important value
   queryset = Product.objects.all()
   serializer_class = ProductSerializers
product_List_view = ProductListAPIView.as_view()
"""

@api_view(['GET','POST'])
def product_alt_view(request, pk=None, *args, **kwargs):
   method = request.method
   if method == "GET":
      if pk is not None:
       # detai view
       obj = get_object_or_404(Product, pk=pk)
       data = ProductSerializers(obj, many=False).data
       return Response(data)
       #url > api/products/pk/
      # list view
      # show all list view
      queryset = Product.objects.all()
      data = ProductSerializers(queryset, many=True).data
      return Response(data)
   if method == "POST":
      #create a product
      serializer = ProductSerializers(data=request.data)
      if serializer.is_valid():
         title = serializer.validated_data.get('title')
         content = serializer.validated_data.get('content')
         if content is None:
            content = title
         serializer.save(content=content)
         return Response(serializer.data)
