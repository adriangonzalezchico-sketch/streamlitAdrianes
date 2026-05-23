# streamlitAdrianes

# Link temporal de la web: https://appadrianes-rtwumwm39a7hznhauivqlv.streamlit.app/

## Lista de tareas principales:
### 1. Clientes por estado y ciudad

Representa una clasificación del número de clientes por estado. Crea una tabla en la que se muestren:
- Estado
- Ciudad
- Número de clientes por ciudad

Tanto la tabla como los gráficos deberán ser dinámicos respecto a la fecha para permitir el análisis temporal de la evolución de clientes.4

---

### 2. Pedidos por ciudad

A la tabla anterior añade las siguientes columnas:
- Número de pedidos
- Porcentaje que representan respecto al total de pedidos

Además, representa el ratio de pedidos por cliente, utilizando el tipo de gráfico que consideres más adecuado.

Tras este análisis, responde a las siguientes cuestiones:
- ¿Qué información o patrones se pueden identificar a partir de estos datos?
> 'Se ve que de media un 4% de los clientes realizan más de un pedido, lo que puede indicar un problema de incentivos para las compras recurrentes'
- ¿Qué acciones, como analista de datos, crees que debería tomar la empresa para mejorar sus ventas?
> 'Sin saber el estado de sostenibilidad de gastos, es decir que tan beneficioso es actualmente el negocio, recomendariamos el añadir algún sistema de puntos (si no hay) o de bonificación por realizar más de un solo pedido. Además de correos promocionales u otra forma de contactar regularmente con clientes que ya han hecho pedidos antes'

---

### 3. Análisis de retrasos en pedidos

Calcula y representa:
- Número de pedidos que llegan tarde por ciudad
- Porcentaje de pedidos retrasados respecto al total de pedidos de la ciudad
- Tiempo medio de retraso en días

Además, al representar esta información, el dashboard deberá incluir un autodiagnóstico que indique la razón más probable del problema.
> 'Las ciudades grandes como Sao Paulo tienen un porcentaje de retrasos entre 5 y 25% porque los repartidores locales están saturados por el volumen de paquetes. En cambio, los pueblos lejanos como Montanha tienen esperas larguísimas porque las rutas de transporte hasta allí están rotas o fallan por completo. Por otra parte, el estado con los retrasos más largos de media es Alagoas (AL), por lo que sería util tenerlo en cuenta al dar una fecha de entrega aproximada'
---

### 4. Reviews y satisfacción del cliente

Calcula y representa:
- Número de reviews por estado
- Score medio de las reviews en cada estado

Para este cálculo, se deberán excluir los pedidos con retraso, ya que se entiende que la valoración negativa podría deberse principalmente al retraso en la entrega del producto.

