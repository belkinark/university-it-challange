const form = document.querySelector("#upload-form");
const fileInput = document.querySelector("#file-input");
const columnInput = document.querySelector("#column-input");
const submitButton = document.querySelector("#submit-button");
const formMessage = document.querySelector("#form-message");
const tasksBody = document.querySelector("#tasks-body");
const tasksMessage = document.querySelector("#tasks-message");
const refreshButton = document.querySelector("#refresh-button");

const statusLabels = {
    pending: "Queued",
    processing: "Processing",
    completed: "Completed",
    failed: "Failed",
};

function setMessage(element, text, type = "") {
    element.textContent = text;
    element.className = `message${type ? ` ${type}` : ""}`;
}

function formatResult(task) {
    if (task.status === "failed") {
        return task.error || "File processing failed";
    }
    if (task.status !== "completed" || !task.result) {
        return "—";
    }

    const { count, min, max, mean } = task.result;
    return `Count: ${count} · min: ${min} · max: ${max} · mean: ${mean}`;
}

function renderTasks(tasks) {
    tasksBody.replaceChildren();

    if (tasks.length === 0) {
        const row = document.createElement("tr");
        const cell = document.createElement("td");
        cell.colSpan = 4;
        cell.className = "empty-state";
        cell.textContent = "No tasks yet. Upload a CSV file above.";
        row.append(cell);
        tasksBody.append(row);
        return;
    }

    for (const task of [...tasks].reverse()) {
        const row = document.createElement("tr");
        const idCell = document.createElement("td");
        idCell.className = "task-id";
        idCell.textContent = `#${task.id}`;

        const columnCell = document.createElement("td");
        columnCell.textContent = task.column;

        const statusCell = document.createElement("td");
        const status = document.createElement("span");
        status.className = `status status-${task.status}`;
        status.textContent = statusLabels[task.status] || task.status;
        statusCell.append(status);

        const resultCell = document.createElement("td");
        resultCell.textContent = formatResult(task);

        row.append(idCell, columnCell, statusCell, resultCell);
        tasksBody.append(row);
    }
}

async function loadTasks() {
    try {
        const response = await fetch("/api/v1/tasks/");
        if (!response.ok) {
            throw new Error(`The server returned error ${response.status}`);
        }

        const tasks = await response.json();
        renderTasks(tasks);
        setMessage(tasksMessage, "");
        return tasks.some((task) => task.status === "pending" || task.status === "processing");
    } catch (error) {
        setMessage(tasksMessage, `Failed to load tasks: ${error.message}`, "error");
        return false;
    }
}

form.addEventListener("submit", async (event) => {
    event.preventDefault();
    setMessage(formMessage, "");

    const file = fileInput.files[0];
    if (!file) {
        setMessage(formMessage, "Please choose a CSV file.", "error");
        return;
    }

    const formData = new FormData();
    formData.append("file", file);
    formData.append("column", columnInput.value.trim());

    submitButton.disabled = true;
    submitButton.querySelector("span:first-child").textContent = "Submitting…";
    try {
        const response = await fetch("/api/v1/tasks/", {
            method: "POST",
            body: formData,
        });
        if (!response.ok) {
            const body = await response.json().catch(() => null);
            throw new Error(body?.detail || `The server returned error ${response.status}`);
        }

        const task = await response.json();
        setMessage(formMessage, `Task #${task.id} has been added to the queue.`, "success");
        form.reset();
        await refreshWhileProcessing();
    } catch (error) {
        setMessage(formMessage, `Failed to submit task: ${error.message}`, "error");
    } finally {
        submitButton.disabled = false;
        submitButton.querySelector("span:first-child").textContent = "Submit for processing";
    }
});

refreshButton.addEventListener("click", refreshWhileProcessing);

let refreshTimeout;
async function refreshWhileProcessing() {
    window.clearTimeout(refreshTimeout);
    if (await loadTasks()) {
        refreshTimeout = window.setTimeout(refreshWhileProcessing, 3000);
    }
}

refreshWhileProcessing();
