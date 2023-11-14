var result = 0;

console.time('duration_sum');
for (var i = 1; i <= 1000; i++){
    result += 1;
}

console.timeEnd('duration_sum');
console.log('Sum from 1 to 1000: %d', result);

console.log('The name oof the currently executed file: %s', __filename);
console.log('The path of the currentlly executed file: %s', __dirname);

var Person = {name: "June", age: 20}
console.dir(Person);