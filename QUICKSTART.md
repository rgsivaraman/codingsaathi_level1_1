# Quick Start Guide

Get the Agent Marketplace up and running in minutes!

## Prerequisites

- Docker & Docker Compose (recommended)
- OR Python 3.11+, Node.js 18+, PostgreSQL 15+ (manual setup)

## 🚀 Quick Start with Docker (5 minutes)

### Step 1: Clone the Repository
```bash
git clone <repository-url>
cd codingsaathi_level1_1
```

### Step 2: Start the Application
```bash
./deploy.sh
```

Or manually:
```bash
docker-compose up --build -d
```

### Step 3: Access the Application
- **Frontend**: http://localhost
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

### Step 4: Create Your First Agent

1. **Register** a new account at http://localhost
2. **Login** with your credentials
3. Click **"Create Agent"**
4. Fill in the form:
   - **Name**: My First Agent
   - **Description**: A simple text reverser
   - **Code**:
     ```python
     text = input_data.get('text', 'Hello')
     result = text[::-1]
     ```
   - **Tags**: text, demo
5. Click **"Create Agent"**

### Step 5: Test Your Agent

1. Click on your agent in the marketplace
2. In the **"Execute Agent"** section, enter:
   ```json
   {"text": "Hello World"}
   ```
3. Click **"Execute"**
4. See the output: `dlroW olleH`

## 🎯 What Can You Do?

### For Users
- ✅ Browse and search agents in the marketplace
- ✅ Execute agents with custom input
- ✅ Fork agents to create your own versions
- ✅ Rate and review agents
- ✅ Create and manage your own agents

### For Developers
- ✅ RESTful API for integration
- ✅ Auto-generated OpenAPI documentation
- ✅ JWT authentication
- ✅ PostgreSQL database
- ✅ Docker containerization

## 📝 Example Agents to Try

### 1. Text Reverser
```python
text = input_data.get('text', '')
result = text[::-1]
```
**Input**: `{"text": "Hello"}`  
**Output**: `olleH`

### 2. Calculator
```python
a = input_data.get('a', 0)
b = input_data.get('b', 0)
op = input_data.get('operation', 'add')

if op == 'add':
    result = a + b
elif op == 'multiply':
    result = a * b
else:
    result = "Invalid operation"
```
**Input**: `{"a": 5, "b": 3, "operation": "multiply"}`  
**Output**: `15`

### 3. Word Counter
```python
text = input_data.get('text', '')
words = len(text.split())
result = f"Word count: {words}"
```
**Input**: `{"text": "Hello world from agent"}`  
**Output**: `Word count: 4`

## 🔧 Troubleshooting

### Ports Already in Use?

If port 80 or 8000 is already in use, edit `docker-compose.yml`:

```yaml
services:
  backend:
    ports:
      - "8001:8000"  # Change to 8001
  
  frontend:
    ports:
      - "8080:80"    # Change to 8080
```

Then access:
- Frontend: http://localhost:8080
- Backend: http://localhost:8001

### Database Connection Issues?

Check if PostgreSQL container is running:
```bash
docker-compose ps
```

View logs:
```bash
docker-compose logs db
docker-compose logs backend
```

### Frontend Not Loading?

Clear browser cache or try incognito mode.

Check frontend logs:
```bash
docker-compose logs frontend
```

## 📚 Next Steps

- Read the [README.md](README.md) for detailed documentation
- Check [EXAMPLES.md](EXAMPLES.md) for more agent examples
- Review [API.md](API.md) for API documentation
- See [DEPLOYMENT.md](DEPLOYMENT.md) for production deployment

## 🛑 Stop the Application

```bash
docker-compose down
```

To remove all data:
```bash
docker-compose down -v
```

## 💡 Tips

1. **Keep your agents simple** - Complex logic may timeout
2. **Test with various inputs** - Handle edge cases
3. **Add good descriptions** - Help others discover your agents
4. **Use meaningful tags** - Make agents searchable
5. **Fork and improve** - Build on others' work

## 🆘 Get Help

- Read the full documentation in [README.md](README.md)
- Check the API docs at http://localhost:8000/docs
- Review example agents in [EXAMPLES.md](EXAMPLES.md)

## 🎉 You're Ready!

Start creating, sharing, and using AI agents in your new marketplace!
