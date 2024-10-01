from flask import Flask, request, render_template
from lexico3 import lexico, lexical_errors
from sintactico3 import sintactico, syntax_errors

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    tokens = None
    syntax_output = None
    syntax_error_output = None
    lexical_error_output = None

    if request.method == 'POST':
        input_text = request.form['text']

        try:
            tokens = lexico(input_text)
            if lexical_errors:
                lexical_error_output = "\n".join(lexical_errors)
        except Exception as e:
            lexical_error_output = f"Error léxico: {str(e)}"

        try:
            syntax_output = sintactico(input_text)
            if syntax_errors:
                syntax_error_output = "\n".join(syntax_errors)
        except Exception as e:
            syntax_error_output = f"Error general: {str(e)}"

        return render_template('virtual3.html', tokens=tokens, text=input_text, sintactico_result=syntax_output, 
                               sintactico_errors=syntax_error_output, lexico_error=lexical_error_output)

    return render_template('virtual3.html', tokens=None, text=None, sintactico_result=None, sintactico_errors=None, lexico_error=None)

if __name__ == '__main__':
    app.run(debug=True)