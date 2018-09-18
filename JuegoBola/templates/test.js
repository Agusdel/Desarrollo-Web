class User {

  constructor(name) {
    this.name = name;
    this.lastName = name;
  }

  getName() { return this.name; }
}


var user = new User("Juan");

console.log("user.name: " + user.name);
console.log("user.getName(): " + user.getName());
console.log("user.lastName: " + user.lastName);

user.name = "Jorge";

console.log("user.name: " + user.name);
console.log("user.getName(): " + user.getName());
console.log("user.lastName: " + user.lastName);