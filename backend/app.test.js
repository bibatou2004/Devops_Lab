const request = require('supertest');
const app = require('./server');

describe('Test des points de terminaison de l\'API News', () => {
  
  // Test de la route racine
  it('GET / devrait retourner un message de bienvenue', async () => {
    const res = await request(app).get('/');
    expect(res.statusCode).toEqual(200);
    expect(res.text).toContain('API Foot News en ligne');
  });

  // Test de validation des données (TDD simple)
  it('POST /news devrait échouer si le titre est manquant', async () => {
    const res = await request(app)
      .post('/news')
      .send({
        content: "Contenu sans titre"
      });
    expect(res.statusCode).toEqual(400);
  });
});