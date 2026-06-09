# Data Augmentation for Power Plant Surveillance

**Final Project — Generative AI / AI Engineering — ProfessionAI**

CyberEye Solutions case: enrich a limited image dataset using generative AI
(image captioning → caption paraphrasing → text-to-image synthesis) to improve
classifier robustness for critical-infrastructure surveillance.

The Oxford-IIIT Pet dataset is used as a controlled experimental proxy: it is
public, curated, and lets us isolate the augmentation effect on a fine-grained
classification task without the security/legal constraints of real CCTV data.

---

## Pipeline

1. **Dataset** — Oxford-IIIT Pet (subset of breeds for clearer signal)
2. **Captioning** — BLIP base generates natural-language descriptions
3. **Paraphrasing** — T5-based paraphraser produces caption variants
4. **Image generation** — SD-turbo creates synthetic images from variants
5. **Training** — ResNet18 transfer learning, two runs (baseline vs augmented)
6. **Evaluation** — accuracy, precision, recall, F1, confusion matrices

---

## Run on Google Colab (free T4)

1. Upload `notebook.ipynb` to Colab.
2. Runtime → Change runtime type → **T4 GPU**.
3. Run cells top-to-bottom. Total runtime ~60–90 min on free T4.
4. (Optional) Mount Google Drive in the first cell to persist artifacts
   across sessions.

### Why these models on T4

| Model | VRAM (fp16) | Why |
|---|---|---|
| BLIP base | ~1 GB | Solid captions, fast |
| T5 paraphraser | ~1 GB | Cheap caption variants |
| SD-turbo | ~4 GB | 1–4 step inference, ~3s/img on T4 |
| ResNet18 | <1 GB | Fast training, enough capacity for the subset |

Models are loaded sequentially and freed (`del` + `torch.cuda.empty_cache()`)
between phases to fit comfortably in 16 GB.

---

## Mapping back to the CyberEye use case

The pipeline is domain-agnostic. To deploy on real surveillance footage:

- Replace the Pet subset with frames extracted from CCTV / drone feeds.
- Fine-tune captioning and SD models on a small annotated set of in-domain
  imagery (or use ControlNet to constrain generation by edges/poses).
- Replace the breed classifier with the target task: anomaly detection,
  intruder vs maintenance, suspicious-object presence, etc.
- Validate synthetic samples with domain experts before training — synthetic
  drift can hurt rather than help if visual statistics differ too much.

---

## Files

- `notebook.ipynb` — end-to-end runnable notebook
- `README.md` — this file
- `requirements.txt` — pinned versions for reproducibility
