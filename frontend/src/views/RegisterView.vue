<template>
  <div class="page">
    <div
      v-if="notify"
      class="notify"
    >
      {{ notify }}
    </div>

    <div class="card">
      <h1>Регистрация</h1>

      <input
        v-model="email"
        placeholder="Email"
      />

      <input
        v-model="password"
        type="password"
        placeholder="Пароль"
      />

      <input
        v-model="confirmPassword"
        type="password"
        placeholder="Повторите пароль"
      />

      <button @click="register">
        Зарегистрироваться
      </button>

      <p>
        Уже есть аккаунт?
        <router-link to="/">
          Войти
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
const confirmPassword = ref("")
const notify = ref("")


function showNotify(message) {
  notify.value = message

  setTimeout(() => {
    notify.value = ""
  }, 3000)
}


async function register() {
  if (password.value !== confirmPassword.value) {
    showNotify("Пароли не совпадают")
    return
  }

  try {
    await api.post(
      "/auth/register",
      {
        email: email.value,
        password: password.value,
        password_confirm: confirmPassword.value
      }
    )

    showNotify("Письмо с ключом отправлено на почту")

    setTimeout(() => {
      router.push("/")
    }, 2000)
  } catch (err) {
    showNotify(
      err.response?.data?.error || "Ошибка регистрации"
    )

    console.log(err.response?.data || err)
  }
}
</script>

<style scoped>
.page {
  min-height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  background: #f5f5f5;
}

.card {
  width: 400px;
  padding: 40px;
  background: white;
  border-radius: 20px;
  box-shadow: 0 0 20px rgba(0,0,0,.08);
}

h1 {
  margin-bottom: 30px;
}

input {
  width: 100%;
  padding: 12px;
  margin-bottom: 15px;
  border: 1px solid #ddd;
  border-radius: 8px;
  box-sizing: border-box;
}

button {
  width: 100%;
  padding: 12px;
  border: none;
  border-radius: 8px;
  background: #ff5555;
  color: white;
  cursor: pointer;
  font-weight: bold;
}

button:hover {
  background: red;
}

p {
  margin-top: 20px;
  text-align: center;
}

.notify {
  position: fixed;
  top: 30px;
  right: 30px;
  background: #333;
  color: white;
  padding: 18px 28px;
  border-radius: 12px;
  box-shadow: 0 10px 30px rgba(0,0,0,.15);
  font-weight: 600;
  z-index: 999;
  animation: show .3s ease;
}

@keyframes show {
  from {
    opacity: 0;
    transform: translateY(-20px);
  }

  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>