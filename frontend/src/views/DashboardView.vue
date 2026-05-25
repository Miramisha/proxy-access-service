<template>
  <div>
    <div
      v-if="notify"
      class="notify"
    >
      {{ notify }}
    </div>

    <div
      v-if="loading"
      class="loader"
    >
      Загрузка...
    </div>

    <div
      v-else
      class="dashboard"
    >
      <div class="card">
        <h1>Личный кабинет</h1>

        <p><b>Email:</b> {{ user.email }}</p>
        <p><b>Active:</b> {{ user.is_active }}</p>

        <p>
          <b>Activation key:</b>
          {{ user.activation_key || "Ключ отсутствует" }}
        </p>

        <p>
          <b>Connection status:</b>

          <span
            :class="[
              'status',
              connectionStatus
            ]"
          >
            {{ connectionStatus }}
          </span>
        </p>

        <div
          v-if="vmInfo"
          class="vm-card"
        >
          <p><b>Current VM:</b> {{ vmInfo.host }}:{{ vmInfo.port }}</p>
          <p><b>Protocol:</b> {{ vmInfo.protocol }}</p>
        </div>

        <h3>Ваши VM</h3>

        <div
          v-if="vms.length === 0"
          class="empty"
        >
          VM не найдены
        </div>

        <div
          v-for="vm in vms"
          :key="vm.id"
          class="vm-card"
        >
          <p><b>Name:</b> {{ vm.name }}</p>
          <p><b>Host:</b> {{ vm.host }}</p>
          <p><b>Port:</b> {{ vm.port }}</p>
          <p><b>Protocol:</b> {{ vm.protocol }}</p>

          <p>
            <b>Status:</b>

            <span
              :class="[
                'status',
                vm.current_user_id ? 'busy' : 'free'
              ]"
            >
              {{ vm.current_user_id ? "занята" : "свободна" }}
            </span>
          </p>
        </div>

        <button @click="refreshKey">
          Обновить ключ
        </button>

        <h3>Смена пароля</h3>

        <input
          v-model="oldPassword"
          type="password"
          placeholder="Старый пароль"
        />

        <input
          v-model="newPassword"
          type="password"
          placeholder="Новый пароль"
        />

        <input
          v-model="confirmPassword"
          type="password"
          placeholder="Повторите пароль"
        />

        <button @click="changePassword">
          Изменить пароль
        </button>

        <button
          class="logout"
          @click="logout"
        >
          Выйти
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import {
  ref,
  onMounted,
  onBeforeUnmount
} from "vue"

import { useRouter } from "vue-router"

import api from "../api/client"


const router = useRouter()

const user = ref({})
const vms = ref([])

const oldPassword = ref("")
const newPassword = ref("")
const confirmPassword = ref("")

const connectionStatus = ref("waiting")
const vmInfo = ref(null)

const loading = ref(true)
const notify = ref("")

let socket = null


function showNotify(message) {
  notify.value = message

  setTimeout(() => {
    notify.value = ""
  }, 3000)
}


async function loadUser() {
  const response = await api.get("/users/me")
  user.value = response.data
}


async function loadVMs() {
  try {
    const response = await api.get("/vms/")
    vms.value = response.data
  } catch (err) {
    console.log(err.response?.data || err)
  }
}


function connectWebSocket() {
  if (!user.value.id) {
    return
  }

  socket = new WebSocket(
    `ws://127.0.0.1:8000/ws/status/${user.value.id}`
  )

  socket.onmessage = (event) => {
    const data = JSON.parse(event.data)

    connectionStatus.value = data.status

    if (data.status === "connected") {
      vmInfo.value = {
        host: data.host,
        port: data.port,
        protocol: data.protocol
      }
    } else {
      vmInfo.value = null
    }
  }

  socket.onerror = () => {
    connectionStatus.value = "error"
  }

  socket.onclose = () => {
    connectionStatus.value = "disconnected"
  }
}


async function refreshKey() {
  try {
    const response = await api.post("/keys/refresh")

    user.value.activation_key =
      response.data.activation_key

    showNotify("Новый ключ создан")
  } catch (err) {
    showNotify("Ошибка обновления ключа")
    console.log(err.response?.data || err)
  }
}


async function changePassword() {
  try {
    await api.post(
      "/users/change-password",
      {
        old_password: oldPassword.value,
        new_password: newPassword.value,
        new_password_confirm: confirmPassword.value
      }
    )

    showNotify("Пароль изменён")

    oldPassword.value = ""
    newPassword.value = ""
    confirmPassword.value = ""
  } catch (err) {
    showNotify("Ошибка смены пароля")
    console.log(err.response?.data || err)
  }
}


function logout() {
  localStorage.removeItem("token")

  if (socket) {
    socket.close()
  }

  router.push("/")
}


onMounted(async () => {
  await loadUser()
  await loadVMs()
  connectWebSocket()

  loading.value = false
})


onBeforeUnmount(() => {
  if (socket) {
    socket.close()
  }
})
</script>

<style scoped>
.dashboard {
  min-height: 100vh;
  display: flex;
  justify-content: center;
  padding: 80px 20px;
  background: #f5f5f5;
}

.card {
  width: 520px;
  padding: 40px;
  background: white;
  border-radius: 20px;
  box-shadow: 0 0 20px rgba(0,0,0,.08);
}

.vm-card {
  padding: 15px;
  border: 1px solid #ddd;
  border-radius: 10px;
  margin-bottom: 12px;
  background: #fafafa;
}

.empty {
  padding: 15px;
  border-radius: 10px;
  background: #f1f1f1;
  margin-bottom: 12px;
  color: #555;
}

input {
  display: block;
  width: 100%;
  padding: 12px;
  margin-top: 10px;
  border-radius: 8px;
  border: 1px solid #ddd;
  box-sizing: border-box;
}

button {
  width: 100%;
  margin-top: 15px;
  padding: 12px;
  border: none;
  border-radius: 8px;
  background: #ff5555;
  color: white;
  font-weight: bold;
  cursor: pointer;
}

button:hover {
  background: red;
}

.logout {
  background: #333;
}

.logout:hover {
  background: #000;
}

.status {
  display: inline-block;
  padding: 4px 10px;
  border-radius: 20px;
  font-size: 13px;
  font-weight: bold;
}

.connected,
.free {
  background: #e8fff0;
  color: green;
}

.disconnected,
.busy,
.error {
  background: #ffe8e8;
  color: red;
}

.waiting {
  background: #fff4d6;
  color: orange;
}

.loader {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  font-size: 30px;
  font-weight: bold;
}

.notify {
  position: fixed;
  top: 20px;
  right: 20px;
  padding: 15px 25px;
  background: #333;
  color: white;
  border-radius: 10px;
  z-index: 999;
  animation: fade .3s;
}

@keyframes fade {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }

  to {
    opacity: 1;
    transform: none;
  }
}
</style>