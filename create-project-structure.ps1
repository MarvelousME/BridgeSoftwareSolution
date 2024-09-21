# Load the necessary .NET assemblies for the GUI
Add-Type -AssemblyName System.Windows.Forms
Add-Type -AssemblyName System.Drawing

# Function to choose the folder location
function Choose-FolderDialog {
    $folderBrowser = New-Object System.Windows.Forms.FolderBrowserDialog
    $folderBrowser.Description = "Select the folder where the file tree will be created"
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

# Define the folder structure
$folders = @(
    "$basePath\TradeXpertAI\data\historical_data",
    "$basePath\TradeXpertAI\data\market_sentiment",
    "$basePath\TradeXpertAI\data\live_data",
    "$basePath\TradeXpertAI\data\models",
    "$basePath\TradeXpertAI\data\logs",
    "$basePath\TradeXpertAI\data\predictions",
    "$basePath\TradeXpertAI\src",
    "$basePath\TradeXpertAI\notebooks",
    "$basePath\TradeXpertAI\config",
    "$basePath\TradeXpertAI\tests",
    "$basePath\TradeXpertAI\reports"
)

# Define the files to be created
$files = @(
    "$basePath\TradeXpertAI\data\historical_data\crypto_data.csv",
    "$basePath\TradeXpertAI\data\historical_data\forex_data.csv",
    "$basePath\TradeXpertAI\data\historical_data\equities_data.csv",
    "$basePath\TradeXpertAI\data\market_sentiment\crypto_sentiment.json",
    "$basePath\TradeXpertAI\data\market_sentiment\forex_sentiment.json",
    "$basePath\TradeXpertAI\data\market_sentiment\equities_sentiment.json",
    "$basePath\TradeXpertAI\data\live_data\live_crypto_data.csv",
    "$basePath\TradeXpertAI\data\live_data\live_forex_data.csv",
    "$basePath\TradeXpertAI\data\live_data\live_equities_data.csv",
    "$basePath\TradeXpertAI\data\models\trained_model_crypto.pkl",
    "$basePath\TradeXpertAI\data\models\trained_model_forex.pkl",
    "$basePath\TradeXpertAI\data\models\trained_model_equities.pkl",
    "$basePath\TradeXpertAI\data\logs\tradexpert_ai_live_learning_log.csv",
    "$basePath\TradeXpertAI\data\logs\trade_execution_log.csv",
    "$basePath\TradeXpertAI\data\logs\model_training_log.csv",
    "$basePath\TradeXpertAI\data\predictions\crypto_predictions.csv",
    "$basePath\TradeXpertAI\data\predictions\forex_predictions.csv",
    "$basePath\TradeXpertAI\data\predictions\equities_predictions.csv",
    "$basePath\TradeXpertAI\src\data_loader.py",
    "$basePath\TradeXpertAI\src\model_trainer.py",
    "$basePath\TradeXpertAI\src\trade_executor.py",
    "$basePath\TradeXpertAI\src\strategy_optimizer.py",
    "$basePath\TradeXpertAI\src\risk_management.py",
    "$basePath\TradeXpertAI\src\logging_handler.py",
    "$basePath\TradeXpertAI\src\config.py",
    "$basePath\TradeXpertAI\src\main.py",
    "$basePath\TradeXpertAI\src\utils.py",
    "$basePath\TradeXpertAI\notebooks\exploratory_data_analysis.ipynb",
    "$basePath\TradeXpertAI\notebooks\model_training.ipynb",
    "$basePath\TradeXpertAI\notebooks\backtesting_simulation.ipynb",
    "$basePath\TradeXpertAI\config\trading_strategy_config.yaml",
    "$basePath\TradeXpertAI\config\model_parameters.yaml",
    "$basePath\TradeXpertAI\config\risk_management_config.yaml",
    "$basePath\TradeXpertAI\config\logging_config.yaml",
    "$basePath\TradeXpertAI\tests\test_data_loader.py",
    "$basePath\TradeXpertAI\tests\test_model_trainer.py",
    "$basePath\TradeXpertAI\tests\test_trade_executor.py",
    "$basePath\TradeXpertAI\tests\test_strategy_optimizer.py",
    "$basePath\TradeXpertAI\tests\test_risk_management.py",
    "$basePath\TradeXpertAI\reports\backtest_report.pdf",
    "$basePath\TradeXpertAI\reports\monthly_performance_report.pdf",
    "$basePath\TradeXpertAI\reports\trade_journal.pdf",
    "$basePath\TradeXpertAI\README.md"
)

# Create the folders
foreach ($folder in $folders) {
    New-Item -ItemType Directory -Path $folder -Force
}

# Create the files
foreach ($file in $files) {
    New-Item -ItemType File -Path $file -Force
}

Write-Host "File and folder structure created successfully at $basePath\TradeXpertAI"
