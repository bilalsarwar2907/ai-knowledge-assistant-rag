<template>
  <div class="page">
    <div class="page-header">
      <h1>Documents</h1>
      <p>Ingest source documents into the vector store and inspect what's stored.</p>
    </div>

    <div class="card actions">
      <div class="action">
        <div>
          <strong>Company policy (.txt)</strong>
          <p>Embed <code>documents/company_policy.txt</code> as a single chunk.</p>
        </div>
        <button class="btn" :disabled="loadingDocs" @click="loadDocs">
          {{ loadingDocs ? "Loading..." : "Load Text Doc" }}
        </button>
      </div>

      <div class="action">
        <div>
          <strong>PDF documents</strong>
          <p>Extract, chunk, and embed every PDF in the <code>documents/</code> folder.</p>
        </div>
        <button class="btn" :disabled="loadingPdfs" @click="loadPdfs">
          {{ loadingPdfs ? "Loading..." : "Load PDFs" }}
        </button>
      </div>

      <p v-if="statusMessage" class="status">{{ statusMessage }}</p>
      <p v-if="error" class="error-text">{{ error }}</p>
    </div>

    <div class="card stats">
      <div>
        <span class="stat-value">{{ count }}</span>
        <span class="stat-label">chunks stored</span>
      </div>
      <button class="btn btn-secondary" :disabled="loadingList" @click="refresh">
        {{ loadingList ? "Refreshing..." : "Refresh" }}
      </button>
    </div>

    <div class="card doc-list">
      <p v-if="documents.length === 0" class="empty">No documents stored yet.</p>

      <div v-for="(doc, index) in documents" :key="doc.id ?? index" class="doc-item">
        <span class="doc-id">{{ doc.id }}</span>
        <p class="doc-text">{{ truncate(doc.text) }}</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue"
import api from "@/services/api"

const loadingDocs = ref(false)
const loadingPdfs = ref(false)
const loadingList = ref(false)
const statusMessage = ref("")
const error = ref("")
const count = ref(0)
const documents = ref([])

function truncate(text, length = 220) {
  if (!text) return ""
  return text.length > length ? `${text.slice(0, length)}...` : text
}

async function loadDocs() {
  loadingDocs.value = true
  error.value = ""
  statusMessage.value = ""

  try {
    const response = await api.get("/load-docs")
    statusMessage.value = response.data.message
    await refresh()
  } catch (err) {
    error.value = "Failed to load the text document."
    console.error(err)
  } finally {
    loadingDocs.value = false
  }
}

async function loadPdfs() {
  loadingPdfs.value = true
  error.value = ""
  statusMessage.value = ""

  try {
    const response = await api.get("/load-pdfs")
    statusMessage.value = `Loaded ${response.data.loaded_chunks} chunk(s) from PDFs.`
    await refresh()
  } catch (err) {
    error.value = "Failed to load PDFs."
    console.error(err)
  } finally {
    loadingPdfs.value = false
  }
}

async function refresh() {
  loadingList.value = true
  error.value = ""

  try {
    const [countResponse, docsResponse] = await Promise.all([
      api.get("/count"),
      api.get("/all-docs"),
    ])

    count.value = countResponse.data.count

    const ids = docsResponse.data.ids ?? []
    const texts = docsResponse.data.documents ?? []
    documents.value = ids.map((id, index) => ({ id, text: texts[index] }))
  } catch (err) {
    error.value = "Failed to load document list."
    console.error(err)
  } finally {
    loadingList.value = false
  }
}

onMounted(refresh)
</script>

<style scoped>
.actions {
  padding: 20px;
  margin-bottom: 20px;
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.action {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
}

.action p {
  margin: 4px 0 0;
  color: var(--color-text-muted);
  font-size: 0.85rem;
}

.action code {
  background: var(--color-bg);
  padding: 1px 6px;
  border-radius: 4px;
  font-size: 0.85em;
}

.status {
  margin: 0;
  font-size: 0.85rem;
  color: var(--color-success);
}

.stats {
  padding: 16px 20px;
  margin-bottom: 20px;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.stat-value {
  font-size: 1.6rem;
  font-weight: 700;
  margin-right: 8px;
}

.stat-label {
  color: var(--color-text-muted);
  font-size: 0.85rem;
}

.doc-list {
  padding: 8px 20px;
}

.empty {
  color: var(--color-text-muted);
  font-size: 0.9rem;
  padding: 12px 0;
}

.doc-item {
  padding: 14px 0;
  border-bottom: 1px solid var(--color-border);
}

.doc-item:last-child {
  border-bottom: none;
}

.doc-id {
  font-size: 0.75rem;
  font-weight: 700;
  color: var(--color-text-muted);
  text-transform: uppercase;
  letter-spacing: 0.03em;
}

.doc-text {
  margin: 6px 0 0;
  font-size: 0.9rem;
  line-height: 1.5;
}
</style>
