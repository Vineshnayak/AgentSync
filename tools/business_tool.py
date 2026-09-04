import sqlite3
import os
from langchain_core.tools import tool
from utils.logging_config import setup_logger, global_metrics
from config.settings import settings

logger = setup_logger("business_tool")

DB_PATH = "enterprise_mock.db"

def init_mock_db():
    """Initializes a mock enterprise database with some sample data."""
    if not os.path.exists(DB_PATH):
        logger.info("Initializing mock enterprise database...")
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Create Sales table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sales (
                id INTEGER PRIMARY KEY,
                region TEXT,
                revenue REAL,
                quarter TEXT
            )
        ''')
        
        # Insert mock data
        sales_data = [
            ("North America", 1500000.00, "Q1"),
            ("North America", 1750000.00, "Q2"),
            ("Europe", 950000.00, "Q1"),
            ("Europe", 1100000.00, "Q2"),
            ("Asia", 2100000.00, "Q1"),
            ("Asia", 2300000.00, "Q2")
        ]
        
        cursor.executemany("INSERT INTO sales (region, revenue, quarter) VALUES (?, ?, ?)", sales_data)
        conn.commit()
        conn.close()

# Initialize DB on load
init_mock_db()

@tool
def query_sales_data(region: str, quarter: str) -> str:
    """Useful for retrieving enterprise sales data.
    Input should be the region (e.g., 'North America', 'Europe', 'Asia') and quarter (e.g., 'Q1', 'Q2').
    """
    logger.info(f"Tool called: query_sales_data for region {region}, quarter {quarter}")
    global_metrics.increment_tool()
    
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute("SELECT revenue FROM sales WHERE region LIKE ? AND quarter = ?", (f"%{region}%", quarter))
        result = cursor.fetchone()
        conn.close()
        
        if result:
            return f"Revenue for {region} in {quarter} was ${result[0]:,.2f}"
        else:
            return f"No sales data found for region: {region}, quarter: {quarter}"
            
    except Exception as e:
        logger.error(f"Database query failed: {e}")
        return f"Database error: {str(e)}"
