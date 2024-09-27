import json
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from .models import Company, Review, Summary


def index(request):
    companies = Company.objects.all()
    return render(request, 'index.html', {'companies': companies})



def get_reviews(request, company_id):
    reviews = Review.objects.filter(company_id=company_id).order_by('-date_created')[:2]
    summary = Summary.objects.filter(company_id=company_id).first()

    review_data = [
        {
            'customer_name': review.customer_name,
            'review_text': review.review_text,
            'date_created': review.date_created.strftime("%Y-%m-%d")
        } for review in reviews
    ]

    return JsonResponse({
        'reviews': review_data,
        'summary': summary.summary_text if summary else "No summary available."
    })

def submit_review(request):
    if request.method == "POST":
        data = json.loads(request.body)
        company = Company.objects.get(id=data['company_id'])
        Review.objects.create(
            company=company,
            customer_name=data['customer_name'],
            review_text=data['review_text'],
            sentiment=0
        )
        return JsonResponse({'message': 'Review submitted successfully!'})
