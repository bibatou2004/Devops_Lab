const request = require('supertest');
const app = require('../../app');

describe('Integration Tests - Complete API Flow', () => {
  
  test('Complete user journey: greet and check status', async () => {
    // Step 1: Get home page
    const homeRes = await request(app).get('/');
    expect(homeRes.statusCode).toBe(200);
    expect(homeRes.text).toBe('Hello, World!');
    
    // Step 2: Get personalized greeting
    const greetRes = await request(app).get('/name/TestUser');
    expect(greetRes.statusCode).toBe(200);
    expect(greetRes.text).toContain('TestUser');
    
    // Step 3: Check API status
    const statusRes = await request(app).get('/api/status');
    expect(statusRes.statusCode).toBe(200);
    expect(statusRes.body.status).toBe('OK');
  });

  test('Calculator flow: add and verify', async () => {
    // Step 1: Add two numbers
    const addRes = await request(app).get('/add/10/20');
    expect(addRes.statusCode).toBe(200);
    expect(addRes.body.sum).toBe(30);
    
    // Step 2: Verify with different operation
    const statusRes = await request(app).get('/api/status');
    expect(statusRes.statusCode).toBe(200);
    expect(statusRes.body.timestamp).toBeDefined();
  });

  test('Handle sequential requests', async () => {
    const requests = [
      request(app).get('/'),
      request(app).get('/name/Test'),
      request(app).get('/add/5/5'),
      request(app).get('/api/status')
    ];

    const results = await Promise.all(requests);
    results.forEach(res => {
      expect(res.statusCode).toBe(200);
    });
  });

  test('Error handling: invalid add request', async () => {
    const res = await request(app).get('/add/abc/xyz');
    expect(res.statusCode).toBe(400);
    expect(res.body.error).toBeDefined();
  });
});
