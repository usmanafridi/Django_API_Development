from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from rest_framework.parsers import JSONParser
from .models import Article

from .serializers import ArticleSerializer 
from django.views.decorators.csrf import csrf_exempt

# Create your views here.



from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from rest_framework.views import APIView
from rest_framework import generics
from rest_framework import mixins
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets


## Now we will be working with class-based API ##

class ArticleAPIView(APIView):
	def get(self, request):
		articles= Article.objects.all()
		serializer= ArticleSerializer(articles, many=True)
		return Response(serializer.data)


	def post(self, request):
		serializer= ArticleSerializer(data=request.data)

		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status=status.HTTP_201_CREATED)

		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)







######Now we will be using REST FRAMEWORK DECORATORS AND WRAPPING IT IN API VIEW
# @api_view(['GET', 'POST'])
# def article_list(request):
# 	if request.method =='GET':
# 		articles= Article.objects.all()
# 		serializer= ArticleSerializer(articles, many=True)
# 		return Response(serializer.data)

# 	elif request.method== 'POST':
# 		serializer= ArticleSerializer(data=request.data)

# 		if serializer.is_valid():
# 			serializer.save()
# 			return Response(serializer.data, status=status.HTTP_201_CREATED)

# 		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)





##### This was function based APIs#########
# @csrf_exempt
# def article_list(request):
# 	if request.method =='GET':
# 		articles= Article.objects.all()
# 		serializer= ArticleSerializer(articles, many=True)
# 		return JsonResponse(serializer.data, safe=False)

# 	elif request.method== 'POST':
# 		data=JSONParser().parse(request)
# 		serializer= ArticleSerializer(data=data)

# 		if serializer.is_valid():
# 			serializer.save()
# 			return JsonResponse(serializer.data, status=201)

# 		return JsonResponse(serializer.errors, status=400)


@api_view(['GET','PUT', 'DELETE'])

def article_detail(request, pk):
	try:
		article= Article.objects.get(pk=pk)

	except Article.DoesNotExist:
		return HttpResponse(status=status.HTTP_404_NOT_FOUND)

	if request.method=='GET':
		serializer=ArticleSerializer(article)
		return Response(serializer.data)

	elif request.method=='PUT':
		
		serializer=ArticleSerializer(article, data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data)

		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


	elif request.method=='DELETE':
		article.delete()
		return Response(status= status.HTTP_204_NO_CONTENT)





##Now work with class-based API detail:

class ArticleDetails(APIView):
	def get_object(self, id):
		try:
			return Article.objects.get(id=id)

		except Article.DoesNotExist:

			return HttpResponse(status=status.HTTP_404_NOT_FOUND)


	def get(self, request, id):
		article=self.object(id)
		serializer=ArticleSerializer(article)
		return Response(serializer.data)

	def put(self, request, id):
		article=self.object(id)
		serializer=ArticleSerializer(article, data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data)

		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


	def delete(self, request, id):
		article=self.object(id)

		article.delete()
		return Response(status= status.HTTP_204_NO_CONTENT)



class GenericAPIView(generics.GenericAPIView, mixins.ListModelMixin, 
	mixins.CreateModelMixin, mixins.RetrieveModelMixin, mixins.DestroyModelMixin):
	serializer_class= ArticleSerializer
	queryset=Article.objects.all()

	lookup_field='id'
	# authentication_classes = [SessionAuthentication, BasicAuthentication]
	authentication_classes = [TokenAuthentication]
	permission_classes = [IsAuthenticated]
   

	def get(self, request, id=None):
		if id:
			return self.retrieve(request)
		else:
			return self.list(request)


	def post(self, request):
		return self.create(request)


	def put(self, request, id=None):
		return self.update(request, id)


	def delete(self, request, id=None):
		return self.destroy(request, id)