import json
from django.http import JsonResponse, HttpResponseBadRequest
from django.shortcuts import render, get_object_or_404
from .models import Company, Review, Summary


def index(request):
    try:
        companies = Company.objects.all()
        return render(request, 'index.html', {'companies': companies})
    except Exception as e:
        # Log the error and return a 500 internal server error
        print(f"Error in index view: {e}")
        return HttpResponseBadRequest("An error occurred while loading the companies.")


def get_reviews(request, company_id):
    try:
        # Ensure that the company exists
        company = get_object_or_404(Company,pk=company_id)
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
    except Company.DoesNotExist:
        return JsonResponse({'error': 'Company not found.'}, status=404)
    except Exception as e:
        # Log the error and return an appropriate message
        print(f"Error in get_reviews view: {e}")
        return JsonResponse({'error': 'An error occurred while fetching the reviews.'}, status=500)


def submit_review(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)

            # Validate the required fields
            if 'company_id' not in data or 'customer_name' not in data or 'review_text' not in data:
                return JsonResponse({'error': 'Invalid data. Company ID, customer name, and review text are required.'},
                                    status=400)

            company = get_object_or_404(Company, id=data['company_id'])

            # Create the new review
            Review.objects.create(
                company=company,
                customer_name=data['customer_name'],
                review_text=data['review_text'],
                sentiment=0  # Default sentiment
            )
            return JsonResponse({'message': 'Review submitted successfully!'})
        except Company.DoesNotExist:
            return JsonResponse({'error': 'Company not found.'}, status=404)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data.'}, status=400)
        except Exception as e:
            # Log the error and return an appropriate error message
            print(f"Error in submit_review view: {e}")
            return JsonResponse({'error': 'An error occurred while submitting the review.'}, status=500)
    else:
        return JsonResponse({'error': 'Invalid request method.'}, status=405)
