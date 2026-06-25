# RecruitVerse Architecture

```mermaid
flowchart TD
    A[Recruiter] --> B[Streamlit Login Page]
    B --> C[Authentication Module]
    C --> D[Protected Dashboard]

    D --> E[Resume Upload]
    E --> F[PDF Parser]
    F --> G[Skill Extractor]
    G --> H[Matching Engine]
    H --> I[Ranking Engine]
    I --> J[Explainability Module]
    J --> K[Analytics / Reports]

    C --> L[FastAPI Backend]
    D --> L
    L --> M[PostgreSQL Database]

    N[Docker Compose] --> L
    N --> M
