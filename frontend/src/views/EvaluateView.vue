<template>
  <div class="page">
    <div class="page-header">
      <h1>Evaluation Suite</h1>
      <p>
        Runs a fixed set of test questions through the live RAG pipeline and
        automatically checks whether the expected fact actually appears in the
        model's answer &mdash; no hardcoded results.
      </p>
    </div>

    <div class="card run-bar">
      <div v-if="hasRun" class="summary">
        <span class="summary-count" :class="allPassed ? 'pass' : 'fail'">
          {{ passedCount }}/{{ results.length }} passed
        </span>
        <span class="summary-label">last run just now</span>
      </div>
      <span v-else class="summary-label">No run yet.</span>

      <button class="btn" :disabled="loading" @click="runEvaluation">
        {{ loading ? "Running..." : "Run Evaluation" }}
      </button>
    </div>

    <p v-if="error" class="error-text">{{ error }}</p>

    <div v-if="results.length > 0" class="cases">
      <div v-for="(result, index) in results" :key="index" class="card case-item">
        <div class="case-head">
          <span class="badge" :class="result.passed ? 'badge-pass' : 'badge-fail'">
            {{ result.passed ? "PASS" : "FAIL" }}
          </span>
          <span class="question">{{ result.question }}</span>
        </div>

        <div class="case-row">
          <span class="row-label">Expected to contain</span>
          <code class="expected">{{ result.expected }}</code>
        </div>

        <div class="case-row">
          <span class="row-label">Actual answer</span>
          <p class="actual">{{ result.actual_answer }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from "vue"
import api from "@/services/api"

const loading = ref(false)
const error = ref("")
const hasRun = ref(false)
const results = ref([])

const passedCount = computed(
  () => results.value.filter((result) => result.passed).length,
)
const allPassed = computed(
  () => results.value.length > 0 && passedCount.value === results.value.length,
)

async function runEvaluation() {
  loading.value = true
  error.value = ""

  try {
    const response = await api.get("/evaluate")
    results.value = response.data
    hasRun.value = true
  } catch (err) {
    error.value = "Evaluation failed. Is the API server running?"
    console.error(err)
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.run-bar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
  padding: 16px 20px;
  margin-bottom: 20px;
}

.summary {
  display: flex;
  align-items: center;
  gap: 10px;
}

.summary-count {
  font-weight: 700;
  font-size: 1rem;
}

.summary-count.pass {
  color: var(--color-success);
}

.summary-count.fail {
  color: var(--color-danger);
}

.summary-label {
  color: var(--color-text-muted);
  font-size: 0.85rem;
}

.cases {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.case-item {
  padding: 18px 20px;
}

.case-head {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 12px;
}

.question {
  font-weight: 600;
  font-size: 0.95rem;
}

.badge-pass {
  background: rgba(22, 163, 74, 0.15);
  color: var(--color-success);
}

.badge-fail {
  background: rgba(220, 38, 38, 0.15);
  color: var(--color-danger);
}

.case-row {
  margin-bottom: 10px;
}

.case-row:last-child {
  margin-bottom: 0;
}

.row-label {
  display: block;
  font-size: 0.7rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.03em;
  color: var(--color-text-muted);
  margin-bottom: 4px;
}

.expected {
  background: var(--color-bg);
  padding: 2px 8px;
  border-radius: 4px;
  font-size: 0.85rem;
}

.actual {
  margin: 0;
  font-size: 0.9rem;
  line-height: 1.5;
}
</style>
