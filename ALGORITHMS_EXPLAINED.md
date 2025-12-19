# Algorithms Explained: DFS & K-Means in AI Study Assistant

## Overview
This project implements two key algorithms from your "Introduction to AI" course:
1. **DFS (Depth-First Search)** - Extract and structure concepts
2. **K-Means Clustering** - Group similar topics for learning

---

## 1. Gemini API Response Format

### What Gemini Returns
When you upload a PDF/PPTX, Gemini generates a **structured summary in Markdown format**:

```
## Machine Learning
- Definition: A subset of AI...
- Types: Supervised, Unsupervised, Reinforcement

### Supervised Learning
- Uses labeled data
- Examples: Classification, Regression

### Unsupervised Learning
- Uses unlabeled data
- Examples: Clustering, Dimensionality Reduction
```

This is **plain text with Markdown headers** (#, ##, ###).

---

## 2. DFS Algorithm - How It Works

### What is DFS?
DFS traverses a tree/graph by going **as deep as possible** before backtracking. In our case, it extracts concepts from the Markdown summary.

### Step-by-Step Process

```
Input Summary (Markdown text):
"## Machine Learning
- Supervised Learning
  - Classification
  - Regression
- Unsupervised Learning
  - Clustering
  - Dimensionality Reduction"

↓ DFS Extraction ↓

Output Hierarchy:
{
  "Machine Learning": [
    "Supervised Learning",
    "Unsupervised Learning"
  ],
  "Supervised Learning": [
    "Classification",
    "Regression"
  ],
  "Unsupervised Learning": [
    "Clustering",
    "Dimensionality Reduction"
  ]
}
```

### Code Implementation
```python
def dfs_extract_concepts(text: str) -> Dict[str, List[str]]:
    lines = text.split('\n')
    concepts = {}
    current_parent = None
    
    for line in lines:
        if line.startswith('###'):
            concept = line.replace('###', '').strip()
            concepts[concept] = []
            current_parent = concept
        elif current_parent and (line.startswith('- ') or line.startswith('* ')):
            subconcept = line.replace('- ', '').strip()
            concepts[current_parent].append(subconcept)
    
    return concepts
```

### Complexity
- **Time**: O(n) where n = number of lines
- **Space**: O(m) where m = number of unique concepts

### Real Output Example
When you upload a summary, DFS extracts:
- Main topics
- Subtopics under each
- Difficulty level based on depth

You see this in the UI under **"Summary Structure Analysis (DFS)"**

---

## 3. K-Means Clustering - How It Works

### What is K-Means?
K-Means groups similar items into **K clusters** based on feature similarity. We use K=3 for Easy, Medium, Hard difficulty levels.

### Step-by-Step Process

```
Input: List of topic names
["Machine Learning", "Classification", "Deep Learning", 
 "Neural Networks", "Linear Regression", "Clustering"]

↓ TF-IDF Vectorization ↓
Convert text to numerical vectors

TF-IDF = Term Frequency - Inverse Document Frequency
- Assigns weight to each word
- Common words = lower weight
- Unique words = higher weight

Example:
"Machine Learning" → [0.45, 0.52, 0.12, ...]
"Deep Learning" → [0.38, 0.58, 0.18, ...]
"Linear Regression" → [0.22, 0.15, 0.68, ...]

↓ K-Means Clustering (K=3) ↓
1. Initialize 3 random centroids
2. Assign each topic to nearest centroid
3. Recalculate centroids
4. Repeat until convergence

Output Clusters:
{
  Cluster 1 (Easy): ["Machine Learning", "Classification"]
  Cluster 2 (Medium): ["Deep Learning", "Neural Networks"]
  Cluster 3 (Hard): ["Linear Regression", "Clustering"]
}
```

### Code Implementation
```python
def cluster_topics_by_similarity(topics: List[Dict]) -> Dict[int, List[str]]:
    topic_names = [t["main"] for t in topics]
    
    # Convert text to numbers
    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(topic_names)
    
    # Apply K-Means with 3 clusters
    kmeans = KMeans(n_clusters=3, random_state=42)
    labels = kmeans.fit_predict(X)
    
    # Group topics by cluster
    clusters = {}
    for idx, label in enumerate(labels):
        if label not in clusters:
            clusters[label] = []
        clusters[label].append(topic_names[idx])
    
    return clusters
```

### How It's Applied to Quiz Generation

1. **Extract topics from summary** (DFS)
2. **Convert topic names to vectors** (TF-IDF)
3. **Group similar topics** (K-Means)
4. **Generate quiz questions** based on clusters
5. **Show grouped results** in UI tabs: Easy | Medium | Hard

### Real Example Flow

```
Gemini Summary (Text)
    ↓
DFS Extract Concepts
    ↓ Topics: [Machine Learning, Supervised Learning, Classification, ...]
    ↓
K-Means Clustering
    ↓ Groups similar topics: {Easy: [...], Medium: [...], Hard: [...]}
    ↓
Generate Quiz
    ↓ Creates questions from each cluster
    ↓
UI Display
    ↓ Shows 3 tabs with grouped topics
```

### Why K-Means?
- **Automatic grouping**: No manual configuration needed
- **Similarity-based**: Groups related topics together
- **Scalable**: Works with any number of topics
- **Educational**: Demonstrates unsupervised learning

### Complexity
- **Time**: O(n * k * i * d) where:
  - n = number of topics
  - k = number of clusters (3)
  - i = iterations to convergence
  - d = dimensions (TF-IDF features)
- **Space**: O(n * d)

---

## 4. How They Work Together in Your App

```
User uploads PDF
    ↓
Gemini generates Markdown summary
    ↓
DFS Algorithm:
  - Parses Markdown structure
  - Extracts main topics & subtopics
  - Builds hierarchy tree
    ↓
K-Means Algorithm:
  - Converts topics to TF-IDF vectors
  - Clusters into 3 groups (by similarity)
  - Maps to Easy/Medium/Hard
    ↓
Quiz Generation:
  - Gemini creates questions for each topic
  - Organized by clusters
    ↓
UI Display:
  - DFS View: Hierarchical tree
  - K-Means View: Grouped tabs
  - Quiz: Progressive difficulty
```

---

## 5. Running the App

```bash
# Activate virtual environment
source venv/bin/activate

# Run the app
streamlit run Dashboard.py
```

### What You'll See

1. **Upload Page** → Upload PDF/PPTX
2. **Create Quiz Page** → Shows:
   - **DFS Section**: Hierarchical concept breakdown
   - **K-Means Section**: Topics grouped by cluster
   - **Quiz**: Generated questions by cluster

---

## 6. Key Takeaways

| Concept | Algorithm | Use Case |
|---------|-----------|----------|
| **Hierarchical Structure** | DFS | Extract nested concepts from text |
| **Similarity Grouping** | K-Means | Organize topics for progressive learning |
| **No Training Data Needed** | Both | Uses your summary directly |
| **Unsupervised Learning** | K-Means | Groups without labels |
| **Depth-First Traversal** | DFS | Explores concept trees |

---

## Dependencies
- `scikit-learn`: For K-Means clustering and TF-IDF vectorization
- `streamlit`: Web UI framework
- `google.genai`: Gemini API for content generation

Install with:
```bash
pip install scikit-learn streamlit google-generativeai
```
