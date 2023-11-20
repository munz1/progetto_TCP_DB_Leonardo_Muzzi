-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Creato il: Nov 20, 2023 alle 00:27
-- Versione del server: 10.4.28-MariaDB
-- Versione PHP: 8.2.4

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `5btepsit`
--

-- --------------------------------------------------------

--
-- Struttura della tabella `dipendenti_leonardo_muzzi`
--

CREATE TABLE `dipendenti_leonardo_muzzi` (
  `id` int(11) NOT NULL,
  `nome` varchar(50) NOT NULL,
  `posizione_lav` varchar(100) NOT NULL,
  `data_di_assunzione` date NOT NULL,
  `telefono` int(10) NOT NULL,
  `codice_fiscale` varchar(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Dump dei dati per la tabella `dipendenti_leonardo_muzzi`
--

INSERT INTO `dipendenti_leonardo_muzzi` (`id`, `nome`, `posizione_lav`, `data_di_assunzione`, `telefono`, `codice_fiscale`) VALUES
(1, 'pinco', 'dipendente', '2023-10-03', 333245698, 'am43nfh2h');

-- --------------------------------------------------------

--
-- Struttura della tabella `zone_di_lavoro_leonardo_muzzi`
--

CREATE TABLE `zone_di_lavoro_leonardo_muzzi` (
  `id_zona` int(11) NOT NULL,
  `nome_zona` varchar(100) NOT NULL,
  `numero_cliente` int(11) NOT NULL,
  `settore_seguito` varchar(20) NOT NULL,
  `cod_dip` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Dump dei dati per la tabella `zone_di_lavoro_leonardo_muzzi`
--

INSERT INTO `zone_di_lavoro_leonardo_muzzi` (`id_zona`, `nome_zona`, `numero_cliente`, `settore_seguito`, `cod_dip`) VALUES
(1, 'baracallo', 43243564, 'agricolo', 1);

--
-- Indici per le tabelle scaricate
--

--
-- Indici per le tabelle `dipendenti_leonardo_muzzi`
--
ALTER TABLE `dipendenti_leonardo_muzzi`
  ADD PRIMARY KEY (`id`);

--
-- Indici per le tabelle `zone_di_lavoro_leonardo_muzzi`
--
ALTER TABLE `zone_di_lavoro_leonardo_muzzi`
  ADD PRIMARY KEY (`id_zona`),
  ADD KEY `cod_dip` (`cod_dip`);

--
-- AUTO_INCREMENT per le tabelle scaricate
--

--
-- AUTO_INCREMENT per la tabella `dipendenti_leonardo_muzzi`
--
ALTER TABLE `dipendenti_leonardo_muzzi`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT per la tabella `zone_di_lavoro_leonardo_muzzi`
--
ALTER TABLE `zone_di_lavoro_leonardo_muzzi`
  MODIFY `id_zona` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
