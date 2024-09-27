### Project Documentation for AI-Powered Sentiment Analysis of Customer Reviews

---

#### 1. **Project Overview**

The objective of this project is to build an AI-powered system to collect and analyze customer reviews for multiple companies, generating summaries and extracting common keywords using existing free AI models. The reviews and their respective analysis will be stored in a database, and summaries will be updated monthly.

#### 2. **Project Architecture**

- **Frontend**: A simple user interface where customers submit reviews.
- **Backend**: REST API to handle review submissions, trigger AI analysis, and store results in a database.
- **AI Model**: Free AI sentiment analysis models, e.g., Hugging Face models, will be used for natural language processing.
- **Database**: A relational database (e.g., MySQL, PostgreSQL) to store company details, customer reviews, summary reports, and keyword analysis.

---

#### 3. **Use Cases**

##### **Use Case 1**: Submitting a Review
**Actors**: User (Customer)
- **Description**: A user submits a review on a company’s website.
- **Preconditions**: The company exists in the database with a unique company ID.
- **Postconditions**: The review is stored in the database, and AI analysis is triggered.
- **Steps**:
  1. The user inputs their name and review on the company’s review page.
  2. The system identifies the company ID.
  3. The review is stored in the database.
  4. The AI model collects all reviews for the company, generates a summary, and identifies five common keywords.
  5. The summarized review and keyword details are saved in the database.

##### **Use Case 2**: Analyzing and Summarizing Reviews
**Actors**: System (AI Model, Database)
- **Description**: The system analyzes all available reviews for a given company and generates a summary.
- **Preconditions**: At least one review exists for the company.
- **Postconditions**: A summarized review with keywords is saved in the database.
- **Steps**:
  1. The system retrieves all reviews for the company from the database.
  2. The AI model generates a sentiment analysis summary.
  3. The model identifies five common keywords and provides individual analysis for each keyword.
  4. The summary and keyword analysis are stored in the database.

##### **Use Case 3**: Updating Monthly Summaries
**Actors**: System
- **Description**: The system updates the summarized review data for each company monthly.
- **Preconditions**: There must be new reviews within the current month.
- **Postconditions**: The summary and keyword data are updated in the database.
- **Steps**:
  1. On a monthly basis, the system triggers a review collection process.
  2. New reviews are analyzed, and the existing summaries are updated.
  3. New keyword insights are saved in a separate table for monthly tracking.

---

#### 4. **User Stories**

##### **User Story 1**: Customer Submits a Review
- **As a customer** of company XYZ, I want to submit my review on the company website so that my feedback can be captured and analyzed.
- **Acceptance Criteria**:
  1. The review should be stored under the correct company ID.
  2. I should be notified that my review was successfully submitted.

##### **User Story 2**: Admin Reviews AI Summary
- **As a company admin**, I want to view a summarized report of customer reviews with key insights so that I can understand customer sentiment.
- **Acceptance Criteria**:
  1. The admin dashboard should display a summary of all reviews.
  2. The system should highlight five keywords and their respective insights.

##### **User Story 3**: Customer Feedback Influences AI Summary
- **As a customer**, I want my feedback to be reflected in the company’s monthly report so that I can see that my input is valued.
- **Acceptance Criteria**:
  1. My review should be included in the summary within the same month.
  2. The company report should update monthly with new reviews.

---

#### 5. **System Flow**

1. **Customer Submission**:
   - A customer submits a review on a company page.
   - The company ID, customer name, and review are sent to the backend API.

2. **Backend Processing**:
   - The API stores the review in the database.
   - The AI model is triggered to retrieve all reviews for the company.

3. **AI Model Analysis**:
   - The AI model generates a summary of the reviews (e.g., sentiment score, main themes).
   - It identifies five common keywords and provides individual insights for each.

4. **Database Updates**:
   - The summary and keyword analysis are saved in the database under separate tables.
   - The summary is updated monthly if new reviews are added.

---

#### 6. **Database Structure**

- **Tables**:
  1. **Companies**: Contains company details.
  2. **Reviews**: Stores individual reviews.
  3. **Summaries**: Stores monthly summaries for each company.
  4. **Keywords**: Stores common keywords and their respective analysis.

##### **Table: Companies**
| Column Name   | Data Type | Description                |
|---------------|-----------|----------------------------|
| company_id    | INT       | Unique ID for each company |
| company_name  | VARCHAR   | Name of the company         |

##### **Table: Reviews**
| Column Name   | Data Type | Description                |
|---------------|-----------|----------------------------|
| review_id     | INT       | Unique ID for each review   |
| company_id    | INT       | Foreign key for company     |
| customer_name | VARCHAR   | Name of the customer        |
| review_text   | TEXT      | Review text provided by customer |
| date_created  | DATETIME  | Timestamp of review         |

##### **Table: Summaries**
| Column Name   | Data Type | Description                |
|---------------|-----------|----------------------------|
| summary_id    | INT       | Unique ID for each summary  |
| company_id    | INT       | Foreign key for company     |
| summary_text  | TEXT      | Summarized review           |
| date_updated  | DATETIME  | Timestamp of update         |

##### **Table: Keywords**
| Column Name   | Data Type | Description                |
|---------------|-----------|----------------------------|
| keyword_id    | INT       | Unique ID for each keyword  |
| company_id    | INT       | Foreign key for company     |
| keyword       | VARCHAR   | Common keyword identified   |
| keyword_summary | TEXT    | Summary for the keyword     |

---

#### 7. **API Endpoints**

1. **POST /reviews**
   - **Description**: Endpoint to submit a new review.
   - **Payload**:
     ```json
     {
       "company_id": 1,
       "customer_name": "abc",
       "review_text": "The service was excellent!"
     }
     ```
   - **Response**: Success message after saving to the database.

2. **GET /summaries/{company_id}**
   - **Description**: Retrieve the summarized reviews and keyword analysis for a company.
   - **Response**:
     ```json
     {
       "summary": "Most customers appreciate the service...",
       "keywords": ["service", "delivery", "support", "pricing", "quality"]
     }
     ```

---

#### 8. **Conclusion**

This project outlines a quick, efficient system to handle the collection, storage, and analysis of customer reviews using AI models. It is designed to be implemented in 4 to 6 hours, using available free AI models for sentiment analysis. The documentation provides clear use cases and steps to achieve the project’s goals.
