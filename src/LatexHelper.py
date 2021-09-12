#!/usr/bin/perl
import os
from jinja2.loaders import FileSystemLoader
#import tempfile
from latex.jinja2 import make_env
from latex import build_pdf
import datetime
import re

class LatexHelper():
    def __init__(self, template="default"):
        self.setTemplate(template)
        
    def setTemplate(self, template):
        self.template = template

    def createLatexFile(self, **kwargs):
        latex_jinja_env = make_env(loader=FileSystemLoader('.'))

        # return a date formatted as 202012, or string "(current)" if value is "NOW"
        def simpledate(value):
            if value == "NOW":
                return "(current)"
            return value.strftime("%Y%m")

        # special escape characters for LaTeX
        def tex_escape(text):
            conv = {
                '&': r'\&',
                '%': r'\%',
                '$': r'\$',
                '#': r'\#',
                '_': r'\_',
                '{': r'\{',
                '}': r'\}',
                '~': r'\textasciitilde{}',
                '^': r'\^{}',
                '\\': r'\textbackslash{}',
                '<': r'\textless{}',
                '>': r'\textgreater{}',
            }
            regex = re.compile('|'.join(re.escape(str(key)) for key in sorted(conv.keys(), key = lambda item: - len(item))))
            return regex.sub(lambda match: conv[match.group()], text)

        latex_jinja_env.filters['simpledate'] = simpledate
        latex_jinja_env.filters['texescape'] = tex_escape

        template = latex_jinja_env.get_template('templates/jinja-{}.tex'.format(self.template))

        try:
            pdf = build_pdf(template.render(photopath='/code/data/myphoto.png', **kwargs))
            pdf.save_to('/code/output/cv_{}.pdf'.format(simpledate(datetime.datetime.now())))

        except IOError:
            print('ooops while creating pdf document. Failed to create latex files')
