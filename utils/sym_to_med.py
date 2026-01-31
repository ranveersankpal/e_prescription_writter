from llama_cpp import Llama
import re

MODEL_PATH = "./models/qwen2.5-1.5b-instruct-q4_k_m.gguf"
#MODEL_PATH = "qwen2.5-1.5b-instruct-q5_k_m.gguf"
#MODEL_PATH = "qwen2.5-1.5b-instruct-q8_0.gguf"

# ---- LOAD MODEL ONCE ----
llm = Llama(
    model_path=MODEL_PATH,
    n_ctx=2048,
    n_threads=8,
    n_gpu_layers=0,
    verbose=False
)

# ---- ALLOWED OTC MEDICINES (SOURCE OF TRUTH) ----
ALLOWED_MEDICINES = {
    "paracetamol",
    "acetaminophen",
    "ibuprofen",
    "aspirin",
    "dextromethorphan",
    "guaifenesin",
    "chlorpheniramine",
    "diphenhydramine"
}

def get_otc_medicines(symptoms: str):
    # ---- STATIC PROMPT + DYNAMIC SYMPTOMS ----
    prompt = f"""<|system|>
You must follow formatting rules strictly.

<|user|>
Output ONLY a comma-separated list of specific over-the-counter medicine NAMES.
No explanations.
No categories.
No extra words.
No sentences.

Symptoms: {symptoms}
<|assistant|>
"""

    response = llm(
        prompt,
        max_tokens=128,
        temperature=0.3,
        top_p=0.9,
        stop=["\n", "<|user|>", "<|system|>"]
    )

    raw = response["choices"][0]["text"].strip()

    # ---- CLEAN OUTPUT ----
    clean = re.sub(r"[^A-Za-z, ]", "", raw)

    items = [
        x.strip()
        for x in clean.split(",")
        if x.strip().lower() in ALLOWED_MEDICINES
    ]

    # Deduplicate + preserve order
    return list(dict.fromkeys(items))

if __name__ == "__main__":
    test_symptoms = "I have a headache and a mild fever."
    medicines = get_otc_medicines(test_symptoms)
    print("Recommended OTC Medicines:", medicines)