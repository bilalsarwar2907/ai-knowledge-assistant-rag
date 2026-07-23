<template>
  <div class="page">
    <div class="page-header">
      <h1>Search the Vector Store</h1>
      <p>
        See what happens before an answer is generated: your question is turned
        into an embedding, compared against every chunk stored in ChromaDB, and
        ranked by vector similarity.
      </p>
    </div>

    <div class="card pipeline">
      <span class="step">Question</span>
      <span class="arrow">&rarr;</span>
      <span class="step">Embedding Vector</span>
      <span class="arrow">&rarr;</span>
      <span class="step">ChromaDB Nearest-Neighbor Search</span>
      <span class="arrow">&rarr;</span>
      <span class="step">Ranked Matches</span>
    </div>

    <form class="card search-form" @submit.prevent="runSearch">
      <input
        v-model="query"
        type="text"
        placeholder='Try "What is RSI?"'
        :disabled="loading"
      />
      <select v-model.number="topK" :disabled="loading">
        <option :value="3">Top 3</option>
        <option :value="5">Top 5</option>
        <option :value="10">Top 10</option>
      </select>
      <button class="btn" type="submit" :disabled="loading || !query.trim()">
        {{ loading ? "Searching..." : "Search" }}
      </button>
    </form>

    <p v-if="error" class="error-text">{{ error }}</p>

    <div v-if="results.length > 0" class="results">
      <div v-for="result in results" :key="result.id" class="card result-item">
        <div class="result-head">
          <span class="rank">#{{ result.rank }}</span>
          <span class="source">{{ result.id }}</span>
          <span class="score">{{ result.similarityPercent }}% match</span>
        </div>
        <div class="score-bar">
          <div
            class="score-bar-fill"
            :style="{ width: result.similarityPercent + '%' }"
          ></div>
        </div>
        <p class="snippet">{{ result.text }}</p>
        <p class="distance">raw vector distance: {{ result.distance.toFixed(4) }}</p>
      </div>
    </div>

    <p v-else-if="searched && !loading" class="empty">No matches found.</p>
  </div>
</template>

<script setup>
import { ref } from "vue"
import api from "@/services/api"

const query = ref("")
const topK = ref(5)
const loading = ref(false)
const error = ref("")
const searched = ref(false)
const results = ref([])

function toSimilarityPercent(distance) {
  // text-embedding-3-small vectors are unit-normalized, and ChromaDB's default
  // space is squared L2, so squared_L2 = 2 - 2*cosine_similarity.
  const cosineSimilarity = 1 - distance / 2
  return Math.round(Math.max(0, Math.min(1, cosineSimilarity)) * 100)
}

async function runSearch() {
  if (!query.value.trim()) return

  loading.value = true
  error.value = ""
  searched.value = true

  try {
    const response = await api.get("/search", {
      params: { query: query.value, n_results: topK.value },
    })

    const ids = response.data.ids?.[0] ?? []
    const documents = response.data.documents?.[0] ?? []
    const distances = response.data.distances?.[0] ?? []

    results.value = ids.map((id, index) => ({
      id,
      text: documents[index],
      distance: distances[index],
      similarityPercent: toSimilarityPercent(distances[index]),
      rank: index + 1,
    }))
  } catch (err) {
    error.value = "Search failed. Is the API server running?"
    console.error(err)
    results.value = []
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.pipeline {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 10px;
  padding: 16px 20px;
  margin-bottom: 20px;
  font-size: 0.85rem;
}

.step {
  padding: 6px 12px;
  border-radius: 999px;
  background: rgba(79, 70, 229, 0.1);
  color: var(--color-primary);
  font-weight: 600;
  white-space: nowrap;
}

.arrow {
  color: var(--color-text-muted);
}

.search-form {
  display: flex;
  gap: 10px;
  padding: 16px 20px;
  margin-bottom: 20px;
}

.search-form input {
  flex: 1;
}

.search-form select {
  border-radius: var(--radius);
  border: 1px solid var(--color-border);
  background: var(--color-surface);
  color: var(--color-text);
  padding: 0 10px;
}

.results {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.result-item {
  padding: 18px 20px;
}

.result-head {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 8px;
}

.rank {
  font-weight: 700;
  color: var(--color-text-muted);
  font-size: 0.85rem;
}

.source {
  flex: 1;
  font-weight: 600;
  font-size: 0.9rem;
}

.score {
  font-size: 0.8rem;
  font-weight: 700;
  color: var(--color-primary);
}

.score-bar {
  height: 6px;
  border-radius: 999px;
  background: var(--color-bg);
  overflow: hidden;
  margin-bottom: 12px;
}

.score-bar-fill {
  height: 100%;
  background: var(--color-primary);
  border-radius: 999px;
  transition: width 0.3s ease;
}

.snippet {
  margin: 0;
  font-size: 0.9rem;
  line-height: 1.5;
  color: var(--color-text);
}

.distance {
  margin: 10px 0 0;
  font-size: 0.75rem;
  color: var(--color-text-muted);
}

.empty {
  color: var(--color-text-muted);
  font-size: 0.9rem;
}
</style>
