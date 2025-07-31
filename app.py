import gradio as gr
import openai
import os

# 🔐 Safe API key from environment
openai.api_key = os.getenv("OPENAI_API_KEY")

def chat_bot(message, state):
    if state is None:
        state = []
    messages = state + [{"role": "user", "content": message}]
    response = openai.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a Catholic chatbot for athletes. You provide prayer, encouragement, and reflection."},
            *messages
        ]
    )
    reply = response.choices[0].message.content
    messages.append({"role": "assistant", "content": reply})
    return messages, messages

def send_cmd(prompt, state):
    return chat_bot(prompt, state)

custom_css = """
body { background-color: #f0f4ff; }
h1, h2 { color: #0c2340; font-family: 'Segoe UI', sans-serif; }
.subtitle { color: #4169e1; font-size: 1.1em; font-weight: 500; margin-bottom: 1rem; }
hr.accent-line {
  border: 0; height: 4px;
  background: linear-gradient(to right, #ffd700, #fbbf24);
  margin: 1rem 0; border-radius: 2px;
}
button {
  background: linear-gradient(to right, #3b82f6, #1e40af);
  color: white !important;
  border-radius: 8px;
  padding: 10px 24px;
  font-weight: bold; font-size: 1.1em;
  box-shadow: 0px 2px 6px rgba(0,0,0,0.15);
  transition: transform 0.2s, box-shadow 0.2s;
}
button:hover {
  transform: translateY(-2px);
  box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.25);
}
textarea, input {
  border: 2px solid #fbbf24 !important;
  border-radius: 6px;
  background-color: white;
  color: #0c2340;
}
"""

with gr.Blocks(css=custom_css) as demo:
    gr.Markdown("<h1>🏅 CATHLETE COMPANION</h1>")
    gr.Markdown("<div class='subtitle'>Your faith-filled chatbot for strength, motivation, and reflection.</div>")
    gr.HTML("<hr class='accent-line'>")

    with gr.Row():
        prayer_btn = gr.Button("🙏 Prayer")
        motivate_btn = gr.Button("🔥 Motivate")
        reflect_btn = gr.Button("🧠 Reflect")
        verse_btn = gr.Button("📖 Bible Verse")

    chatbot = gr.Chatbot(label="Your Conversation", type="messages")
    msg = gr.Textbox(placeholder="Type a message here...", label="")
    state = gr.State([])

    msg.submit(chat_bot, [msg, state], [chatbot, state])
    prayer_btn.click(lambda s: send_cmd("Prayer please", s), [state], [chatbot, state])
    motivate_btn.click(lambda s: send_cmd("Motivate me", s), [state], [chatbot, state])
    reflect_btn.click(lambda s: send_cmd("Give me something to reflect on", s), [state], [chatbot, state])
    verse_btn.click(lambda s: send_cmd("Give me a Bible verse", s), [state], [chatbot, state])

demo.launch()
