<template>
  <div class="page">
    <div class="card">
      <h1>Вход</h1>

      <input
        v-model="email"
        placeholder="Email"
      />

      <input
        v-model="password"
        type="password"
        placeholder="Пароль"
      />

      <button @click="login">
        Войти
      </button>

      <p>
        Нет аккаунта?
        <router-link to="/register">
          Зарегистрироваться
        </router-link>
      </p>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue"
import { useRouter } from "vue-router"
import api from "../api/client"

const router = useRouter()

const email = ref("")
const password = ref("")

async function login() {
  try {
    const response = await api.post(
      "/auth/login",
      {
        email: email.value,
        password: password.value
      }
    )

    localStorage.setItem(
      "token",
      response.data.access_token
    )

    router.push("/dashboard")

  } catch (err) {
    alert(
      err.response?.data?.error || "Ошибка входа"
    )
  }
}
</script>

<style scoped>
.page{
min-height:100vh;
display:flex;
justify-content:center;
align-items:center;
background:#f5f5f5;
}

.card {
  width: 380px;
  padding: 40px;
  border-radius: 20px;
  background: white;
  box-shadow: 0 0 25px rgba(0, 0, 0, 0.08);
}

h1 {
  margin-bottom: 25px;
}

input {
  width: 100%;
  padding: 12px;
  margin-bottom: 15px;
  border: 1px solid #ddd;
  border-radius: 8px;
}

button {
width:100%;
padding:12px;
border:none;
border-radius:8px;
background:#ff5555;
color:white;
font-weight:bold;
cursor:pointer;
transition:.2s;
}

button:hover{
background:red;
}

p {
  margin-top: 20px;
  text-align: center;
}
</style>