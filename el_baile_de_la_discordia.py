import pandas as pd
from pyomo.environ import*
import time

# Lectura de datos
file_path = "data/gc_4_1"
data = pd.read_csv(file_path, header=None, delimiter=' ')
print(data)
pNo_Alumnos = data[0][0]
pNo_Rivalidad = data[1][0]
pRivalidad = {(j, i): data[j][i+1] for i in range(pNo_Rivalidad) for j in range(2)}


input_data = {None: {
    'sAlumnos': {None: list(range(pNo_Alumnos))},
    'sRivalidad': {None: list(range(pNo_Rivalidad))},
    'pRivalidad': pRivalidad,
    'pNo_Alumnos': {None: pNo_Alumnos},
    'pNo_Rivalidad': {None: pNo_Rivalidad}
}}
# Creación del modelo
model = AbstractModel()

# Defino los sets
model.sAlumnos = Set()
model.sRivalidad = Set()

# Defino los parámetros
model.pRivalidad = Param(model.sRivalidad, model.sRivalidad, mutable=True)
model.pNo_Alumnos = Param()
model.pNo_Rivalidad = Param()

# Defino las variables
model.vColor = Var(model.sAlumnos, within=NonNegativeReals)
# model.vAlpha = Var(model.sRivalidad, within=Binary)

# Defino la función objetivo
def obj(model):
    return sum(model.vColor[i] for i in model.sAlumnos)


model.obj = Objective(rule=obj, sense=pyomo.core.minimize)


# Defino las restricciones
def c1(model, sRivalidad):
    return model.vColor[pRivalidad[1, sRivalidad]] - model.vColor[pRivalidad[0, sRivalidad]] >= 1
           # + \
           # (1 - model.vAlpha[sRivalidad]) * model.pNo_Alumnos


# def c2(model):
#     return sum(model.vAlpha[i] for i in model.sRivalidad) == model.pNo_Rivalidad


model.const = Constraint(model.sRivalidad, rule=c1)
# model.const = Constraint(rule=c2)

# Crea una instancia del modelo con los datos
instance = model.create_instance(input_data)

start_time = time.time()

# Resuelve el modelo
opt = SolverFactory('cbc', executable=r'C:\cbc\bin\cbc.exe')
results = opt.solve(instance)

end_time = time.time()
execution_time = end_time - start_time

print("Estado de la solución:", results.solver.termination_condition)


for i in instance.sAlumnos:
    print("Alumno {}: Color {}".format(i, value(instance.vColor[i])))

print("Tiempo de ejecución:", execution_time, "segundos")
