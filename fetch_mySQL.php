<?php
$servername = "localhost";
$username = "XXXXXX";
$password = "XXXXXXXX";
$dbname = "muon_flux";

// Crear conexión
$conn = new mysqli($servername, $username, $password, $dbname);

// Verificar conexión
if ($conn->connect_error) {
    die("Conexión fallida: " . $conn->connect_error);
}

// Obtener las fechas desde la solicitud
$start_date = $_GET['start_date'];
$end_date = $_GET['end_date'];

// Consulta SQL
$sql = "SELECT date_time, R1, R2, P, T, H, date_time_rec FROM data WHERE date_time BETWEEN '$start_date' AND '$end_date'";
$result = $conn->query($sql);

$data = array();
if ($result->num_rows > 0) {
    while($row = $result->fetch_assoc()) {
        $data[] = $row;
    }
}

// Devolver los datos en formato JSON
echo json_encode($data);

$conn->close();
?>