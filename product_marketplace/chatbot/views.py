from django.shortcuts import render

import openai
from rest_framework.views import APIView
from rest_framework.response import Response
from products.models import Product
from .models import ChatMessage

# Create your views here.

openai.api_key = "YOUR_API_KEY"

class ChatbotView(APIView):
    def post(self, request):
        question = request.data.get("question")

        products = Product.objects.filter(status='approved')
        product_list = "\n".join(
            [f"{p.name}: ${p.price} - {p.description}" for p in products]
        )

        prompt = f"""
        You are a product assistant.
        Answer only using the products below.

        Products:
        {product_list}

        Question:
        {question}
        """

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )

        answer = response['choices'][0]['message']['content']

        ChatMessage.objects.create(
            user=request.user,
            question=question,
            answer=answer
        )

        return Response({"answer": answer})



def chatbot_page(request):
    answer = None

    if request.method == "POST":
        question = request.POST.get("question")

        products = Product.objects.filter(status='approved')
        product_list = "\n".join(
            [f"{p.name}: ${p.price} - {p.description}" for p in products]
        )

        prompt = f"""
        You are a product assistant.
        Use only the products below.

        Products:
        {product_list}

        Question:
        {question}
        """

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )

        answer = response['choices'][0]['message']['content']

    return render(request, 'chat.html', {
        'answer': answer
    })
