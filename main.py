#!/usr/bin/env python
import os
import jinja2
import webapp2


template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), autoescape=False)


class BaseHandler(webapp2.RequestHandler):

    def write(self, *a, **kw):
        return self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        return self.write(self.render_str(template, **kw))

    def render_template(self, view_filename, params=None):
        if params is None:
            params = {}
        template = jinja_env.get_template(view_filename)
        return self.response.out.write(template.render(params))


class MainHandler(BaseHandler):
    def get(self):
        return self.render_template("index.html")
    def post(self):
        seznam_vaj = []
        j = 0
        for j in range(1, 21, 1):
            vaja = "st_vaje_na_progi_" + str(j)
            vrednost=self.request.get(vaja)
            seznam_vaj.append(vrednost)
        rezultat = seznam_vaj
        params={"list":rezultat}
        return self.render_template("poslano.html", params=params)
class VnosVajHandler(BaseHandler):
    def get(self):
        return self.render_template("vnos_vaj.html")
    def post(self):
        #vse vaje dam v list, da potem lahko preverim, ce je checkbox true,
        seznam_vseh_vaj=[]
        j=0
        for j in range(0,73,1):
            vaja="vaja_"+str(j)
            seznam_vseh_vaj.append(vaja)
        #preverim pri katerih je kljukica in pri tistih dobim njihovo zaporedno stevilko
        #Ali bi bilo dovolj bez kljukice, kar po stevikah? 0 je pac,da ni v progi?
        zaporedje_vaj_slovar = {}
        for vaja in seznam_vseh_vaj:
            #pri kateri vaji v seznamu smo
            x = seznam_vseh_vaj.index(vaja)
            #vnos zaporedne stevilke vaje
            zaporedna_st="zaporedna_st_"+str(x)

            vrednost_zaporedne_stevilke=self.request.get(zaporedna_st)
            if vaja:

               zaporedje_vaj_slovar[vaja] = str(vrednost_zaporedne_stevilke)


        rezultat = zaporedje_vaj_slovar

        params={"vse_vaje":rezultat}
        return self.render_template("index.html",params=params)

app = webapp2.WSGIApplication([
    webapp2.Route('/', MainHandler),
    
    webapp2.Route('/vnos_vaj', VnosVajHandler),
], debug=True)
