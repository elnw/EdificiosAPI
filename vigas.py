import numpy as np


class Viga:
    MODULO_ELASTICIDAD = 2e7

    def CalcularDeformacion(self, base, altura):
        # procesamiento
        inercia = base * (altura**(3)/12)
        longitud1 = 6
        longitud2 = 6

        matrizRigidez1 = np.zeros((4, 4))

        matrizRigidez1[0, :] = self.MODULO_ELASTICIDAD * inercia * np.array([12/longitud1**3, 6/(longitud1**2), -12/(longitud1**3), 6/(longitud1**2)])

        matrizRigidez1[1, :] = self.MODULO_ELASTICIDAD * inercia * np.array([6/(longitud1**2) ,4/longitud1, -6/(longitud1**2), 2/longitud1])

        matrizRigidez1[2, :] = self.MODULO_ELASTICIDAD * inercia * np.array([-12/(longitud1**3), -6/(longitud1**2), 12/(longitud1**3), -6/(longitud1**2)])

        matrizRigidez1[3, :] = self.MODULO_ELASTICIDAD * inercia * np.array([6/(longitud1**2), 2/longitud1, -6/(longitud1**2), 4/longitud1])


        matrizRigidez2 = np.zeros((4, 4))
        matrizRigidez2[0, :] = self.MODULO_ELASTICIDAD * inercia * np.array([12/(longitud2**3), 6/(longitud2**2), -12/(longitud2**3), 6/(longitud2**2)])

        matrizRigidez2[1, :] = self.MODULO_ELASTICIDAD * inercia * np.array([6/(longitud2**2), 4/longitud2, -6/(longitud2**2), 2/longitud2])

        matrizRigidez2[2, :] = self.MODULO_ELASTICIDAD * inercia * np.array([-12/(longitud2**3), -6/(longitud2**2), 12/(longitud2**3), -6/(longitud2**2)])

        matrizRigidez2[3, :] = self.MODULO_ELASTICIDAD * inercia * np.array([6/(longitud2**2),2/longitud2,-6/(longitud2**2),4/longitud2])

        rigidezEstructura = np.zeros((6, 6))
        gradosLibertad1 = np.array([1, 2, 3, 4])
        matrizRigidez1Auxiliar = matrizRigidez1

        DeltaMatrizRigidez1 = np.zeros((6, 6))
        DeltaMatrizRigidez1[0:4, 0:4] = matrizRigidez1Auxiliar

        rigidezEstructura = rigidezEstructura.__add__(DeltaMatrizRigidez1)

        gradosLibertad2 = np.array([3, 4, 5, 6])
        matrizRigidez2Auxiliar = matrizRigidez2

        DeltaMatrizRigidez2 = np.zeros((6, 6))
        DeltaMatrizRigidez2[2:6, 2:6] = matrizRigidez2Auxiliar
        rigidezEstructura = rigidezEstructura.__add__(DeltaMatrizRigidez2)

        # Calcular desplazamientos

        seccionA = np.array([0, 1, 4, 5])
        seccionB = np.array([2, 3])

        matrizSeccionAB = rigidezEstructura[np.ix_(seccionA, seccionB)]

        matrizSeccionBB = rigidezEstructura[np.ix_(seccionB, seccionB)]

        matrizP = np.array([[0], [0], [-100], [0], [0], [0]])
        parteB = matrizP[2:4]

        desplazamientoB = np.linalg.lstsq(matrizSeccionBB, parteB)[0]

        parteA = np.dot(matrizSeccionAB, desplazamientoB)
        desplazamiento = np.zeros((6, 1))

        desplazamiento[2:4] = desplazamientoB
        # Cortantes y momentos de los elementos

        despElemento1 = desplazamiento[0:4]
        elemParte1 = np.multiply(matrizRigidez1, despElemento1)

        despElemento2 = desplazamiento[2:6]
        elemParte2 = np.multiply(matrizRigidez2, despElemento2)

        return desplazamiento.tolist()




