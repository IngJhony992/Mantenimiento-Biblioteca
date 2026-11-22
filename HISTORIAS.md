# Historias de usuario del sistema de biblioteca

| ID y rama | Historia | Criterio de aceptación |
|---|---|---|
| HU-01 · feature/hu01-persistencia | Como bibliotecario quiero recuperar usuarios y préstamos al volver a abrir el programa para continuar la atención. | Tras guardar y reabrir, el ISBN 101 sigue asignado a Ana y ella puede devolverlo. |
| HU-02 · feature/hu02-busqueda | Como lector quiero buscar por una parte del título o del autor para encontrar libros sin conocer el ISBN. | Buscar un apellido en minúsculas recupera sus dos títulos. Una consulta sin coincidencias muestra un aviso. |
| HU-03 · feature/hu03-isbn | Como bibliotecario quiero detectar ISBN repetidos para conservar una única ficha por libro. | Un segundo registro del ISBN muestra un aviso y conserva el título original. |
| HU-04 · feature/hu04-devolucion | Como bibliotecario quiero validar al titular de la devolución para mantener coherente el inventario. | Luis no puede devolver el libro asignado a Ana. Ana sí puede y el libro queda disponible. |
| HU-05 · feature/hu05-prestamos | Como bibliotecario quiero consultar los préstamos activos para identificar el ISBN y su titular. | Dos préstamos en la misma fecha aparecen con sus titulares. Tras una devolución solo queda el otro. |
