from Utility.formater import response_formater
import logging
logger = logging.getLogger(__name__)


class ReviewAnalysisService:
    def extractSummarizeReviewsByCustomer(self, company, reviews):
        try:
            summary = response_formater(reviews, company)
            return summary
        except Exception as e:
            logger.info(f"Error occurred while extract summary: {e}")
            raise e

