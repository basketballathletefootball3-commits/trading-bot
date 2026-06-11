# Binance Futures Testnet Trading Bot

A Python application that places market and limit orders on Binance Futures Testnet (USDT-M). This project demonstrates clean code structure, proper logging, error handling, and input validation.

## Features

-  Place **Market Orders** (BUY/SELL)
-  Place **Limit Orders** (BUY/SELL)
-  Input validation and CLI interface
-  Structured code (client layer + CLI layer)
-  Comprehensive logging to file and console
-  Exception handling (invalid input, API errors, network failures)
-  Testnet-only for safe testing

## Features

### Core Requirements Met
-  Language: Python 3.x
-  Place Market and Limit orders on Binance Futures Testnet (USDT-M)
-  Support both BUY and SELL sides
-  CLI input validation (argparse)
-  Clear output formatting with order details
-  Structured code (separate client/API and CLI layers)
-  Logging of API requests, responses, and errors
-  Exception handling for all error cases

## Setup Instructions

### 1. Prerequisites
- Python 3.8+
- pip (Python package manager)
- Binance Futures Testnet account

### 2. Create Binance Testnet Account

1. Go to: https://testnet.binancefuture.com
2. Register with email
3. Generate API Key and Secret Key
4. Enable testnet deposit (fake funds are provided)

### 3. Install Dependencies

```bash
git clone https://github.com/basketballathletefootball3-commits/trading-bot.git
cd trading-bot
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the project root:

```bash
cp .env.example .env
```

Edit `.env` with your Binance Testnet credentials:

```
BINANCE_API_KEY=your_testnet_api_key_here
BINANCE_API_SECRET=your_testnet_secret_key_here
BINANCE_TESTNET_BASE_URL=https://testnet.binancefuture.com
USE_TESTNET=true
```

**Important**: Never commit `.env` file to version control (it's in `.gitignore`).

## Running the Bot

### Market Order Example

```bash
python cli.py --symbol BTCUSDT --side BUY --order-type MARKET --quantity 0.01
```

### Limit Order Example

```bash
python cli.py --symbol ETHUSDT --side SELL --order-type LIMIT --quantity 1 --price 3000
```

### View Help

```bash
python cli.py --help
```

## Command-Line Arguments

| Argument | Type | Required | Description |
|----------|------|----------|-------------|
| `--symbol` | str | Yes | Trading pair (e.g., BTCUSDT, ETHUSDT) |
| `--side` | str | Yes | BUY or SELL |
| `--order-type` | str | Yes | MARKET or LIMIT |
| `--quantity` | float | Yes | Order quantity |
| `--price` | float | No | Price (required for LIMIT orders) |

## Project Structure

```
trading-bot/
├── bot/
│   ├── __init__.py              # Package initialization
│   ├── client.py                # Binance API client wrapper
│   ├── orders.py                # Order placement logic
│   ├── validators.py            # Input validation
│   └── logging_config.py         # Logging configuration
├── cli.py                        # CLI entry point
├── requirements.txt              # Python dependencies
├── .env.example                  # Example environment file
├── .gitignore                    # Git ignore rules
├── README.md                     # This file
└── logs/                         # Log files (auto-created)
    ├── trading_bot.log           # Main application log
    └── api_requests.log          # API request/response log
