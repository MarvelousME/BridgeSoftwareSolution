# Load the necessary .NET assemblies for the GUI
Add-Type -AssemblyName System.Windows.Forms
Add-Type -AssemblyName System.Drawing

# Function to choose the folder location
function Choose-FolderDialog {
    $folderBrowser = New-Object System.Windows.Forms.FolderBrowserDialog
    $folderBrowser.Description = "Select the folder where the front-end file tree will be created"
    $folderBrowser.ShowNewFolderButton = $true
    
    $dialogResult = $folderBrowser.ShowDialog()
    
    if ($dialogResult -eq [System.Windows.Forms.DialogResult]::OK) {
        return $folderBrowser.SelectedPath
    } else {
        Write-Host "No folder selected. Script exiting."
        exit
    }
}

# Get the base path
$basePath = Choose-FolderDialog

# Define the front-end folder structure
$folders = @(
    "$basePath\TradeXpertAI\frontend\src",
    "$basePath\TradeXpertAI\frontend\public",
    "$basePath\TradeXpertAI\frontend\styles",
    "$basePath\TradeXpertAI\frontend\components",
    "$basePath\TradeXpertAI\frontend\assets",
    "$basePath\TradeXpertAI\frontend\tests"
)

# Define the front-end files to be created
$files = @(
    "$basePath\TradeXpertAI\frontend\src\index.js",
    "$basePath\TradeXpertAI\frontend\src\app.js",
    "$basePath\TradeXpertAI\frontend\src\server.js",
    "$basePath\TradeXpertAI\frontend\public\index.html",
    "$basePath\TradeXpertAI\frontend\styles\main.css",
    "$basePath\TradeXpertAI\frontend\components\Header.js",
    "$basePath\TradeXpertAI\frontend\components\Footer.js",
    "$basePath\TradeXpertAI\frontend\components\Sidebar.js",
    "$basePath\TradeXpertAI\frontend\assets\logo.png",
    "$basePath\TradeXpertAI\frontend\assets\background.jpg",
    "$basePath\TradeXpertAI\frontend\tests\app.test.js",
    "$basePath\TradeXpertAI\frontend\tests\header.test.js",
    "$basePath\TradeXpertAI\frontend\tests\footer.test.js",
    "$basePath\TradeXpertAI\frontend\README.md"
)

# Create the folders
foreach ($folder in $folders) {
    New-Item -ItemType Directory -Path $folder -Force
}

# Create the files
foreach ($file in $files) {
    New-Item -ItemType File -Path $file -Force
}

Write-Host "Front-end file and folder structure created successfully at $basePath\TradeXpertAI\frontend"

