const chai = require('chai');
const { createQueue } = require('kue');
const createPushNotificationsJobs = require('./8-job');
const expect = chai.expect;

const queue = createQueue();

const jobs = [
  {
    phoneNumber: '4153518780',
    message: 'This is the code 1234 to verify your account'
  },
  {
    phoneNumber: '4779565978',
    message: 'This is the code 6809 to verify your account'
  }
];
createPushNotificationsJobs(jobs, queue);

describe('createPushNotificationsJobs', function () {
  before(() => {
    queue.testMode.enter();
  });
  afterEach(() => {
    queue.testMode.clear();
  });
  after(() => {
    queue.testMode.exit();
  });

  it('checks that throws error for non-arrays', function () {
    expect(() => createPushNotificationsJobs('braap', queue)).to.throw(Error, 'Jobs is not an array');
  });

  it('Test whether jobs are created', function () {
    createPushNotificationsJobs(jobs, queue);

    expect(queue.testMode.jobs.length).to.equal(2);

    expect(queue.testMode.jobs[0].type).to.equal('push_notification_code_3');
    expect(queue.testMode.jobs[0].data).to.eql(jobs[0]);

    expect(queue.testMode.jobs[1].type).to.equal('push_notification_code_3');
    expect(queue.testMode.jobs[1].data).to.eql(jobs[1]);
  });
});