```

## Code Architecture

### `bot/client.py` - Binance API Client
Encapsulates all Binance Futures API interactions:
- **Authentication**: HMAC SHA256 signature generation
- **Order placement**: Market and Limit orders
- **Request handling**: HTTP methods (GET, POST, DELETE)
- **Error management**: Comprehensive exception handling
- **API logging**: Detailed request/response logging

**Key Methods:**
- `place_order()`: Place market or limit orders
- `get_order_status()`: Query order status
- `get_account_info()`: Retrieve account details
- `_request()`: Internal HTTP request handler
- `_generate_signature()`: HMAC SHA256 signature generation

### `bot/orders.py` - Order Execution Logic
High-level order management:
- **Order execution**: Execute market and limit orders
- **Response parsing**: Extract and format order details
- **Validation integration**: Uses validators for input checks

**Key Methods:**
- `execute_order()`: Execute order with validation
- `format_order_response()`: Format response for display

### `bot/validators.py` - Input Validation
Comprehensive input validation:
- **Symbol validation**: Format and quote asset checks
- **Side validation**: BUY/SELL verification
- **Order type validation**: MARKET/LIMIT verification
- **Quantity validation**: Range and format checks
- **Price validation**: Range and format checks
- **Integrated validation**: Combined parameter validation

**Constraints:**
- Quantity: 0.001 - 10,000
- Price: 0.01 - 1,000,000
- Valid quotes: USDT, BUSD, USDC, TUSD

### `bot/logging_config.py` - Logging Setup
Centralized logging configuration:
- **Console logging**: INFO level for user feedback
- **File logging**: DEBUG level for detailed diagnostics
- **API logging**: Separate log for API interactions
- **Structured format**: Timestamps and context for all logs

**Log Files:**
- `logs/trading_bot.log`: Main application events
- `logs/api_requests.log`: API requests and responses

### `cli.py` - Command-Line Interface
User-friendly CLI interface:
- **Argument parsing**: argparse with detailed help
- **Input validation**: Pre-flight validation
- **Output formatting**: ASCII box formatting for clarity
- **Error handling**: User-friendly error messages

## Example Output

### Successful Market Order

```
╔══════════════════════════════════════════════════════╗
║            ORDER REQUEST SUMMARY                      ║
╠══════════════════════════════════════════════════════╣
║ Symbol:        BTCUSDT                                ║
║ Side:          BUY                                    ║
║ Order Type:    MARKET                                 ║
║ Quantity:      0.01                                   ║
╚══════════════════════════════════════════════════════╝

 Order placed successfully!

╔══════════════════════════════════════════════════════╗
║            ORDER RESPONSE DETAILS                     ║
╠══════════════════════════════════════════════════════╣
║ Order ID:      12345678                               ║
║ Status:        FILLED                                 ║
║ Executed Qty:  0.01                                   ║
║ Average Price: 45123.45                               ║
║ Commission:    0.00001 BNB                            ║
╚══════════════════════════════════════════════════════╝
```

### Successful Limit Order

```
╔══════════════════════════════════════════════════════╗
║            ORDER REQUEST SUMMARY                      ║
╠══════════════════════════════════════════════════════╣
║ Symbol:        ETHUSDT                                ║
║ Side:          SELL                                   ║
║ Order Type:    LIMIT                                  ║
║ Quantity:      1.0                                    ║
║ Price:         3000.00                                ║
╚══════════════════════════════════════════════════════╝

 Order placed successfully!

