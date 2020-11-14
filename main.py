from flask import Flask, request
from flask_restful import Resource, Api
from vigas import Viga
app = Flask(__name__)
api = Api(app)


class VigaAPI(Resource):
    def get(self):
        baseViga = request.args.get('baseViga', default=0.0, type=float)
        alturaViga = request.args.get('alturaViga', default=0.0, type=float)
        respuesta = {}

        if baseViga == 0.0 and alturaViga == 0.0:
            respuesta.update({"respuesta": [0]})
        else:
            calculoViga = Viga()
            respuesta.update({"respuesta": calculoViga.CalcularDeformacion(baseViga, alturaViga)})
        return respuesta


api.add_resource(VigaAPI, '/api/v1/viga')
