from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from openai import OpenAI
from django.conf import settings
from products.models import Product
from .models import ChatMessage

from django.contrib.auth.decorators import login_required
import os

# Create your views here.

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

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

def build_product_context(products):
    if not products:
        return "No products are currently available."

    lines = []
    for p in products:
        lines.append(
            f"- {p.name}: {p.description} (Price: ${p.price})"
        )
    return "\n".join(lines)

@login_required
def chat_view(request):
    response_text = None

    if request.method == "POST":
        user_message = request.POST.get("message")

        # 🔹 STEP 1: Query products (PUBLIC PRODUCTS)
        products = Product.objects.all()

        # 🔹 STEP 2: Optional simple filtering
        lower_msg = user_message.lower()
        if "under $" in lower_msg:
            try:
                price = float(lower_msg.split("under $")[1].split()[0])
                products = products.filter(price__lt=price)
            except Exception:
                pass

        product_context = build_product_context(products)

        # 🔹 STEP 3: AI prompt (STRICT)
        prompt = f"""
You are a product assistant.

Answer ONLY using the product list below.
If the answer is not in the list, say you don't know.

Products:
{product_context}

User question:
{user_message}
"""

        ai_response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful product assistant."},
                {"role": "user", "content": prompt},
            ],
        )

        response_text = ai_response.choices[0].message.content

        # 🔹 STEP 4: Store chat history
        ChatMessage.objects.create(
            user=request.user,
            user_message=user_message,
            ai_response=response_text,
        )

    return render(request, "chat.html", {"response": response_text})
