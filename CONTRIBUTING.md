# Contributing to Agent Marketplace

Thank you for your interest in contributing to Agent Marketplace! This document provides guidelines and instructions for contributing.

## Table of Contents
- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [How to Contribute](#how-to-contribute)
- [Coding Standards](#coding-standards)
- [Testing](#testing)
- [Pull Request Process](#pull-request-process)

## Code of Conduct

### Our Pledge
We are committed to providing a welcoming and inclusive environment for all contributors.

### Our Standards
- Be respectful and considerate
- Welcome newcomers and help them learn
- Focus on constructive feedback
- Accept gracefully when others disagree

## Getting Started

1. **Fork the repository** on GitHub
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/YOUR_USERNAME/codingsaathi_level1_1.git
   cd codingsaathi_level1_1
   ```
3. **Add upstream remote**:
   ```bash
   git remote add upstream https://github.com/rgsivaraman/codingsaathi_level1_1.git
   ```

## Development Setup

### Backend Setup

1. Navigate to backend directory:
   ```bash
   cd backend
   ```

2. Create and activate virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   ```bash
   cp .env.example .env
   # Edit .env with your local configuration
   ```

5. Run the development server:
   ```bash
   uvicorn app.main:app --reload
   ```

### Frontend Setup

1. Navigate to frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start development server:
   ```bash
   npm start
   ```

### Database Setup

Option 1: Use Docker:
```bash
docker run -d -p 5432:5432 -e POSTGRES_PASSWORD=postgres -e POSTGRES_DB=agent_marketplace postgres:15-alpine
```

Option 2: Install PostgreSQL locally and create database:
```bash
createdb agent_marketplace
```

## How to Contribute

### Reporting Bugs

1. **Check existing issues** to avoid duplicates
2. **Use the bug report template**
3. **Include details**:
   - Steps to reproduce
   - Expected vs actual behavior
   - Screenshots if applicable
   - Environment details (OS, browser, versions)

### Suggesting Enhancements

1. **Check existing issues** for similar suggestions
2. **Describe the enhancement** clearly
3. **Explain the use case**
4. **Consider implementation details**

### Contributing Code

1. **Pick an issue** or create one for discussion
2. **Create a feature branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. **Make your changes**
4. **Write/update tests**
5. **Update documentation**
6. **Commit your changes**:
   ```bash
   git commit -m "Add feature: description"
   ```
7. **Push to your fork**:
   ```bash
   git push origin feature/your-feature-name
   ```
8. **Create a Pull Request**

## Coding Standards

### Python (Backend)

- Follow **PEP 8** style guide
- Use **type hints** where appropriate
- Write **docstrings** for functions/classes
- Keep functions **focused and small**
- Use **meaningful variable names**

Example:
```python
def create_agent(
    agent_data: AgentCreate,
    db: Session,
    current_user: User
) -> Agent:
    """
    Create a new agent in the database.
    
    Args:
        agent_data: The agent data to create
        db: Database session
        current_user: The authenticated user
        
    Returns:
        The created agent object
    """
    # Implementation
    pass
```

### JavaScript (Frontend)

- Use **ES6+** features
- Follow **Airbnb style guide** (generally)
- Use **functional components** with hooks
- Keep components **small and focused**
- Use **meaningful component names**

Example:
```javascript
// Good
function AgentCard({ agent, onUpdate }) {
  const handleClick = () => {
    // Handle logic
  };
  
  return (
    <div onClick={handleClick}>
      {agent.name}
    </div>
  );
}

// Avoid deeply nested components
```

### Git Commits

- Use **clear, descriptive messages**
- Start with a **verb** (Add, Fix, Update, Remove)
- Keep first line **under 72 characters**
- Add details in body if needed

Examples:
```
Good:
- Add agent forking functionality
- Fix rating calculation bug
- Update deployment documentation
- Remove deprecated API endpoint

Avoid:
- Fixed stuff
- WIP
- Updates
- asdf
```

## Testing

### Backend Tests

```bash
cd backend
pytest
pytest --cov=app  # With coverage
```

### Frontend Tests

```bash
cd frontend
npm test
npm test -- --coverage
```

### Manual Testing

1. Test all CRUD operations
2. Test authentication flows
3. Test agent execution
4. Test error handling
5. Test on different browsers

## Pull Request Process

### Before Submitting

- [ ] Code follows style guidelines
- [ ] Tests pass locally
- [ ] New tests added for new features
- [ ] Documentation updated
- [ ] No merge conflicts
- [ ] Commit messages are clear

### PR Description Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
How has this been tested?

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Comments added for complex code
- [ ] Documentation updated
- [ ] Tests added/updated
- [ ] All tests passing
```

### Review Process

1. Maintainers will review your PR
2. Address feedback and make changes
3. Request re-review after changes
4. Once approved, maintainers will merge

### After Merge

- Delete your feature branch
- Pull latest changes from upstream
- Celebrate! 🎉

## Project Structure

```
codingsaathi_level1_1/
├── backend/
│   ├── app/
│   │   ├── core/        # Configuration, database, security
│   │   ├── models/      # Database models
│   │   ├── routers/     # API endpoints
│   │   ├── schemas/     # Pydantic schemas
│   │   └── services/    # Business logic
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── components/  # Reusable components
│   │   ├── pages/       # Page components
│   │   └── services/    # API calls
│   └── package.json
└── docker-compose.yml
```

## Areas Needing Contribution

### High Priority
- [ ] OAuth integration (Google, GitHub)
- [ ] Email notifications
- [ ] Advanced search
- [ ] Agent collaboration features
- [ ] Performance optimization

### Medium Priority
- [ ] Dark mode
- [ ] Export/import agents
- [ ] Agent templates
- [ ] Usage analytics
- [ ] API rate limiting

### Documentation
- [ ] Video tutorials
- [ ] More example agents
- [ ] Troubleshooting guide
- [ ] API client libraries

## Questions?

- Open an issue for discussion
- Tag maintainers for urgent questions
- Check existing documentation first

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

Thank you for contributing to Agent Marketplace! 🚀
