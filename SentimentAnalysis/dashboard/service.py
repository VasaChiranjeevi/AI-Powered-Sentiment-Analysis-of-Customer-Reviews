from dashboard.models import Review
import logging
logger = logging.getLogger(__name__)

class DashboardService:

    def get_all_reviews_by_company(self, company, data, date_created, sentiment_label):
        try:
            Review.objects.create(
                company=company,
                customer_name=data['customer_name'],
                date_created=date_created,
                review_text=data['review_text'],
                sentiment=sentiment_label
            )
            # Update summary
            reviews = Review.objects.filter(company=company)
            return reviews
        except Exception as e:
            logger.info(f"Error occured while extract summary: {e}")
            raise e
