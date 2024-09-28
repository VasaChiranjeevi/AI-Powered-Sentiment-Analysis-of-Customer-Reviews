import json
from datetime import datetime

from django.http import JsonResponse, HttpResponseBadRequest
from django.shortcuts import render, get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .constant import POSITIVE, NEGATIVE, NEUTRAL
from .models import Company, Review, Summary,KeywordSummary
from .Apiconnect import generate_response
from .formater import generate_summary_prompt,response_formater
from .sentiment_analyzer import SentimentAnalyser
from django.http import JsonResponse
from django.views import View
from django.shortcuts import get_object_or_404, render
import logging
logger = logging.getLogger(__name__)

def index(request):
    try:
        companies = Company.objects.all()
        return render(request, 'index.html', {'companies': companies})
    except Exception as e:
        # Log the error and return a 500 internal server error
        logger.error(f"Error in index view: {e}")
        return HttpResponseBadRequest("An error occurred while loading the companies.")


def get_reviews(request, company_id,renderpage=False):
    try:
        # Ensure that the company exists
        company = get_object_or_404(Company,pk=company_id)
        reviews = Review.objects.filter(company_id=company_id).order_by('-review_id')
        summary = Summary.objects.filter(company_id=company_id).latest('summary_id')
        postive_count = Review.objects.filter(company_id=company_id,sentiment=POSITIVE).count()
        negative_count = Review.objects.filter(company_id=company_id, sentiment=NEGATIVE).count()
        neutral_count = Review.objects.filter(company_id=company_id, sentiment=NEUTRAL).count()

        review_data = [
            {
                'customer_name': review.customer_name,
                'review_text': review.review_text,
                'date_created': review.date_created.strftime("%Y-%m-%d"),
            } for review in reviews[:2]
        ]

        if not summary:
            # Generate the response
            responces = generate_response(generate_summary_prompt(review_data))

            # Print for debugging
            logger.info(f"Generated responces: {responces}")

            # Use a regular expression to extract only the valid JSON part
            json_start = responces.find('{')  # Find the position of the first curly brace
            if json_start != -1:
                responces_cleaned = responces[json_start:]  # Remove anything before the first brace
            else:
                return JsonResponse({'error': 'Invalid response format.'}, status=400)

            # Now try to parse the cleaned JSON
            try:
                responces_dict = json.loads(responces_cleaned)
            except json.JSONDecodeError as e:
                print(f"Failed to decode JSON: {e}")
                return JsonResponse({'error': 'Invalid JSON format.'}, status=400)

            # Extract summary and keywords from the cleaned response
            summary_text = responces_dict.get("Overview")
            keywords = responces_dict.get("Keywords", {})

            # Save the summary to the database
            summary = Summary.objects.create(
                company=company,
                summary_text=summary_text
            )

            # Save each keyword and its description to the KeywordSummary table
            for keyword, keyword_summary in keywords.items():
                KeywordSummary.objects.create(
                    company=company,
                    keyword=keyword,
                    keyword_summary=keyword_summary
                )
        if renderpage:
            return {
            'reviews': review_data,
            'summary': summary.summary_text,  # Return the saved summary
        }

        return JsonResponse({
            'reviews': review_data,
            'summary': summary.summary_text,
            'positive': postive_count,
            'negative': negative_count,
            'neutral': neutral_count
        })
    except Company.DoesNotExist:
        return JsonResponse({'error': 'Company not found.'}, status=404)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Failed to parse JSON response.'}, status=400)
    except Exception as e:
        # Log the error and return an appropriate message
        logger.error(f"Error in get_reviews view: {e}")
        return JsonResponse({'error': 'An error occurred while fetching the reviews.'}, status=500)



class AnalyseReviews(APIView):
    def post(self, request):
        return Response({"success": "Analyze Review"}, status=status.HTTP_200_OK)


class SubmitResponse(View):
    def post(self, request):
        try:
            data = json.loads(request.body)

            # Validate the required fields
            if 'company_id' not in data or 'customer_name' not in data or 'review_text' not in data:
                return JsonResponse({'error': 'Invalid data. Company ID, customer name, and review text are required.'}, status=400)

            company = get_object_or_404(Company, pk=data['company_id'])
            date_created = datetime.now()
            company_id = data['company_id']
            sentiment_label = SentimentAnalyser().get_sentiment(data['review_text'])

            # Create the new review
            Review.objects.create(
                company=company,
                customer_name=data['customer_name'],
                date_created=date_created,
                review_text=data['review_text'],
                sentiment=sentiment_label
            )

            # Update summary
            reviews = Review.objects.filter(company=company)
            response_formater(reviews, company)

            # Render the index.html template with the updated context
            context = get_reviews(request, company_id)
            return render(request, 'index.html', context)

        except Company.DoesNotExist:
            return JsonResponse({'error': 'Company not found.'}, status=404)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data.'}, status=400)
        except Exception as e:
            # Log the error and return an appropriate error message
            logger.error(f"Error in submit_review view: {e}")
            return JsonResponse({'error': 'An error occurred while submitting the review.'}, status=500)

