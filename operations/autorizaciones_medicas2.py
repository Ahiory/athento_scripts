# Operation properties
import os
import shutil
from datetime import datetime

from operations.enums import ProcessOperationParameterType, ProcessOperationParameterChoiceType
from django.utils.translation import gettext as _

VERSION = "1.1"
NAME = _("Envia autorizaciones medicas Github clone")
DESCRIPTION = _("Esto es una prueba de clonacion dde operaciones del repositorio")
ORDER = 100
CATEGORY = ""
DEPRECATED = False # If it's true,the operations doesn't appear in the marketplace
POSTLOAD = True # Esto es un ejemplo
POSTCHARACT = False
POSTCLASSIF = False
POSTEXTRACTION = False

CONFIGURATION_PARAMETERS = {
}


def run(uuid=None, **params):
    from file.utils import get_document
    fil = get_document(uuid, **params)
    if fil:
                num_sorweb = fil.gmv('metadata.autorizaciones_medicas_no_solicitud')
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"{num_sorweb}_{timestamp}.txt"
                path_txt = base_path + filename
                carpeta = base_path + f'{num_sorweb}_{timestamp}'
                os.makedirs(carpeta, exist_ok=True)
                with open(path_txt, 'w') as f:
                    serie = fil.gmv('metadata.autorizaciones_medicas_serie')
                    oficina = fil.gmv('metadata.autorizaciones_medicas_oficina')
                    f.write(serie)
                    f.write(';')
                    f.write(oficina)
                    f.write('\n')
                    consecutivo_linea = 1
                    for rel in fil.get_children():
                        f.write(rel.filename)
                        f.write(';')
                        f.write(str(rel.gmv('metadata.autorizaciones_medicas_credencial')) or '')
                        f.write('|')
                        f.write(rel.gmv('metadata.autorizaciones_medicas_nombres_apellidos') or '')
                        f.write('|')
                        f.write(rel.gmv('metadata.autorizaciones_medicas_no_identificacion') or '')
                        f.write('|')
                        f.write('') # Espacio Ubicacion GD
                        f.write('|')
                        f.write(rel.gmvp('metadata.autorizaciones_medicas_ciudad') or '')
                        f.write('|')
                        f.write(rel.gmv('metadata.autorizaciones_medicas_no_solicitud') or '')
                        f.write('|')
                        f.write(rel.gmv('metadata.autorizaciones_medicas_fecha_creacion') or '')
                        f.write('|;')
                        f.write(rel.gmv('metadata.autorizaciones_medicas_tipo_documental') or '')
                        f.write(';')
                        f.write(str(consecutivo_linea))
                        f.write(';;')
                        f.write(rel.gmv('metadata.autorizaciones_medicas_proceso') or '')
                        f.write(';')
                        if rel.has_content():
                            extension = rel.get_extension()
                            rel_filename = str(rel.uuid)[:4] + '_' + rel.filename.replace(extension, '') + extension
                            f.write(rel_filename)
                            shutil.copy(rel.path(), carpeta + '/' + rel_filename)
                        else:
                            f.write('')

                        f.write('\n')

                        consecutivo_linea += 1

    return {'msg_type': 'warning', 'msg': 'Operation run ok'}
