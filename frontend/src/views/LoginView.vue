<template>
  <div class="login-page">
    <div class="card login-card">
      <h1>AI Knowledge Assistant</h1>
      <p class="subtitle">Sign in to chat with your documents.</p>

      <button class="btn login-btn" :disabled="loading" @click="handleLogin">
        {{ loading ? "Signing in..." : "Login as Demo User" }}
      </button>

      <p v-if="error" class="error-text">{{ error }}</p>

      <p class="hint">
        This is a portfolio demo &mdash; the backend issues a JWT for a single
        demo account, no password required.
      </p>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue"
import { useRouter } from "vue-router"
import { useAuth } from "@/composables/useAuth"

const router = useRouter()
const { login } = useAuth()

const loading = ref(false)
const error = ref("")

async function handleLogin() {
  loading.value = true
  error.value = ""

  try {
    await login()
    router.push({ name: "chat" })
  } catch (err) {
    error.value = "Could not sign in. Is the API server running?"
    console.error(err)
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.login-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
}

.login-card {
  width: 100%;
  max-width: 380px;
  padding: 32px;
  text-align: center;
}

.login-card h1 {
  margin: 0 0 8px;
  font-size: 1.4rem;
}

.subtitle {
  margin: 0 0 24px;
  color: var(--color-text-muted);
  font-size: 0.95rem;
}

.login-btn {
  width: 100%;
}

.hint {
  margin-top: 20px;
  font-size: 0.8rem;
  color: var(--color-text-muted);
}
</style>
