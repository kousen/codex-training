const express = require('express');
const app = express();

app.use(express.json());

app.get('/health', (req, res) => {
  res.json({ status: 'healthy', service: 'auth-service' });
});

// TODO: Implement authentication endpoints using Codex
// - POST /api/auth/register
// - POST /api/auth/login
// - POST /api/auth/refresh
// - POST /api/auth/logout

const PORT = process.env.PORT || 3001;
app.listen(PORT, () => {
  console.log(`Auth service running on port ${PORT}`);
});