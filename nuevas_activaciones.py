from utils import snowflake_login, enviar_email
import os
from datetime import date
import sys

#Logueamos
user, cursor, snowflake_connection = snowflake_login()

try:
    #Se descarga resultado del modelo
    cursor.execute('SELECT * FROM SANDBOX_PLUS.DWH.RESULTADO_MODELO_PRICING_198 WHERE FECHA_EJECUCION = CURRENT_DATE')
    df = cursor.fetch_pandas_all()

    if df.shape[0] == 0:
        enviar_email(sender='marcos.larran@tata.com.uy', receiver=['ds-team@gdn.com.uy'],
                     subject='Nuevas activaciones', body='Checkear task', files=[])
        sys.exit()

    #Se define mes y dia actual
    if len(str(date.today().month)) > 1:
        mes = str(date.today().month)
    else:
        mes = '0' + str(date.today().month)
    
    if len(str(date.today().day)) > 1:
        dia = str(date.today().day)
    else:
        dia = '0' + str(date.today().day)
    
    #Se guarda
    df.to_excel('NUEVAS ACTIVACIONES ' + str(date.today().year) + mes + dia + '.xlsx', index=False)

    #Se envía mail
    enviar_email(sender='marcos.larran@tata.com.uy', receiver=['marcela.moreira@tata.com.uy', 'nahuel.hartwig@tata.com.uy'],
                 subject='Modelo Pricing Ecommerce',
                 body='Buenas tardes\n\nSe envían las nuevas activaciones del día de ayer.\n\nSaludos,',
                 files=['NUEVAS ACTIVACIONES ' + str(date.today().year) + mes + dia + '.xlsx'])
    
    #Se elimina el excel
    os.remove('NUEVAS ACTIVACIONES ' + str(date.today().year) + mes + dia + '.xlsx')
except:
    #Si algo falla avisamos
    enviar_email(sender='marcos.larran@tata.com.uy', receiver=['ds-team@gdn.com.uy'],
                 subject='Nuevas activaciones', body='Hubo un problema con el flujo', files=[])
    try:
        #Se elimina el excel
        os.remove('NUEVAS ACTIVACIONES ' + str(date.today().year) + mes + dia + '.xlsx')
    except:
        pass