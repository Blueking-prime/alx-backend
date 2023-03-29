import { createQueue } from 'kue';

const JobData = {
  phoneNumber: '1-800-braap',
  message: 'finesse'
};

const queue = createQueue();
const job = queue
  .create('push_notification_code', JobData)
  .save((err) => {
    if (!err) {
      console.log('Notification job created:', job.id);
    }
  })
  .on('complete', () => {
    console.log('Notification job completed');
  })
  .on('failed', () => {
    console.log('Notification job failed');
  });
