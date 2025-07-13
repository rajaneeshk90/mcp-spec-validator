import gradio as gr
import asyncio
import json
from typing import Dict, Any
from dotenv import load_dotenv
from my_agent import BecknAgent

load_dotenv(override=True)

beckn_agent = BecknAgent()


async def run(beckn_payload_str: str):
    try:
        # Parse the JSON string to dict
        beckn_payload = json.loads(beckn_payload_str)
        
        # Run the async function
        result = await beckn_agent.run(beckn_payload)
        return result
    except json.JSONDecodeError:
        return "Error: Invalid JSON format. Please provide a valid JSON."
    except Exception as e:
        return f"Error: {str(e)}"


with gr.Blocks(theme=gr.themes.Default(primary_hue="sky")) as ui:
    gr.Markdown("# Beckn Research")
    query_textbox = gr.Textbox(label="What payload would you like to research?")
    run_button = gr.Button("Run", variant="primary")
    report = gr.Markdown(label="Report")
    
    run_button.click(fn=run, inputs=query_textbox, outputs=report)
    query_textbox.submit(fn=run, inputs=query_textbox, outputs=report)

ui.launch(inbrowser=True)