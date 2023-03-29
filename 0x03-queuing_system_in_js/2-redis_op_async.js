import { promisify } from 'util';
import { createClient, print } from 'redis';

const client = createClient();

client
  .on('error', (err) => {
    console.log('Redis client not connected to the server:', err);
  })
  .on('connect', () => {
    console.log('Redis client connected to the server');
  });

function setNewSchool (schoolName, value) {
  client.set(schoolName, value, print);
}

async function displaySchoolValue (schoolName) {
  const get = promisify(client.get).bind(client);
  await get(schoolName)
    .catch((err) => {
      if (err) {
        console.log(err);
        throw err;
      }
    })
    .then((res) => { console.log(res); });
}

displaySchoolValue('Holberton');
setNewSchool('HolbertonSanFrancisco', '100');
displaySchoolValue('HolbertonSanFrancisco');
