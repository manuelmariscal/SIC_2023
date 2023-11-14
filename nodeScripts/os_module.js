var os = require('os');

console.log('System hostname: %s', os.hostname());
console.log('Memory of system: %d /%d', os.freemem(),os.totalmem());

console.log('System CPU information \n');
console.dir(os.cpus());
console.log('System network interface information \n');
console.dir(os.networkInterfaces());