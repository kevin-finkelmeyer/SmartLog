const logInput = document.getElementById('log');
const logButton = document.getElementById('log-button');
const fileNameSpan = document.getElementById('file-name');
const resultDiv = document.getElementById('result');

async function uploadFile(log) {
    const form = new FormData();
    form.append("file", log)
    const response = await fetch("/upload", {
        method: "POST", body: form
    })
    return await response.json();
}

async function analyzeFile(data) {
    const analyze_response = await fetch("/analyze", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({'file_path': data['file_path']})
    })

    return await analyze_response.json();
}

function updateResultDiv(result) {
    const styles = {
        'ANOMALY': {bg: 'bg-red-50', border: 'border-red-400', text: 'text-red-800', icon: '⚠️'},
        'ROOT CAUSE': {bg: 'bg-orange-50', border: 'border-orange-400', text: 'text-orange-800', icon: '🔍'},
        'ACTION': {bg: 'bg-emerald-50', border: 'border-emerald-400', text: 'text-emerald-800', icon: '🛠️'}
    };
    const splits = result['result'].split('\n\n')
    resultDiv.innerText = ""

    splits.forEach(item => {
        const [type, ...messageParts] = item.split(':');
        const message = messageParts.join(':').trim()
        const style = styles[type.trim()]

        const div = document.createElement("div");

        div.classList.add("p-4", "mt-2", "rounded-lg", "border", style.bg, style.border);

        const header = document.createElement("div");
        header.classList.add("font-bold", "uppercase", "tracking-widest", "text-xs", "mb-1", style.text)
        header.textContent = style.icon + type;

        const body = document.createElement("p");
        body.classList.add("text-gray-700", "text-sm", "leading-relaxed")
        body.textContent = message;

        div.appendChild(header);
        div.appendChild(body)

        resultDiv.appendChild(div);
    })
}

logButton.addEventListener('click', async () => {
    const log = logInput.files[0];
    if (!log) return;
    const data = await uploadFile(log);
    const result = await analyzeFile(data);
    updateResultDiv(result);
})
logInput.addEventListener('change', () => {
    fileNameSpan.innerText = logInput.files[0].name;
})
