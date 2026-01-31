from llama_cpp import Llama
import re

MODEL_PATH = "./models/qwen2.5-1.5b-instruct-q4_k_m.gguf"
#MODEL_PATH = "./models/qwen2.5-1.5b-instruct-q5_k_m.gguf"
#MODEL_PATH = "./models/qwen2.5-1.5b-instruct-q8_0.gguf"

# ---- LOAD MODEL ONCE ----
llm = Llama(
    model_path=MODEL_PATH,
    n_ctx=2048,
    n_threads=8,
    n_gpu_layers=0,
    verbose=False
)



def get_otc_medicines(symptoms: str):
    # ---- STATIC PROMPT + DYNAMIC SYMPTOMS ----
    prompt = f"""<|system|>
    You are a pharmaceutical database.

    STRICT OUTPUT RULES:
    - Output ONLY real medicine NAMES (generic or brand)
    - Each item must be 1–3 words MAX
    - Do NOT output treatment phrases (like "pain relief" or "fever reducer")
    - Do NOT describe effects
    - Do NOT output categories
    - Do NOT combine multiple drugs
    - If unsure, output nothing

    Format strictly: Name, Name, Name

    <|user|>
    Symptoms: {symptoms}
    <|assistant|>
    """



    response = llm(
        prompt,
        max_tokens=128,
        temperature=0.1,
        top_p=0.8,
        stop=["\n", "<|user|>", "<|system|>"]
    )

    raw = response["choices"][0]["text"].strip()

    # ---- CLEAN OUTPUT ----
    clean = re.sub(r"[^A-Za-z, ]", "", raw)

    items = [
        x.strip()
        for x in clean.split(",")
    ]

    # Deduplicate + preserve order
    return list(dict.fromkeys(items))

if __name__ == "__main__":
    test_symptoms = "I have a headache and a mild fever."
    medicines = get_otc_medicines(test_symptoms)
    print("Recommended OTC Medicines:", medicines)