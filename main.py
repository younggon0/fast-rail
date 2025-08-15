from fasthtml.common import *

app, rt = fast_app()

@rt("/")
def get():
    return Titled("FastHTML + Railway Template",
        Div(
            H1("Welcome to your FastHTML App"),
            P("This is a template ready for hackathon development!"),
            P("Edit main.py to start building your app."),
            style="text-align: center; margin-top: 50px;"
        )
    )

@rt("/health")
def health():
    return {"status": "healthy"}

if __name__ == "__main__":
    serve()