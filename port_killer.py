import subprocess
import tkinter as tk
from tkinter import messagebox, scrolledtext


def kill_processes_on_port(port: int, output_box):
    try:
        # Очищаем текстовое поле
        output_box.delete(1.0, tk.END)

        result = subprocess.run(
            ["netstat", "-ano"],
            capture_output=True,
            text=True,
            check=True
        )

        lines = result.stdout.splitlines()
        pids = set()

        for line in lines:
            if f":{port} " in line:
                parts = line.split()
                pid = parts[-1]
                if pid.isdigit():
                    pids.add(pid)

        if not pids:
            messagebox.showinfo("Результат", f"На порту {port} ничего не слушает.")
            return

        output_box.insert(tk.END, f"Найдены PID: {', '.join(pids)}\n")

        for pid in pids:
            subprocess.run(["taskkill", "/PID", pid, "/F"])
            output_box.insert(tk.END, f"✅ Убит процесс PID {pid}\n")

        messagebox.showinfo("Готово", f"Все процессы на порту {port} убиты.")

    except subprocess.CalledProcessError as e:
        messagebox.showerror("Ошибка", f"Ошибка выполнения команды: {e}")
    except Exception as e:
        messagebox.showerror("Ошибка", str(e))


def main():
    window = tk.Tk()
    window.title("Убить процессы по порту")
    window.geometry("500x300")

    tk.Label(window, text="Введите порт:").pack(pady=5)

    port_entry = tk.Entry(window, width=20)
    port_entry.pack(pady=5)

    output_box = scrolledtext.ScrolledText(window, width=60, height=10)
    output_box.pack(pady=10)

    def on_kill():
        try:
            port = int(port_entry.get())
            kill_processes_on_port(port, output_box)
        except ValueError:
            messagebox.showerror("Ошибка", "Порт должен быть числом.")

    tk.Button(window, text="Убить процессы", command=on_kill).pack(pady=5)

    window.mainloop()


if __name__ == "__main__":
    main()
