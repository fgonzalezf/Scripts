#!/usr/bin/env python3
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
    """Minify HTML or JS or CSS (depending on `filename`) that is in the
    bytestring `inp`. If `inp` is absent, the content is read from `filename`.
    Return a tuple of the new filename and a bytestring of the minified
    content, or None if the file type was not recognized."""
    if inp is None:
        with open(filename, 'rb') as f:
            inp = f.read()
    result = None
    if filename.endswith('.css'):
        result = minify_css(inp.decode('utf-8'))
    elif filename.endswith('.js'):
        if max(map(len, inp.splitlines())) <= 200:
            result = minify_js(inp.decode('utf-8'))
    elif filename.endswith('.ls'):
        filename = filename[:-3]+'.js'
        result = minify_js(compile_ls(inp.decode('utf-8')))
    elif filename.endswith('.html'):
        result = minify_html(inp.decode('utf-8'))
    if result is not None:
        return filename, result.encode('utf-8')

minify(r"C:\Users\fgonzalezf\Documents\minify_pruebas\sismos\index.html")