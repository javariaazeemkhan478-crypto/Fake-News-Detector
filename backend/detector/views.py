from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated
from .ml_utils import predict
from .models import Prediction
import requests
from bs4 import BeautifulSoup

def scrape_url(url):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
        r = requests.get(url, timeout=15, headers=headers)
        soup = BeautifulSoup(r.content, 'html.parser')
        
        # Remove unwanted tags
        for tag in soup(['script', 'style', 'nav', 'footer', 'header']):
            tag.decompose()
        
        # Try article tag first
        article = soup.find('article')
        if article:
            text = ' '.join(p.get_text() for p in article.find_all('p'))
        else:
            text = ' '.join(p.get_text() for p in soup.find_all('p'))
        
        text = ' '.join(text.split())
        return text if len(text) > 100 else None
    except:
        return None

class LoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user:
            token, _ = Token.objects.get_or_create(user=user)
            return Response({'token': token.key, 'username': user.username})
        return Response({'error': 'Invalid credentials'}, status=400)
    
    from django.contrib.auth.models import User

class RegisterView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        email    = request.data.get('email', '')

        if not username or not password:
            return Response({'error': 'Username and password required'}, status=400)
        if User.objects.filter(username=username).exists():
            return Response({'error': 'Username already exists'}, status=400)

        user  = User.objects.create_user(username=username, password=password, email=email)
        token, _ = Token.objects.get_or_create(user=user)
        return Response({'token': token.key, 'username': user.username})

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        request.user.auth_token.delete()
        return Response({'message': 'Logged out'})

class PredictView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        text = request.data.get('text', '')
        url  = request.data.get('url', '')
        if url:
            text = scrape_url(url)
            if not text:
                return Response({'error': 'Could not scrape URL'}, status=400)
        if not text or len(text.strip()) < 20:
            return Response({'error': 'Text too short'}, status=400)
        result = predict(text)
        Prediction.objects.create(
            text=text[:500],
            label=result['label'],
            confidence=result['confidence'],
            user=request.user
        )
        return Response(result)

class AnalyticsView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        preds  = Prediction.objects.filter(user=request.user)
        total  = preds.count()
        fake   = preds.filter(label='FAKE').count()
        real   = preds.filter(label='REAL').count()
        recent = list(preds.order_by('-created_at')[:10].values('label', 'confidence', 'created_at'))
        return Response({'total': total, 'fake': fake, 'real': real, 'recent': recent})