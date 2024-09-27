from django.db import models
# from SentimentAnalysis.SentimentAnalysis.constants import REVIEW_SENTIMENTS


class Company(models.Model):
    company_id = models.AutoField(primary_key=True)
    company_name = models.CharField(max_length=255)

    def __str__(self):
        return self.company_name

    class Meta:
        db_table = "company"


class KeywordSummary(models.Model):
    keyword_id = models.AutoField(primary_key=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    keyword = models.CharField(max_length=255)
    keyword_summary = models.TextField()
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Keyword Summary for {self.company}: {self.keyword}"

    class Meta:
        db_table = "keyword_summary"


class Review(models.Model):
    REVIEW_SENTIMENTS = (
        (-1, 'Negative'),
        (0, 'Neutral'),
        (1, 'Positive')
    )

    review_id = models.AutoField(primary_key=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    customer_name = models.CharField(max_length=255)
    review_text = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    sentiment = models.IntegerField(choices=REVIEW_SENTIMENTS)

    def __str__(self):
        return f"Review {self.review_id} for {self.company}"

    class Meta:
        db_table = "review"


class Summary(models.Model):
    summary_id = models.AutoField(primary_key=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    summary_text = models.TextField()
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Summary for {self.company}"

    class Meta:
        db_table = "summary"
