-- phpMyAdmin SQL Dump
-- version 5.0.4
-- https://www.phpmyadmin.net/
--
-- Host: localhost
-- Generation Time: Sep 18, 2025 at 06:44 AM
-- Server version: 10.4.17-MariaDB
-- PHP Version: 7.2.34

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `appTareas`
--

-- --------------------------------------------------------

--
-- Table structure for table `usuarios`
--

CREATE TABLE `usuarios` (
  `id` int(11) NOT NULL,
  `nombre` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  `contraseña` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `usuarios`
--

INSERT INTO `usuarios` (`id`, `nombre`, `email`, `contraseña`) VALUES
(1, 'Primera ', ' tarea', '$2b$12$70BNyK2gIEVVw9g85VZKsuxShH7TOgeYZEpJQCb0XOmj1vUoU9jda'),
(2, 'Primera ', ' tareaa', '$2b$12$iyUscDv0ElXqpSrLYIEW1etIUn.GN8C0FnjOEZNYwUCdx1dVFae/y'),
(3, 'Primera ', ' tareaaa', '$2b$12$RFs5l4B6nnodp6/OuPqipOKZbXm6CThEWJTU7vdfYJbyf/Wql/bdK'),
(4, 'Primera ', ' tareaajja', '$2b$12$dipRyRVNHKBBejYmdc5xm.4x7uklkphT7SfmuikNDPVRYpvoA5CcG');

-- --------------------------------------------------------

--
-- Table structure for table `tareas`
--

CREATE TABLE `tareas` (
  `id` int(11) NOT NULL,
  `descripcion` text DEFAULT NULL,
  `user_id` int(11) NOT NULL,
  `fecha_creacion` timestamp NOT NULL DEFAULT current_timestamp(),
  `fecha_actualizacion` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `tareas`
--

INSERT INTO `tareas` (`id`, `descripcion`, `user_id`, `fecha_creacion`, `fecha_actualizacion`) VALUES
(4, 'Primera tarea', 1, '2025-09-02 01:11:44', '2025-09-02 01:11:44'),
(5, 'Una tarea', 1, '2025-09-02 01:12:03', '2025-09-02 01:12:03'),
(6, 'Una tarea', 2, '2025-09-03 01:10:31', '2025-09-03 01:10:31'),
(7, 'Una tarea', 2, '2025-09-03 01:15:20', '2025-09-03 01:15:20');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `tareas`
--
ALTER TABLE `tareas`
  ADD PRIMARY KEY (`id`),
  ADD KEY `fk_tareas_user` (`user_id`);

--
-- Indexes for table `usuarios`
--
ALTER TABLE `usuarios`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `email` (`email`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `tareas`
--
ALTER TABLE `tareas`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT for table `usuarios`
--
ALTER TABLE `usuarios`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- Constraints for table `tareas`
--
ALTER TABLE `tareas`
  ADD CONSTRAINT `fk_tareas_user` FOREIGN KEY (`user_id`) REFERENCES `usuarios` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
