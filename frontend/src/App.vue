<template>
  <div class="app-shell">
    <NavBar v-if="isAuthenticated()" />
    <main>
      <router-view />
    </main>
  </div>
</template>

<script setup>
import NavBar from "@/components/NavBar.vue"
import { useAuth } from "@/composables/useAuth"

const { isAuthenticated } = useAuth()
</script>

<style scoped>
.app-shell {
  min-height: 100vh;
}
</style>
