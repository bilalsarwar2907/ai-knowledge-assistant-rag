<template>
  <header class="navbar">
    <div class="navbar-inner">
      <span class="brand">AI Knowledge Assistant</span>

      <nav class="links">
        <router-link to="/" class="link">Chat</router-link>
        <router-link to="/agent" class="link">Agent</router-link>
        <router-link to="/documents" class="link">Documents</router-link>
        <router-link to="/search" class="link">Search</router-link>
      </nav>

      <div class="user">
        <span class="username">{{ username }}</span>
        <button class="btn btn-secondary" @click="handleLogout">Logout</button>
      </div>
    </div>
  </header>
</template>

<script setup>
import { useRouter } from "vue-router"
import { useAuth } from "@/composables/useAuth"

const router = useRouter()
const { username, logout } = useAuth()

function handleLogout() {
  logout()
  router.push({ name: "login" })
}
</script>

<style scoped>
.navbar {
  border-bottom: 1px solid var(--color-border);
  background: var(--color-surface);
  position: sticky;
  top: 0;
  z-index: 10;
}

.navbar-inner {
  max-width: 860px;
  margin: 0 auto;
  padding: 14px 20px;
  display: flex;
  align-items: center;
  gap: 24px;
}

.brand {
  font-weight: 700;
  white-space: nowrap;
}

.links {
  display: flex;
  gap: 4px;
  flex: 1;
}

.link {
  padding: 8px 12px;
  border-radius: var(--radius);
  color: var(--color-text-muted);
  text-decoration: none;
  font-size: 0.9rem;
  font-weight: 600;
}

.link:hover {
  background: var(--color-bg);
  color: var(--color-text);
}

.link.router-link-exact-active {
  background: rgba(79, 70, 229, 0.12);
  color: var(--color-primary);
}

.user {
  display: flex;
  align-items: center;
  gap: 10px;
}

.username {
  font-size: 0.85rem;
  color: var(--color-text-muted);
}

@media (max-width: 640px) {
  .navbar-inner {
    flex-wrap: wrap;
    gap: 10px;
  }

  .links {
    order: 3;
    width: 100%;
  }
}
</style>
