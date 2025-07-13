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
        
        # Ensure we always return a proper message
        if result:
            return f"✅ **Validation Complete!**\n\n{result}"
        else:
            return "✅ **Validation Complete!**\n\nNo issues found with the Beckn payload."
            
    except json.JSONDecodeError:
        return "❌ **Error: Invalid JSON format.** Please provide a valid JSON payload."
    except Exception as e:
        return f"❌ **Error:** {str(e)}"


def create_ui():
    with gr.Blocks(
        theme=gr.themes.Default(primary_hue="sky"),
        title="Beckn Protocol Validator",
        css="""
        .gradio-container {
            max-width: 1200px !important;
            margin: 0 auto !important;
        }
        .processing-message {
            color: #1f77b4;
            font-weight: bold;
            text-align: center;
            padding: 10px;
            background-color: #f0f8ff;
            border-radius: 5px;
            margin: 10px 0;
        }
        """
    ) as ui:
        
        # Header
        gr.Markdown("""
        # 🔍 Beckn Protocol Validator
        
        Validate your Beckn protocol JSON payloads against the specification.
        """)
        
        with gr.Row():
            with gr.Column(scale=1):
                # Instructions panel on the left
                gr.Markdown("""
                ### ℹ️ Instructions
                
                1. **Paste your Beckn JSON payload** in the text area
                2. **Click "Validate Payload"** to check against the specification
                3. **Review the results** in the report section below
                """)
            
            with gr.Column(scale=2):
                # Input section
                gr.Markdown("### 📥 Input Payload")
                query_textbox = gr.Textbox(
                    label="Beckn JSON Payload",
                    placeholder="Paste your Beckn JSON payload here...",
                    lines=12,
                    max_lines=20,
                    show_label=True
                )
                
                with gr.Row():
                    run_button = gr.Button(
                        "🚀 Validate Payload", 
                        variant="primary",
                        size="lg"
                    )
                    clear_button = gr.Button(
                        "🗑️ Clear", 
                        variant="secondary",
                        size="lg"
                    )
                
                # Status indicator
                status_text = gr.Markdown(
                    "Ready to validate...",
                    elem_classes=["processing-message"]
                )
        
        # Results section
        gr.Markdown("### 📊 Validation Report")
        report = gr.Markdown(
            "Results will appear here after validation...",
            label="Report"
        )
        
        # Event handlers
        def on_run_click():
            return gr.update(interactive=False), "⏳ Processing request, please wait..."
        
        def on_run_complete():
            return gr.update(interactive=True), "✅ Validation complete!"
        
        def clear_all():
            return "", "Ready to validate...", "Results will appear here after validation..."
        
        # Run button click events
        run_button.click(
            fn=on_run_click,
            outputs=[run_button, status_text]
        ).then(
            fn=run,
            inputs=query_textbox,
            outputs=report
        ).then(
            fn=on_run_complete,
            outputs=[run_button, status_text]
        )
        
        # Enter key in textbox
        query_textbox.submit(
            fn=on_run_click,
            outputs=[run_button, status_text]
        ).then(
            fn=run,
            inputs=query_textbox,
            outputs=report
        ).then(
            fn=on_run_complete,
            outputs=[run_button, status_text]
        )
        
        # Clear button
        clear_button.click(
            fn=clear_all,
            outputs=[query_textbox, status_text, report]
        )
    
    return ui


def main():
    ui = create_ui()
    ui.launch(
        inbrowser=True,
        server_name="0.0.0.0",
        server_port=7860,
        share=False
    )


if __name__ == "__main__":
    main()