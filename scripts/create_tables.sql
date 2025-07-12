-- Creación de la base de datos
CREATE DATABASE IF NOT EXISTS sematec;
USE sematec;

-- Tabla usuario
CREATE TABLE usuario (
    id_usuario INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    correo VARCHAR(150) NOT NULL UNIQUE,
    contraseña VARCHAR(255) NOT NULL,
    rol ENUM('estudiante', 'profesor', 'administrador') NOT NULL
);

-- Tabla perfilprofesor
CREATE TABLE perfilprofesor (
    id_usuario INT PRIMARY KEY,
    especialidad VARCHAR(150),
    FOREIGN KEY (id_usuario) REFERENCES usuario(id_usuario) ON DELETE CASCADE
);

-- Tabla perfilestudiante
CREATE TABLE perfilestudiante (
    id_usuario INT PRIMARY KEY,
    edad INT,
    nivel_educativo VARCHAR(100),
    ocupacion VARCHAR(100),
    FOREIGN KEY (id_usuario) REFERENCES usuario(id_usuario) ON DELETE CASCADE
);

-- Tabla curso
CREATE TABLE curso (
    id_curso INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(200) NOT NULL,
    descripcion TEXT,
    categoria VARCHAR(100),
    nivel VARCHAR(50),
    id_profesor INT NOT NULL,
    FOREIGN KEY (id_profesor) REFERENCES usuario(id_usuario) ON DELETE CASCADE
);

-- Tabla inscripcion
CREATE TABLE inscripcion (
    id_inscripcion INT AUTO_INCREMENT PRIMARY KEY,
    id_usuario INT NOT NULL,
    id_curso INT NOT NULL,
    fecha_inscripcion DATE NOT NULL,
    estado VARCHAR(50) NOT NULL,
    FOREIGN KEY (id_usuario) REFERENCES usuario(id_usuario) ON DELETE CASCADE,
    FOREIGN KEY (id_curso) REFERENCES curso(id_curso) ON DELETE CASCADE,
    UNIQUE KEY (id_usuario, id_curso)
);

-- Tabla avancecurso
CREATE TABLE avancecurso (
    id_avance INT AUTO_INCREMENT PRIMARY KEY,
    id_inscripcion INT NOT NULL,
    modulo VARCHAR(100) NOT NULL,
    porcentaje DECIMAL(5,2) NOT NULL,
    fecha DATE NOT NULL,
    FOREIGN KEY (id_inscripcion) REFERENCES inscripcion(id_inscripcion) ON DELETE CASCADE
);

-- Tabla evaluacion
CREATE TABLE evaluacion (
    id_evaluacion INT AUTO_INCREMENT PRIMARY KEY,
    id_curso INT NOT NULL,
    titulo VARCHAR(200) NOT NULL,
    fecha DATE NOT NULL,
    FOREIGN KEY (id_curso) REFERENCES curso(id_curso) ON DELETE CASCADE
);

-- Tabla resultadoevaluacion
CREATE TABLE resultadoevaluacion (
    id_resultado INT AUTO_INCREMENT PRIMARY KEY,
    id_evaluacion INT NOT NULL,
    id_usuario INT NOT NULL,
    puntaje DECIMAL(5,2) NOT NULL,
    FOREIGN KEY (id_evaluacion) REFERENCES evaluacion(id_evaluacion) ON DELETE CASCADE,
    FOREIGN KEY (id_usuario) REFERENCES usuario(id_usuario) ON DELETE CASCADE,
    UNIQUE KEY (id_evaluacion, id_usuario)
);

-- Tabla forocurso
CREATE TABLE forocurso (
    id_foro INT AUTO_INCREMENT PRIMARY KEY,
    id_curso INT NOT NULL,
    tema VARCHAR(200) NOT NULL,
    FOREIGN KEY (id_curso) REFERENCES curso(id_curso) ON DELETE CASCADE
);

-- Tabla comentarioforo
CREATE TABLE comentarioforo (
    id_comentario INT AUTO_INCREMENT PRIMARY KEY,
    id_foro INT NOT NULL,
    id_usuario INT NOT NULL,
    mensaje TEXT NOT NULL,
    fecha DATETIME NOT NULL,
    FOREIGN KEY (id_foro) REFERENCES forocurso(id_foro) ON DELETE CASCADE,
    FOREIGN KEY (id_usuario) REFERENCES usuario(id_usuario) ON DELETE CASCADE
);

-- Índices adicionales para mejorar el rendimiento
CREATE INDEX idx_curso_profesor ON curso(id_profesor);
CREATE INDEX idx_inscripcion_usuario ON inscripcion(id_usuario);
CREATE INDEX idx_inscripcion_curso ON inscripcion(id_curso);
CREATE INDEX idx_avance_inscripcion ON avancecurso(id_inscripcion);
CREATE INDEX idx_evaluacion_curso ON evaluacion(id_curso);
CREATE INDEX idx_resultado_evaluacion ON resultadoevaluacion(id_evaluacion);
CREATE INDEX idx_resultado_usuario ON resultadoevaluacion(id_usuario);
CREATE INDEX idx_foro_curso ON forocurso(id_curso);
CREATE INDEX idx_comentario_foro ON comentarioforo(id_foro);
CREATE INDEX idx_comentario_usuario ON comentarioforo(id_usuario);