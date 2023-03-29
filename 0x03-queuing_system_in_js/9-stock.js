import { createClient, print } from 'redis';
import promisify from 'util';
const express = require('express');

const client = createClient();

client
  .on('error', (err) => {
    console.log('Redis client not connected to the server:', err);
  })
  .on('connect', () => {
    console.log('Redis client connected to the server');
  });
const listProducts = [
  { itemId: 1, itemName: 'Suitcase 250', price: 50, initialAvailableQuantity: 4 },
  { itemId: 2, itemName: 'Suitcase 450', price: 100, initialAvailableQuantity: 10 },
  { itemId: 3, itemName: 'Suitcase 650', price: 350, initialAvailableQuantity: 2 },
  { itemId: 4, itemName: 'Suitcase 1050', price: 550, initialAvailableQuantity: 5 }
];

function getItemById (id) {
  return listProducts.find((id));
}

function reserveStockById (itemId, stock) {
  client.set(itemId, stock, print);
}

async function getCurrentReservedStockById (itemId) {
  const get = promisify(client.get).bind(client);
  await get(itemId)
    .catch((err) => {
      if (err) {
        console.log(err);
        throw err;
      }
    })
    .then((res) => { return res; });
}

const app = express();
const port = 1245;

app.get('/', (req, res) => {
  res.send('Hello Holberton School!');
});

app.get('/list_products', (req, res) => {
  res.json(listProducts);
});

app.get('/list_products/:itemId', (req, res) => {
  const itemId = req.params.itemId;
  if (getItemById(itemId)) {
    getCurrentReservedStockById(itemId)
      .catch(() => {
        res.json({ status: 'Product not found' });
      })
      .then((output) => {
        res.json(output);
      });
  }
});

app.get('/reserve_product/:itemId', (req, res) => {
  const itemId = req.params.itemId;
  if (getItemById(itemId)) {
    getCurrentReservedStockById(itemId)
      .catch(() => {
        res.json({ status: 'Product not found' });
      })
      .then((output) => {
        if (output.currentQuantity < 1) {
          res.json({ status: 'Not enough stock available', itemId: itemId });
        } else {
          reserveStockById(itemId, 1);
          res.json({ status: 'Reservation confirmed', itemId: itemId });
        }
      });
  }
});

app.listen(port, () => {});

module.exports = app;
