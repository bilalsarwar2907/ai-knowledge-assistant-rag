import { ref } from "vue"
import api from "@/services/api"

const token = ref(localStorage.getItem("token") || "")
const username = ref(localStorage.getItem("username") || "")

async function login() {
  const response = await api.get("/login")
  const accessToken = response.data.access_token

  const verify = await api.get("/protected", {
    params: { token: accessToken },
  })

  token.value = accessToken
  username.value = verify.data.user

  localStorage.setItem("token", token.value)
  localStorage.setItem("username", username.value)
}

function logout() {
  token.value = ""
  username.value = ""
  localStorage.removeItem("token")
  localStorage.removeItem("username")
}

function isAuthenticated() {
  return !!token.value
}

export function useAuth() {
  return { token, username, login, logout, isAuthenticated }
}
