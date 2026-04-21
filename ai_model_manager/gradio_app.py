import gradio as gr
import requests

def chat(message, history):
    response = requests.post(
        "http://127.0.0.1:8000/chat/func",
        json={"message": message},
        stream=True
    )
    result = ""
    for chunk in response.iter_content(chunk_size=None, decode_unicode=True):
        if chunk:
            result += chunk
            yield result

demo = gr.ChatInterface(
    fn=chat,
    title="AI 模型管理助手",
    description="可以查询模型列表、查询时间、查询天气"
)

demo.launch()