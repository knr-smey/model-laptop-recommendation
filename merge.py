from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import PeftModel
import torch

BASE_MODEL = "mistralai/Mistral-7B-Instruct-v0.3"

print("Loading base model...")

base_model = AutoModelForCausalLM.from_pretrained(
    BASE_MODEL,
    torch_dtype=torch.float16,
    device_map="cpu"
)

print("Loading LoRA adapter...")

model = PeftModel.from_pretrained(
    base_model,
    "./laptop-ai-lora"
)

print("Merging model...")

merged_model = model.merge_and_unload()

print("Saving merged model...")

merged_model.save_pretrained("./merged-model")
AutoTokenizer.from_pretrained(BASE_MODEL).save_pretrained("./merged-model")

print("Done!")