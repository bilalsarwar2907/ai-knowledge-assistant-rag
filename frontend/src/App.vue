<!-- ==========================================================
     AI KNOWLEDGE ASSISTANT UI
     ========================================================== -->

<template>
  <div>

    <!-- ==========================================================
         1. PAGE TITLE
         ========================================================== -->

    <h1>AI Knowledge Assistant</h1>

    <!-- ==========================================================
         2. QUESTION INPUT
         ========================================================== -->

    <input
      v-model="question"
      placeholder="Ask a question..."
    />

    <!-- ==========================================================
         3. SEND BUTTON
         ========================================================== -->

    <button @click="askQuestion">
      Send
    </button>

    <!-- ==========================================================
         4. LOADING MESSAGE
         ========================================================== -->

    <p v-if="loading">
      Thinking...
    </p>

    <!-- ==========================================================
         5. AI RESPONSE
         ========================================================== -->

    <p>
      {{ answer }}
    </p>

  </div>
</template>

<script setup>

// ==========================================================
// 6. IMPORTS
// ==========================================================

import { ref } from "vue"
import axios from "axios"

// ==========================================================
// 7. STATE
// ==========================================================

const question = ref("")
const answer = ref("")
const loading = ref(false)

// ==========================================================
// 8. ASK RAG ENDPOINT
// ==========================================================

async function askQuestion() {
  if (!question.value.trim()) {
  return
}

  try {

    loading.value = true
    answer.value = ""

    const response = await axios.get(
      "http://127.0.0.1:8001/ask-rag",
      {
        params: {
          question: question.value
        }
      }
    )

    answer.value = response.data.answer

  } catch (error) {

    answer.value = "Something went wrong."

    console.error(error)

  } finally {

    loading.value = false

  }

}

</script>

<style>

/* ==========================================================
   9. STYLING
   ========================================================== */

</style>