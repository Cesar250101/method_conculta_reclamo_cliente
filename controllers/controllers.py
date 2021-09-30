# -*- coding: utf-8 -*-
from odoo import http

# class MethodConcultaReclamoCliente(http.Controller):
#     @http.route('/method_conculta_reclamo_cliente/method_conculta_reclamo_cliente/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/method_conculta_reclamo_cliente/method_conculta_reclamo_cliente/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('method_conculta_reclamo_cliente.listing', {
#             'root': '/method_conculta_reclamo_cliente/method_conculta_reclamo_cliente',
#             'objects': http.request.env['method_conculta_reclamo_cliente.method_conculta_reclamo_cliente'].search([]),
#         })

#     @http.route('/method_conculta_reclamo_cliente/method_conculta_reclamo_cliente/objects/<model("method_conculta_reclamo_cliente.method_conculta_reclamo_cliente"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('method_conculta_reclamo_cliente.object', {
#             'object': obj
#         })