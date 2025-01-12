from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from .serializers import RegisterSerializer
from rest_framework import status
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken 
from decimal import Decimal
import random

class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Usuario cadastrado com sucesso!"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        user = authenticate(request, username=username, password=password)

        #tentativa por email
        if user is None:
            try:
                user = User.objects.get(email=username)
                authenticate(request, username=user.username, password=password)
            except User.DoesNotExist:
                pass

        if user:
            refresh = RefreshToken.for_user(user)
            return Response ({
                "refresh": str(refresh),
                "access": str(refresh.access_token) 
            })

        return Response({"error": "autenticação não permitida!"}, status=status.HTTP_401_UNAUTHORIZED)

class SaldoView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        saldo_account = request.user.bet_account
        return Response({"saldo": saldo_account.balance + saldo_account.bonus})

class DepositarView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        amount = request.data.get("amount")

        try:
            amount = Decimal(amount)

        except:
            return Response({"erro": "Algo deu errado!"}, status=status.HTTP_400_BAD_REQUEST)

        saldo_account = request.user.bet_account
        saldo_account.deposit_balance(amount)
        saldo_account.deposit_bonus(amount)

        return Response({"Adicionado": amount+amount}, status=status.HTTP_200_OK)
    
class SacarView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        amount = request.data.get("amount")

        try:
            amount = Decimal(amount)

        except:
            return Response({"erro": "Algo deu errado"}, status=status.HTTP_400_BAD_REQUEST)

        saldo_account = request.user.bet_account

        try:
            res1 = saldo_account.withdrawal_balance(amount)

            if res1 == True:
                return Response({"Sacado": amount}, status=status.HTTP_200_OK)
            else:
                res = saldo_account.withdrawal_bonus(amount)

                if res == True:
                    return Response({"Sacado": amount}, status=status.HTTP_200_OK)
                else:
                    return Response({"error": "saldo insuficiente"}, status=status.HTTP_400_BAD_REQUEST)

        except:
            return Response({"error": "saldo insuficiente"}, status=status.HTTP_400_BAD_REQUEST)

class FogueteView(APIView):
    def post(self, request):
        amount = request.user.get("amount")

        rand_number = random.randint(0, 10)

