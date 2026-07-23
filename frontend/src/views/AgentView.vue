<template>
  <div class="page">
    <div class="page-header">
      <h1>Smart Agent</h1>
      <p>
        The backend decides per-question whether to answer directly with GPT
        or fall back to document retrieval (RAG).
      </p>
    </div>

    <div class="card chat-window">
      <div class="messages">
        <p v-if="history.length === 0" class="empty">
          No messages yet &mdash; ask something below.
        </p>

        <ChatMessage
          v-for="(chat, index) in history"
          :key="index"
          :question="chat.question"
          :answer="chat.answer"
          :badge="chat.decision"
        />

        <p v-if="loading" class="thinking">Thinking...</p>
        <p v-if="error" class="error-text">{{ error }}</p>

        <div ref="conversationEnd"></div>
      </div>

      <form class="composer" @submit.prevent="askAgent">
        <input
          v-model="question"
          type="text"
          placeholder="Ask the agent anything..."
          :disabled="loading"
        />
        <button class="btn" type="submit" :disabled="loading || !question.trim()">
          Send
        </button>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, nextTick } from "vue"
import api from "@/services/api"
import ChatMessage from "@/components/ChatMessage.vue"

const question = ref("")
const loading = ref(false)
const error = ref("")
const history = ref([])
const conversationEnd = ref(null)

async function askAgent() {
  if (!question.value.trim()) return

  const askedQuestion = question.value
  loading.value = true
  error.value = ""

  try {
    const response = await api.get("/agent", {
      params: { question: askedQuestion },
    })

    history.value.push({
      question: askedQuestion,
      answer: response.data.answer ?? response.data.error,
      decision: response.data.agent_decision,
    })

    question.value = ""
    await nextTick()
    conversationEnd.value?.scrollIntoView({ behavior: "smooth" })
  } catch (err) {
    error.value = "Something went wrong. Please try again."
    console.error(err)
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.chat-window {
  display: flex;
  flex-direction: column;
  height: 60vh;
  overflow: hidden;
}

.messages {
  flex: 1;
  overflow-y: auto;
  padding: 20px;
}

.empty {
  color: var(--color-text-muted);
  font-size: 0.9rem;
}

.thinking {
  color: var(--color-text-muted);
  font-style: italic;
  font-size: 0.9rem;
}

.composer {
  display: flex;
  gap: 10px;
  padding: 16px 20px;
  border-top: 1px solid var(--color-border);
}

.composer input {
  flex: 1;
}
</style>
