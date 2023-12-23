<?php
require __DIR__ . '/vendor/autoload.php';

use DeividFortuna\Fipe\FipeCarros;

if ($_SERVER['REQUEST_METHOD'] !== 'GET' || !isset($_GET['codMarca'])) {
    header('Content-Type: application/json');
    echo json_encode(['error' => 'Invalid request']);
    exit;
}

// Verifica se é uma solicitação para obter todas as marcas
if (isset($_GET['todas_marcas'])) {
	$marcas = FipeCarros::getMarcas();
	// Retorna apenas as marcas como resposta JSON
	header('Content-Type: application/json');
	echo json_encode($marcas);
	exit; // Encerra a execução após enviar a resposta JSON
}

// Adiciona verificação para obter modelos se um código de marca for fornecido
if (isset($_GET['codMarca'])) {
	$codMarca = $_GET['codMarca'];
	$modelos = FipeCarros::getModelos($codMarca);
	// Retorna apenas os modelos como resposta JSON
	header('Content-Type: application/json');
	echo json_encode($modelos);
	exit; // Encerra a execução após enviar a resposta JSON
}


// Se a solicitação não incluir uma marca, retorna um JSON vazio
echo json_encode([]);