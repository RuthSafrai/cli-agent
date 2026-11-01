import time

from dotenv import load_dotenv
from google import genai
from google.genai import types
import gradio as gr
from pathlib import Path

load_dotenv()

# מודל הAI והפרופמט
MODEL = "gemini-3.8-flash"
# SYSTEM_PROMPT = "תמיר את ההוראה/בקשה שהתקבלה לפקודה שמוכנה להרצה בשורת הפקודה, ללא מלל מיותר. רק פקודה"
PROMPT_FILE = "prompt.md"

# המרת הפרופמט לעברית תקינה
def load_prompt():
    path = Path(__file__).parent / PROMPT_FILE
    return path.read_text(encoding="utf-8")

def text_to_command(user_text):
    client = genai.Client()
    response = client.models.generate_content(
        model=MODEL,
        contents=user_text,
        config=types.GenerateContentConfig(
            system_instruction=load_prompt(),
            temperature=0,
            thinking_config=types.ThinkingConfig(thinking_level="low"),
        ),
    )

    return response.text.strip()

def main():
    with gr.Blocks() as demo:
        gr.Markdown(
            "# 🖥️ Text to CLI Agent\n"
            "כתבי הוראה בשפה טבעית וקבלי פקודה לשורת הפקודה."
        )
        with gr.Row():
            with gr.Column():
                user_input = gr.Textbox(
                    label="הוראה בשפה טבעית",
                    placeholder="למשל: מה כתובת ה-IP של המחשב שלי",
                    lines=3,
                    rtl=True,
                )
                run_btn = gr.Button("המר לפקודה", variant="primary")
            with gr.Column():
                output = gr.Code(
                    label="פקודת CLI",
                    language="shell",
                    interactive=False,
                )

        gr.Examples(
            examples=[
                ["מה כתובת ה-IP של המחשב שלי"],
                ["איזה תהליכים רצים כרגע במערכת"],
                ["צור תיקייה חדשה בשם projects"],
            ],
            inputs=user_input,
        )

        run_btn.click(fn=text_to_command, inputs=user_input, outputs=output)
        user_input.submit(fn=text_to_command, inputs=user_input, outputs=output)

    demo.launch(theme=gr.themes.Soft())