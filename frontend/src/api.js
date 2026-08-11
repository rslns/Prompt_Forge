import axios from "axios";

const API_BASE = import.meta.env.VITE_API_BASE_URL;

export async function evaluatePrompt(rawText) {
  const res = await axios.post(`${API_BASE}/evaluate`, { raw_text: rawText });
  return res.data;
}

export async function improvePrompt(promptId, rawText, strategy = "meta_prompt") {
  const res = await axios.post(`${API_BASE}/improve`, {
    prompt_id: promptId,
    raw_text: rawText,
    strategy,
  });
  return res.data;
}