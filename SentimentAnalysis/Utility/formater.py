from django.http import JsonResponse
import json
from .Apiconnect import generate_response
from dashboard.models import KeywordSummary, Summary
from Utility.constant import Summary_prompt

import logging
logger = logging.getLogger(__name__)


def generate_summary_prompt(reviews):
    review_data_formatted = ''.join([
        f"{review.review_text}\n"
        for review in reviews
 
    ])
    
    return f"{Summary_prompt}\nThe reviews are:\n{{\n{review_data_formatted}\n}}"+"Please generate the response in JSON format. start from { and Avoid using special characters"

def response_formater(reviews,company):
    # Generate the response
    try:
            responces = generate_response(generate_summary_prompt(reviews))

            # Print for debugging
            print(f"Generated responces: {responces}")
            
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
                # Check if a KeywordSummary already exists for the same company and keyword
                existing_summary = KeywordSummary.objects.filter(company=company, keyword=keyword).first()

                if existing_summary:
                    # Optionally, you could update the existing one instead of creating a new one
                    existing_summary.keyword_summary = keyword_summary
                    existing_summary.save()
                else:
                    # Create a new record if none exists
                    KeywordSummary.objects.create(
                        company=company,
                        keyword=keyword,
                        keyword_summary=keyword_summary
                    )

            return summary

    except Exception as e:
        logger.info(f"Error occurred while response format: {e}")
        raise e