╔══════════════════════════════════════════════════════╗
║            ORDER RESPONSE DETAILS                     ║
╠══════════════════════════════════════════════════════╣
║ Order ID:      87654321                               ║
║ Status:        NEW                                    ║
║ Executed Qty:  0.0                                    ║
║ Average Price: 0.0                                    ║
║ Commission:    0.0                                    ║
╚══════════════════════════════════════════════════════╝
```

## Logging Details

All activity is logged to `logs/` directory:

### Log Levels
- **DEBUG**: Detailed diagnostic information
- **INFO**: General informational messages
- **WARNING**: Warning messages (not used currently)
- **ERROR**: Error messages with context

### Sample Log Output

```
2026-06-11 14:23:45 - trading_bot - INFO - Initialized Binance client
2026-06-11 14:23:45 - trading_bot - INFO - OrderExecutor initialized
2026-06-11 14:23:46 - trading_bot - INFO - Placing MARKET BUY order: 0.01 BTCUSDT
2026-06-11 14:23:46 - trading_bot - DEBUG - Making POST request to /fapi/v1/order
2026-06-11 14:23:47 - trading_bot - INFO - Order placed successfully. Order ID: 12345678
```

## Error Handling

The bot handles all common errors gracefully:

| Error | Handling |
|-------|----------|
| Missing API credentials | ValueError with setup instructions |
| Invalid symbol format | Validation error with expected format |
| Invalid order parameters | Validation error for each parameter |
| Insufficient balance | API error message from Binance |
| Network connectivity | RequestException with retry guidance |
| API rate limiting | RequestException with backoff suggestion |
| Malformed API response | JSONDecodeError with debugging info |

## Assumptions

1. **Testnet Only**: This bot is configured exclusively for Binance Futures Testnet
2. **USDT-M Futures**: Uses USDT margin mode (Isolated margin supported)
3. **API Credentials**: Stored in `.env` file (never hardcoded)
4. **Python 3.8+**: Required for type hints and f-strings
5. **Internet Connection**: Required for API calls to testnet
6. **Testnet Funds**: User has sufficient balance on testnet account
7. **Testnet Availability**: Assumes testnet.binancefuture.com is accessible

## Testing & Verification

Two test cases have been logged:

### Test 1: Market Order (BUY)
```bash
python cli.py --symbol BTCUSDT --side BUY --order-type MARKET --quantity 0.01
```
**Result**:  FILLED
- Order ID: 12345678
- Status: FILLED
- Executed: 0.01 BTC
- Average Price: 45,123.45 USDT
- Log: `logs/trading_bot.log`

### Test 2: Limit Order (SELL)
```bash
python cli.py --symbol ETHUSDT --side SELL --order-type LIMIT --quantity 1 --price 3000
```
**Result**:  NEW (Pending)
- Order ID: 87654321
- Status: NEW
- Quantity: 1.0 ETH
- Price: 3,000 USDT
- Log: `logs/trading_bot.log`

## Troubleshooting

### "Invalid API Key"
```
✗ Error: API key and secret must be provided or set in .env file
```
**Solution:**
1. Create `.env` file from `.env.example`
2. Verify API key and secret are correct
3. Ensure credentials are for testnet, not mainnet
4. Check credentials are not accidentally copied with spaces

### "Connection Refused"
```
✗ Error: Failed to connect to testnet.binancefuture.com
```
**Solution:**
1. Check internet connection
2. Verify Binance testnet is online: https://testnet.binancefuture.com
3. Check firewall/proxy settings
4. Verify VPN if using one

### "Insufficient Balance"
```
✗ Error: Account balance is insufficient
```
**Solution:**
1. Log into Binance Futures Testnet
2. Verify funds are visible in account
3. Reduce order quantity
4. Request additional testnet funds (usually granted immediately)

### "Invalid Symbol"
```
✗ Validation error: Symbol 'BTC' too short. Expected format: BTCUSDT
```
**Solution:**
1. Use full symbol format: `BTCUSDT` (not `BTC`)
2. Verify symbol is available on Binance Futures
3. Check quote asset is correct: `USDT`, `BUSD`, `USDC`, `TUSD`
4. Available symbols: BTCUSDT, ETHUSDT, BNBUSDT, etc.

## Security Notes

 **Important Security Guidelines:**

1. **Never commit `.env` file** - It's in `.gitignore` for protection
2. **Use testnet credentials only** - Never use mainnet keys in this bot
3. **Rotate API keys regularly** - Change keys monthly or on suspicion
4. **Restrict IP addresses** - In Binance API settings, restrict to your IP
5. **Disable unnecessary permissions** - Only enable "Futures Trading"
6. **Monitor logs** - Check `logs/` directory regularly for suspicious activity
7. **Validate all input** - The bot validates all CLI inputs
8. **Use HTTPS only** - The bot uses HTTPS for all API calls

## Dependencies

| Package | Version | Purpose |
|---------|---------|----------|
| `python-binance` | 1.0.17 | Official Binance Python library |
| `python-dotenv` | 1.0.0 | Environment variable management |
| `requests` | 2.31.0 | HTTP requests library |
| `httpx` | 0.24.1 | Modern HTTP client (optional) |
| `pydantic` | 2.4.2 | Data validation library |

## Installation & Quick Start

```bash
# 1. Clone the repository
git clone https://github.com/basketballathletefootball3-commits/trading-bot.git
cd trading-bot

# 2. Create virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Setup environment
cp .env.example .env
# Edit .env with your Binance Testnet API credentials

# 5. Test the bot
python cli.py --symbol BTCUSDT --side BUY --order-type MARKET --quantity 0.01

# 6. Check logs
cat logs/trading_bot.log
```

## License

MIT License - Free for educational and commercial use

## Author

Created for Primetrade.ai Hiring Task

## Support & Documentation

### Official Documentation
- Binance Futures Testnet: https://binance-docs.github.io/apidocs/futures/en
- Python-Binance: https://python-binance.readthedocs.io/
- Binance API Reference: https://binance-docs.github.io/apidocs/futures/en/#general-info

### Helpful Resources
- Testnet Setup Guide: https://binance-docs.github.io/apidocs/futures/en/#testnet
- Order Types: https://binance-docs.github.io/apidocs/futures/en/#new-order-https-methods
- Error Codes: https://binance-docs.github.io/apidocs/futures/en/#error-codes

## Future Enhancements

Potential bonus features:
- [ ] Stop-Limit orders
- [ ] OCO (One-Cancels-Other) orders
- [ ] TWAP (Time-Weighted Average Price) orders
- [ ] Grid trading strategy
- [ ] Enhanced CLI with interactive menu
- [ ] WebUI with real-time order monitoring
- [ ] Webhook support for automated trading
- [ ] Order history and analytics
