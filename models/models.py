# -*- coding: utf-8 -*-

import decimal
import logging
from datetime import date, datetime, timedelta
import pytz
from six import string_types

from odoo import api, fields, models, tools
from odoo.exceptions import UserError
from odoo.tools.translate import _
from odoo.addons import decimal_precision as dp

_logger = logging.getLogger(__name__)


try:
    from facturacion_electronica import facturacion_electronica as fe
    from facturacion_electronica import clase_util as util
except Exception as e:
    _logger.warning("Problema al cargar Facturación electrónica: %s" % str(e))
try:
    from io import BytesIO
except ImportError:
    _logger.warning("no se ha cargado io")
try:
    import pdf417gen
except ImportError:
    _logger.warning("Cannot import pdf417gen library")
try:
    import base64
except ImportError:
    _logger.warning("Cannot import base64 library")
try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    _logger.warning("no se ha cargado PIL")

class ModuleName(models.Model):
    _inherit = 'account.invoice'

    name = fields.Char(string='Name')
    
    @api.multi
    def get_dte_claim_mass(self):
        facturas=self.env['account.invoice'].search([('journal_id','=',1),
                                                     ('claim_description','=',False),
                                                     ('sii_document_number','!=',False),
                                                     ('state','!=','draft'),
                                                     ('sii_code','=',33)])
        for f in facturas:
            tipo_dte = f.document_class_id.sii_code
            datos = f._get_datos_empresa(f.company_id)
            rut_emisor = f.company_id.partner_id.rut()
            if f.type in ["in_invoice", "in_refund"]:
                partner_id = f.commercial_partner_id or f.partner_id.commercial_partner_id
                rut_emisor = partner_id.rut()
            datos["DTEClaim"] = [
                {
                    "RUTEmisor": rut_emisor,
                    "TipoDTE": tipo_dte,
                    "Folio": str(f.sii_document_number),
                }
            ]
            try:
                respuesta = fe.consulta_reclamo_documento(datos)
                key = "RUT%sT%sF%s" %(rut_emisor,
                                    tipo_dte, str(f.sii_document_number))
                f.claim_description = respuesta[key]
            except Exception as e:
                if e.args[0][0] == 503:
                    raise UserError(
                        "%s: Conexión al SII caída/rechazada o el SII está temporalmente fuera de línea, reintente la acción"
                        % (tools.ustr(e))
                    )
                raise UserError(tools.ustr(e))
