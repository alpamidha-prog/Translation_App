const micBtn = document.getElementById('mic-btn');
const statusText = document.getElementById('status');
const transcribedEl = document.getElementById('transcribed-text');
const translatedEl = document.getElementById('translated-text');
const langSwitch = document.getElementById('lang-switch');
const labelEn = document.getElementById('label-en');
const labelFi = document.getElementById('label-fi');
const srcBadge = document.getElementById('src-lang-badge');
const destBadge = document.getElementById('dest-lang-badge');
const cameraBtn = document.getElementById('camera-btn');
const cameraFeed = document.getElementById('camera-feed');
const cameraStatus = document.getElementById('camera-status');
const cameraPlaceholder = document.getElementById('camera-placeholder');

let isListening = false;
let isCameraOn = false;
let cameraStream = null;
let recognition;

// Initialize Speech Recognition
if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    recognition = new SpeechRecognition();
    recognition.continuous = false; // We use single-shot and restart to minimize latency
    recognition.interimResults = true;

    recognition.onstart = () => {
        isListening = true;
        micBtn.classList.add('listening');
        statusText.innerText = "Listening...";
    };

    recognition.onresult = (event) => {
        let interimTranscript = '';
        let finalTranscript = '';

        for (let i = event.resultIndex; i < event.results.length; ++i) {
            if (event.results[i].isFinal) {
                finalTranscript += event.results[i][0].transcript;
            } else {
                interimTranscript += event.results[i][0].transcript;
            }
        }

        const currentText = finalTranscript || interimTranscript;
        transcribedEl.innerText = currentText;

        if (finalTranscript) {
            translateText(finalTranscript);
        }
    };

    recognition.onerror = (event) => {
        console.error("Speech recognition error:", event.error);
        stopListening();
        statusText.innerText = "Error, try again";
    };

    recognition.onend = () => {
        if (isListening) {
            // Restart automatically if we want continuous flow
            recognition.start();
        } else {
            stopListening();
        }
    };
} else {
    statusText.innerText = "Speech API not supported";
    micBtn.disabled = true;
}

// Toggle logic
langSwitch.addEventListener('change', () => {
    const isFi = langSwitch.checked;
    
    if (isFi) {
        labelEn.classList.remove('active');
        labelFi.classList.add('active');
        srcBadge.innerText = 'FI';
        destBadge.innerText = 'EN';
        recognition.lang = 'fi-FI';
    } else {
        labelEn.classList.add('active');
        labelFi.classList.remove('active');
        srcBadge.innerText = 'EN';
        destBadge.innerText = 'FI';
        recognition.lang = 'en-US';
    }
    
    // Reset output
    transcribedEl.innerText = '...';
    translatedEl.innerText = '...';
});

// Set default lang
recognition.lang = 'en-US';

micBtn.addEventListener('click', () => {
    if (!isListening) {
        startListening();
    } else {
        stopListening();
    }
});

function startListening() {
    isListening = true;
    recognition.start();
}

function stopListening() {
    isListening = false;
    recognition.stop();
    micBtn.classList.remove('listening');
    statusText.innerText = "Click to Speak";
}

async function translateText(text) {
    const isEnToFi = !langSwitch.checked;
    const src = isEnToFi ? 'en' : 'fi';
    const dest = isEnToFi ? 'fi' : 'en';

    translatedEl.innerText = "Translating...";

    try {
        // Using a free translation API endpoint for demonstration
        // Note: For production, use a private backend or official keys
        const response = await fetch(`https://translate.googleapis.com/translate_a/single?client=gtx&sl=${src}&tl=${dest}&dt=t&q=${encodeURIComponent(text)}`);
        const data = await response.json();
        
        if (data && data[0] && data[0][0] && data[0][0][0]) {
            translatedEl.innerText = data[0][0][0];
        } else {
            translatedEl.innerText = "Translation error";
        }
    } catch (error) {
        console.error("Translation error:", error);
        translatedEl.innerText = "Network error";
    }
}

// Camera Functions
async function toggleCamera() {
    if (!isCameraOn) {
        await startCamera();
    } else {
        stopCamera();
    }
}

async function startCamera() {
    try {
        cameraStream = await navigator.mediaDevices.getUserMedia({ video: true, audio: false });
        cameraFeed.srcObject = cameraStream;
        cameraFeed.style.display = 'block';
        cameraPlaceholder.style.display = 'none';
        cameraBtn.classList.add('active');
        cameraStatus.innerText = "Close Camera";
        isCameraOn = true;
    } catch (error) {
        console.error("Camera access error:", error);
        cameraStatus.innerText = "Access Denied";
    }
}

function stopCamera() {
    if (cameraStream) {
        cameraStream.getTracks().forEach(track => track.stop());
    }
    cameraFeed.srcObject = null;
    cameraFeed.style.display = 'none';
    cameraPlaceholder.style.display = 'block';
    cameraBtn.classList.remove('active');
    cameraStatus.innerText = "Open Camera";
    isCameraOn = false;
}

cameraBtn.addEventListener('click', toggleCamera);
