<template>
  <div class="message-pair">
    <div class="bubble user-message">
      <strong>You</strong>
      <p>{{ question }}</p>
    </div>

    <div class="bubble ai-message">
      <div class="ai-header">
        <strong>Assistant</strong>
        <span v-if="badge" class="badge" :class="badgeClass">{{ badge }}</span>
      </div>
      <p>{{ answer }}</p>
    </div>
  </div>
</template>

<script setup>
import { computed } from "vue"

const props = defineProps({
  question: { type: String, required: true },
  answer: { type: String, required: true },
  badge: { type: String, default: "" },
})

const badgeClass = computed(() =>
  props.badge?.toLowerCase() === "rag" ? "badge-rag" : "badge-gpt",
)
</script>

<style scoped>
.message-pair {
  display: flex;
  flex-direction: column;
  gap: 8px;
  margin-bottom: 16px;
}

.bubble {
  padding: 12px 16px;
  border-radius: var(--radius);
  max-width: 85%;
}

.bubble p {
  margin: 4px 0 0;
  white-space: pre-wrap;
  line-height: 1.5;
}

.bubble strong {
  font-size: 0.75rem;
  text-transform: uppercase;
  letter-spacing: 0.04em;
  color: var(--color-text-muted);
}

.user-message {
  align-self: flex-end;
  background: rgba(79, 70, 229, 0.1);
}

.ai-message {
  align-self: flex-start;
  background: var(--color-surface);
  border: 1px solid var(--color-border);
}

.ai-header {
  display: flex;
  align-items: center;
  gap: 8px;
}
</style>
