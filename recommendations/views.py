import re
from django.shortcuts import render
from products.models import Product
from .forms import GiftRecommendationForm
from .services.groq_service import call_groq

def _to_any(v: str) -> str:
    return v if v else "Any"

def _build_prompt(budget, occasion, gender, age_range, relationship, products):
    lines = []
    for p in products:
        desc = (p.productDescription or "").strip().replace("\n", " ")
        desc = desc[:250]
        lines.append(f"- ID:{p.id} | {p.productName} | price:{p.productPrice} | desc:{desc}")

    products_block = "\n".join(lines) if lines else "No products available."

    return f"""
You recommend gifts from the given product list.

User constraints:
- Budget: {budget}
- Occasion: {occasion}
- Recipient gender: {_to_any(gender)}
- Age range: {_to_any(age_range)}
- Relationship: {_to_any(relationship)}

Products:
{products_block}

Task:
1) Choose up to 6 products that best match the occasion and user constraints AND are within budget.
2) Return ONLY product IDs in this exact format:
IDs: 12, 5, 33
"""

def _extract_ids(ai_text: str):
    m = re.search(r"IDs\s*:\s*([0-9,\s]+)", ai_text, re.IGNORECASE)
    if not m:
        return []
    nums = re.findall(r"\d+", m.group(1))
    return [int(x) for x in nums][:6]

def recommend_gift(request):
    recommendations = []
    ai_raw = None
    error = None

    if request.method == "POST":
        form = GiftRecommendationForm(request.POST)
        if form.is_valid():
            budget = form.cleaned_data["budget"]
            occasion = form.cleaned_data["occasion"]
            gender = form.cleaned_data.get("gender", "")
            age_range = form.cleaned_data.get("age_range", "")
            relationship = form.cleaned_data.get("relationship", "")

            products = Product.objects.filter(productPrice__lte=budget).order_by("productPrice")[:80]

            prompt = _build_prompt(budget, occasion, gender, age_range, relationship, products)

            try:
                ai_raw = call_groq(prompt)
                ids = _extract_ids(ai_raw)
                if ids:
                    recommendations = list(Product.objects.filter(id__in=ids))
            except Exception as e:
                error = str(e)
        else:
            error = "Please check the form inputs."
    else:
        form = GiftRecommendationForm()

    return render(request, "recommendations/recommend_gift.html", {
        "form": form,
        "recommendations": recommendations,
        "ai_raw": ai_raw,  
        "error": error,
    })
