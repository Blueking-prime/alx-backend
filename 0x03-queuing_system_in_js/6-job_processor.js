import { createQueue } from 'kue';

const queue = createQueue();

function sendNotification (phoneNumber, message) {
  console.log(`Sending notification to ${phoneNumber}, with message: ${message}`);
}

queue.process('push_notification_code', (message, done) => {
  sendNotification(message.data.phoneNumber, message.data.message);
  done();
});
