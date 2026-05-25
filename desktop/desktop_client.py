"""Минимальное десктопное приложение для подключения по activation key.

Запуск локально:
    pip install -r desktop/requirements.txt
    python desktop/desktop_client.py
"""
from __future__ import annotations

import json
import queue
import threading
import time
import tkinter as tk
from tkinter import messagebox
from urllib import error, request

import websocket

API_URL = "http://127.0.0.1:8000"
WS_URL = "ws://127.0.0.1:8000"


class DesktopClient(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("Proxy Access Client")
        self.geometry("520x340")
        self.resizable(False, False)
        self.queue: queue.Queue[dict] = queue.Queue()
        self.ws_app: websocket.WebSocketApp | None = None

        tk.Label(self, text="Вставьте ваш ключ", font=("Arial", 14)).pack(pady=(24, 8))
        self.key_entry = tk.Entry(self, width=58, show="*")
        self.key_entry.pack(pady=8)

        self.connect_button = tk.Button(self, text="Подключиться", command=self.connect)
        self.connect_button.pack(pady=8)

        self.disconnect_button = tk.Button(self, text="Отключиться", command=self.disconnect, state="disabled")
        self.disconnect_button.pack(pady=4)

        self.status_label = tk.Label(self, text="Статус: ожидание", font=("Arial", 12))
        self.status_label.pack(pady=8)

        self.vm_label = tk.Label(self, text="", justify="left")
        self.vm_label.pack(pady=8)

        self.after(250, self.process_queue)

    def connect(self) -> None:
        key = self.key_entry.get().strip()
        if not key:
            messagebox.showwarning("Ключ", "Введите ключ активации")
            return
        self.status_label.config(text="Статус: ожидание")
        self.connect_button.config(state="disabled")
        threading.Thread(target=self.activate_key, args=(key,), daemon=True).start()

    def activate_key(self, key: str) -> None:
        payload = json.dumps({"activation_key": key}).encode("utf-8")
        req = request.Request(
            f"{API_URL}/api/activate-key",
            data=payload,
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        try:
            with request.urlopen(req, timeout=10) as response:
                data = json.loads(response.read().decode("utf-8"))
            self.queue.put({"type": "connected", "data": data})
            self.start_websocket(data["user_id"])
        except error.HTTPError as exc:
            body = exc.read().decode("utf-8")
            try:
                parsed = json.loads(body)
                detail = parsed.get("error") or parsed.get("detail")
            except Exception:
                detail = body
            self.queue.put({"type": "error", "message": detail})
        except Exception as exc:
            self.queue.put({"type": "error", "message": str(exc)})

    def start_websocket(self, user_id: int) -> None:
        def on_message(_ws, message: str) -> None:
            try:
                self.queue.put({"type": "ws_status", "data": json.loads(message)})
            except json.JSONDecodeError:
                self.queue.put({"type": "ws_status", "data": {"status": message}})

        def on_error(_ws, exc: Exception) -> None:
            self.queue.put({"type": "ws_error", "message": str(exc)})

        def on_close(_ws, *_args) -> None:
            self.queue.put({"type": "ws_status", "data": {"status": "disconnected"}})

        def on_open(ws) -> None:
            def ping_loop() -> None:
                while self.ws_app is ws:
                    try:
                        ws.send("status")
                    except Exception:
                        break
                    time.sleep(5)
            threading.Thread(target=ping_loop, daemon=True).start()

        self.ws_app = websocket.WebSocketApp(
            f"{WS_URL}/ws/connection-status/{user_id}/",
            on_open=on_open,
            on_message=on_message,
            on_error=on_error,
            on_close=on_close,
        )
        threading.Thread(target=self.ws_app.run_forever, daemon=True).start()

    def disconnect(self) -> None:
        if self.ws_app:
            self.ws_app.close()
            self.ws_app = None
        self.status_label.config(text="Статус: отключено")
        self.disconnect_button.config(state="disabled")
        self.connect_button.config(state="normal")

    def process_queue(self) -> None:
        try:
            while True:
                event = self.queue.get_nowait()
                if event["type"] == "connected":
                    data = event["data"]
                    self.status_label.config(text="Статус: подключено")
                    self.vm_label.config(
                        text=(
                            f"VM #{data['vm_id']}\n"
                            f"Host: {data['host']}\n"
                            f"Port: {data['port']}\n"
                            f"Protocol: {data['protocol']}"
                        )
                    )
                    self.disconnect_button.config(state="normal")
                elif event["type"] == "ws_status":
                    self.status_label.config(text=f"Статус: {event['data'].get('status', 'unknown')}")
                elif event["type"] == "ws_error":
                    self.status_label.config(text="Статус: ошибка WebSocket")
                else:
                    self.status_label.config(text="Статус: ошибка")
                    self.vm_label.config(text=event.get("message", "Неизвестная ошибка"))
                    self.connect_button.config(state="normal")
        except queue.Empty:
            pass
        self.after(250, self.process_queue)


if __name__ == "__main__":
    DesktopClient().mainloop()
