import gradio as gr


if __name__ == '__main__':

    demo = gr.Blocks(theme=gr.themes.Soft())
    
    with demo:
        gr.Markdown(
            f"""
            # Hello
            """)
        

    demo.launch(debug=True, server_name="0.0.0.0", server_port=8080)