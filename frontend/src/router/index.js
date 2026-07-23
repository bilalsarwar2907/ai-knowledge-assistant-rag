import { createRouter, createWebHistory } from "vue-router"
import { useAuth } from "@/composables/useAuth"

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/login",
      name: "login",
      component: () => import("@/views/LoginView.vue"),
    },
    {
      path: "/",
      name: "chat",
      component: () => import("@/views/ChatView.vue"),
      meta: { requiresAuth: true },
    },
    {
      path: "/agent",
      name: "agent",
      component: () => import("@/views/AgentView.vue"),
      meta: { requiresAuth: true },
    },
    {
      path: "/documents",
      name: "documents",
      component: () => import("@/views/DocumentsView.vue"),
      meta: { requiresAuth: true },
    },
    {
      path: "/search",
      name: "search",
      component: () => import("@/views/SearchView.vue"),
      meta: { requiresAuth: true },
    },
    {
      path: "/evaluate",
      name: "evaluate",
      component: () => import("@/views/EvaluateView.vue"),
      meta: { requiresAuth: true },
    },
  ],
})

router.beforeEach((to) => {
  const { isAuthenticated } = useAuth()

  if (to.meta.requiresAuth && !isAuthenticated()) {
    return { name: "login" }
  }

  if (to.name === "login" && isAuthenticated()) {
    return { name: "chat" }
  }
})

export default router
