const request = require('supertest');
const app = require('../../app');

describe('Test the root path', () => {
  test('It should respond to the GET method', async () => {
    const response = await request(app).get('/');
    expect(response.statusCode).toBe(200);
    expect(response.text).toBe('Hello, World!');
  });
});

describe('Test the /name/:name path', () => {
  test('It should respond with a personalized greeting', async () => {
    const name = 'Alice';
    const response = await request(app).get(`/name/${name}`);
    expect(response.statusCode).toBe(200);
    expect(response.text).toBe(`Hello, ${name}!`);
  });

  test('It should work with different names', async () => {
    const names = ['Bob', 'Charlie', 'Diana', 'DevOps'];
    
    for (const name of names) {
      const response = await request(app).get(`/name/${name}`);
      expect(response.statusCode).toBe(200);
      expect(response.text).toBe(`Hello, ${name}!`);
    }
  });
});

describe('Test the /api/status path', () => {
  test('It should return status OK', async () => {
    const response = await request(app).get('/api/status');
    expect(response.statusCode).toBe(200);
    expect(response.body.status).toBe('OK');
    expect(response.body.timestamp).toBeDefined();
  });
});

describe('Test 404 errors', () => {
  test('It should return 404 for non-existent routes', async () => {
    const response = await request(app).get('/nonexistent');
    expect(response.statusCode).toBe(404);
  });
});

describe('Test the /add/:a/:b path', () => {
  test('It should add two positive numbers', async () => {
    const response = await request(app).get('/add/5/3');
    expect(response.statusCode).toBe(200);
    expect(response.body.a).toBe(5);
    expect(response.body.b).toBe(3);
    expect(response.body.sum).toBe(8);
  });

  test('It should add negative numbers', async () => {
    const response = await request(app).get('/add/-5/-3');
    expect(response.statusCode).toBe(200);
    expect(response.body.sum).toBe(-8);
  });

  test('It should add decimal numbers', async () => {
    const response = await request(app).get('/add/5.5/2.3');
    expect(response.statusCode).toBe(200);
    expect(response.body.sum).toBeCloseTo(7.8, 1);
  });

  test('It should return error for non-numeric input', async () => {
    const response = await request(app).get('/add/abc/5');
    expect(response.statusCode).toBe(400);
    expect(response.body.error).toBeDefined();
  });

  test('It should return error when both are non-numeric', async () => {
    const response = await request(app).get('/add/abc/xyz');
    expect(response.statusCode).toBe(400);
    expect(response.body.error).toContain('must be valid numbers');
  });

  test('It should handle zero', async () => {
    const response = await request(app).get('/add/0/5');
    expect(response.statusCode).toBe(200);
    expect(response.body.sum).toBe(5);
  });

  test('It should add mixed positive and negative', async () => {
    const response = await request(app).get('/add/10/-5');
    expect(response.statusCode).toBe(200);
    expect(response.body.sum).toBe(5);
  });
});
