import gradio as gr 
from google.cloud import storage


def get_base_file():
    return gr.File(file_count="single", label="Raw file")

def get_base_markdown():
    return gr.Markdown(
        f"""
        ```

        



        ```
        """
        )


def clean():
    return (
        gr.File(file_count="single", label="Raw file"),
        gr.Markdown(
        f"""
        ```

        



        ```
        """
        )
    )


def summarize_file(file):
    # TODO:
    # storage_client = storage.Client()
    # bucket = storage_client.bucket(bucket_name)
    # blob = bucket.blob(destination_blob_name)
    # blob.upload_from_filename(file.name)

    gr.Info(f"File processed successfully!")
    return gr.Markdown(
                f"""
                It is a long established fact that a reader will be distracted by the readable content of a page when looking at its layout. The point of using Lorem Ipsum is that it has a more-or-less normal distribution of letters, as opposed to using 'Content here, content here', making it look like readable English. Many desktop publishing packages and web page editors now use Lorem Ipsum as their default model text, and a search for 'lorem ipsum' will uncover many web sites still in their infancy. Various versions have evolved over the years, sometimes by accident, sometimes on purpose (injected humour and the like).
                """
            )


if __name__ == '__main__':
    demo = gr.Blocks(theme=gr.themes.Soft())
    
    with demo:
        gr.Markdown(
            f"""
            # Convert2PDF: Demo
            """
        )
        with gr.Row():
            with gr.Column():
                file = get_base_file()
                with gr.Row():
                    btn_summarize = gr.Button(value="✨ Summarize", interactive=True)
                    btn_clean = gr.Button(value="🗑️ Clean", interactive=True)
        
            with gr.Column(visible=True) as summary_result:
                summary_markdown = get_base_markdown()

        btn_summarize.click(
            fn=summarize_file,
            inputs=[file],
            outputs=[summary_markdown]
        )

        btn_clean.click(
            fn=clean,
            inputs=[],
            outputs=[
                file,
                summary_markdown
            ]
        )

    demo.launch(debug=True, server_name="0.0.0.0", server_port=8080)