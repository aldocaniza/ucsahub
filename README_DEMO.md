# UCSA Hub - Demo Feria Tecnológica

## Módulos funcionales
- **Portal Académico - Estudiantes** (`?app=academico`): Login demo (A-00123/demo), inicio, mis materias, horario, calificaciones, inscripciones, trámites, pagos, perfil.
- **Gestión RRHH** (`?app=rrhh`): Dashboard, legajo, asistencias, nómina, evaluaciones, solicitudes.
- **Ecommerce UCSA** (`?app=ecommerce`): Tienda, catálogo, carrito, pedidos, ventas, stock.

## Ejecutar
```bash
cd /home/acaniza/.herdr/worktrees/ucsahub/worktree-calm-river-2a41
PYTHONPATH=. /usr/bin/python3 -m streamlit run app.py --server.port 8989
```

## Verificación
Todos los módulos pasan AppTest sin excepciones.
