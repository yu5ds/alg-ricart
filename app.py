from flask import Flask, request, jsonify
import threading
import time

app = Flask(__name__)

# Simulando la estructura de procesos
processes = {}

# Guardar el estado de los procesos
class Process:
    def __init__(self, pid):
        self.pid = pid
        self.time_stamp = int(time.time() * 1000)  # Usamos milisegundos
        self.queue = []
        self.in_critical_section = False

    def request_access(self):
        print(f"Process {self.pid} requesting access to the critical section.")
        for process in processes.values():
            if process.pid != self.pid:
                process.receive_request(self)

    def receive_request(self, requester):
        if self.in_critical_section:
            self.queue.append(requester)
            print(f"Process {self.pid} is in critical section. Request from {requester.pid} queued.")
        elif requester.time_stamp < self.time_stamp:
            print(f"Process {self.pid} giving OK to process {requester.pid}")
            requester.receive_ok(self)
        else:
            print(f"Process {self.pid} is requesting access. Request from {requester.pid} queued.")
            self.queue.append(requester)

    def receive_ok(self, process):
        print(f"Process {self.pid} received OK from process {process.pid}.")
        if len(self.queue) == 0:
            self.enter_critical_section()

    def enter_critical_section(self):
        print(f"Process {self.pid} entering critical section.")
        self.in_critical_section = True
        time.sleep(2)  # Simula trabajo en la región crítica
        self.exit_critical_section()

    def exit_critical_section(self):
        print(f"Process {self.pid} exiting critical section.")
        self.in_critical_section = False
        while self.queue:
            next_process = self.queue.pop(0)
            next_process.receive_ok(self)

@app.route('/request_access/<int:pid>', methods=['POST'])
def request_access(pid):
    if pid not in processes:
        processes[pid] = Process(pid)
    process = processes[pid]
    process.request_access()
    return jsonify({"message": f"Process {pid} requested access."}), 200

@app.route('/status')
def status():
    return jsonify({pid: {"time_stamp": p.time_stamp, "in_critical_section": p.in_critical_section} for pid, p in processes.items()})

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)
