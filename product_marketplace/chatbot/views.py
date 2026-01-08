from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from openai import OpenAI
from django.conf import settings
from products.models import Product
from .models import ChatMessage

# Create your views here.

client = OpenAI(api_key=settings.OPENAI_API_KEY)

class ChatbotView(APIView):
    def post(self, request):
        question = request.data.get("question")

        products = Product.objects.filter(status='approved')
        product_list = "\n".join(
            [f"{p.name}: ${p.price} - {p.description}" for p in products]
        )

        prompt = f"""
You are a product assistant.
Answer ONLY using the products below.

Products:
{product_list}

Question:
{question}
"""

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "user", "content": prompt}
            ],
        )

        answer = response.choices[0].message.content

        ChatMessage.objects.create(
            user=request.user if request.user.is_authenticated else None,
            question=question,
            answer=answer
        )

        return Response({"answer": answer})


from django.shortcuts import render
from openai import OpenAI
from django.conf import settings
from products.models import Product

client = OpenAI(api_key=settings.OPENAI_API_KEY)


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
Answer ONLY using the products below.

Products:
{product_list}

Question:
{question}
"""

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "user", "content": prompt}
            ],
        )

        answer = response.choices[0].message.content

    return render(request, "chat.html", {"answer": answer})
