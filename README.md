# Consultant's Brain: The Elite SQL Vector Shootout 🚀

This project is the architectural foundation for a high-performance **Retrieval-Augmented Generation (RAG)** system designed for elite Microsoft Data Platform consulting. 

The goal is to benchmark and architect a "Consultant's Brain"—a system capable of storing and retrieving deep technical knowledge using the latest vector search capabilities in the Microsoft ecosystem.

## 🏗️ The Architecture
We are comparing three distinct approaches to vector storage and retrieval to determine the most cost-effective and performant solution for enterprise clients:

1.  **SQL Server 2025 (Native):** Utilizing the new `VECTOR` data type and `DiskANN` indexing for millisecond latency.
2.  **SQL Server 2022 (JSON Hack):** A legacy-compatible approach using `NVARCHAR(MAX)` and custom T-SQL logic to handle embeddings.
3.  **PostgreSQL 17 (pgvector):** The industry-standard "sidecar" database used as a baseline for performance and feature parity.



## 🛠️ Tech Stack
* **Engine:** SQL Server 2025 (latest), SQL Server 2022, PostgreSQL 17 + pgvector.
* **Orchestration:** Docker & Docker Compose.
* **Language:** Python 3.12 (Containerized).
* **Libraries:** `pymssql`, `psycopg2`, `NumPy`, `Faker`.

## 🚀 Getting Started

### Prerequisites
* Docker Desktop
* Git

### Deployment
1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/YOUR_USERNAME/DBA-Vector-Shootout.git](https://github.com/YOUR_USERNAME/DBA-Vector-Shootout.git)
    cd DBA-Vector-Shootout
    ```

2.  **Configure Environment:**
    Create a `.env` file in the root (see `.env.example`) with your `MSSQL_SA_PASSWORD`.

3.  **Launch the Stack:**
    ```bash
    docker-compose up --build
    ```
    The `ingest-engine` will automatically wait for all databases to be healthy before initializing tables and generating 100 synthetic test records.

## 🎯 Project Roadmap
- [x] Dockerized Multi-DB Environment.
- [x] Automated Data Ingestion Engine.
- [ ] Latency Benchmark Shootout (Coming Soon).
- [ ] RAG Integration with OpenAI/Azure OpenAI.
- [ ] Elite Consulting Dashboard.

## 🇧🇷 About the Author
Senior AI Architect and Microsoft Data Platform Mentor specializing in SQL Server performance tuning and modern AI integration. Preparing for **DP-300**, **DP-700**, and **DP-600** certifications.