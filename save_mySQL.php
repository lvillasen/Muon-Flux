<?php
// Conexión a la base de datos MySQL
$servername = "localhost";  // o la IP del servidor de MySQL si está en otro lugar
$username = "lvillasen";
$password = "Brunito0";
$dbname = "muon_flux";

// Crear la conexión
$conn = new mysqli($servername, $username, $password, $dbname);

// Verificar la conexión
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

// Verificar si los datos fueron enviados por POST
if ($_SERVER['REQUEST_METHOD'] == 'POST') {
    $date_time = $_POST['date_time'];
    $r1 = $_POST['r1'];
    $r2 = $_POST['r2'];
    $P = $_POST['P'];
    $T = $_POST['T'];
    $H = $_POST['H'];
    $temperature= $_POST['temperature'];

    $datetime = date('Y-m-d H:i:s');
    

// Consulta SQL para insertar los datos
    $sql = "INSERT INTO data (date_time, r1, r2, p, t, h, date_time_rec,temperature) 
        VALUES ('$date_time', '$r1', '$r2', '$P', '$T', '$H','$datetime','$temperature')";

    // Ejecutar la consulta
    if ($conn->query($sql) === TRUE) {
        echo "Data saved successfully";
    } else {
        echo "Error: " . $sql . "<br>" . $conn->error;
    }
} else {
    echo "No data received";
}

// Cerrar la conexión
$conn->close();
?>
