MAX_ATTEMPTS = 2

Summary_prompt = '''"You are an AI that specializes in analyzing product reviews and identifying key insights. I will provide you with a set of customer reviews. Your task is to :

1. Summarize the overall sentiment of the reviews, highlighting the positive and negative aspects.
2. Identify and list the most common keywords related to the product (not adjectives), along with a brief description of each keyword. Focus on features, functionality, or technical aspects mentioned by multiple reviewers.

The response should be in the format of JSON with the following structure:
{
  "Overview": "<summary of overall sentiment>",
  "Keywords": {
    "<Keyword1>": "<description of keyword based on common mentions>",
    "<Keyword2>": "<description of keyword based on common mentions>",
    ...
  }
}

Here are the reviews:

'''

