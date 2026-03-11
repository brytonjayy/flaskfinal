from flask import Flask, render_template, url_for, request
from searchWTF import AskForTitle

app = Flask(__name__)
app.secret_key = b'(YPT#{@#YAS^RPPF#TA#DGA#adsg' # This should be protected ie don't record it on zoom ;)
app.config.from_object(__name__)
@app.route('/')
def index():
    return render_template ('index.html')

@app.route("/bytitle")
def bytitle():
    title_form = AskForTitle()
    if title_form.validate_on_submit():
        return "Form Submitted"
    return render_template ('bytitle.html', form=title_form)

@app.route("/titles", methods=['GET', 'POST'])
def list_of_titles():
    searchby = request.form.get('book_title')
    return f"You searched for {searchby}"

if __name__ == '__main__':
    app.run(debug=True)
    
