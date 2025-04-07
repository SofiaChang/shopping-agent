# Project Roadmap & Milestones

## MVP (Current Implementation)

The MVP consists of a functional prototype that parses natural language queries using regular
expressions to extract user constraints such as price ranges, ratings, reviews, and prime
shipping requirements. The agent scrapes product data from Amazon using Selenium,
gathering essential information including titles, prices, ratings, review counts, prime status,
product URLs, and thumbnail images. A user interface built with Streamlit clearly presents these
search results, facilitating easy review and interaction for users.
**Timeline:** Completed
**Success Criteria**
The MVP successfully provides relevant products based on clear and accurately parsed user
queries, demonstrating basic functionality and usability. Additionally, it includes basic anti-bot
measures and handles simple conversational refinements.

## V1 (Backend Improvements)

In V1, the primary focus will be enhancing the backend for improved performance, scalability,
and reliability. Optimized query processing will significantly reduce response latency, ensuring
quicker results for users. Enhanced natural language processing capabilities will enable the
agent to accurately interpret and handle more complex and detailed user queries. Robust traffic
management strategies will accommodate a higher volume of concurrent users without service
degradation. Additionally, essential data logging and storage mechanisms will be implemented
to facilitate effective analytics, performance monitoring, and future enhancements.
**Timeline:** ~2 weeks
**Dependencies**
Implementation success depends on setting up robust backend infrastructure capable of
supporting increased user traffic and data management.
**Critical Path Items**
The critical item for V1 is the optimization of query handling for improved performance and
scalability.
**Technical Risks**


Primary technical risks include potential detection by Amazon’s anti-bot measures and scraping
rate limitations.
**Contingency Plan**
If scraping encounters significant issues, additional bot-evasion tactics such as increased
randomization, proxy rotation, or headless browser alternatives will be employed to maintain
continuous service availability.
**Testing and Validation**
Improvements will be validated through comprehensive load testing simulating high user
volumes, tracking query response performance, and ensuring a minimum 50% reduction in
latency compared to the MVP.
**Success Criteria**
Success criteria will include measurable improvements in query response times, increased
handling of complex queries, stable web scraping performance without disruptions, and
demonstrable scalability and robustness in high-traffic scenarios.

## V2 (Frontend & Backend Enhancements)

**Frontend Enhancements**
Frontend improvements will focus on creating a more intuitive and engaging conversational
interface. Results will dynamically update beside the conversation, significantly reducing
scrolling and enhancing usability. Users will benefit from personalized features, including saving
search histories and receiving proactive product recommendations based on previous
interactions. Introducing product price history tracking will further enrich the user experience,
providing valuable insights and boosting satisfaction.
**Backend Enhancements**
Backend enhancements will introduce advanced NLP capabilities using modern solutions like
OpenAI's GPT models or open-source alternatives from Hugging Face. These improvements
will handle more nuanced queries, allowing the agent to understand context better and respond
effectively to complex user requests. Additionally, the backend will facilitate comparisons of
product listings across multiple e-commerce sites (e.g., Amazon and Walmart), aiding informed
decision-making. Enhanced user history management will utilize data analytics for
personalization, anticipating user preferences and improving overall engagement.


A practical personalization example would be recognizing common first-use scenarios, such as
shopping for everyday household items or frequently purchased categories, to immediately tailor
recommendations and save users time.
**Estimated Timeline**
Version 2 enhancements are projected to take approximately 2-4 weeks and can be executed
concurrently between frontend and backend teams. Regular synchronization checkpoints and
comprehensive end-to-end testing will ensure feature compatibility throughout the development
process.
**Dependencies**
Dependencies include the selection and integration of an NLP solution (OpenAI or Hugging
Face), the development of reliable web-scraping for multi-site data retrieval, and scaling
infrastructure to accommodate the additional computational requirements of advanced NLP.
**Critical Path Items**
The critical path encompasses NLP model integration and testing, essential UI/UX
improvements, and establishing robust user data management systems. Multi-site comparisons
will be considered a stretch goal and addressed in a subsequent development phase or if
resources and time permit.
**Technical Risks**
Technical risks include increased computational overhead from advanced NLP processing,
potential API rate limits from third-party services, and the challenge of maintaining consistent
data quality.
**Contingency Plan**
NLP implementation will be completed in phases. Starting with basic improvements to more
advanced capabilities to help manage complexity and mitigate risks. Infrastructure scaling and
caching mechanisms will handle computational demands effectively, and fallback solutions,
such as simpler query handling and cached responses, will ensure consistent service
availability.
**Success Criteria**
Success criteria include measurable improvements in user engagement metrics, such as
increased session duration, higher retention and revisit rates, positive user feedback on
enhanced usability and recommendations, and reliable functionality of personalized
recommendations and advanced query handling.


## Resource Planning

