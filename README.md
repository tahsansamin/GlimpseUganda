# GlimpseUganda 🇺🇬

Glimpse Uganda is a interactive AI-powered tourism assistant platform. It combines a React-based interactive vector map frontend with RAG (Retrieval-Augmented Generation) backend. Visitors can explore locations across Uganda and ask questions about them. I built this app after observing the difference between information online versus the ground reality for many tourist destinations and experiences in Uganda. As a tourist, your first stop for information is the internet, but when the information is not aligned with the ground reality, it creates a fragmented tourism experience.

Through this app I hope to bridge this gap and make tourism in Uganda more accessible. What makes this chatbot unique is that instead of relying on information online it would be based on reliable, up to date documents provided by the park rangers, tour operators, the National Board of Tourism, Uganda Wildlife Authority (UWA) and other verified stakeholders, ensuring accurate up to date information.

Project demo: https://www.youtube.com/watch?v=WOX65yovd8A

Try out the app: https://glimpse-uganda.vercel.app/


## 🌟 Key Features

### 📍 Interactive Vector Map & Location-Aware Chat
* **Sleek Mapping Interface**: A beautiful custom map with elegant teardrop pins marking Uganda's key destinations.
* **Specialized RAG Assistants**: Every destination has a tailored AI companion acting as a local expert, powered by partitioned vector search namespaces.
* **Micro-Animations**: Rich animations, custom hover states, and smooth transition states.

### 🧠 Advanced RAG Architecture (Backend)
* **Namespace Isolation**: Uses **Pinecone** partitioned by namespace for each destination. Queries for a specific location only search the corresponding namespace, ensuring high accuracy and preventing cross-location context leakage.
* **Sentence Transformers**: Generates highly accurate embeddings locally using the `all-MiniLM-L6-V2` model.
* **Cohere Reranking**: Leverages `rerank-english-v3.0` to filter the top 8 vector hits down to the 4 most relevant chunks before sending to the LLM, reducing latency and token usage.
* **Powerful Inference**: Powered by **Groq (Llama-3.3-70b)** for lightning-fast and highly contextual answers.

### 🛡️ Smart Document Processing & Category Verification
* **Supabase Integration**: Documents uploaded to the Supabase storage bucket trigger real-time background processing webhooks (`/transfer_to_pinecone`) that chunk, embed, and index new PDFs/DOCs into Pinecone.
* **AI-Powered Category Verification**: A strict document gatekeeper (`/verify_document`) analyzes uploaded files using PyMuPDF and Groq to calculate if at least **50% of the content** directly focuses on the selected category or location. If a document is generic or off-topic, it is flagged and blocked from indexing.



## ⚙️ Configuration & Environment Variables

Create a `.env` file in the root directory (or individual envs inside `backend` and `frontend` directories):

```env
# Backend API Keys
GROQ_API_KEY=your_groq_api_key_here
PINECONE_KEY=your_pinecone_api_key_here
COHERE_API_KEY=your_cohere_api_key_here
WEBHOOK_SECRET=your_supabase_webhook_shared_secret

# Supabase Configurations (Shared)
VITE_SUPABASE_URL=https://your-supabase-project.supabase.co
VITE_SUPABASE_KEY=your-supabase-anon-or-service-role-key
```

---

## 🚀 Getting Started

### 🔌 Backend Setup (FastAPI)

1. Navigate to the backend folder:
   ```bash
   cd backend
   ```
2. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the development server:
   ```bash
   uvicorn app_main:app --reload --port 8000
   ```

### 💻 Frontend Setup (React + Vite)

1. Navigate to the frontend folder:
   ```bash
   cd frontend
   ```
2. Install the packages:
   ```bash
   npm install
   ```
3. Launch the hot-reloading development server:
   ```bash
   npm run dev
   ```


## 🛠️ Technical Skills & Technologies Demonstrated

This project showcases a wide spectrum of modern full-stack engineering, AI/RAG system design, and cloud integration skills:

### 🤖 Generative AI & Retrieval-Augmented Generation (RAG)
* **Contextual Namespace Partitioning**: Engineered a partitioned vector indexing strategy using **Pinecone** namespaces to prevent cross-location hallucinations.
* **Vector Embeddings**: Leveraged local embedding pipelines with **SentenceTransformers** (`all-MiniLM-L6-V2`).
* **Semantic Reranking**: Integrated **Cohere Rerank** (`rerank-english-v3.0`) for filtering noise, dramatically reducing LLM token consumption and increasing prompt fidelity.
* **Robust Prompt Engineering**: Designed system/human message templates using **LangChain** and structured outputs evaluated against LLM validation gates.

### 🐍 Backend & Data Engineering
* **FastAPI Development**: Built a high-performance asynchronous REST API backend in Python.
* **Smart Data Extraction**: Created parsers for extraction from complex unstructured documents (PDFs/Word) using **PyMuPDF (`fitz`)**.
* **AI Content Guardrails**: Implemented verification algorithms analyzing document topic ratios with structured JSON outputs.

### 💻 Frontend & UI/UX Engineering
* **React Web Applications**: Built a stateful client using React and Vite.


### ☁️ Cloud & DevOps Integration
* **Real-time Synchronization**: Architected a real-time webhooks listener connected directly with **Supabase Storage** events, automatically vectorizing new documents as they are uploaded.
* **Automated Unit Testing**
* **CICD pipelines using GitHub**
