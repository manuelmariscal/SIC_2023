var nconf = require('nconf');

nconf.env();
console.log('Value of OS enviroment variables: %s', nconf.get('OS'));