**Team Composition**
The project will require 1-2 engineers to implement backend and frontend enhancements.
Additionally, a UI/UX designer will support frontend improvements, particularly to refine user
interaction flows. Engineers will act as product engineers, managing development, feature
prioritization, and basic project management tasks. All team members will participate in testing
phases.
**External Dependencies**
● Access to third-party NLP APIs (such as OpenAI's GPT models) or integration with
open-source NLP solutions (e.g., Hugging Face).
● Potential future integration with the Amazon Product API.
**Infrastructure Requirements**
● MVP/V1: Simple cloud hosting solution like Dokku, without the need for database
integration.
● V2: Scalable hosting and database integration (Postgres or similar) to manage user
data, preferences, and product history.
**Cost Estimates**
● MVP/V1: Approximately $20-50 per month utilizing simple cloud hosting solutions.
● V2: Anticipated costs of $100-200 per month, including scalable hosting and database
expenses.
To minimize costs, lightweight cloud hosting platforms like Dokku will be leveraged initially,
alongside open-source NLP solutions such as Hugging Face to reduce reliance on paid APIs.
Scaling resources incrementally based on actual usage will further control infrastructure
expenses.
**Technical Debt Considerations**
Initial reliance on regex-based parsing will require replacement or significant enhancement with
advanced NLP in V2. Additionally, manual data scraping introduces maintenance overhead and
fragility, requiring a future transition to robust, API-driven integrations to ensure long-term
stability.


# Agent Architecture

**Current MVP Architecture**
The current MVP employs basic regex parsing to handle natural language queries, including
limited continuous conversational capabilities. It utilizes Selenium web scraping to retrieve
product data from Amazon. The interface, built with Streamlit, provides straightforward query
submission and displays product results in a simple and accessible manner.
**Autonomy & Decision Making**
Building upon this foundation, the agent will integrate advanced NLP and ML models, such as
OpenAI’s GPT or Hugging Face models, to more accurately predict user intent and dynamically
interpret complex queries. Continuous learning from user interactions and feedback will enable
the agent to refine search accuracy automatically, anticipate user needs, and provide
increasingly relevant recommendations.
**Complex Scenarios**
Enhancing the MVP’s conversational capabilities, the architecture will handle advanced
multi-step interactions and detailed conversational refinements (e.g., subsequent queries like
"cheaper options"). It will robustly maintain conversational context across multiple user inputs,
offering sophisticated filtering based on dynamic product attributes and generating tailored
recommendations derived from aggregated user behaviors, effectively managing intricate
shopping scenarios.
**Context & Personalization**
To extend personalization, the system will incorporate secure third-party login integrations, such
as Google OAuth, to facilitate user account management. User preferences, search histories,
and frequently used queries will be securely stored in a backend database using hashing and
encryption. The architecture will adopt a hybrid storage model, caching frequently accessed
non-sensitive data client-side for improved responsiveness, while maintaining sensitive data
securely on the server-side to ensure privacy and data security.

# Evaluation & Testing

**Measuring Helpfulness**
We will create user personas to simulate realistic shopping scenarios and evaluate agent
effectiveness. Engagement metrics such as revisit rates and on-site interaction will help gauge
user satisfaction. Brief pop-up surveys integrated within the UI will collect immediate user
feedback efficiently.


**Evaluating Quality**
Quality assessments will include accuracy of query results, response speed, user retention, and
user growth. Regular metric analysis will support continuous enhancements.
**User Feedback**
Immediate feedback prompts will capture quick user impressions, supplemented by targeted
in-app notifications at key engagement milestones. This method ensures relevant feedback
while minimally disrupting user experiences.
**Debugging & Testing**
We will use automatic error detection with alerts for quick issue resolution. Systems will feature
auto-generated error reports, instantaneous pod restarts, and automated retries (2-3 attempts)
before user-facing errors. Unit tests and automated testing will be implemented using
open-source tools such as PyTest and Selenium to keep costs minimal.

# Key Challenges & Solutions

**Anti-Bot Measures**
We will enhance existing measures, including randomized user-agent rotation, varied request
delays, and low-cost proxy services to further reduce detection risks and maintain reliable
scraping operations.
**Scaling**
Resource management will involve efficient load balancing and auto-scaling solutions,
dynamically adjusting server capacity in response to user demand, optimizing both performance
and cost-effectiveness.
**Data Changes**
Scheduled scraping combined with real-time checks during high-demand periods and historical
data analysis will help maintain data accuracy, ensuring consistent and valuable user
experiences.
**Rate Limiting**
Clearly communicated UI cool-down periods and proactive logging of rate-limit events will
effectively manage user expectations and inform scaling decisions to preempt service
disruptions.


**Ambiguous Requests**
The agent will actively engage users through targeted clarification prompts to refine unclear or
broad queries, delivering precise and relevant search results.

# Future Improvements

**1. Price Matching and Cross-Site Comparisons**
    Allow users to quickly check if products are cheaper or better-rated on competitor
    websites (e.g., Walmart, Target), ensuring optimal purchasing decisions.
**2. One-Click Purchasing Integration**
    Seamlessly integrate Amazon user accounts to enable fast, secure, one-click purchasing
    directly through the agent, significantly streamlining the shopping experience.
**3. Direct Amazon API Integration**
    Transition from current web-scraping techniques to robust, API-driven data retrieval,
    enhancing reliability, accuracy, reducing downtime risks, and improving response times.
**4. Performance Optimization**
    Regularly audit and enhance infrastructure and NLP components to efficiently handle
    increased traffic and consistently maintain rapid response times.
**5. Direct Product Input and "Dupe" Recommendations**
    Allow users to input specific products (e.g., via URLs) and receive recommendations for
    comparable or more affordable alternatives available on Amazon.
**6. Curated Thematic Collections**
    Offer pre-built, curated product lists organized by popular themes or occasions (e.g.,
    "Back to School Essentials," "Home Office Setup"), enhancing convenience and
    simplifying shopping decisions.
------------------------------------------------ End of Document —-----------------------------------------------
