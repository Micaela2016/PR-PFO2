# Respuestas Conceptuales - PFO 2

## 1. ¿Por qué hashear contraseñas?

Hashear contraseñas es fundamental para proteger la información de los usuarios.  
Cuando una contraseña se guarda en texto plano, cualquier persona con acceso a la base de datos puede verla directamente. En cambio, al aplicar un hash, la contraseña se transforma en una cadena irreconocible e irreversible.
Esto mejora la seguridad porque evita exponer las contraseñas reales en caso de robo o filtracion de la base de datos, reduce el riesgo de que el atacante utilice esas credenciales robadas en otros sistemas, permite verificar que la contraseña que se ingresa sin la necesidad de almacenarla de forma visible.
---

## 2. Ventajas de usar SQLite en este proyecto

SQLite fue una excelente elección para este proyecto por ser una base de datos liviana, rápida y sencilla de implementar.

Sus principales ventajas son:
- No requiere instalar un servidor adicional.
- Toda la base se guarda en un solo archivo, facilitando su uso y transporte.
- Se integra directamente con Python mediante el módulo `sqlite3`.
- Consume pocos recursos del sistema.
- Permite trabajar con SQL real, útil para aprender bases de datos relacionales.

*
**Autor:** Micaela Lujan Orellano  
**Curso:** Programación sobre Redes  
**Año:** 2026  
**Proyecto:** PFO 2 - Sistema de Gestión de Tareas