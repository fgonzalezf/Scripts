import subprocess

import htmlmin
import csscompressor


def minify_css(inp):
    "Minify CSS that is in the Unicode string `inp`"
    return csscompressor.compress(inp)

def minify_js(inp):
    "Minify JavaScript that is in the Unicode string `inp`"
    return subprocess.check_output(
        'uglifyjs --compress --mangle --comments'.split(),
        input=inp.encode('utf-8')
    ).decode('utf-8')

def _handle_pre(tag, data):
    if tag == 'style':
        return '\n'+minify_css(data)+'\n'
    if tag == 'script':
        return '\n'+minify_js(data)+'\n'
    return data
def minify_html(inp):
    """Minify HTML that is in the Unicode string `inp`,
    including the <script> and <style> blocks inside it"""
    return htmlmin.minify(inp, remove_comments=True, handle_pre=_handle_pre)

def compile_ls(inp):
    "Compile LiveScript that is in the Unicode string `inp` to JavaScript"
    return subprocess.check_output(
        'lsc --compile --stdin --print'.split(),
        input=inp.encode('utf-8')
    ).decode('utf-8')

def minify(filename, inp=None):

    if inp is None:
        with open(filename, 'rb') as f:
            inp = f.read()
    result = None
    if filename.endswith('.css'):
        result = minify_css(inp.decode('utf-8'))
    elif filename.endswith('.js'):
        if max(map(len, inp.splitlines())) <= 200: # maybe it's already minified
            result = minify_js(inp.decode('utf-8'))
    elif filename.endswith('.ls'):
        filename = filename[:-3]+'.js'
        result = minify_js(compile_ls(inp.decode('utf-8')))
    elif filename.endswith('.html'):
        result = minify_html(inp.decode('utf-8'))
    if result is not None:
        return filename, result.encode('utf-8')


def escribir(file):
    result=minify(file)
    file = open(file.split(".")[0]+"-min."+file.split(".")[1], "w")
    file.write(result[1])
    file.close()

escribir(r"C:\Users\Desarrollo\Documents\sismos\Visor_22_08_2017\js\app_v5.js")