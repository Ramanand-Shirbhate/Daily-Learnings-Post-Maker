# Automated Daily Learning Social Posting Workflow

[cite_start]**Author:** Ramanand Anilrao Shirbhate [cite: 3]  
[cite_start]**Subject:** Workshop Technology (Introduction to Generative AI) [cite: 5]  
[cite_start]**Academic Year:** 2025-26 [cite: 8]

## 📖 Project Overview
[cite_start]This project is a fully automated n8n workflow designed to publish daily learning reflections across LinkedIn and Twitter without manual intervention[cite: 10]. 

[cite_start]Instead of manually logging in and posting every day, this system reads daily learning notes from a Google Sheet, processes them at a scheduled time, and uses **Gemini AI** to rewrite the text into engaging social media content[cite: 11, 12]. [cite_start]The workflow ensures consistency, reduces daily effort, and supports continuous learning documentation[cite: 13].

## 🛠️ Tools & Technologies
[cite_start]This automation pipeline utilizes the following tools and APIs[cite: 15]:

* [cite_start]**n8n:** The primary workflow automation platform managing node-level execution[cite: 16, 17].
* [cite_start]**Google Sheets:** Serves as the structured database for storing daily learnings[cite: 20, 21].
* [cite_start]**Gemini AI:** Generative AI service used to rewrite raw notes into professional short-form posts[cite: 22, 23].
* [cite_start]**LinkedIn API:** Used for automatic publishing to a personal profile[cite: 28, 29].
* [cite_start]**Twitter / X API:** Used for automatic tweeting[cite: 30, 31].
* [cite_start]**ChatGPT:** Used for prompt refinement and workflow planning[cite: 32, 33].

## ⚙️ Architecture & Workflow
[cite_start]The workflow follows a structured multi-layer pipeline[cite: 44]:

1.  [cite_start]**Trigger Layer:** Activates daily at a scheduled time (evening)[cite: 45, 61].
2.  [cite_start]**Data Layer:** Retrieves learning entries from Google Sheets[cite: 47, 62].
3.  [cite_start]**Validation Layer:** An `IF` node checks if the current entry has already been marked as "Posted" to prevent duplication[cite: 50, 63].
4.  [cite_start]**AI Processing Layer:** Gemini AI rewrites the raw text into a polished post[cite: 52, 64].
5.  [cite_start]**Publishing Layer:** Content is posted simultaneously to LinkedIn and Twitter/X[cite: 54, 65].
6.  [cite_start]**Persistence Layer:** The Google Sheet row is updated to mark the entry as "Yes" (Posted), ensuring it is not processed again[cite: 56, 66].

## 🤖 AI Prompt Engineering
[cite_start]The following system prompt is used within the Gemini node to ensure high-quality output[cite: 37, 38]:

> [cite_start]"Rewrite the following learning note into a concise, engaging, professional social media post. Make the tone positive, curious, reflective. Keep it within 250 characters. Keep core meaning. Add relevant hashtags. DO NOT mention that it is rewritten or AI generated." [cite: 38-40]

[cite_start]**Input:** `{{$json["Learning Summary"]}}` [cite: 41]

## 📋 Setup & Configuration

### 1. Google Sheets Setup
[cite_start]Create a Google Sheet with the following headers [cite: 92-94]:
| Date | Learning Summary | Posted? |
|------|------------------|---------|
| DD-MM-YYYY | [Your raw notes here] | No |

[cite_start]*Note: The workflow looks for rows where "Posted?" is set to "No"[cite: 63].*

### 2. n8n Credentials Required
* **Google Sheets OAuth2:** To read/write to the sheet.
* **Google Gemini API:** To access the generative AI model.
* **LinkedIn OAuth2:** For posting to your profile.
* **Twitter/X OAuth1/2:** For creating tweets.

### 3. Workflow Logic
* [cite_start]**Schedule Trigger:** set to run every evening[cite: 61].
* [cite_start]**Update Row Node:** Automatically changes the "Posted?" column from `No` to `Yes` after successful publishing[cite: 73, 66].

## 📊 Results
* [cite_start]**Automated Consistency:** Eliminates manual effort for daily documentation[cite: 68].
* [cite_start]**Quality Control:** AI ensures posts are audience-friendly and professional[cite: 42].
* [cite_start]**Duplicate Prevention:** Logic ensures only new learnings are published[cite: 67].

---
[cite_start]*This project demonstrates the practical application of workflow automation, API integration, and generative AI in a personal knowledge management context[cite: 240].*
