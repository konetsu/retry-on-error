from flask import Flask, render_template_string, session
import time

app = Flask(__name__)

@app.route('/')
def index():
    return page(1)

@app.route('/page/<page>')
def page(page):
    if int(page)==1:
        session['errorcount']=0

    if int(page)==3 and session['errorcount']<3:
        session['errorcount']+=1
        print("error: "+str(session['errorcount']))
        time.sleep(3)
        return("error"), 502
    if int(page)==3:
        print("now it should continue loading the content")
    template="""{% if page==1 %}<!doctype html>{% endif %}

{% for i in range(1,11) %}
{% if loop.last and numberofpages>page %}
<div hx-target="#infinitescrolltarget" hx-get="/page/{{page+1}}" hx-trigger="revealed" hx-swap="outerHTML" style="height:300px; width:300px; background:gray; margin:5px ">post {{(page-1)*10+i}}</div>
<div id="infinitescrolltarget" hx-target="#infinitescrolltarget" hx-get="/page/{{page+1}}" hx-trigger="click" hx-swap="outerHTML"></div>
{% else %}
<div style="height:300px; width:300px; background:gray; margin:5px ">post {{(page-1)*10+i}}</div>
{% endif %}
{% endfor %}

{% if page==1 %} 
<script src="https://unpkg.com/htmx.org@1.9.9"></script>
<script>
document.body.addEventListener("htmx:responseError", function(e) {retryinfinitescroll(e)});
document.body.addEventListener("htmx:sendError", function(e) {retryinfinitescroll(e)});
document.body.addEventListener("htmx:timeout", function(e) {retryinfinitescroll(e)});


function retryinfinitescroll(e) {
	if (e.detail.elt.outerHTML.includes('hx-target="#infinitescrolltarget"')) {
        setTimeout(() => {document.getElementById("infinitescrolltarget").click();}, "2000");
    } 
	else {
		//error is not from the infinite scroll
	}
}
</script>
{% endif %}
 """
    return render_template_string(template, page=int(page), numberofpages=10)

app.config['SECRET_KEY'] = "secret"
app.run(host='0.0.0.0', port=81)